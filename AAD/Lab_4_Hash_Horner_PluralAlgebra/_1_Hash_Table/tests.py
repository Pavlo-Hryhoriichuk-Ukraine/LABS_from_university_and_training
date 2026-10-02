import os
import time
import random
import string
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

ROOT_DIR = Path()

from decode_and_hash import (
    decode_file,
    convert_binary_message,
    hash_pair_division,
    hash_pair_mul,
    hash_middle_square,
    HashTableChaining,
    HashTableLinearProbing,
    HashTableQuadraticProbing,
    HashTableDoubleHashing,
    ASCIIBitset,
)

# --- Налаштування тестування ---
MSG_FILENAME = "message.txt"
KEY1_FILENAME = "key1.txt"
KEY2_FILENAME = "key2.txt"

# Розміри для великого тесту (Performance Test)
# 5 МБ для кожного файлу цілком достатньо, щоб побачити O(N) і не чекати вічність
LARGE_FILE_SIZE = 250_000


def generate_test_files(size: int):
    """Генерує випадкові текстові файли заданого розміру."""
    print(f"[*] Генерація тестових файлів ({size / 1_000_000:.1f} MB кожен)...")
    chars = string.ascii_letters + string.digits + string.punctuation + " \n"

    for filename in [MSG_FILENAME, KEY1_FILENAME, KEY2_FILENAME]:
        with open(filename, "w", encoding="utf-8") as f:
            # Генерація блоками для економії оперативної пам'яті
            for _ in range(size // 100_000):
                f.write("".join(random.choices(chars, k=100_000)))
            # Залишок
            f.write("".join(random.choices(chars, k=size % 100_000)))
    print("[+] Файли успішно згенеровано.\n")


def cleanup_files():
    """Видаляє згенеровані файли після тестів."""
    for filename in [MSG_FILENAME, KEY1_FILENAME, KEY2_FILENAME]:
        if os.path.exists(filename):
            os.remove(filename)


def run_benchmark(name: str, collection_cls, hash_func=None):
    """
    Запускає розкодування з обраною колекцією, заміряє час та виводить статистику.
    Повертає отриманий бітовий рядок (для перевірки коректності).
    """
    # Ініціалізація колекцій
    if hash_func:
        col1 = collection_cls(hash_func=hash_func)
        col2 = collection_cls(hash_func=hash_func)
    else:
        col1 = collection_cls()
        col2 = collection_cls()

    start_time = time.perf_counter()
    binary_result = decode_file(MSG_FILENAME, KEY1_FILENAME, KEY2_FILENAME, col1, col2)
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    print(f"--- {name} ---")
    print(f"Час виконання: {execution_time:.4f} сек")

    stats = {}
    if hasattr(col1, 'get_statistics'):
        print(f"Статистика Key 1: {col1.get_statistics()}")
        stats = {
            "collisions": col1.total_collisions,
            "max_chain": col1.max_chain_length,
            "table_ref": col1 # Зберігаємо посилання на таблицю для гістограми
        }

    print("-" * 40)
    return binary_result, execution_time, stats

def plot_performance_metrics(results_dict):
    """Будує графіки порівняння часу та кількості колізій для всіх методів."""
    names = []
    times = []
    collisions = []

    for name, data in results_dict.items():
        # data[1] це execution_time, data[2] це stats
        names.append(name)
        times.append(data[1])
        # Для Bitset та Set немає поля collisions, ставимо 0
        collisions.append(data[2].get("collisions", 0) if data[2] else 0)

    # 1. Графік часу виконання
    plt.figure(figsize=(12, 6))
    y_pos = np.arange(len(names))
    plt.barh(y_pos, times, color='skyblue', edgecolor='black')
    plt.yticks(y_pos, names)
    plt.xlabel('Час виконання (секунди)')
    plt.title('Порівняння швидкодії структур даних (O(N) тест)')
    plt.tight_layout()
    plt.savefig( ROOT_DIR / 'execution_time_comparison.png')
    plt.show()

    # 2. Графік кількості колізій (відфільтровуємо Set та Bitset)
    hash_names = [n for n in names if "Set" not in n and "Bitset" not in n]
    hash_collisions = [c for n, c in zip(names, collisions) if "Set" not in n and "Bitset" not in n]

    if hash_names:
        plt.figure(figsize=(12, 6))
        y_pos_hash = np.arange(len(hash_names))
        plt.barh(y_pos_hash, hash_collisions, color='salmon', edgecolor='black')
        plt.yticks(y_pos_hash, hash_names)
        plt.xlabel('Загальна кількість колізій при заповненні')
        plt.title('Порівняння ефективності вирішення колізій')
        plt.tight_layout()
        plt.savefig(ROOT_DIR / 'collisions_comparison.png')
        plt.show()

def plot_chaining_histogram(chaining_table_instance, title_suffix=""):
    """
    Аналізує масив таблиці Chaining і будує гістограму розподілу довжин ланцюжків.
    Показує, скільки комірок мають 0 елементів, 1 елемент, 2 елементи тощо.
    """
    # Збираємо довжини всіх списків у хеш-таблиці
    bucket_sizes = [len(bucket) if bucket is not None else 0 for bucket in chaining_table_instance.table]

    plt.figure(figsize=(10, 5))

    # Визначаємо максимальну довжину для налаштування кордонів (bins)
    max_size = max(bucket_sizes) if bucket_sizes else 0
    bins = np.arange(-0.5, max_size + 1.5, 1)

    plt.hist(bucket_sizes, bins=bins, color='lightgreen', edgecolor='black', alpha=0.8) # type: ignore

    plt.xticks(range(0, max_size + 1))
    plt.xlabel('Довжина ланцюжка (кількість елементів у комірці)')
    plt.ylabel('Кількість таких комірок')
    plt.title(f'Гістограма розподілу колізій: Chaining ({title_suffix})')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Додаємо текстову статистику на графік
    empty_buckets = bucket_sizes.count(0)
    plt.text(0.95, 0.95, f'Порожніх комірок: {empty_buckets}',
             horizontalalignment='right', verticalalignment='top',
             transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5))

    plt.tight_layout()
    plt.savefig(ROOT_DIR / f'histogram_chaining_{title_suffix.replace(" ", "_")}.png')
    plt.show()


