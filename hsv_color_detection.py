import argparse
from pathlib import Path

import cv2
import numpy as np


WINDOW_ORIGINAL = "Original"
WINDOW_MASK = "Mask"
WINDOW_RESULT = "Result"
WINDOW_CONTROLS = "HSV Controls"


def _noop(_: int) -> None:
    pass


def create_trackbars() -> None:
    cv2.namedWindow(WINDOW_CONTROLS)
    cv2.createTrackbar("L-H", WINDOW_CONTROLS, 0, 179, _noop)
    cv2.createTrackbar("L-S", WINDOW_CONTROLS, 0, 255, _noop)
    cv2.createTrackbar("L-V", WINDOW_CONTROLS, 0, 255, _noop)
    cv2.createTrackbar("U-H", WINDOW_CONTROLS, 179, 179, _noop)
    cv2.createTrackbar("U-S", WINDOW_CONTROLS, 255, 255, _noop)
    cv2.createTrackbar("U-V", WINDOW_CONTROLS, 255, 255, _noop)


def get_hsv_bounds() -> tuple[np.ndarray, np.ndarray]:
    lower = np.array(
        [
            cv2.getTrackbarPos("L-H", WINDOW_CONTROLS),
            cv2.getTrackbarPos("L-S", WINDOW_CONTROLS),
            cv2.getTrackbarPos("L-V", WINDOW_CONTROLS),
        ],
        dtype=np.uint8,
    )
    upper = np.array(
        [
            cv2.getTrackbarPos("U-H", WINDOW_CONTROLS),
            cv2.getTrackbarPos("U-S", WINDOW_CONTROLS),
            cv2.getTrackbarPos("U-V", WINDOW_CONTROLS),
        ],
        dtype=np.uint8,
    )
    return lower, upper


def render_detection(frame: np.ndarray) -> None:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower, upper = get_hsv_bounds()
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow(WINDOW_ORIGINAL, frame)
    cv2.imshow(WINDOW_MASK, mask)
    cv2.imshow(WINDOW_RESULT, result)


def parse_source(source: str) -> int | str:
    if source.isdigit():
        return int(source)

    path = Path(source).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Input source not found: {source}")
    return str(path)


def run_video(source: int | str) -> None:
    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        raise RuntimeError(f"Unable to open video source: {source}")

    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break

            render_detection(frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q")):
                break
    finally:
        capture.release()


def run_image(image_path: str) -> None:
    image = cv2.imread(image_path)
    if image is None:
        raise RuntimeError(f"Unable to load image: {image_path}")

    while True:
        render_detection(image)
        key = cv2.waitKey(1) & 0xFF
        if key in (27, ord("q")):
            break


def main() -> None:
    parser = argparse.ArgumentParser(description="Real-time HSV color detection with OpenCV.")
    parser.add_argument(
        "--source",
        default="0",
        help="Camera index (e.g. 0), video path, or image path.",
    )
    parser.add_argument(
        "--mode",
        choices=("video", "image"),
        default="video",
        help="Use 'image' to tune HSV on a static image; default uses a video stream.",
    )
    args = parser.parse_args()

    source = parse_source(args.source)
    create_trackbars()

    try:
        if args.mode == "image":
            if isinstance(source, int):
                raise ValueError("Image mode requires --source to point to an image file.")
            run_image(source)
        else:
            run_video(source)
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
