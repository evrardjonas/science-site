"""Rebuild the Kundt figures from the reported means; requires matplotlib."""

import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "src/content/kundt-measurements.json").read_text())
TOKENS = dict(re.findall(r"(--[\w-]+):\s*([^;]+);", (ROOT / "src/styles/tokens.css").read_text()))
READINGS = DATA["readings"]
MODES = [reading["mode"] for reading in READINGS]
SPACINGS = [reading["meanNodeSpacingCm"] for reading in READINGS]
# Unweighted least squares for d = L/n, constrained by the closed-tube model.
LENGTH_CM = sum(d / n for n, d in zip(MODES, SPACINGS)) / sum(1 / n**2 for n in MODES)
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


def draw(mobile: bool) -> None:
    plt.rcParams.update({
        "svg.fonttype": "none",
        "svg.hashsalt": "kundt-measured-node-spacing",
        "font.size": 12 if mobile else 13,
        "text.color": TOKENS["--color-ink"],
        "axes.labelcolor": TOKENS["--color-ink"],
        "xtick.color": TOKENS["--color-muted"],
        "ytick.color": TOKENS["--color-muted"],
        "axes.edgecolor": TOKENS["--color-muted"],
        "axes.facecolor": TOKENS["--color-surface"],
        "figure.facecolor": TOKENS["--color-surface"],
    })
    fig, ax = plt.subplots(figsize=(4.4, 5.0) if mobile else (9.0, 5.5))
    fig.subplots_adjust(left=0.19 if mobile else 0.11, right=0.96, bottom=0.20 if mobile else 0.18, top=0.79 if mobile else 0.80)
    x = [2 + 3 * i / 200 for i in range(201)]
    ax.plot(x, [LENGTH_CM / n for n in x], color=TOKENS["--color-muted"], linewidth=1.8,
            linestyle=(0, (4, 3)), label="Fit: d = L / n")
    ax.scatter(MODES, SPACINGS, s=65 if mobile else 80, color=TOKENS["--color-primary"],
               zorder=3, label="Measured means")
    for n, d in zip(MODES, SPACINGS):
        ax.annotate(f"{d:.1f} cm", (n, d), xytext=(0, 17 if mobile else 11), textcoords="offset points",
                    ha="center", color=TOKENS["--color-primary-dark"], fontsize=11 if mobile else 12)
    ax.set(xlim=(1.65, 5.35), ylim=(0, 60), xticks=MODES, yticks=list(range(0, 61, 10)),
           xlabel="Mode number n", ylabel="Mean node spacing d (cm)")
    ax.grid(axis="y", color=TOKENS["--color-line"], linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(length=0, pad=8)
    fig.text(0.5, 0.95, "Measured node spacing", ha="center", va="top", fontsize=15 if mobile else 18,
             fontweight="bold")
    fig.text(0.5, 0.89, f"Air temperature: {DATA['airTemperatureC']:.1f} °C", ha="center", va="top",
             color=TOKENS["--color-muted"], fontsize=11 if mobile else 12)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles[::-1], labels[::-1], loc="lower center", ncol=1 if mobile else 2,
               frameon=False, fontsize=10 if mobile else 12, bbox_to_anchor=(0.56 if mobile else 0.53, 0.005))
    name = "kundt-node-spacing" + ("-mobile" if mobile else "")
    output = ROOT / "public/media/scienteens" / f"{name}.svg"
    fig.savefig(output, metadata={"Date": None, "Creator": "Jonas · Sciences"})
    plt.close(fig)
    # Keep SVG text selectable and use the site's existing font stack.
    tree = ET.parse(output)
    svg = tree.getroot()
    title = ET.Element(f"{{{SVG_NS}}}title")
    title.text = "Mean node spacing for modes 2 to 5"
    description = ET.Element(f"{{{SVG_NS}}}desc")
    description.text = ("Measured mean distances: mode 2, 50.5 cm; mode 3, 33.5 cm; "
                        "mode 4, 25.0 cm; mode 5, 20.1 cm. Air temperature: 22.8 °C. "
                        "The dashed curve is an unweighted fit of d = L/n to these four means.")
    svg.insert(0, title)
    svg.insert(1, description)
    for node in svg.iter(f"{{{SVG_NS}}}text"):
        style = node.get("style", "")
        node.set("style", re.sub(r"font-family:[^;]+", "font-family: " + TOKENS["--font-body"], style))
    tree.write(output, encoding="unicode", xml_declaration=True)


if __name__ == "__main__":
    draw(False)
    draw(True)
    print(f"Generated both figures; fitted effective length = {LENGTH_CM:.3f} cm.")
