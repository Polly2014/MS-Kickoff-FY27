"""Split the approved white-background creator sheet into transparent layers."""
from pathlib import Path
import argparse
import cv2
import numpy as np
from PIL import Image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    sheet = np.array(Image.open(args.source).convert("RGB"))
    height, width = sheet.shape[:2]
    for index, name in enumerate(("Baoli-Wang", "Yun-Gu")):
        rgb = sheet[:, index * (width // 2):(index + 1) * (width // 2)].copy()
        # Remove only neutral white regions connected to the outside, retaining
        # interior eye whites, teeth and other enclosed light details.
        candidate = ((rgb.min(axis=2) > 225) &
                     (np.ptp(rgb.astype(np.int16), axis=2) < 20)).astype(np.uint8)
        padded = np.pad(candidate, 1, constant_values=1)
        cv2.floodFill(padded, None, (0, 0), 2)
        background = padded[1:-1, 1:-1] == 2
        alpha = (~background).astype(np.uint8) * 255
        alpha = cv2.GaussianBlur(alpha, (3, 3), 0.45)
        ys, xs = np.where(alpha > 8)
        box = (max(0, xs.min() - 8), max(0, ys.min() - 8),
               min(rgb.shape[1], xs.max() + 9), min(height, ys.max() + 9))
        output = args.source.parent / f"F-cameo-{name}-{args.version}-transparent.png"
        if output.exists():
            raise FileExistsError(output)
        Image.fromarray(np.dstack((rgb, alpha))).crop(box).save(output)
        print(output)


if __name__ == "__main__":
    main()
