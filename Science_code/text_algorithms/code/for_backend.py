import io
import base64
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.figure import Figure
import numpy as np
from string import punctuation

from matrix_analize import (
    analyze_eigenvalues, build_matrix_16, normalize_matrix,
    build_matrix_32, build_matrix_64, build_matrix_128, build_matrix_256
)
from huffman import result_analize
from triangles import calculate_triangle_angles, calculate_means


def clean_text(text: str) -> str:
    CUSTOM_PUNCTUATION = punctuation + "«»—–’‘”“" + "1234567890"
    DELETE_TABLE = str.maketrans('', '', CUSTOM_PUNCTUATION)
    return text.strip().casefold().translate(DELETE_TABLE)

# ---------------------------------------------------------
# VISUALIZATION MODULE
# ---------------------------------------------------------

def plot_transition_matrix(matrix: np.ndarray, title: str = "Transition Matrix") -> Figure:
    """
    Generates a heatmap visualization of the state transition matrix.
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    cax = ax.imshow(matrix, cmap='magma', interpolation='nearest')
    fig.colorbar(cax, ax=ax, label="Transition Probability")

    ax.set_title(title, fontsize=14, pad=15)
    ax.set_xlabel("Next State (Class)")
    ax.set_ylabel("Current State (Class)") # type: ignore

    ax.set_xticks(np.arange(-0.5, matrix.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, matrix.shape[0], 1), minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=0.5, alpha=0.1)
    ax.tick_params(which="minor", size=0)

    fig.tight_layout()
    return fig

def fig_to_base64(fig: Figure) -> str:
    """
    Converts a Matplotlib figure into a Base64 string for API transmission.
    Closes the figure automatically to prevent memory leaks on the server.
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

def plot_means_triangle(am: float, gm: float, hm: float, angles: list[float]) -> Figure:
    """
    Plots a spectral triangle based on Arithmetic, Geometric, and Harmonic means.
    """
    fig, ax = plt.subplots(figsize=(6, 6))

    p1 = np.array([0.0, 0.0])
    p2 = np.array([am, 0.0])

    # Calculate the third vertex using the Law of Cosines
    x3 = (am**2 + gm**2 - hm**2) / (2 * am)
    y3 = np.sqrt(abs(gm**2 - x3**2))
    p3 = np.array([x3, y3])

    triangle = Polygon([p1, p2, p3], closed=True, facecolor='cyan', edgecolor='blue', alpha=0.3, linewidth=2)
    ax.add_patch(triangle)

    ax.set_aspect('equal')
    ax.set_xlim(-0.05 * am, am * 1.05)
    ax.set_ylim(-0.05 * am, y3 * 1.15)

    ax.text(am / 2, -0.05 * am, f"AM = {am:.3f}", ha='center', va='top', fontsize=10, color='blue')
    ax.text(x3 / 2, y3 / 2, f"GM = {gm:.3f}", ha='right', va='bottom', fontsize=10, color='blue')
    ax.text((am + x3) / 2, y3 / 2, f"HM = {hm:.3f}", ha='left', va='bottom', fontsize=10, color='blue')

    title_text = f"Spectral Triangle\nAngles: {angles[0]:.1f}°, {angles[1]:.1f}°, {angles[2]:.1f}°"
    ax.set_title(title_text, fontsize=12, pad=15)
    ax.axis('off')

    return fig


def analyze_zipf_and_plot(cleaned_text: str) -> tuple[float, str]:
    """
    Plots the Zipf's Law distribution (Log-Log scale) and returns the trendline slope.
    """
    words = cleaned_text.split()
    if not words:
        return 0.0, ""

    word_counts = Counter(words)
    frequencies = np.array([count for _, count in word_counts.most_common()])
    ranks = np.arange(1, len(frequencies) + 1)

    log_ranks = np.log10(ranks)
    log_freqs = np.log10(frequencies)

    if len(ranks) > 1:
        slope, intercept = np.polyfit(log_ranks, log_freqs, 1)
    else:
        slope, intercept = 0.0, log_freqs[0]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.loglog(ranks, frequencies, marker='.', linestyle='none', color='indigo', alpha=0.7)

    trend_line = (10 ** intercept) * (ranks ** slope)
    ax.plot(ranks, trend_line, color='red', linestyle='--', label=f'Trend (Slope: {slope:.2f})')

    ax.set_title("Zipf's Law (Log-Log Scale)")
    ax.set_xlabel("Log(Rank)")
    ax.set_ylabel("Log(Frequency)")
    ax.legend()
    ax.grid(True, which="both", linestyle='--', alpha=0.3)
    fig.tight_layout()

    return float(slope), fig_to_base64(fig)


# ---------------------------------------------------------
# MAIN DECISION ENGINE (PIPELINE)
# ---------------------------------------------------------

