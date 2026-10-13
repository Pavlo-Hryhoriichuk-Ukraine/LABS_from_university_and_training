import math
from dataclasses import dataclass
from collections.abc import Iterator
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import numba
from numba.typed import List
from scipy.fft import rfft, rfftfreq  # type: ignore
from scipy.signal import find_peaks   # type: ignore
import time
from pathlib import Path
import sys
import os

SAVE_PATH = Path(__file__).parent.resolve() / "results"

# Додаємо кореневу папку проекту до шляхів пошуку Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from core.word_huffman import get_binary_from_file


def _python_factorize(n: int) -> tuple[list[int], list[int]]:
    """
    Звичайна пайтонівська функція факторизації.
    Повертає два списки: дільники та їхні степені.
    Автоматично підтримує будь-яку розрядність (хоч 64, хоч 256 біт).
    """
    primes = []
    exponents = []

    if n < 2:
        if n > 0:
            primes.append(n)
            exponents.append(1)
        return primes, exponents

    # 1. Витягуємо всі двійки
    count_2 = 0
    while n % 2 == 0:
        count_2 += 1
        n //= 2

    if count_2 > 0:
        primes.append(2)
        exponents.append(count_2)

    # 2. Перевіряємо непарні дільники
    divisor = 3
    limit = math.isqrt(n) # math.isqrt працює набагато швидше з Bignum

    while divisor <= limit:
        count = 0
        while n % divisor == 0:
            count += 1
            n //= divisor

        if count > 0:
            primes.append(divisor)
            exponents.append(count)
            limit = math.isqrt(n) # Динамічне звуження межі

        divisor += 2

    # 3. Якщо залишилося просте число
    if n > 1:
        primes.append(n)
        exponents.append(1)

    return primes, exponents

@dataclass(slots=True, frozen=True)
class FactorizationResult:
    """
    Immutable data structure for storing factorization results.
    """
    primes: list[int]
    exponents: list[int]


class HuffmanFactorizer:
    def __init__(self, block_size: int = 64) -> None:
        self.block_size = block_size

    def _chunk_generator(self, binary_sequence: str) -> Iterator[int]:
        seq_len = len(binary_sequence)
        for i in range(0, seq_len, self.block_size):
            chunk = binary_sequence[i : i + self.block_size]
            if len(chunk) < self.block_size:
                return
            yield int(chunk, 2)

    def factorize(self, n: int) -> FactorizationResult:
        """
        Викликає C-скомпільовану функцію і пакує результат у dataclass.
        Перший виклик буде трохи довшим (йде компіляція Numba),
        усі наступні працюватимуть зі швидкістю C.
        """
        raw_primes, raw_exponents = _python_factorize(n)

        # Перетворюємо Numba List назад у звичайні Python list для сумісності з іншим кодом
        return FactorizationResult(
            primes=list(raw_primes),
            exponents=list(raw_exponents)
        )

    def process_sequence(self, binary_sequence: str) -> list[FactorizationResult]:
        # 1. Спочатку розбиваємо на блоки і рахуємо їхню кількість
        chunks = list(self._chunk_generator(binary_sequence))
        total_chunks = len(chunks)
        results = []

        print(f"\n[INFO] Знайдено {total_chunks} блоків для факторизації.")
        print("[INFO] Починаємо обробку (це може зайняти час для 63-бітних блоків)...")

        start_time = time.time()

        # 2. Обробляємо в звичайному циклі з виводом прогресу
        for i, num in enumerate(chunks):
            # Виводимо прогрес кожні 500 блоків
            if i > 0 and i % 500 == 0:
                elapsed = time.time() - start_time
                speed = i / elapsed
                print(f" ⏳ Оброблено: {i} / {total_chunks} блоків | Швидкість: {speed:.1f} блоків/сек")

            results.append(self.factorize(num))

        total_time = time.time() - start_time
        print(f"✅ Факторизацію завершено за {total_time:.2f} сек.")

        return results

# ==========================================
# 2. SIGNAL EXTRACTOR FUNCTIONS
# ==========================================

