"""Palettes for mono (2-colour) and coloured (16-colour) map art."""

# Mono palette: black / white concrete

MONO_PALETTE = [
    ("minecraft:black_concrete", (25, 25, 25)),
    ("minecraft:white_concrete", (251, 251, 251)),
]

MONO_PALETTE_IDS = [bid for bid, _ in MONO_PALETTE]

# Luminance targets and midpoint threshold for the mono dither path.
BLACK_LUMA = 25.0  # 0x191919
WHITE_LUMA = 255.0  # 0xFFFFFF
MONO_THRESHOLD = (BLACK_LUMA + WHITE_LUMA) / 2.0

# Coloured palette: 16 concrete blocks

COLOUR_PALETTE = [
    ("minecraft:white_concrete", (251, 251, 251)),
    ("minecraft:light_gray_concrete", (151, 151, 151)),
    ("minecraft:gray_concrete", (75, 75, 75)),
    ("minecraft:black_concrete", (25, 25, 25)),
    ("minecraft:brown_concrete", (100, 75, 50)),
    ("minecraft:red_concrete", (151, 50, 50)),
    ("minecraft:orange_concrete", (213, 125, 50)),
    ("minecraft:yellow_concrete", (225, 225, 50)),
    ("minecraft:lime_concrete", (125, 201, 25)),
    ("minecraft:green_concrete", (100, 125, 50)),
    ("minecraft:cyan_concrete", (75, 125, 151)),
    ("minecraft:light_blue_concrete", (100, 151, 213)),
    ("minecraft:blue_concrete", (50, 75, 175)),
    ("minecraft:purple_concrete", (125, 62, 175)),
    ("minecraft:magenta_concrete", (175, 75, 213)),
    ("minecraft:pink_concrete", (238, 125, 162)),
]

COLOUR_PALETTE_IDS = [bid for bid, _ in COLOUR_PALETTE]
