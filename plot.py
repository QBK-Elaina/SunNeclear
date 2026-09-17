# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""
Read the file in data/, make one picture, save it to out/.

    uv run plot.py
"""

from pathlib import Path
import matplotlib.pyplot as plt

FILE = "sunspots.csv"                          # 与 fetch.py 中的文件名一致
PICTURE = "plot.png"                           # 保存的图片名称

HERE = Path(__file__).parent
DATA = HERE / "data" / FILE
OUT = HERE / "out"


def rows(path):
    """读取 SILSO 的 CSV 文件（以分号分隔），返回有效行列表。"""
    kept = []
    text = path.read_text(encoding="utf-8")
    for line in text.strip().splitlines():
        parts = line.split(";")
        if len(parts) >= 4:
            kept.append(parts)
    return kept


def main():
    table = rows(DATA)
    print(f"{DATA.name}: {len(table)} rows. The first one: {table[0]}")

    time_axis, spots = [], []
    for row in table:                            # 核心要求：循环遍历数据
        try:
            year = float(row[0])
            month = float(row[1])
            spot = float(row[3])                 # 第四列是月平均黑子数
            if spot >= 0:
                # 将年和月转化为小数形式作为时间轴
                time_axis.append(year + (month - 1) / 12.0)
                spots.append(spot)
        except ValueError:
            continue

    print(f"{len(spots)} values, from {min(spots)} to {max(spots)}")

    # 绘制百年太阳黑子周期折线图
    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.plot(time_axis, spots, color="#e34a33", linewidth=0.6)
    ax.set_xlabel("Year")
    ax.set_ylabel("Monthly Mean Sunspot Number")
    ax.set_title("Solar Activity Cycle: Monthly Mean Sunspots (1749 - Present)")
    ax.grid(True, linestyle="--", alpha=0.3)
    fig.tight_layout()

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=300)
    print(f"saved out/{PICTURE}")
    plt.show()


if __name__ == "__main__":
    main()