def extract_smoothness_signal(results: list[FactorizationResult]) -> list[int]:
    """
    Returns an array of exponent sums (total number of divisors) for each block.
    """
    return [sum(res.exponents) for res in results]

def extract_lpf_signal(results: list[FactorizationResult]) -> list[int]:
    """
    Returns an array of the Largest Prime Factors (LPF) for each block.
    """
    return [res.primes[-1] if res.primes else 1 for res in results]

# ==========================================
# 3. ANALYZERS AND VISUALIZERS
# ==========================================

class StatisticalVisualizer:
    """
    Analyzes and visualizes the statistical distribution of integer metrics
    (smoothness index, powers of two, etc.) to detect generation anomalies.
    """
    def __init__(self, signal_data: list[int]) -> None:
        self.signal = signal_data

    def plot_histogram(self, filename, title: str = "Distribution of Smoothness Index (Sum of Exponents)") -> None:
        """
        Builds a bar chart of frequencies and calculates the variance of the array.
        """
        if not self.signal:
            print("The data array is empty.")
            return

        # 1. Calculate frequencies (how many times each sum occurs)
        counts = Counter(self.signal)

        # Sort x-values from smallest to largest
        x_values = sorted(counts.keys())
        y_values = [counts[x] for x in x_values]

        # 2. Mathematical statistics for AI analysis
        mean_val = float(np.mean(self.signal))
        variance_val = float(np.var(self.signal)) # Variance is our main detector!

        # 3. Plotting the graph
        plt.figure(figsize=(10, 5))

        # Draw bars. zorder=3 puts them above the grid
        bars = plt.bar(
            x_values,
            y_values,
            color="mediumseagreen",
            edgecolor="darkgreen",
            alpha=0.85,
            zorder=3
        )

        # 4. Add exact numbers on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height + (max(y_values) * 0.015), # Slightly above the top
                str(height),
                ha='center',
                va='bottom',
                fontsize=10,
                fontweight='bold'
            )

        # 5. Formatting and design
        plt.title(f"FILENAME: {filename}  |  {title}\nVariance: {variance_val:.2f} | Mean: {mean_val:.2f}", fontsize=14, pad=15)
        plt.xlabel("Sum of exponents (Number of 'atoms' in a block)", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)

        # Ensure all integer steps are displayed on the X-axis
        plt.xticks(range(min(x_values), max(x_values) + 1))

        # Add a horizontal grid for better readability
        plt.grid(axis='y', linestyle='--', alpha=0.6, zorder=0)
        plt.tight_layout()
        plt.savefig(SAVE_PATH / f"2_{filename}__histogram.png")
        plt.show()

class LPFSpectralAnalyzer:
    """
    Applies Fast Fourier Transform to the discrete signal of Largest Prime Factors (LPF).
    """
    def __init__(self, lpf_signal: list[int]) -> None:
        self.raw_signal = lpf_signal
        self.signal: np.ndarray | None = None
        self.frequencies: np.ndarray | None = None
        self.amplitudes: np.ndarray | None = None
        self.peaks_indices: np.ndarray | None = None

    def run_pipeline(self) -> dict:
        """Executes the pipeline and returns spectral metrics."""
        if not self.raw_signal:
            return {}

        # Zero-mean centering and normalization
        raw_array = np.array(self.raw_signal, dtype=np.float32)
        centered_array = raw_array - np.mean(raw_array)
        max_abs_val = np.max(np.abs(centered_array))
        self.signal = centered_array / max_abs_val if max_abs_val > 0 else centered_array

        # Apply RFFT
        n = len(self.signal) # type: ignore
        fft_result = np.asarray(rfft(self.signal))
        self.frequencies = rfftfreq(n, d=1.0)

        raw_amplitudes = np.abs(fft_result)
        normalized_amps = (raw_amplitudes * 2.0) / n
        normalized_amps[0] /= 2.0
        if n % 2 == 0:
            normalized_amps[-1] /= 2.0

        self.amplitudes = normalized_amps

        baseline_noise = float(np.median(self.amplitudes)) # type: ignore

        # Lower thresholds for short test arrays
        min_height = baseline_noise * 1.5
        min_prominence = baseline_noise * 0.5

        self.peaks_indices, properties = find_peaks(
            self.amplitudes,
            height=min_height,
            prominence=min_prominence
        )

        peak_count = int(len(self.peaks_indices)) # type: ignore
        if peak_count > 0 and "peak_heights" in properties:
            max_amplitude = float(np.max(properties["peak_heights"]))
            snr = float(max_amplitude / (baseline_noise + 1e-10))
        else:
            max_amplitude = float(np.max(self.amplitudes)) if len(self.amplitudes) > 0 else 0.0 # type: ignore
            snr = 1.0

        return {
            "peak_count": peak_count,
            "max_amplitude": max_amplitude,
            "baseline_noise": baseline_noise,
            "snr": snr
        }

