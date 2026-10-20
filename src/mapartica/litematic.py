"""Build a flat .litematic from a palette-index mask."""

from pathlib import Path

import numpy as np
from litemapy import BlockState, Region


def build_litematic(
    output_path: Path,
    indices: np.ndarray,
    palette_ids: list[str],
    canvas_w: int,
    canvas_h: int,
    x_offset: int,
    y_offset: int,
    background_block: str | None = None,
) -> None:
    """
    Write a flat map art onto a `canvas_w` x `canvas_h` XZ plane.

    `indices` are palette indices into `palette_ids`. Pixels not covered by
    the image are filled with `background_block` (or left as air if None).
    """
    img_h, img_w = indices.shape

    # Region(x, y, z, width, height, length)
    region = Region(0, 0, 0, canvas_w, 1, canvas_h)

    blocks = [BlockState(bid) for bid in palette_ids]
    bg = BlockState(background_block) if background_block else None

    for canvas_y in range(canvas_h):
        img_y = canvas_y - y_offset
        for canvas_x in range(canvas_w):
            img_x = canvas_x - x_offset
            if 0 <= img_x < img_w and 0 <= img_y < img_h:
                region[canvas_x, 0, canvas_y] = blocks[int(indices[img_y, img_x])]
            elif bg is not None:
                region[canvas_x, 0, canvas_y] = bg

    schematic = region.as_schematic(
        name="MapArt",
        author="mapartica",
        description="Image -> Litematica map art (Floyd-Steinberg)",
    )
    schematic.save(str(output_path))
