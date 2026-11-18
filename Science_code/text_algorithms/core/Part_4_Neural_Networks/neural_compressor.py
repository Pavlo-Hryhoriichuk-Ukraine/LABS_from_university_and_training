from pathlib import Path

TEXT_DIR = Path(__file__).parent.parent.parent


import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
# Глушимо повідомлення C++ бекенду TensorFlow
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import math

import numpy as np
import tensorflow as tf

# Максимально утилізуємо всі ядра процесора
num_cores = os.cpu_count() or 8
tf.config.threading.set_inter_op_parallelism_threads(num_cores)
tf.config.threading.set_intra_op_parallelism_threads(num_cores)

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Підключаємо батьківські шляхи на випадок запуску з підпапки
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from word_huffman import get_binary_from_file
except ImportError:
    # Запасний імпорт, якщо лежить безпосередньо в core
    from text_algorithms.core.word_huffman import get_binary_from_file


def prepare_dataset(binary_stream: str):
    """Генерує двійкові індекси-координати довжини d та цільові біти."""
    n_samples = len(binary_stream)
    d = math.ceil(math.log2(n_samples)) if n_samples > 1 else 1

    X = np.zeros((n_samples, d), dtype=np.float32)
    for i in range(n_samples):
        bin_str = format(i, f"0{d}b")
        X[i] = [float(b) for b in bin_str]

    Y = np.array([float(b) for b in binary_stream], dtype=np.float32).reshape(-1, 1)
    return X, Y, d


class FastNeuralCompressor(tf.Module):
    """
    Низькорівнева модель без оверхеду Keras layers.
    Усі операції скомпільовані в один C++ граф.
    """

    def __init__(self, input_dim: int, hidden_dim: int, lr: float = 0.03):
        super().__init__()
        # Ініціалізація ваг Альфа (вхід -> прихований шар)
        w_init = tf.initializers.GlorotUniform()
        self.W_alpha = tf.Variable(
            w_init(shape=(input_dim, hidden_dim)), name="W_alpha"
        )
        self.b_alpha = tf.Variable(tf.zeros(shape=(hidden_dim,)), name="b_alpha")

        # Ініціалізація ваг Бета (прихований -> вихідний біт)
        self.W_beta = tf.Variable(w_init(shape=(hidden_dim, 1)), name="W_beta")
        self.b_beta = tf.Variable(tf.zeros(shape=(1,)), name="b_beta")

        # Ініціалізуємо та білдимо оптимізатор поза tf.function
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=lr)
        self.optimizer.build(self.trainable_variables)

    def forward(self, x):
        h = tf.tanh(tf.matmul(x, self.W_alpha) + self.b_alpha)
        out = tf.sigmoid(tf.matmul(h, self.W_beta) + self.b_beta)
        return out

    @tf.function
    def train_step(self, x, y):
        with tf.GradientTape() as tape:
            preds = self.forward(x)
            # Стабільний binary crossentropy
            loss = tf.reduce_mean(
                -y * tf.math.log(preds + 1e-7)
                - (1.0 - y) * tf.math.log(1.0 - preds + 1e-7)
            )
        grads = tape.gradient(loss, self.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.trainable_variables))
        return loss, preds


def fast_train_loop(
    model: FastNeuralCompressor,
    X_tf,
    Y_tf,
    ground_truth: np.ndarray,
    max_epochs: int = 2000,
):
    for epoch in range(1, max_epochs + 1):
        loss, preds = model.train_step(X_tf, Y_tf)

        # Перевірка точності кожні 40 епох для економії часу
        if epoch % 40 == 0 or epoch == max_epochs:
            predicted_bits = (preds.numpy() >= 0.5).astype(int).flatten()
            correct = np.sum(predicted_bits == ground_truth)
            acc = correct / len(ground_truth)

            if acc == 1.0:
                return True, epoch

            # Раннє відсікання: якщо за 200 епох навіть 65% не береться, кидаємо цей m
            if epoch == 200 and acc < 0.65:
                return False, epoch

    return False, max_epochs


def quantize_and_verify(
    weights, X: np.ndarray, ground_truth: np.ndarray, bits_mode: int
):
    """Перевірка точності після округлення ваг у дискретну сітку int4, int8 або float16."""
    W_alpha, b_alpha, W_beta, b_beta = weights
    all_weights = [W_alpha, b_alpha, W_beta, b_beta]

    if bits_mode == 16:
        q_weights = [w.astype(np.float16).astype(np.float32) for w in all_weights]
        scale = 1.0
    elif bits_mode in (4, 8):
        max_val = max(np.max(np.abs(w)) for w in all_weights)
        if max_val == 0:
            return False, None, 1.0
        int_max = 7 if bits_mode == 4 else 127
        scale = float(max_val / int_max)

        q_weights = []
        for w in all_weights:
            quantized = np.clip(np.round(w / scale), -int_max, int_max)
            dequantized = (quantized * scale).astype(np.float32)
            q_weights.append(dequantized)
    else:
        return False, None, 1.0

    W_a, b_a, W_b, b_b = q_weights
    hidden = np.tanh(np.dot(X, W_a) + b_a)
    output = 1.0 / (1.0 + np.exp(-(np.dot(hidden, W_b) + b_b)))
    predicted_bits = (output >= 0.5).astype(int).flatten()

    is_perfect = np.array_equal(predicted_bits, ground_truth.flatten())
    return is_perfect, q_weights, scale


