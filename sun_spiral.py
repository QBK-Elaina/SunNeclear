# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""
Transform the linear solar cycle into a polar spiral to highlight the 11-year periodicity.
    uv run sun_spiral.py
"""

from pathlib import Path
import math
import matplotlib.pyplot as plt

FILE = "sunspots.csv"
PICTURE = "sun_spiral.png"

HERE = Path(__file__).parent
DATA = HERE / "data" / FILE
OUT = HERE / "out"


def main():
    text = DATA.read_text(encoding="utf-8")
    years, spots = [], []
    for line in text.strip().splitlines():
        parts = line.split(";")
        if len(parts) >= 4:
            try:
                y = float(parts[0])
                m = float(parts[1])
                val = float(parts[3])
                if val >= 0:
                    years.append(y + (m - 1) / 12.0)
                    spots.append(val)
            except ValueError:
                continue

    # 将 11 年作为一个完整圆周 (2 * pi)
    cycle_years = 11.0
    theta = [((y % cycle_years) / cycle_years) * 2 * math.pi for y in years]
    r = spots

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})

    # 散点颜色映射年份，让远古和现代有色彩区分
    scatter = ax.scatter(theta, r, c=years, cmap="hot", s=4, alpha=0.5)

    ax.set_title("Solar Activity 11-Year Phase Spiral", va="bottom", fontsize=12)
    fig.colorbar(scatter, label="Year", pad=0.1)

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=300)
    print(f"saved out/{PICTURE}")
    plt.show()


if __name__ == "__main__":
    main()
