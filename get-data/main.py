from io import BytesIO

import requests
from datasets import load_dataset
from PIL import Image, UnidentifiedImageError
from save_data import save_image, save_json

from src.log import get_logger

log = get_logger()

log.info("Loading dataset")
dataset = load_dataset(
    "ChristophSchuhmann/improved_aesthetics_6.5plus",
    split="train",
    keep_in_memory=True,
)

log.info("Downloading images")
descriptions = {}
for i, row in enumerate(dataset):
    log.info(
        f"Processing row {i} of {len(dataset)} ({i/len(dataset)*100:.2f}%)"
    )
    try:
        image_response = requests.get(row["URL"], timeout=5)
        image = Image.open(BytesIO(image_response.content))
        image.thumbnail((256, 256))
        # save the image as a jpg
        save_image(image=image, filename=row["hash"])

        descriptions[row["hash"]] = row["TEXT"]
    except (requests.RequestException, UnidentifiedImageError, OSError) as e:
        log.error(f"Error downloading image from {row['URL']}")
        log.error(e)
        continue

save_json(descriptions, "descriptions")