def compress_chunk(chunk_bits: str):
    N = len(chunk_bits)
    X, Y, d = prepare_dataset(chunk_bits)
    ground_truth = Y.flatten().astype(int)

    # Максимальна стеля m для найвигіднішого режиму int4 (Params * 4 + 32 < N)
    max_m_int4 = int((N - 32) / (4 * (d + 2)))
    if max_m_int4 < 1:
        return {"mode": "raw", "stored_bits": N + 2, "m": 0, "bits_per_weight": 0}

    # Перебираємо тільки перспективні m з більшим кроком
    m_search_limit = min(max_m_int4, 32)
    m_candidates = [m for m in range(4, m_search_limit + 1, 4)]

    X_tf = tf.constant(X)
    Y_tf = tf.constant(Y)

    best_result = None
    min_stored_bits = N

    for m in m_candidates:
        model = FastNeuralCompressor(input_dim=d, hidden_dim=m, lr=0.03)
        is_perfect, _ = fast_train_loop(
            model, X_tf, Y_tf, ground_truth, max_epochs=1500
        )

        if not is_perfect:
            continue

        weights = [
            model.W_alpha.numpy(),
            model.b_alpha.numpy(),
            model.W_beta.numpy(),
            model.b_beta.numpy(),
        ]
        total_params = m * (d + 2) + 1

        for mode, bit_size in [("int4", 4), ("int8", 8), ("float16", 16)]:
            ok, _, _ = quantize_and_verify(weights, X, ground_truth, bits_mode=bit_size)
            if ok:
                size_bits = total_params * bit_size + 32  # 32 біти — заголовок блоку
                if size_bits < min_stored_bits:
                    min_stored_bits = size_bits
                    best_result = {
                        "mode": mode,
                        "stored_bits": size_bits,
                        "m": m,
                        "bits_per_weight": bit_size,
                    }
                break

        # Якщо вже досягнуто виграшу > 15%, немає сенсу пробувати більші m
        if best_result and best_result["stored_bits"] < N * 0.85:
            break

    if best_result is not None:
        return best_result

    # Безпечний фолбек (сирі біти Гаффмана + 2 біти прапорця)
    return {"mode": "raw", "stored_bits": N + 2, "m": 0, "bits_per_weight": 0}


def run_pipeline(filename: str, chunk_size: int = 2048):
    print("=" * 70)
    print("ПРИСКОРЕНИЙ ЕКСПЕРИМЕНТ: HUFFMAN vs FAST NEURAL COMPRESSOR")
    print("=" * 70)

    file_path = TEXT_DIR / "texts" / (filename + ".txt")

    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    raw_text_bits = len(raw_text.encode("utf-8")) * 8
    huffman_bits_stream = get_binary_from_file(filename)
    huffman_total_bits = len(huffman_bits_stream)

    print(f"Файл: {filename}")
    print(f"Оригінальний текст: {raw_text_bits} біт ({raw_text_bits / 8:.1f} Б)")
    print(
        f"Код Гаффмана:      {huffman_total_bits} біт ({huffman_total_bits / 8:.1f} Б)"
    )
    print(f"Стиснення Гаффмана: {raw_text_bits / huffman_total_bits:.3f}x\n")

    actual_chunk_size = chunk_size
    if huffman_total_bits < chunk_size:
        actual_chunk_size = 2 ** max(7, math.floor(math.log2(huffman_total_bits)))

    chunks = [
        huffman_bits_stream[i : i + actual_chunk_size]
        for i in range(0, huffman_total_bits, actual_chunk_size)
    ]
    print(f"Розмір блоку: {actual_chunk_size} біт. Всього блоків: {len(chunks)}\n")

    total_compressed_bits = 0
    stats = {"int4": 0, "int8": 0, "float16": 0, "raw": 0}

    for idx, chunk in enumerate(chunks):
        print(
            f"Блок {idx + 1}/{len(chunks)} ({len(chunk)} біт)... ", end="", flush=True
        )
        res = compress_chunk(chunk)
        stats[res["mode"]] += 1
        total_compressed_bits += res["stored_bits"]

        if res["mode"] == "raw":
            print(f"-> Фолбек (Raw біти). Розмір: {res['stored_bits']} біт")
        else:
            gain = ((len(chunk) - res["stored_bits"]) / len(chunk)) * 100.0
            print(
                f"-> УСПІХ! Режим: {res['mode']}, m={res['m']}, "
                f"розмір: {res['stored_bits']} біт (виграш {gain:.1f}%)"
            )

    print("\n" + "=" * 70)
    print("ПІДСУМКОВІ РЕЗУЛЬТАТИ:")
    print(f"- Оригінальний текст:     {raw_text_bits:>10} біт  (100.0%)")
    print(
        f"- Послідовний Гаффман:    {huffman_total_bits:>10} біт  "
        f"({(huffman_total_bits / raw_text_bits) * 100:.2f}% від оригіналу)"
    )
    print(
        f"- Нейромережа + Квант:    {total_compressed_bits:>10} біт  "
        f"({(total_compressed_bits / raw_text_bits) * 100:.2f}% від оригіналу)"
    )

    diff = huffman_total_bits - total_compressed_bits
    if diff > 0:
        pct = (diff / huffman_total_bits) * 100.0
        print(
            f"\n✅ ВИСНОВОК: Нейромережа покращила Гаффмана на {pct:.2f}% "
            f"(заощаджено {diff} біт)."
        )
    else:
        print(
            "\n⚖️ ВИСНОВОК: Перевагу збережено за чистим Гаффманом (висока ентропія блоків)."
        )


if __name__ == "__main__":
    TEST_FILE = "AI_GEMINI__Modern Urban Aesthetics"
    run_pipeline(filename=TEST_FILE, chunk_size=2048)
