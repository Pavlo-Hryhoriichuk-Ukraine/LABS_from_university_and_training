import os
import subprocess
import subprocess
import sys
from pathlib import Path
from for_backend import run_matrix_pipeline

PROJECT_DIR = Path(__file__).resolve().parent.parent


def generate_local_report(text: str, output_filename: str = "undef_report.html"):

    print("⏳ Starting analysis pipeline... This may take a few seconds depending on the text length.")

    data = run_matrix_pipeline(text)

    print("✅ Analisis complete. Generating HTML report...")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="uk">
    <head>
        <meta charset="UTF-8">
        <title>AlgorithmStudio - Full Text Analysis</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 20px; }}
            .container {{ max-width: 1200px; margin: auto; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .verdict-box {{ background-color: #e8f8f5; border-left: 6px solid #1abc9c; padding: 20px; margin-bottom: 30px; font-size: 18px; font-weight: bold; line-height: 1.5; }}
            .section {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }}
            h2 {{ color: #2980b9; margin-top: 0; }}
            .metrics-list {{ font-size: 16px; background: #fdfefe; padding: 15px; border-radius: 5px; border: 1px solid #eaeded; }}
            .images-grid {{ display: flex; gap: 20px; flex-wrap: wrap; margin-top: 15px; }}
            .images-grid div {{ flex: 1; min-width: 400px; text-align: center; }}
            img {{ max-width: 100%; border: 1px solid #bdc3c7; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔬 AlgorithmStudio: Full Text Analysis</h1>

            <div class="verdict-box">
                {data['overall_verdict']}
            </div>

            <div class="section">
                <h2>1. Zipf's Law and Huffman Coding</h2>
                <div class="metrics-list">
                    <strong>Zipf:</strong> Slope = {data['zipf']['slope']} <br><br>
                    <strong>Huffman:</strong>
                    Entropy (H) = {data['huffman']['entropy_H']} |
                    Avg. Length (L) = {data['huffman']['avg_length_L']} |
                    Redundancy (R) = {data['huffman']['redundancy_R']}
                </div>
                <div class="images-grid">
                    <div>
                        <img src="data:image/png;base64,{data['zipf']['plot_base64']}" alt="Zipf Plot">
                    </div>
                </div>
            </div>
    """

    for size, matrix_data in data['matrices'].items():
        html_content += f"""
            <div class="section">
                <h2>2. Markov Analysis (Matrix {size}x{size})</h2>
                <div class="metrics-list">
                    <strong>λ2 (Relaxation Speed):</strong> {matrix_data['metrics']['lambda_2']} <br>
                    <strong>Deterministic Rows (Patterns):</strong> {matrix_data['metrics']['deterministic_rows']} <br>
                    <strong>Triangle Angles:</strong> {matrix_data['metrics']['angles']}
                </div>
                <div class="images-grid">
                    <div>
                        <h3>Heatmap of Transitions</h3>
                        <img src="data:image/png;base64,{matrix_data['visualizations']['heatmap_base64']}" alt="Heatmap {size}">
                    </div>
        """

        if matrix_data['visualizations']['triangle_base64']:
            html_content += f"""
                    <div>
                        <h3> Spectral Triangle</h3>
                        <img src="data:image/png;base64,{matrix_data['visualizations']['triangle_base64']}" alt="Triangle {size}">
                    </div>
            """
        html_content += """
                </div>
            </div>
        """

    html_content += """
        </div>
    </body>
    </html>
    """

    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(html_content)

    filepath = os.path.realpath(output_filename)
    try:
        if sys.platform == "win32":
            os.startfile(filepath)  # For Windows
        elif sys.platform == "darwin":
            subprocess.run(["open", filepath])  # For macOS
        else:
            subprocess.run(["xdg-open", filepath])  # For Linux
        print(f"🌐 Report opened in your system browser! (File: {output_filename})")
    except Exception as e:
        print(f"Error occurred while trying to open the report. Please open the file manually: {filepath}")



def main():
    raw_filename = "test_Luke1.txt"
    text_filename = PROJECT_DIR / "texts" / raw_filename
    output_file = PROJECT_DIR / "results" / (raw_filename + "_report.html")

    with open(text_filename, "r", encoding="utf-8") as file:
        raw_text = file.read()

    generate_local_report(raw_text, output_filename=str(output_file))


if __name__ == "__main__":
    main()