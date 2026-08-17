# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Build data files, figures and README.md from nysflag_colormaps.py.

Usage: uv run scripts/build_assets.py   (run in the repository root)
"""
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

import nysflag_colormaps as nyc

DATA = ROOT / "data"
CSV_DIR = DATA / "csv"
IMG = ROOT / "images"
for d in (DATA, CSV_DIR, IMG):
    d.mkdir(exist_ok=True)

FAMILY_DISPLAY = {"pink": "Pink", "reds_crown": "Reds", "reds_mods": "Reds",
                  "reds_capes": "Reds", "reds_trans": "Reds", "gold": "Gold",
                  "tenne": "Tenne", "green": "Green", "teal": "Teal",
                  "bedsheet": "Bedsheet", "purple": "Purple", "grey": "Grey",
                  "cendere": "Cendere"}
HEX_TO_FAMILIES: dict[str, set[str]] = {}
for fam, entries in nyc.RAW.items():
    for _, rgb in entries:
        HEX_TO_FAMILIES.setdefault(nyc.rgb_to_hex(rgb), set()).add(
            FAMILY_DISPLAY[fam])

SEQ_FAMILY = {"nyf_gold_seq": "Gold", "nyf_blue_seq": "Bedsheet",
              "nyf_red_seq": "Reds", "nyf_pink_seq": "Pink",
              "nyf_green_seq": "Green", "nyf_tenne_seq": "Tenne",
              "nyf_grey_seq": "Grey", "nyf_cendere_seq": "Cendere"}
DIV_FAMILIES = {
    "nyf_red_blue": "Reds, Bedsheet",
    "nyf_tenne_teal": "Tenne, Teal, Bedsheet",
    "nyf_gold_purple": "Gold, Purple",
    "nyf_pink_green": "Pink, Green",
    "nyf_blue_gold": "Bedsheet, Gold",
    "nyf_tenne_blue": "Tenne, Bedsheet",
    "nyf_red_teal": "Reds, Teal, Bedsheet",
    "nyf_pink_blue": "Pink, Bedsheet",
}

USE = {"qualitative": "categorical data",
       "sequential": "ordered data",
       "diverging": "data with a center value"}


def kind_of(name):
    if name in nyc.QUALITATIVE:
        return "qualitative"
    if name in nyc.SEQUENTIAL_STOPS:
        return "sequential"
    return "diverging"


def colors_of(name):
    if name in nyc.QUALITATIVE:
        return nyc.QUALITATIVE[name]
    if name in nyc.SEQUENTIAL_STOPS:
        return nyc.SEQUENTIAL_STOPS[name]
    s = nyc.DIVERGING_STOPS[name]
    return s["left"] + s["center"] + s["right"]


# --------------------------------------------------------------------------
# 1. raw data exports
# --------------------------------------------------------------------------
meta: dict[str, dict] = {}
for name in nyc.ALL_NAMES:
    kind = kind_of(name)
    cols = colors_of(name)
    entry: dict = {"type": kind, "colors": cols,
                   "use": USE[kind],
                   "lstar": [round(nyc.lstar(nyc.hex_to_rgb(h)), 1)
                             for h in cols]}
    if kind == "qualitative":
        entry["source_families"] = sorted(
            {f for h in cols for f in HEX_TO_FAMILIES.get(h, set())})
        entry["min_de"] = round(nyc._min_de(cols), 1)
    elif kind == "sequential":
        entry["source_families"] = [SEQ_FAMILY[name]]
        dl = [round(b - a, 1) for a, b in zip(entry["lstar"],
                                              entry["lstar"][1:])]
        entry["dlstar"] = dl
        entry["ramp_256"] = nyc.sequential_ramp(name)
    else:
        entry["source_families"] = DIV_FAMILIES[name].split(", ")
        entry["ramp_256"] = nyc.diverging_ramp(name)
    meta[name] = entry

    with open(CSV_DIR / f"{name}.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["index", "hex", "red", "green", "blue", "lstar"])
        for i, h in enumerate(cols):
            r, g, b = nyc.hex_to_rgb(h)
            w.writerow([i, h, r, g, b,
                        round(nyc.lstar(nyc.hex_to_rgb(h)), 1)])

with open(DATA / "palettes.json", "w") as fh:
    json.dump({"source": "New York State flag diagram, 109 shades",
               "colormaps": meta}, fh, indent=2)

# --------------------------------------------------------------------------
# 2. figures
# --------------------------------------------------------------------------
rng = np.random.default_rng(7)
X, Y = np.mgrid[-3:3:200j, -3:3:200j]
Z = (1 - X / 2 + X**5 + Y**3) * np.exp(-X**2 - Y**2)
W = np.sin(X) * np.cos(Y * 0.7) + 0.3 * X
WMAX = np.abs(W).max()


def lab_of(h):
    return nyc.rgb_to_lab(nyc.hex_to_rgb(h))


def txt_color(h):
    return "black" if lab_of(h)[0] > 60 else "white"


def stop_positions(hexes):
    labs = [lab_of(h) for h in hexes]
    d = [sum(abs(a[i] - b[i]) for i in range(3))
         for a, b in zip(labs, labs[1:])]
    return np.concatenate(([0], np.cumsum(d))) / (sum(d) or 1.0)


def swatch_strip(ax, hexes):
    ax.imshow(np.arange(len(hexes))[None, :], cmap=ListedColormap(hexes),
              aspect="auto", interpolation="nearest")
    ax.set_xticks(range(len(hexes)))
    ax.set_xticklabels(hexes, rotation=45, ha="right", fontsize=8)
    ax.set_yticks([])
    for i, h in enumerate(hexes):
        ax.text(i, 0, f"L*{lab_of(h)[0]:.0f}", ha="center", va="center",
                fontsize=8, color=txt_color(h))


def figure_qualitative(name):
    hexes = nyc.QUALITATIVE[name]
    fig = plt.figure(figsize=(11, 9))
    gs = GridSpec(3, 2, figure=fig, height_ratios=[1.1, 3, 3],
                  hspace=0.55, wspace=0.25)
    swatch_strip(fig.add_subplot(gs[0, :]), hexes)
    ax1 = fig.add_subplot(gs[1, 0])
    for k in range(8):
        c = rng.normal(0, 1, (60, 2)) + rng.normal(0, 2.2, 2)
        ax1.scatter(c[:, 0], c[:, 1], s=16, color=hexes[k],
                    label=f"group {k + 1}", edgecolors="none")
    ax1.set_title("categorical scatter")
    ax1.legend(ncol=4, fontsize=7, frameon=False)
    ax2 = fig.add_subplot(gs[1, 1])
    ax2.bar(range(8), rng.uniform(20, 90, 8), yerr=rng.uniform(3, 9, 8),
            capsize=4, color=hexes, edgecolor="0.3")
    ax2.set_xticks(range(8))
    ax2.set_xticklabels([f"cat {i + 1}" for i in range(8)], fontsize=8)
    ax2.set_title("bar chart with error bars")
    ax3 = fig.add_subplot(gs[2, :])
    t = np.linspace(0, 10, 50)
    for k in range(8):
        ax3.plot(t, np.sin(t * (0.5 + 0.13 * k) + k) + 0.15 * k,
                 color=hexes[k], lw=2, label=f"series {k + 1}")
    ax3.set_title("line plot")
    ax3.legend(ncol=8, fontsize=7, frameon=False)
    fig.suptitle(f"{name} - qualitative (8 categorical colors)",
                 fontweight="bold")
    fig.savefig(IMG / f"{name}.png", dpi=130, bbox_inches="tight")
    plt.close(fig)


def figure_ramp(name, stops, ramp, kind):
    fig = plt.figure(figsize=(11, 8))
    gs = GridSpec(3, 2, figure=fig, height_ratios=[1, 1.2, 3.2],
                  hspace=0.6, wspace=0.25, width_ratios=[1, 2])
    pos = stop_positions(stops)
    center_at = pos[len(stops) // 2] if kind == "diverging" else None
    ax0 = fig.add_subplot(gs[0, :])
    ax0.imshow(np.arange(len(ramp))[None, :], cmap=ListedColormap(ramp),
               aspect="auto", interpolation="nearest")
    ax0.set_xticks([])
    ax0.set_yticks([])
    if center_at is not None:
        ax0.axvline(center_at * (len(ramp) - 1), color="0.25", ls=":", lw=1)
    swatch_strip(fig.add_subplot(gs[1, :]), stops)
    axl = fig.add_subplot(gs[2, 0])
    t = np.linspace(0, 1, len(ramp))
    axl.plot(t, [lab_of(h)[0] for h in ramp], "k-", lw=1.2)
    axl.scatter(pos, [lab_of(h)[0] for h in stops], c=stops,
                edgecolor="0.3", s=40, zorder=3)
    axl.set_ylim(0, 105)
    axl.set_xlabel("position")
    axl.set_ylabel("CIELAB L*")
    axl.set_title("lightness profile")
    axf = fig.add_subplot(gs[2, 1])
    if kind == "diverging":
        axf.pcolormesh(X, Y, W, cmap=ListedColormap(ramp), shading="auto",
                       vmin=-WMAX, vmax=WMAX)
        axf.set_title("diverging field (centered norm)")
    else:
        axf.pcolormesh(X, Y, Z, cmap=ListedColormap(ramp), shading="auto")
        axf.set_title("sequential field")
    axf.set_xticks([])
    axf.set_yticks([])
    fig.suptitle(f"{name} - {kind} (stops from the NY flag diagram)",
                 fontweight="bold")
    fig.savefig(IMG / f"{name}.png", dpi=130, bbox_inches="tight")
    plt.close(fig)


for name in nyc.QUALITATIVE:
    figure_qualitative(name)
for name, stops in nyc.SEQUENTIAL_STOPS.items():
    figure_ramp(name, stops, nyc.sequential_ramp(name), "sequential")
for name, s in nyc.DIVERGING_STOPS.items():
    figure_ramp(name, s["left"] + s["center"] + s["right"],
                nyc.diverging_ramp(name), "diverging")

# --------------------------------------------------------------------------
# 3. highlights figure
# --------------------------------------------------------------------------
HIGHLIGHTS = ["nyf_forest", "nyf_cvd", "nyf_earth", "nyf_harvest",
              "nyf_gold_seq", "nyf_tenne_seq", "nyf_red_blue",
              "nyf_gold_purple"]


def center_of(name):
    s = nyc.DIVERGING_STOPS[name]
    labs = [lab_of(h) for h in s["left"] + s["center"] + s["right"]]
    d = [sum(abs(a[i] - b[i]) for i in range(3))
         for a, b in zip(labs, labs[1:])]
    return sum(d[: len(s["left"])]) / sum(d)


fig = plt.figure(figsize=(17, 9.5))
outer = GridSpec(2, 4, figure=fig, hspace=0.55, wspace=0.28)
for i, name in enumerate(HIGHLIGHTS):
    cell = GridSpecFromSubplotSpec(2, 1, subplot_spec=outer[i // 4, i % 4],
                                   height_ratios=[1, 3.4], hspace=0.18)
    ax_strip = fig.add_subplot(cell[0])
    ax_demo = fig.add_subplot(cell[1])
    kind = kind_of(name)
    if kind == "qualitative":
        hexes = nyc.QUALITATIVE[name]
        ax_strip.imshow(np.arange(len(hexes))[None, :],
                        cmap=ListedColormap(hexes), aspect="auto",
                        interpolation="nearest")
        ax_strip.set_xticks([])
        for k in range(8):
            c = rng.normal(0, 1, (45, 2)) + rng.normal(0, 2.2, 2)
            ax_demo.scatter(c[:, 0], c[:, 1], s=10, color=hexes[k],
                            edgecolors="none")
    else:
        ramp = (nyc.sequential_ramp(name) if kind == "sequential"
                else nyc.diverging_ramp(name))
        ax_strip.imshow(np.arange(len(ramp))[None, :],
                        cmap=ListedColormap(ramp), aspect="auto",
                        interpolation="nearest")
        ax_strip.set_xticks([])
        if kind == "diverging":
            ax_strip.axvline(center_of(name) * (len(ramp) - 1),
                             color="0.3", ls=":", lw=1)
        field = Z if kind == "sequential" else W
        if kind == "diverging":
            ax_demo.pcolormesh(X, Y, field, cmap=ListedColormap(ramp),
                               shading="auto", vmin=-WMAX, vmax=WMAX)
        else:
            ax_demo.pcolormesh(X, Y, field, cmap=ListedColormap(ramp),
                               shading="auto")
    ax_strip.set_yticks([])
    ax_demo.set_xticks([])
    ax_demo.set_yticks([])
    ax_strip.set_title(name, loc="left", fontsize=11, fontweight="bold",
                       pad=14)
    ax_strip.text(1.0, 1.6, kind, transform=ax_strip.transAxes, ha="right",
                  va="center", fontsize=8, style="italic", color="0.45")
fig.savefig(IMG / "highlights.png", dpi=140, bbox_inches="tight")
plt.close(fig)

# --------------------------------------------------------------------------
# 3b. minified glossary figure: every colormap, strip + name + type
# --------------------------------------------------------------------------
fig = plt.figure(figsize=(20, 10))
gs = GridSpec(4, 8, figure=fig, hspace=0.9, wspace=0.3)
for i, name in enumerate(nyc.ALL_NAMES):
    ax = fig.add_subplot(gs[i // 8, i % 8])
    kind = kind_of(name)
    if kind == "qualitative":
        hexes = nyc.QUALITATIVE[name]
        ax.imshow(np.arange(len(hexes))[None, :], cmap=ListedColormap(hexes),
                  aspect="auto", interpolation="nearest")
    else:
        ramp = (nyc.sequential_ramp(name) if kind == "sequential"
                else nyc.diverging_ramp(name))
        ax.imshow(np.arange(len(ramp))[None, :], cmap=ListedColormap(ramp),
                  aspect="auto", interpolation="nearest")
        if kind == "diverging":
            ax.axvline(center_of(name) * (len(ramp) - 1), color="0.3",
                       ls=":", lw=0.8)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(name, loc="left", fontsize=9, fontweight="bold", pad=10)
    ax.text(1.0, 1.55, kind, transform=ax.transAxes, ha="right",
            va="center", fontsize=7, style="italic", color="0.45")
fig.savefig(IMG / "glossary.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# --------------------------------------------------------------------------
# 4. README.md (ASD-STE100 simplified technical English)
# --------------------------------------------------------------------------
L: list[str] = []
add = L.append
add("# nysflag-colormaps")
add("")
add("This repository contains 32 colormaps for scientific plots.")
add("All colors come from one source diagram.")
add("The diagram shows 109 shades of the New York State flag.")
add("The set has three types of colormap:")
add("")
add("- 16 qualitative colormaps for categorical data.")
add("- 8 sequential colormaps for ordered data.")
add("- 8 diverging colormaps for data with a center value.")
add("")
add("Sequential colormaps have equal steps of lightness (L*).")
add("Diverging colormaps have a neutral center color.")
add("One Python module registers all colormaps in matplotlib.")
add("")
add("![Eight selected colormaps](images/highlights.png)")
add("")
add("Figure 1 shows eight selected colormaps.")
add("")
add("![Glossary of all colormaps](images/glossary.png)")
add("")
add("Figure 2 shows all 32 colormaps with their type.")
add("")
add("## Repository contents")
add("")
add("| Path | Content |")
add("| --- | --- |")
add("| `nysflag_colormaps.py` | Python module. It registers all colormaps in matplotlib. |")
add("| `data/palettes.json` | All colormaps in JSON format, with metadata. |")
add("| `data/csv/` | One CSV file for each colormap. |")
add("| `images/` | One figure for each colormap. |")
add("| `scripts/build_assets.py` | Script. It builds the data files, the figures and this README. |")
add("")
add("## Use with matplotlib")
add("")
add("The module needs Python 3 and matplotlib. It does not need numpy.")
add("")
add("1. Put `nysflag_colormaps.py` in your Python path.")
add("2. Register the colormaps:")
add("")
add("```python")
add("import nysflag_colormaps as nyc")
add("nyc.register_all()")
add("```")
add("")
add("3. Use a colormap by name:")
add("")
add("```python")
add("import matplotlib.pyplot as plt")
add('plt.pcolormesh(x, y, z, cmap="nyf_gold_seq")')
add("```")
add("")
add("## Raw data files")
add("")
add("Each colormap has a CSV file in `data/csv/`.")
add("Each row has one color of the colormap.")
add("The columns are: index, hex, red, green, blue, lightness.")
add("For sequential and diverging colormaps, the rows are the stop colors.")
add("`data/palettes.json` also has the 256-color ramp of each sequential")
add("and diverging colormap.")
add("")
add("## Build the assets again")
add("")
add("Run this command in the repository root:")
add("")
add("```")
add("uv run scripts/build_assets.py")
add("```")
add("")
add("The script needs matplotlib and numpy.")
add("It writes the `data/` files, the `images/` files and this README.")
add("")
add("## Overview of the colormaps")
add("")
add("| Name | Type | Colors | Use |")
add("| --- | --- | --- | --- |")
for name in nyc.ALL_NAMES:
    add(f"| {name} | {meta[name]['type']} | {len(meta[name]['colors'])} "
        f"| {meta[name]['use']} |")
add("")
add("## The colormaps")
for name in nyc.ALL_NAMES:
    m = meta[name]
    add("")
    add(f"### {name}")
    add("")
    add(f"![{name}](images/{name}.png)")
    add("")
    add("| Property | Value |")
    add("| --- | --- |")
    add(f"| Type | {m['type']} |")
    add(f"| Number of colors | {len(m['colors'])} |")
    add(f"| Source families | {', '.join(m['source_families'])} |")
    if m["type"] == "qualitative":
        add(f"| Minimum color difference (dE) | {m['min_de']} |")
    if m["type"] == "sequential":
        add(f"| Lightness step (dL*) | {min(m['dlstar'])} to "
            f"{max(m['dlstar'])} |")
    add(f"| Lightness range (L*) | {min(m['lstar'])} to {max(m['lstar'])} |")
    add("")
    add("Hex values: " + " ".join(f"`{h}`" for h in m["colors"]))
    add("")
    add(f"Use it for {m['use']}.")
add("")

(ROOT / "README.md").write_text("\n".join(L))
print("wrote", len(nyc.ALL_NAMES), "csv files, figures and README.md")
