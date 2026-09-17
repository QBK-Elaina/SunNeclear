# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""
Render a century of solar activity as a color grid.
    uv run sun_heatmap.py
"""

from pathlib import Path
import matplotlib.pyplot as plt

FILE = "sunspots.csv"
PICTURE = "sun_heatmap.png"

HERE = Path(__file__).parent
DATA = HERE / "data" / FILE
OUT = HERE / "out"


def main():
    text = DATA.read_text(encoding="utf-8")
    data_dict = {}
    for line in text.strip().splitlines():
        parts = line.split(";")
        if len(parts) >= 4:
            try:
                y = int(float(parts[0]))
                m = int(float(parts[1]))
                val = float(parts[3])
                if val >= 0:
                    data_dict[(y, m)] = val
            except ValueError:
                continue

    # 选取最近 100 年 (1926 - 2026) 制作精细热力图
    years = list(range(1926, 2027))
    matrix = []
    for y in years:
        row = [data_dict.get((y, m), 0) for m in range(1, 13)]
        matrix.append(row)

    fig, ax = plt.subplots(figsize=(10, 6))
    cax = ax.imshow(matrix, aspect="auto", cmap="inferno", origin="lower",
                    extent=[1, 12, years[0], years[-1]])

    fig.colorbar(cax, label="Monthly Mean Sunspot Number")
    ax.set_xlabel("Month")
    ax.set_ylabel("Year")
    ax.set_title("Solar Activity Intensity Heatmap (1926 - 2026)")
    fig.tight_layout()

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=300)
    print(f"saved out/{PICTURE}")
    plt.show()


if __name__ == "__main__":
    main()
