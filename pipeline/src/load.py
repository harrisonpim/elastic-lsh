import json
import os
from io import BytesIO
from pathlib import Path

import boto3
import numpy as np
from PIL import Image

from src.log import get_logger

log = get_logger()

storage_env = os.environ.get("STORAGE_ENVIRONMENT")

if storage_env == "s3":
    bucket = os.environ.get("AWS_S3_BUCKET_ID")
    boto3.setup_default_session(
        profile_name=os.environ.get("AWS_PROFILE", None)
    )
    assume_role_arn = os.environ.get("AWS_LOCAL_ROLE_ARN", None)
    if assume_role_arn:
        sts = boto3.client("sts")
        credentials = sts.assume_role(
            RoleArn=assume_role_arn, RoleSessionName="local-session"
        )["Credentials"]
        s3 = boto3.client(
            "s3",
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
        )
    else:
        s3 = boto3.client("s3")
else:
    data_dir = Path("/data").absolute()
    data_dir.mkdir(parents=True, exist_ok=True)
    image_dir = data_dir / "images"
    image_dir.mkdir(parents=True, exist_ok=True)
    feature_dir = data_dir / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    model_dir = data_dir / "models"
    model_dir.mkdir(parents=True, exist_ok=True)


def load_image(filename: str):
    if storage_env == "local":
        return load_image_locally(filename)
    elif storage_env == "s3":
        return load_image_from_s3(filename)
    else:
        raise ValueError(f"Unknown environment: {storage_env}")


def load_image_locally(filename: str):
    path = image_dir / f"{filename}.jpg"
    log.info(f"Loading image from {path}")
    return Image.open(path)


def load_image_from_s3(filename: str):
    key = f"images/{filename}.jpg"
    log.info(f"Loading image from s3: {bucket} {key}")
    image_bytes = BytesIO(s3.get_object(Bucket=bucket, Key=key)["Body"].read())
    return Image.open(image_bytes)


def yield_image_filenames():
    if storage_env == "local":
        return yield_image_filenames_locally()
    elif storage_env == "s3":
        return yield_image_filenames_from_s3()
    else:
        raise ValueError(f"Unknown environment: {storage_env}")


def yield_image_filenames_locally():
    for path in image_dir.iterdir():
        yield path.stem


def yield_image_filenames_from_s3():
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix="images"):
        for content in page["Contents"]:
            yield Path(content["Key"]).stem


def count_images():
    if storage_env == "local":
        return count_images_locally()
    elif storage_env == "s3":
        return count_images_from_s3()
    else:
        raise ValueError(f"Unknown environment: {storage_env}")


def count_images_locally():
    return len(list(image_dir.iterdir()))


def count_images_from_s3():
    paginator = s3.get_paginator("list_objects_v2")
    count = 0
    for page in paginator.paginate(Bucket=bucket, Prefix="images"):
        count += len(page["Contents"])
    return count


def load_features(filename: str):
    if storage_env == "local":
        return load_features_locally(filename)
    elif storage_env == "s3":
        return load_features_from_s3(filename)
    else:
        raise ValueError(f"Unknown environment: {storage_env}")


def load_features_locally(filename: str):
    path = feature_dir / f"{filename}.npy"
    log.info(f"Loading numpy array from {path}")
    return np.load(path)


def load_features_from_s3(filename: str):
    key = f"features/{filename}.npy"
    log.info(f"Loading numpy array from s3: {bucket} {key}")
    return np.load(
        BytesIO(s3.get_object(Bucket=bucket, Key=key)["Body"].read())
    )


def yield_feature_filenames():
    if storage_env == "local":
        return yield_features_filenames_locally()
    elif storage_env == "s3":
        return yield_features_filenames_from_s3()
    else:
        raise ValueError(f"Unknown environment: {storage_env}")


def yield_features_filenames_locally():
    for path in feature_dir.iterdir():
        yield path.stem


def yield_features_filenames_from_s3():
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix="features"):
        for content in page["Contents"]:
            yield Path(content["Key"]).stem


def count_features():
    if storage_env == "local":
        return count_features_locally()
    elif storage_env == "s3":
        return count_features_from_s3()
    else:
        raise ValueError(f"Unknown environment: {storage_env}")


def count_features_locally():
    return len(list(feature_dir.iterdir()))


def count_features_from_s3():
    paginator = s3.get_paginator("list_objects_v2")
    count = 0
    for page in paginator.paginate(Bucket=bucket, Prefix="features"):
        count += len(page["Contents"])
    return count


def get_latest_model_name():
    if storage_env == "local":
        return get_latest_model_name_locally()
    elif storage_env == "s3":
        return get_latest_model_name_from_s3()
    else:
        raise ValueError(f"Unknown environment: {storage_env}")


def get_latest_model_name_locally():
    models = list(model_dir.iterdir())
    if not models:
        raise ValueError("No models found")
    return max(models, key=os.path.getctime).stem


def get_latest_model_name_from_s3():
    paginator = s3.get_paginator("list_objects_v2")
    models = []
    for page in paginator.paginate(Bucket=bucket, Prefix="models"):
        for content in page["Contents"]:
            models.append(Path(content["Key"]).stem)
    if not models:
        raise ValueError("No models found")
    return max(models)


def load_model(model_name: str):
    if storage_env == "local":
        return load_model_locally(model_name)
    elif storage_env == "s3":
        return load_model_from_s3(model_name)
    else:
        raise ValueError(f"Unknown environment: {storage_env}")


def load_model_locally(model_name: str):
    path = model_dir / f"{model_name}.npy"
    log.info(f"Loading model from {path}")
    return np.load(path)


def load_model_from_s3(model_name: str):
    key = f"models/{model_name}.npy"
    log.info(f"Loading model from s3: {bucket} {key}")
    return np.load(
        BytesIO(s3.get_object(Bucket=bucket, Key=key)["Body"].read())
    )


def load_json(filename: str):
    if storage_env == "local":
        return load_json_locally(filename)
    elif storage_env == "s3":
        return load_json_from_s3(filename)
    else:
        raise ValueError(f"Unknown environment: {storage_env}")


def load_json_locally(filename: str):
    path = data_dir / f"{filename}.json"
    log.info(f"Loading json from {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_json_from_s3(filename: str):
    key = f"{filename}.json"
    log.info(f"Loading json from s3: {bucket} {key}")
    return json.loads(s3.get_object(Bucket=bucket, Key=key)["Body"].read())