def run_matrix_pipeline(raw_text: str) -> dict:
    """
    Executes the full text analysis pipeline: Zipf's law, Huffman entropy,
    Markov transition matrices (16-256), and Spectral Geometry.
    Returns a structured dictionary with metrics, Base64 images, and the final verdict.
    """
    cleaned_text = clean_text(raw_text)

    # 1. Zipf Analysis
    zipf_slope, zipf_b64 = analyze_zipf_and_plot(cleaned_text)

    # 2. Huffman Analysis (Entropy, Avg Length, Redundancy)
    try:
        H, L, R = result_analize(raw_text)
    except Exception:
        H, L, R = 0.0, 0.0, 0.0

    # 3. Markov Matrix Initialization
    matrix_builders = {
        "16": build_matrix_16,
        "32": build_matrix_32,
        "64": build_matrix_64,
        "128": build_matrix_128,
        "256": build_matrix_256
    }

    response_data: dict[str, dict | str] = {
        "zipf": {
            "slope": round(zipf_slope, 4),
            "plot_base64": zipf_b64
        },
        "huffman": {
            "entropy_H": round(H, 4),
            "avg_length_L": round(L, 4),
            "redundancy_R": round(R, 4)
        },
        "matrices": {},
        "overall_verdict": ""
    }

    human_score = 0
    ai_score = 0
    valid_lambda_2s = []
    equilateral_triangles = 0
    total_deterministic_rows = 0

    # 4. Matrix Iteration and Spectral Analysis
    for size_str, builder_func in matrix_builders.items():
        raw_matrix = builder_func(raw_text)
        norm_matrix = normalize_matrix(raw_matrix)

        # Identify absolute deterministic states (Zero Conditional Entropy)
        deterministic_rows = int(np.sum(norm_matrix == 1.0))
        total_deterministic_rows += deterministic_rows

        eigenvalues = analyze_eigenvalues(norm_matrix)
        lambda_2 = float(eigenvalues[1]) if len(eigenvalues) > 1 else 0.0
        valid_lambda_2s.append(lambda_2)

        fig_matrix = plot_transition_matrix(norm_matrix, title=f"Transition Matrix ({size_str}x{size_str})")
        b64_heatmap = fig_to_base64(fig_matrix)

        b64_triangle = None
        triangle_angles = None

        try:
            am, gm, hm = calculate_means(eigenvalues)

            # Перевірка нерівності трикутника (AM завжди найбільша сторона)
            if (gm + hm) > am:
                angles = calculate_triangle_angles(am, gm, hm)
                triangle_angles = [float(a) for a in angles]
                fig_tri = plot_means_triangle(am, gm, hm, triangle_angles)
                b64_triangle = fig_to_base64(fig_tri)

                # Equilateral triangle detection (AI marker)
                if (max(triangle_angles) - min(triangle_angles)) < 20.0:
                    equilateral_triangles += 1
            else:
                # Сторони не утворюють трикутник
                triangle_angles = None
                b64_triangle = None
                print(f"The triangle cannot be made: AM={am:.2f}, GM={gm:.2f}, HM={hm:.2f}")

        except ValueError as e:
            print(f"ValueError (maybe, complex values) : {e}")
            triangle_angles = None
            b64_triangle = None

        response_data["matrices"][size_str] = { # type: ignore
            "metrics": {
                "lambda_2": round(lambda_2, 4),
                "deterministic_rows": deterministic_rows,
                "angles": [round(a, 1) for a in triangle_angles] if triangle_angles else None
            },
            "visualizations": {
                "heatmap_base64": b64_heatmap,
                "triangle_base64": b64_triangle
            }
        }

    # 5. Scoring System (AI vs Human)
    if -1.15 <= zipf_slope <= -0.85:
        human_score += 2
    else:
        ai_score += 2

    avg_lambda_2 = sum(valid_lambda_2s) / len(valid_lambda_2s) if valid_lambda_2s else 0
    if avg_lambda_2 > 0.5: human_score += 1
    elif avg_lambda_2 < 0.3: ai_score += 1

    if total_deterministic_rows > 15:
        ai_score += 2
    elif total_deterministic_rows <= 5:
        human_score += 1

    if equilateral_triangles >= 2: ai_score += 2
    else: human_score += 1

    if R > 0.4: human_score += 2
    elif R < 0.2: ai_score += 2

    # 6. Final Verdict Generation
    total_score = human_score - ai_score

    if total_score >= 3:
        verdict = (
            f"CONCLUSION: The text was likely written by a human. A natural vocabulary distribution (Zipf diagram slope = {zipf_slope:.2f}), "
            f"high informational redundancy (R = {R:.2f}), and an asymmetrical transition structure "
            f"confirm a genuine authorial style."
        )
    elif total_score <= -3:
        verdict = (
            f"CONCLUSION: The text was generated by AI. A perfectly symmetrical distribution (Spectral Triangles), "
            f"low redundancy (R = {R:.2f}), and an anomalous number of rigid templates "
            f"({total_deterministic_rows} perfect rows in matrices) indicate machine generation."
        )
    else:
        verdict = (
            f"CONCLUSION: 'Gray Zone'. This may be human text heavily edited by AI (or vice versa). "
            f"The metrics are mixed: Zipf diagram slope = {zipf_slope:.2f}, R = {R:.2f}, λ2 = {avg_lambda_2:.2f}. "
            f"Found {total_deterministic_rows} deterministic patterns in matrixes."
        )

    response_data["overall_verdict"] = verdict
    return response_data