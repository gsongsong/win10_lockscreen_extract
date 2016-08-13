# Win10 Lockscreen Extract

This is a Python 3 script that extracts Windows 10 lock screen images

## Requirement

- Windows 10
- Python 3 with NumPy, SciPy and PIL

## How it works

1. A script looks for files in `~/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets/`
1. A script copies files whose dimensions are either 1920x1080 or 1080x1920
1. It automatically matches a landscape picture and a portrait picture

## Usage

    python3 extract.py

## Note and future work

Sometimes it incorrectly matches a landscape picture and a portrait picutre