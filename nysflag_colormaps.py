"""nysflag-colormaps: colormaps from the "New York State Flag - 109 shades" diagram.

Provides 32 scientific-plotting palettes built exclusively from the
diagram's swatches: 16 qualitative, 8 perceptually uniform sequential,
8 diverging.  See QUALITATIVE / SEQUENTIAL_STOPS / DIVERGING_STOPS for
the full roster; report() prints a per-palette L* / min-dE audit.

The RAW table below transcribes every numerically-labelled swatch from the
diagram (105 numbered + 4 special-gradient shades = 109).  Matplotlib is
imported lazily; the color math and data are dependency-free.
"""

from __future__ import annotations

# --------------------------------------------------------------------------
# Raw swatch data, transcribed from the diagram.
# Each entry: (diagram label or "", (R, G, B)).
# --------------------------------------------------------------------------

RAW: dict[str, list[tuple[str, tuple[int, int, int]]]] = {
    # "Pink (red to light orange)", listed in the diagram's Lum' order
    "pink": [
        ("137 lips", (211, 112, 80)),
        ("150 lips", (216, 130, 102)),
        ("159 skin", (230, 156, 108)),
        ("181 skin", (246, 181, 138)),
        ("195 lips", (242, 190, 172)),
        ("200 skin", (255, 204, 170)),
        ("206 skin", (254, 212, 184)),
    ],
    # "Reds (dark red to rose)" - crown column, even shades G=B
    "reds_crown": [
        ("crown", (174, 32, 32)),
        ("crown", (208, 43, 43)),
        ("crown", (216, 44, 44)),
        ("crown", (232, 66, 66)),
        ("crown", (255, 90, 90)),
    ],
    # "Reds" - mods column
    "reds_mods": [
        ("mods G", (171, 37, 28)),
        ("mods =", (190, 31, 31)),
        ("mods", (222, 53, 53)),
        ("mods", (235, 80, 80)),
    ],
    # "Reds" - boxed capes shades
    "reds_capes": [
        ("capes", (230, 109, 109)),
        ("capes", (241, 117, 117)),
        ("capes", (245, 126, 126)),
    ],
    # "Trans capes": single translucent swatch (lower half reads B=169)
    "reds_trans": [
        ("trans capes", (250, 150, 150)),
    ],
    # Gold family (dark gold -> light yellow / light orange)
    "gold": [
        ("", (170, 133, 60)),
        ("", (195, 159, 85)),
        ("p", (203, 170, 96)),
        ("", (216, 181, 99)),
        ("Orange", (217, 150, 67)),
        ("", (224, 187, 111)),
        ("p", (224, 190, 114)),
        ("", (229, 202, 139)),
        ("p", (236, 200, 117)),
        ("p", (239, 210, 142)),
        ("", (241, 216, 158)),
        ("", (243, 215, 157)),
        ("", (244, 219, 167)),
        ("206 Light yellow", (250, 226, 188)),
        ("214 Light orange p", (251, 232, 203)),
    ],
    # Tenne (browns / tans), red number order
    "tenne": [
        ("P Outline", (51, 40, 41)),
        ("", (76, 46, 34)),
        ("boat", (99, 70, 51)),
        ("", (114, 102, 85)),
        ("", (115, 108, 91)),
        ("", (124, 116, 104)),
        ("hair", (127, 93, 71)),
        ("Brown", (138, 136, 78)),
        ("hair", (143, 110, 86)),
        ("", (146, 121, 115)),
        ("", (160, 149, 123)),
        ("", (163, 149, 101)),
        ("hair", (165, 130, 105)),
        ("", (171, 161, 113)),
        ("", (183, 167, 131)),
        ("", (183, 178, 155)),
        ("pike", (192, 185, 168)),
        ("Tan", (206, 192, 163)),
        ("Tan", (208, 201, 170)),
        ("Tan", (221, 218, 209)),
    ],
    # Green family
    "green": [
        ("", (47, 80, 50)),
        ("Dark green", (75, 95, 59)),
        ("", (79, 105, 79)),
        ("Green", (105, 121, 102)),
        ("", (77, 129, 85)),
        ("", (80, 133, 88)),
        ("Olive green", (134, 135, 107)),
        ("", (82, 137, 90)),
        ("Olive green", (127, 140, 104)),
        ("gem", (86, 144, 95)),
        ("Green", (139, 160, 151)),
        ("Green", (153, 169, 157)),
        ("Light green", (167, 183, 179)),
    ],
    # Teal (single swatch)
    "teal": [
        ("Teal =", (93, 128, 128)),
    ],
    # Bedsheet (blues), blue number order
    "bedsheet": [
        ("Dark blue", (0, 45, 114)),
        ("Blue-grey", (86, 127, 137)),
        ("Dark blue", (35, 108, 140)),
        ("eyes", (73, 121, 141)),
        ("3 p", (26, 108, 149)),
        ("", (95, 135, 149)),
        ("2 p", (31, 132, 182)),
        ("", (131, 171, 183)),
        ("", (120, 166, 185)),
        ("", (54, 142, 186)),
        ("", (102, 161, 187)),
        ("p", (64, 147, 188)),
        ("1", (76, 152, 190)),
        ("", (137, 180, 195)),
        ("p gem", (45, 148, 200)),
        ("", (89, 174, 218)),
        ("light blue", (133, 196, 227)),
    ],
    # Purple family
    "purple": [
        ("Grey-50%", (125, 110, 126)),
        ("Indigo", (105, 101, 134)),
        ("Blue-grey", (86, 99, 130)),
    ],
    # White / grey ramp (eye pure -> motto)
    "grey": [
        ("eye pure p", (255, 255, 255)),
        ("", (242, 242, 242)),
        ("", (230, 230, 230)),
        ("", (215, 215, 215)),
        ("", (204, 204, 204)),
        ("", (203, 203, 203)),
        ("p", (188, 188, 188)),
        ("", (180, 180, 180)),
        ("p", (169, 169, 169)),
        ("motto Grey-80%", (26, 26, 26)),
    ],
    # Cendere (grey-greens)
    "cendere": [
        ("Grey-25%", (183, 189, 179)),
        ("Grey-50%", (126, 135, 117)),
        ("", (119, 132, 116)),
        ("", (115, 109, 99)),
        ("", (105, 120, 113)),
        ("", (100, 115, 113)),
    ],
}

