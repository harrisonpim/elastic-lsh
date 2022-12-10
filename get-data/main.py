from io import BytesIO

import requests
from datasets import load_dataset
from PIL import Image, UnidentifiedImageError
from save_data import save_image, save_json
from tqdm import tqdm

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
        # save the image as a jpg
        save_image(image=image, filename=row["hash"])

        descriptions[row["hash"]] = row["TEXT"]
    except (requests.RequestException, UnidentifiedImageError, OSError):
        continue

save_json(descriptions, "descriptions")
