# Win10 Lockscreen Extract

This is a Python 3 script that extracts Windows 10 lock screen images

## Requirement

- Windows 10
- Python 3

## How it works

1. A script looks for files in `~/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets/`
1. A script copies files larger than 400 KB to `~/Pictures/win10_lockscreen`

## Usage

    python3 extract.py

## Note and future work

Sometimes it incorrectly matches a landscape picture and a portrait picutre.