# "specials": the two labelled gradients carry no numeric values in the
# diagram; hexes below are visual approximations and are NOT used to build
# any palette.  sky counts as 2 shades, sails as 2 -> 105 + 4 = 109.
SPECIALS_APPROX: dict[str, list[str]] = {
    "sky": ["#4a94c8", "#5f6fae"],    # blue -> slate-violet gradient
    "sails": ["#c9c0ac", "#9fa4a8"],  # tan -> grey gradient
}


# --------------------------------------------------------------------------
# Color math: sRGB <-> CIELAB (D65), pure python
# --------------------------------------------------------------------------

def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#%02x%02x%02x" % rgb


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _srgb_to_linear(c: float) -> float:
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c: float) -> float:
    c = min(max(c, 0.0), 1.0)
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def rgb_to_lab(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    r, g, b = (_srgb_to_linear(c) for c in rgb)
    x = 0.4124564 * r + 0.3575761 * g + 0.1804375 * b
    y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    z = 0.0193339 * r + 0.1191920 * g + 0.9503041 * b
    x /= 0.95047
    z /= 1.08883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > (6 / 29) ** 3 else t / (3 * (6 / 29) ** 2) + 4 / 29

    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def lab_to_rgb(lab: tuple[float, float, float]) -> tuple[int, int, int]:
    L, a, b = lab
    fy = (L + 16) / 116
    fx = fy + a / 500
    fz = fy - b / 200

    def finv(t: float) -> float:
        return t ** 3 if t > 6 / 29 else 3 * (6 / 29) ** 2 * (t - 4 / 29)

    x = finv(fx) * 0.95047
    y = finv(fy)
    z = finv(fz) * 1.08883
    r = 3.2404542 * x - 1.5371385 * y - 0.4985314 * z
    g = -0.9692660 * x + 1.8760108 * y + 0.0415560 * z
    b_ = 0.0556434 * x - 0.2040259 * y + 1.0572252 * z
    return tuple(round(_linear_to_srgb(c) * 255) for c in (r, g, b_))  # type: ignore[return-value]


def lstar(rgb: tuple[int, int, int]) -> float:
    return rgb_to_lab(rgb)[0]


# --------------------------------------------------------------------------
# Palette construction helpers
# --------------------------------------------------------------------------

def family_hexes(name: str) -> list[str]:
    return [rgb_to_hex(rgb) for _, rgb in RAW[name]]


def even_l_stops(hexes: list[str], n: int) -> list[str]:
    """Pick n swatches whose L* values are as evenly spaced as possible.

    Swatches are sorted by L*; target lightnesses are linspace(min, max, n)
    and each target takes its nearest unused swatch.
    """
    pairs = sorted({h: rgb_to_lab(hex_to_rgb(h))[0] for h in hexes}.items(),
                   key=lambda kv: kv[1])
    lmin, lmax = pairs[0][1], pairs[-1][1]
    tol = 0.5 * (lmax - lmin) / (n - 1)  # min L* gap between stops
    stops: list[tuple[str, float]] = []
    used: set[str] = set()
    for target in [lmin + (lmax - lmin) * i / (n - 1) for i in range(n)]:
        cands = sorted((p for p in pairs if p[0] not in used),
                       key=lambda p: abs(p[1] - target))
        best = next((p for p in cands
                     if all(abs(p[1] - s[1]) >= tol for s in stops)),
                    cands[0])
        used.add(best[0])
        stops.append(best)
    return [h for h, _ in sorted(stops, key=lambda p: p[1])]


def even_l_interpolated(hexes: list[str], n: int) -> list[str]:
    """n colors at exactly even L* targets, sampled from the Lab ramp.

    For families whose swatches cluster in lightness, discrete selection
    cannot space stops evenly; interpolating keeps both L* and chroma on
    a smooth monotonic path.
    """
    ramp = lab_ramp(hexes, 512)
    ls = [rgb_to_lab(hex_to_rgb(h))[0] for h in ramp]
    lmin, lmax = ls[0], ls[-1]
    return [min(zip(ramp, ls), key=lambda p: abs(p[1] - t))[0]
            for t in (lmin + (lmax - lmin) * i / (n - 1) for i in range(n))]


def lab_ramp(hexes: list[str], n: int = 256) -> list[str]:
    """Smooth ramp through the stops, interpolated in CIELAB.

    Samples per segment are proportional to its Lab length, giving a
    near-uniform perceptual gradient.
    """
    labs = [rgb_to_lab(hex_to_rgb(h)) for h in hexes]
    if len(labs) == 1:
        return [hexes[0]] * n
    seg_len = [
        sum(abs(a[i] - b[i]) for i in range(3)) ** 0.5
        for a, b in zip(labs, labs[1:])
    ]
    total = sum(seg_len) or 1.0
    out: list[str] = []
    for si, (a, b) in enumerate(zip(labs, labs[1:])):
        count = max(2, round(n * seg_len[si] / total))
        for i in range(count):
            t = i / count
            out.append(rgb_to_hex(lab_to_rgb(tuple(a[i] + (b[i] - a[i]) * t for i in range(3)))))
    out.append(hexes[-1])
    # resample to exactly n, evenly spaced
    return [out[round(i * (len(out) - 1) / (n - 1))] for i in range(n)]


# --------------------------------------------------------------------------
# The eight palettes
# --------------------------------------------------------------------------

# Qualitative: 16 themed 8-color sets, every hex a RAW diagram swatch.
QUALITATIVE: dict[str, list[str]] = {
    "nyf_bold": ["#d02b2b", "#d99643", "#e0be72", "#4d8155",
                 "#5d8080", "#1a6c95", "#696586", "#7f5d47"],
    "nyf_earth": ["#f17575", "#f6b58a", "#cec0a3", "#86876b",
                  "#8ba097", "#a9a9a9", "#566382", "#a0957b"],
    "nyf_pastel": ["#f57e7e", "#fed4b8", "#e6e6e6", "#a7b7b3",
                   "#f6b58a", "#85c4e3", "#83abb7", "#7d6e7e"],
    "nyf_deep": ["#ae2020", "#aa853c", "#4c2e22", "#2f5032",
                 "#4b5f3b", "#5d8080", "#002d72", "#1a1a1a"],
    # Okabe-Ito-style colorblind-safe selection
    "nyf_cvd": ["#d99643", "#85c4e3", "#1a6c95", "#e0be72",
                "#d02b2b", "#696586", "#5d8080", "#a9a9a9"],
    "nyf_warm": ["#ae2020", "#eb5050", "#f57e7e", "#f6b58a",
                 "#d99643", "#aa853c", "#7f5d47", "#cec0a3"],
    "nyf_cool": ["#002d72", "#1a6c95", "#368eba", "#85c4e3",
                 "#5d8080", "#4d8155", "#8ba097", "#696586"],
    "nyf_sunset": ["#ab251c", "#eb5050", "#f57e7e", "#f6b58a",
                   "#fae2bc", "#d99643", "#7d6e7e", "#566382"],
    "nyf_forest": ["#2f5032", "#4b5f3b", "#4d8155", "#86876b",
                   "#8ba097", "#7f5d47", "#cec0a3", "#5d8080"],
    "nyf_ocean": ["#002d72", "#1a6c95", "#4c98be", "#85c4e3",
                  "#5d8080", "#83abb7", "#99a99d", "#566382"],
    "nyf_orchard": ["#d02b2b", "#f17575", "#d99643", "#e0be72",
                    "#4d8155", "#86876b", "#cec0a3", "#7f5d47"],
    "nyf_mineral": ["#1a1a1a", "#a9a9a9", "#566382", "#86876b",
                    "#7d6e7e", "#5d8080", "#83abb7", "#cec0a3"],
    # alternating dark/light neighbors for max adjacent contrast
    "nyf_contrast": ["#ae2020", "#fae2bc", "#002d72", "#f57e7e",
                     "#2f5032", "#85c4e3", "#4c2e22", "#e6e6e6"],
    "nyf_dusk": ["#236c8c", "#696586", "#7d6e7e", "#002d72",
                 "#5d8080", "#4b5f3b", "#ae2020", "#aa853c"],
    "nyf_blossom": ["#f57e7e", "#fed4b8", "#7d6e7e", "#696586",
                    "#8ba097", "#a7b7b3", "#85c4e3", "#f6b58a"],
    "nyf_harvest": ["#aa853c", "#e0be72", "#fae2bc", "#86876b",
                    "#7f5d47", "#d02b2b", "#d99643", "#cec0a3"],
}

# Sequential: even-L* stops drawn from a single family (8 stops each).
# Gold excludes its high-chroma "Orange" swatch so the hue path stays smooth.
# Blue keeps only the saturated branch of the Bedsheet family: mixing in the
# desaturated blue-grey swatches makes chroma dip mid-ramp, which the eye
# reads as non-monotonic even when L* is even.
_GOLD_SEQ = [h for h in family_hexes("gold") if h != rgb_to_hex((217, 150, 67))]
_BLUE_SEQ = [rgb_to_hex(v) for v in ((0, 45, 114), (26, 108, 149),
                                     (31, 132, 182), (45, 148, 200),
                                     (54, 142, 186), (76, 152, 190),
                                     (89, 174, 218), (133, 196, 227))]
_RED_SEQ = [rgb_to_hex(v) for v in ((171, 37, 28), (190, 31, 31),
                                    (222, 53, 53), (235, 80, 80),
                                    (245, 126, 126), (250, 150, 150))]
_PINK_SEQ = [rgb_to_hex(v) for v in ((211, 112, 80), (216, 130, 102),
                                     (230, 156, 108), (246, 181, 138),
                                     (242, 190, 172), (255, 204, 170),
                                     (254, 212, 184))]
_GREEN_SEQ = [rgb_to_hex(v) for v in ((47, 80, 50), (77, 129, 85),
                                      (80, 133, 88), (86, 144, 95),
                                      (139, 160, 151), (167, 183, 179))]
_TENNE_SEQ = [rgb_to_hex(v) for v in ((76, 46, 34), (99, 70, 51),
                                      (127, 93, 71), (143, 110, 86),
                                      (165, 130, 105), (206, 192, 163),
                                      (221, 218, 209))]
_CENDERE_SEQ = [rgb_to_hex(v) for v in ((100, 115, 113), (105, 120, 113),
                                        (119, 132, 116), (126, 135, 117),
                                        (183, 189, 179))]
SEQUENTIAL_STOPS: dict[str, list[str]] = {
    "nyf_gold_seq": even_l_stops(_GOLD_SEQ, 8),
    # saturated branch lacks swatches at mid lightnesses, so blue stops are
    # Lab-interpolated at exact even L* instead of swatch-picked
    "nyf_blue_seq": even_l_interpolated(_BLUE_SEQ, 8),
    "nyf_red_seq": even_l_interpolated(_RED_SEQ, 8),
    "nyf_pink_seq": even_l_interpolated(_PINK_SEQ, 8),
    "nyf_green_seq": even_l_interpolated(_GREEN_SEQ, 8),
    "nyf_tenne_seq": even_l_interpolated(_TENNE_SEQ, 8),
    "nyf_grey_seq": even_l_interpolated(
        sorted(family_hexes("grey"), key=lambda h: lstar(hex_to_rgb(h))), 8),
    "nyf_cendere_seq": even_l_interpolated(_CENDERE_SEQ, 8),
}

# Diverging: dark -> light anchors, neutral center, light -> dark anchors.
DIVERGING_STOPS: dict[str, dict[str, list[str]]] = {
    "nyf_red_blue": {
        "left": ["#ab251c", "#eb5050", "#f57e7e"],
        "center": ["#f2f2f2"],
        "right": ["#89b4c3", "#368eba", "#002d72"],
    },
    "nyf_tenne_teal": {
        "left": ["#4c2e22", "#8f6e56", "#cec0a3"],
        "center": ["#e6e6e6"],
        "right": ["#5d8080", "#236c8c", "#002d72"],
    },
    "nyf_gold_purple": {
        "left": ["#aa853c", "#d8b563", "#fae2bc"],
        "center": ["#f2f2f2"],
        "right": ["#7d6e7e", "#696586", "#566382"],
    },
    "nyf_pink_green": {
        "left": ["#d37050", "#e69c6c", "#fed4b8"],
        "center": ["#f2f2f2"],
        "right": ["#a7b7b3", "#56905f", "#2f5032"],
    },
    "nyf_blue_gold": {
        "left": ["#002d72", "#368eba", "#89b4c3"],
        "center": ["#f2f2f2"],
        "right": ["#fae2bc", "#d8b563", "#aa853c"],
    },
    "nyf_tenne_blue": {
        "left": ["#4c2e22", "#8f6e56", "#cec0a3"],
        "center": ["#e6e6e6"],
        "right": ["#85c4e3", "#368eba", "#002d72"],
    },
    "nyf_red_teal": {
        "left": ["#ab251c", "#eb5050", "#f57e7e"],
        "center": ["#f2f2f2"],
        "right": ["#89b4c3", "#5d8080", "#236c8c"],
    },
    "nyf_pink_blue": {
        "left": ["#d37050", "#e69c6c", "#ffccaa"],
        "center": ["#f2f2f2"],
        "right": ["#85c4e3", "#368eba", "#002d72"],
    },
}

ALL_NAMES = list(QUALITATIVE) + list(SEQUENTIAL_STOPS) + list(DIVERGING_STOPS)


def sequential_ramp(name: str, n: int = 256) -> list[str]:
    return lab_ramp(SEQUENTIAL_STOPS[name], n)


def diverging_ramp(name: str, n: int = 256) -> list[str]:
    s = DIVERGING_STOPS[name]
    return lab_ramp(s["left"] + s["center"] + s["right"], n)


# --------------------------------------------------------------------------
# Matplotlib registration (lazy import)
# --------------------------------------------------------------------------

def register_all() -> dict[str, object]:
    """Register all eight palettes with matplotlib; returns {name: cmap}."""
    import matplotlib
    from matplotlib.colors import ListedColormap, LinearSegmentedColormap

    cmaps: dict[str, object] = {}
    for name, hexes in QUALITATIVE.items():
        cmaps[name] = ListedColormap(hexes, name=name)
    for name in SEQUENTIAL_STOPS:
        cmaps[name] = LinearSegmentedColormap.from_list(
            name, sequential_ramp(name), N=256)
    for name in DIVERGING_STOPS:
        cmaps[name] = LinearSegmentedColormap.from_list(
            name, diverging_ramp(name), N=256)
    for name, cm in cmaps.items():
        if name not in matplotlib.colormaps:
            matplotlib.colormaps.register(cm, name=name)
    return cmaps


def _min_de(hexes: list[str]) -> float:
    labs = [rgb_to_lab(hex_to_rgb(h)) for h in hexes]
    return min(
        sum((a[i] - b[i]) ** 2 for i in range(3)) ** 0.5
        for i, a in enumerate(labs) for b in labs[i + 1:]
    )


def report() -> str:
    """Human-readable L* / min-dE audit of every palette."""
    lines: list[str] = []
    for name, hexes in QUALITATIVE.items():
        ls = [round(lstar(hex_to_rgb(h)), 1) for h in hexes]
        lines.append(f"{name:16s} min dE = {_min_de(hexes):5.1f}  L* = {ls}")
    for name, stops in SEQUENTIAL_STOPS.items():
        ls = [lstar(hex_to_rgb(h)) for h in stops]
        d = [round(b - a, 1) for a, b in zip(ls, ls[1:])]
        lines.append(f"{name:16s} L* = {[round(v, 1) for v in ls]}  dL* = {d}")
    for name in DIVERGING_STOPS:
        ls = [lstar(hex_to_rgb(h)) for h in diverging_ramp(name, 17)]
        lines.append(f"{name:16s} L* profile = {[round(v) for v in ls]}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(report())
