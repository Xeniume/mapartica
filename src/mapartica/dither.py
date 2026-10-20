"""Floyd-Steinberg dithering"""

import numpy as np

from mapartica.palette import (
    BLACK_LUMA,
    COLOUR_PALETTE,
    MONO_THRESHOLD,
    WHITE_LUMA,
)

_COLOUR_ARRAY = np.asarray([rgb for _, rgb in COLOUR_PALETTE], dtype=np.float32)


def _diffuse(
    work: np.ndarray, x: int, y: int, dx: int, err: np.float32 | np.ndarray
) -> None:
    """Spread `err` to the unprocessed neighbours."""
    h, w = work.shape[:2]

    w_right = 7.0 / 16.0
    w_down_right = 1.0 / 16.0
    w_down = 5.0 / 16.0
    w_down_left = 3.0 / 16.0

    nx = x + dx
    if 0 <= nx < w:
        work[y, nx] += err * w_right

    ny = y + 1
    if ny < h:
        if 0 <= nx < w:
            work[ny, nx] += err * w_down_right
        work[ny, x] += err * w_down
        px = x - dx
        if 0 <= px < w:
            work[ny, px] += err * w_down_left


def floyd_steinberg_mono(gray: np.ndarray) -> np.ndarray:
    """Quantize grayscale to 2 levels. Returns palette indices: 0=black, 1=white."""
    h, w = gray.shape
    work = gray.astype(np.float32, copy=True)
    indices = np.zeros((h, w), dtype=np.uint8)

    for y in range(h):
        left_to_right = y % 2 == 0
        x_range = range(w) if left_to_right else range(w - 1, -1, -1)
        dx = 1 if left_to_right else -1

        for x in x_range:
            old = work[y, x]
            is_white = old >= MONO_THRESHOLD
            new = WHITE_LUMA if is_white else BLACK_LUMA
            indices[y, x] = 1 if is_white else 0

            err = old - new
            _diffuse(work, x, y, dx, err)

    return indices


def floyd_steinberg_colour(rgb: np.ndarray) -> np.ndarray:
    """Quantize RGB to nearest palette colour. Returns palette indices."""
    h, w, _ = rgb.shape
    work = rgb.astype(np.float32, copy=True)
    indices = np.zeros((h, w), dtype=np.uint8)

    for y in range(h):
        left_to_right = y % 2 == 0
        x_range = range(w) if left_to_right else range(w - 1, -1, -1)
        dx = 1 if left_to_right else -1

        for x in x_range:
            old = work[y, x]
            diffs = _COLOUR_ARRAY - old
            dist2 = np.einsum("ij,ij->i", diffs, diffs)
            best = int(np.argmin(dist2))
            new = _COLOUR_ARRAY[best]
            indices[y, x] = best

            err = old - new
            _diffuse(work, x, y, dx, err)

    return indices
