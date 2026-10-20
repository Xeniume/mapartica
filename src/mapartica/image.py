"""Image loading and resampling."""

from pathlib import Path

import numpy as np
from PIL import Image


def load_gray(path: Path) -> np.ndarray:
    """Load as 2D float32 grayscale array [0, 255]."""
    img = Image.open(path).convert("L")
    return np.asarray(img, dtype=np.float32)


def load_rgb(path: Path) -> np.ndarray:
    """Load as 3D float32 RGB array (H, W, 3), range [0, 255]."""
    img = Image.open(path).convert("RGB")
    return np.asarray(img, dtype=np.float32)


def resample_to_fit(
    src: np.ndarray, long_side_target: int
) -> tuple[np.ndarray, int, int, int, int]:
    """
    Scale `src` so its longer side equals `long_side_target`, preserving aspect ratio.

    The shorter side is scaled proportionally, then the canvas is rounded up
    to the nearest multiple of 128 (minimum 1 map) to fit it. The image is
    centered on this canvas.

    Returns: (resized_array, canvas_w, canvas_h, x_offset, y_offset).
    """
    h, w = src.shape[:2]

    if w >= h:
        scaled_w = long_side_target
        scaled_h = max(1, round(h * long_side_target / w))
        canvas_w = long_side_target
        canvas_h = max(128, ((scaled_h + 127) // 128) * 128)
    else:
        scaled_h = long_side_target
        scaled_w = max(1, round(w * long_side_target / h))
        canvas_h = long_side_target
        canvas_w = max(128, ((scaled_w + 127) // 128) * 128)

    shrinking = max(scaled_w, scaled_h) < max(w, h)
    method = Image.Resampling.BOX if shrinking else Image.Resampling.LANCZOS

    if src.ndim == 3:
        raw = Image.fromarray(src.astype(np.uint8), mode="RGB")
        raw = raw.resize((scaled_w, scaled_h), method)
        resized = np.asarray(raw, dtype=np.float32)
    else:
        raw = Image.fromarray(src, mode="F")
        raw = raw.resize((scaled_w, scaled_h), method)
        resized = np.asarray(raw, dtype=np.float32)

    x_off = (canvas_w - scaled_w) // 2
    y_off = (canvas_h - scaled_h) // 2
    return resized, canvas_w, canvas_h, x_off, y_off
