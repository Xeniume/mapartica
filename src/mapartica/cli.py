import argparse
import sys
from pathlib import Path

from mapartica.dither import floyd_steinberg_colour, floyd_steinberg_mono
from mapartica.image import load_gray, load_rgb, resample_to_fit
from mapartica.litematic import build_litematic
from mapartica.palette import COLOUR_PALETTE_IDS, MONO_PALETTE_IDS


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mapartica",
        description=("Convert an image into a Minecraft map art (.litematic)."),
    )
    parser.add_argument("-i", "--input", required=True, help="path to the input image")
    parser.add_argument(
        "-x",
        type=int,
        required=True,
        metavar="N",
        help="long-side size multiplier; long side is 128*N blocks",
    )
    parser.add_argument(
        "--mode",
        choices=("mono", "colour"),
        default="mono",
        help="mono: 2-colour black/white (default); colour: 16-colour palette",
    )
    parser.add_argument(
        "--background",
        default="air",
        help="background block id (default: air, e.g. minecraft:red_concrete)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.x < 1:
        parser.error("-x must be a positive integer (N >= 1)")

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"error: input file not found: {input_path}", file=sys.stderr)
        return 1

    long_side_target = 128 * args.x

    try:
        if args.mode == "mono":
            src = load_gray(input_path)
            resized, canvas_w, canvas_h, x_off, y_off = resample_to_fit(
                src, long_side_target
            )
            indices = floyd_steinberg_mono(resized)
            palette_ids = MONO_PALETTE_IDS
        else:
            src = load_rgb(input_path)
            resized, canvas_w, canvas_h, x_off, y_off = resample_to_fit(
                src, long_side_target
            )
            indices = floyd_steinberg_colour(resized)
            palette_ids = COLOUR_PALETTE_IDS
    except Exception as e:
        print(f"error: failed to process {input_path}: {e}", file=sys.stderr)
        return 1

    bg_id = None if args.background.lower() == "air" else args.background

    output_path = Path.cwd() / f"{input_path.stem}.litematic"
    try:
        build_litematic(
            output_path,
            indices,
            palette_ids,
            canvas_w,
            canvas_h,
            x_off,
            y_off,
            background_block=bg_id,
        )
    except Exception as e:
        print(f"error: failed to write {output_path}: {e}", file=sys.stderr)
        return 1

    print(f"wrote {output_path} ({canvas_w}x{canvas_h} canvas, mode={args.mode})")
    return 0
