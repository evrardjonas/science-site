"""Régression f = v / lambda et figures du tube de Kundt.

Exécution : python scripts/plot-kundt-measurements.py
Dépendances : numpy et matplotlib.
Les quatre points utilisent les fréquences choisies et les distances moyennes
mesurées. La droite passe par l'origine ; les longueurs d'onde sont en mètres.
"""

import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "src/content/kundt-measurements.json").read_text())
TOKENS = dict(re.findall(r"(--[\w-]+):\s*([^;]+);", (ROOT / "src/styles/tokens.css").read_text()))
READINGS = DATA["readings"]
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


def regress(readings: list[dict]) -> dict:
    # Deux nœuds voisins sont séparés d'une demi-longueur d'onde.
    wavelength = np.array([2 * row["meanNodeSpacingCm"] / 100 for row in readings])
    frequency = np.array([row["frequencyHz"] for row in readings], dtype=float)
    if not (len(readings) >= 2 and np.all(np.isfinite(wavelength))
            and np.all(np.isfinite(frequency)) and np.all(wavelength > 0)
            and np.all(frequency > 0)):
        raise ValueError("Il faut au moins deux couples fréquence / distance valides.")
    inverse_wavelength = 1 / wavelength
    # Moindres carrés sans constante : v = somme(x f) / somme(x²).
    speed = float(np.dot(inverse_wavelength, frequency) / np.dot(inverse_wavelength, inverse_wavelength))
    predicted = speed * inverse_wavelength
    residual = frequency - predicted
    residual_sum_squares = float(np.dot(residual, residual))
    centred_sum_squares = float(np.sum((frequency - frequency.mean()) ** 2))
    if centred_sum_squares == 0:
        raise ValueError("Le R² centré nécessite des fréquences distinctes.")
    # R² centré : référence à la moyenne des fréquences, même sans constante.
    r_squared = 1 - residual_sum_squares / centred_sum_squares
    return {
        "model": "f = v / lambda",
        "throughOrigin": True,
        "speedMS": speed,
        "rSquared": r_squared,
        "rSquaredDefinition": "1 - sum((f - v / lambda)^2) / sum((f - mean(f))^2)",
        "residualSumSquaresHz2": residual_sum_squares,
        "centredSumSquaresHz2": centred_sum_squares,
        "points": [
            {"mode": row["mode"], "frequencyHz": float(f), "meanNodeSpacingCm": row["meanNodeSpacingCm"],
             "wavelengthM": float(lam), "inverseWavelengthM": float(x),
             "predictedFrequencyHz": float(fit), "residualHz": float(error)}
            for row, f, lam, x, fit, error in zip(readings, frequency, wavelength, inverse_wavelength, predicted, residual)
        ],
    }


def draw(result: dict, mobile: bool) -> None:
    plt.rcParams.update({
        "svg.fonttype": "none",
        "svg.hashsalt": "kundt-sound-speed-regression",
        "font.size": 12 if mobile else 13,
        "text.color": TOKENS["--color-ink"],
        "axes.labelcolor": TOKENS["--color-ink"],
        "xtick.color": TOKENS["--color-muted"],
        "ytick.color": TOKENS["--color-muted"],
        "axes.edgecolor": TOKENS["--color-muted"],
        "axes.facecolor": TOKENS["--color-surface"],
        "figure.facecolor": TOKENS["--color-surface"],
    })
    fig, ax = plt.subplots(figsize=(4.4, 5.5) if mobile else (9.0, 5.5))
    fig.subplots_adjust(left=0.19 if mobile else 0.11, right=0.96, bottom=0.20 if mobile else 0.18, top=0.79 if mobile else 0.80)
    points = result["points"]
    x = np.linspace(0, 2.8, 201)
    ax.plot(x, result["speedMS"] * x, color=TOKENS["--color-muted"], linewidth=1.8,
            linestyle=(0, (4, 3)), label="Linear fit through origin")
    ax.scatter([p["inverseWavelengthM"] for p in points], [p["frequencyHz"] for p in points],
               s=65 if mobile else 80, color=TOKENS["--color-primary"], zorder=3, label="Measurements")
    for point in points:
        ax.annotate(f"n = {point['mode']}", (point["inverseWavelengthM"], point["frequencyHz"]),
                    xytext=(-8, 10), textcoords="offset points", ha="right",
                    color=TOKENS["--color-primary-dark"], fontsize=10 if mobile else 12)
    ax.text(0.06, 0.95, f"f = v × (1/λ)\nv = {result['speedMS']:.2f} m/s\nR² = {result['rSquared']:.6f}",
            transform=ax.transAxes, va="top", fontsize=12 if mobile else 14, linespacing=1.5)
    ax.set(xlim=(0, 2.8), ylim=(0, 1000), xticks=np.arange(0, 3, 0.5), yticks=list(range(0, 1001, 200)),
           xlabel="Inverse wavelength 1/λ (m⁻¹)", ylabel="Driving frequency f (Hz)")
    ax.grid(axis="y", color=TOKENS["--color-line"], linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(length=0, pad=8)
    fig.text(0.5, 0.95, "Frequency and inverse wavelength", ha="center", va="top", fontsize=14 if mobile else 18,
             fontweight="bold")
    fig.text(0.5, 0.89, f"Closed tube: {DATA['tubeLengthM']:.2f} m | Air: {DATA['airTemperatureC']:.1f} °C", ha="center", va="top",
             color=TOKENS["--color-muted"], fontsize=11 if mobile else 12)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles[::-1], labels[::-1], loc="lower center", ncol=1 if mobile else 2,
               frameon=False, fontsize=10 if mobile else 12, bbox_to_anchor=(0.56 if mobile else 0.53, 0.005))
    name = "kundt-sound-speed" + ("-mobile" if mobile else "")
    output = ROOT / "public/media/scienteens" / f"{name}.svg"
    fig.savefig(output, metadata={"Date": None})
    plt.close(fig)
    # Keep SVG text selectable and use the site's existing font stack.
    tree = ET.parse(output)
    svg = tree.getroot()
    title = ET.Element(f"{{{SVG_NS}}}title")
    title.text = "Driving frequency as a function of inverse measured wavelength"
    description = ET.Element(f"{{{SVG_NS}}}desc")
    description.text = (
        "; ".join(f"mode {p['mode']}: f = {p['frequencyHz']:g} Hz, λ = {p['wavelengthM']:.3f} m" for p in points)
        + f". Air temperature: {DATA['airTemperatureC']:.1f} °C. "
        + f"Least-squares fit through the origin: f = v / λ, v = {result['speedMS']:.2f} m/s, "
        + f"centred R² = {result['rSquared']:.6f}."
    )
    svg.insert(0, title)
    svg.insert(1, description)
    for node in svg.iter(f"{{{SVG_NS}}}text"):
        style = node.get("style", "")
        node.set("style", re.sub(r"font-family:[^;]+", "font-family: " + TOKENS["--font-body"], style))
    tree.write(output, encoding="unicode", xml_declaration=True)


if __name__ == "__main__":
    result = regress(READINGS)
    output = ROOT / "src/content/kundt-regression.json"
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    draw(result, False)
    draw(result, True)
    print(f"v = {result['speedMS']:.6f} m/s ; R² centré = {result['rSquared']:.9f}")
