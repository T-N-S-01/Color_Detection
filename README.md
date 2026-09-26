# Real-Time HSV Color Detection System

A lightweight, interactive Python application built with OpenCV to detect colors in real time from an image or video feed.

## Key Features

- Interactive trackbars for lower/upper Hue, Saturation, and Value thresholds
- HSV conversion for robust color detection under varying lighting
- Live mask and masked-output preview while tuning values
- Easy HSV value tuning for downstream vision tasks

## Tech Stack

- Python 3.x
- OpenCV (`cv2`)
- NumPy

## Installation

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install opencv-python numpy
```

## Usage

### 1) Video feed (webcam index 0 by default)

```bash
python hsv_color_detection.py
```

You can also pass a camera index or video file:

```bash
python hsv_color_detection.py --source 1
python hsv_color_detection.py --source ./video.mp4 --mode video
```

### 2) Static image tuning

```bash
python hsv_color_detection.py --source ./image.jpg --mode image
```

## Controls

- Adjust `L-H`, `L-S`, `L-V` and `U-H`, `U-S`, `U-V` in the **HSV Controls** window.
- Press `q` or `Esc` to quit.
