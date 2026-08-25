from string import punctuation
from collections import Counter
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def clean_text(text: str) -> str:

    CUSTOM_PUNCTUATION = punctuation + "«»—–’‘”" + "1234567890"
    DELETE_TABLE = str.maketrans('', '', CUSTOM_PUNCTUATION)
    return text.strip().casefold().translate(DELETE_TABLE)


def get_words(text: str)-> Counter[str]:
    cleaned_text = clean_text(text)
    words = cleaned_text.split()
    word_counts = Counter(words)
    return word_counts

def prepare_zipf_data(word_counts: Counter[str]) -> tuple[np.ndarray, np.ndarray]:
    sorted_items = word_counts.most_common()

    frequencies = [item[1] for item in sorted_items]

    y_freqs = np.array(frequencies)

    x_ranks = np.arange(1, len(y_freqs) + 1)

    return x_ranks, y_freqs

def show_plot_standard_zipf(x_ranks: np.ndarray, y_freqs: np.ndarray) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(x_ranks, y_freqs, color='blue', linewidth=2)
    plt.title("Zipf's Law (Standard Scale) --> Gospel of John")
    plt.xlabel("Word Rank")
    plt.ylabel("Frequency")
    plt.grid(True, linestyle='--', alpha=0.7)
    project_dir = Path(__file__).resolve().parent.parent
    output_path = project_dir / "results" / "zipf_gospel_john.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()


def main():
    project_dir = Path(__file__).resolve().parent.parent
    gospel_john = project_dir / "texts" / "test_John1.txt"
    epistale_john = project_dir / "texts" / "test_1_2_3_John.txt"

    with open(gospel_john, "r", encoding="utf-8") as file:
        text = file.read()

    cleaned_text = clean_text(text)
    word_counts = get_words(cleaned_text)
    x_ranks, y_freqs = prepare_zipf_data(word_counts)
    show_plot_standard_zipf(x_ranks, y_freqs)


if __name__ == "__main__":
    main()