import time
import typing

import PIL
from nudenet import NudeDetector
from pathlib import Path
import os
import shutil
from rich.progress import track
from PIL import Image
from rich import print
"""
Folder Structure: 
girl
    ⤷ Bottomless
    ⤷ Topless
    ⤷ All
    
    
Criteria:
Bottomless
    ⤷ EXPOSED_ANUS || EXPOSED_GENITALIA_F || EXPOSED_BUTTOCKS
Topless
    ⤷ EXPOSED_BREAST_F
"""

bottomless_criteria = {"EXPOSED_ANUS", "EXPOSED_GENITALIA_F", "EXPOSED_BUTTOCKS"}
topless_criteria = {"EXPOSED_BREAST_F", }
covered_criteria = {"COVERED_BUTTOCKS", "COVERED_BREAST_F", "COVERED_GENITALIA_F"}


img_dir = Path("./images")
target = img_dir.joinpath("alicebong")
all_dir = target.joinpath("All")
bottomless_dir = target.joinpath("Bottomless")
topless_dir = target.joinpath("Topless")
clothed_dir = target.joinpath("Clothed")
try:
    bottomless_dir.mkdir()
    topless_dir.mkdir()
    clothed_dir.mkdir()
except FileExistsError:
    pass

f: str
files: list[Path] = [all_dir.joinpath(f) for f in os.listdir(all_dir)]

for image in track(files):
    detector = NudeDetector()
    try:
        Image.open(image).verify()
    except PIL.UnidentifiedImageError:
        print(f"[red]NotAnImageError: {image}")
        continue
    try:
        result: set[str] = {box.get("label") for box in detector.detect(str(image))}
    except Exception:
        print(f"[red]Failed Detection on: {image}")
        continue

    if any(topless_results := result & topless_criteria):
        shutil.copy(image, topless_dir)
        print(f"[green]Copied {image} to Topless. Values: {topless_results}")
    if any(bottomless_results := result & bottomless_criteria):
        shutil.copy(image, bottomless_dir)
        print(f"[green]Copied {image} to Bottomless. Values: {bottomless_results}")

    if not any(topless_results) and not any(bottomless_results):
        shutil.copy(image, clothed_dir)
        print(f"[green]Copied {image} to Clothed. Values: {result & covered_criteria}")


    # input()