class SpectralVisualizer:
    """
    Visualizes the frequency spectrum and detected peaks.
    """
    def __init__(self, analyzer: LPFSpectralAnalyzer) -> None:
        self.analyzer = analyzer

    def plot_spectrum(self, filename, show_peaks: bool = True) -> None:
        if self.analyzer.frequencies is None or self.analyzer.amplitudes is None:
            return

        freqs = self.analyzer.frequencies
        amps = self.analyzer.amplitudes

        plt.figure(figsize=(12, 6))
        plt.plot(freqs, amps, color="steelblue", linewidth=1.2, alpha=0.85, label="LPF Spectrum")

        if show_peaks and self.analyzer.peaks_indices is not None and len(self.analyzer.peaks_indices) > 0:
            peak_idx = self.analyzer.peaks_indices
            plt.scatter(
                freqs[peak_idx],
                amps[peak_idx],
                color="crimson",
                marker="o",
                s=60,
                zorder=5,
                label=f"Peaks ({len(peak_idx)})"
            )

        plt.title(f"FILENAME: {filename}  |  Spectral Analysis of the LPF Array (AI vs Human)", fontsize=14)
        plt.xlabel("Frequency (cycles per block)", fontsize=12)
        plt.ylabel("Normalized Amplitude", fontsize=12)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig(SAVE_PATH / f"1_{filename}__FFT_factorize_huffman_likewords.png")
        plt.show()

# ==========================================
# MAIN EXECUTION BLOCK
# ==========================================
if __name__ == "__main__":

    filename = "Human 53 (30000)"
    binary_text = get_binary_from_file(filename)
    print("[1] Starting factorization of 32-bit blocks...")
    factorizer = HuffmanFactorizer(block_size=32)
    print(binary_text)
    results = factorizer.process_sequence(binary_text)
    print(f"Successfully processed blocks: {len(results)}\n")

    # ---------------------------------------------------------
    # Stage A: Statistical Analysis of Smoothness
    # ---------------------------------------------------------
    print("[2] Stage A: Smoothness Index Analysis...")
    smoothness_signal = extract_smoothness_signal(results)
    print(f"Array of exponent sums: {smoothness_signal}")

    stat_visualizer = StatisticalVisualizer(smoothness_signal)

    # NOTE: The plot blocks code execution. Close the plot window to continue.
    stat_visualizer.plot_histogram(filename)

    # ---------------------------------------------------------
    # Stage B: Spectral Analysis of the Largest Prime Factors (LPF)
    # ---------------------------------------------------------
    print("\n[3] Stage B: Spectral analysis of the LPF signal...")
    lpf_signal = extract_lpf_signal(results)
    print(f"LPF array: {lpf_signal}")

    lpf_analyzer = LPFSpectralAnalyzer(lpf_signal)
    metrics = lpf_analyzer.run_pipeline()

    print("\n=== Spectrum Metrics (LPF) ===")
    for k, v in metrics.items():
        print(f" - {k}: {v:.4f}" if isinstance(v, float) else f" - {k}: {v}")

    spectrum_visualizer = SpectralVisualizer(lpf_analyzer)
    spectrum_visualizer.plot_spectrum(filename)

    print("\n[4] Analysis completed successfully.")

