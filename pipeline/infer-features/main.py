import torch
from src.io import (
    count_images,
    load_image,
    save_features,
    yield_image_filenames,
    yield_feature_filenames,
)
from src.log import get_logger
from torchvision import transforms
from torchvision.models.vgg import vgg16

log = get_logger()

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

existing_features = set(yield_feature_filenames())
total_images = count_images()
for i, image_filename in enumerate(yield_image_filenames()):
    if image_filename in existing_features:
        log.info(
            f"Skipping image {i + 1}/{total_images} "
            f"({i/total_images*100:.2f}%)"
        )
        continue
    else:
        log.info(
            f"Processing image {i + 1}/{total_images} "
            f"({i/total_images*100:.2f}%)"
        )
        try:
            image = load_image(image_filename)
            image_tensor = transform_pipeline(image).unsqueeze(0)
            features = feature_extractor(image_tensor)
            features = features.to_dense().detach().numpy().flatten()
        except Exception as e:
            log.error(f"Error processing image {image_filename}: {e}")

        save_features(features, image_filename)
