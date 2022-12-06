from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from torchvision.models.vgg import vgg16
from tqdm import tqdm

data_dir = Path("/data")
model_dir = data_dir / "models"
images_dir = data_dir / "raw" / "images"
features_dir = data_dir / "raw" / "features"

transform_pipeline = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.Lambda(lambda image: image.convert("RGB")),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],  # imagenet_mean
            std=[0.229, 0.224, 0.225],  # imagenet_std
        ),
    ]
)

torch.hub.set_dir("/data/models")
feature_extractor = vgg16(progress=False).eval()
feature_extractor.classifier = feature_extractor.classifier[:4]

for image_path in tqdm(
    images_dir.glob("*.jpg"), total=len(list(images_dir.glob("*.jpg")))
):
    image = Image.open(image_path)
    image_tensor = transform_pipeline(image).unsqueeze(0)
    features = feature_extractor(image_tensor)
    features = features.to_dense().detach().numpy().flatten()

    np.save(features_dir / f"{image_path.stem}.npy", features)
