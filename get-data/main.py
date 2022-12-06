import json
from io import BytesIO
from pathlib import Path

import requests
from datasets import load_dataset
from PIL import Image, UnidentifiedImageError
from tqdm import tqdm

data_dir = Path("/data/raw")

dataset = load_dataset(
    "ChristophSchuhmann/improved_aesthetics_6.5plus",
    split="train",
    keep_in_memory=True,
)

descriptions = {}
for i, row in tqdm(
    enumerate(dataset), total=len(dataset), desc="Downloading images"
):
    try:
        image_response = requests.get(row["URL"], timeout=5)
        image = Image.open(BytesIO(image_response.content))
        image.thumbnail((256, 256))
        image.save(data_dir / "images" / f'{row["hash"]}.jpg')

        descriptions[row["hash"]] = row["TEXT"]
    except (requests.RequestException, UnidentifiedImageError, OSError):
        continue


with open(data_dir / "descriptions.json", "w", encoding="utf-8") as f:
    json.dump(descriptions, f)