def main():
    try:
        # 1. Створюємо файли
        generate_test_files(LARGE_FILE_SIZE)

        results = {}

        print("========== ТЕСТУВАННЯ ШВИДКОДІЇ ТА СТРУКТУР (Пункт В, Г) ==========\n")

        # Тест вбудованого set (Еталон для перевірки правильності та швидкості)
        results['Built-in Set'] = run_benchmark("Built-in Python Set (Пункт Г)", set)

        # Тест Bitset (Пряма адресація)
        results['ASCII Bitset'] = run_benchmark("Direct Addressing Bitset (Пункт В)", ASCIIBitset)


        print("\n========== ТЕСТУВАННЯ ХЕШ-ТАБЛИЦЬ (Пункт А) ==========\n")

        hash_functions = [
            ("Division", hash_pair_division),
            ("Multiplication", hash_pair_mul),
            ("Middle Square", hash_middle_square)
        ]

        hash_tables = [
            ("Chaining", HashTableChaining),
            ("Open - Linear", HashTableLinearProbing),
            ("Open - Quadratic", HashTableQuadraticProbing),
            ("Open - Double Hashing", HashTableDoubleHashing)
        ]

        # Проходимося по всіх комбінаціях таблиць та функцій
        for table_name, table_cls in hash_tables:
            for func_name, func in hash_functions:
                test_name = f"{table_name} + {func_name}"
                # Зберігаємо весь кортеж (binary_result, execution_time, stats)
                results[test_name] = run_benchmark(test_name, table_cls, func)

        # 2. Перевірка коректності (Correctness Check)
        print("\n========== ПЕРЕВІРКА КОРЕКТНОСТІ ==========")
        # reference_bits лежить під індексом 0 у кортежі результатів еталонного Set
        reference_bits = results['Built-in Set'][0]
        all_passed = True

        for name, data in results.items():
            bits = data[0]
            if bits != reference_bits:
                print(f"[ПОМИЛКА] Алгоритм '{name}' видав неправильний результат!")
                all_passed = False

        if all_passed:
            print("[УСПІХ] Всі алгоритми та хеш-функції видали абсолютно ідентичний та правильний результат!")

            # Перевіримо, чи взагалі щось розкодувалося
            decoded_text = convert_binary_message(reference_bits)
            print(f"Згенеровано валідних символів ASCII з бітів: {len(decoded_text)}")

        # 3. Побудова графіків
        print("\n========== ПОБУДОВА ГРАФІКІВ ==========")
        print("[*] Генерація загальних метрик (швидкодія та колізії)...")
        plot_performance_metrics(results)

        print("[*] Генерація гістограм розподілу для методу ланцюжків...")
        for name, data in results.items():
            if "Chaining" in name:
                table_ref = data[2].get("table_ref")
                if table_ref:
                    # name має формат "Chaining + Division", беремо другу частину для заголовка
                    plot_chaining_histogram(table_ref, title_suffix=name.split(" + ")[1])

    finally:
        # Прибираємо за собою файли, щоб не засмічувати диск
        cleanup_files()
        print("\n[+] Тестові файли видалено. Завершення роботи.")

if __name__ == "__main__":
    main()