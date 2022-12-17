from io import BytesIO

import requests
from datasets import load_dataset
from PIL import Image, UnidentifiedImageError
from src.io import save_image, save_json, yield_image_filenames
from src.log import get_logger

log = get_logger()

log.info("Loading dataset")
dataset = load_dataset(
    "ChristophSchuhmann/improved_aesthetics_6.5plus",
    split="train",
    keep_in_memory=True,
)

log.info("Saving descriptions")
descriptions = {row["hash"]: row["TEXT"] for row in dataset}
save_json(descriptions, "descriptions")

log.info("Downloading images")
existing_images = set(yield_image_filenames())
for i, row in enumerate(dataset):
    if str(row["hash"]) in existing_images:
        log.info(
            f"Skipping row {i}/{len(dataset)} ({i/len(dataset)*100:.2f}%)")
        continue
    else:
        log.info(
            f"Processing row {i}/{len(dataset)} ({i/len(dataset)*100:.2f}%)"
        )
        try:
            log.debug(f"Downloading {row['URL']}")
            image_response = requests.get(row["URL"], timeout=5)
            image = Image.open(BytesIO(image_response.content))
            image = image.convert("RGB")
            image.thumbnail((256, 256))

            save_image(image=image, filename=row["hash"])
            descriptions[row["hash"]] = row["TEXT"]

        except (
            requests.RequestException,
            UnidentifiedImageError,
            OSError,
        ) as e:
            log.error(f"Error downloading image from {row['URL']}: {e}")
            continue
