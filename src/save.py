import json
import os
from io import BytesIO
from pathlib import Path

import boto3
import numpy as np
from PIL import Image

from .log import get_logger
from .model import LSHModel

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
    data_dir = Path(os.environ.get("DATA_DIR"))


def save_image(image: Image, filename: str):
    if storage_env == "local":
        save_image_locally(image, filename)
    elif storage_env == "s3":
        save_image_to_s3(image, filename)
    else:
        raise ValueError("Unknown environment")


def save_image_locally(image: Image, filename: str):
    path = data_dir / "raw" / "images" / f"{filename}.jpg"
    log.info(f"Saving image to {path}")
    image.save(path)


def save_image_to_s3(image: Image, filename: str):
    key = f"images/{filename}.jpg"
    log.info(f"Saving image to s3: {bucket} {key}")
    image_bytes = BytesIO()
    image.save(image_bytes, format="JPEG")
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=image_bytes.getvalue(),
        ContentType="image/jpeg",
    )


def save_json(json_data: dict, filename: str):
    if storage_env == "local":
        save_json_locally(json_data, filename)
    elif storage_env == "s3":
        save_json_to_s3(json_data, filename)
    else:
        raise ValueError("Unknown environment")


def save_json_locally(json_data: dict, filename: str):
    path = data_dir / "raw" / f"{filename}.json"
    log.info(f"Saving json to {path}")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(json_data, f)


def save_json_to_s3(json_data: dict, filename: str):
    key = f"{filename}.json"
    log.info(f"Saving image to s3: {bucket} {key}")
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(json_data).encode("utf-8"),
        ContentType="application/json",
    )


def save_features(array: np.ndarray, filename: str):
    if storage_env == "local":
        save_features_locally(array, filename)
    elif storage_env == "s3":
        save_features_to_s3(array, filename)
    else:
        raise ValueError("Unknown environment")


def save_features_locally(array: np.ndarray, filename: str):
    path = data_dir / "raw" / "features" / f"{filename}.npy"
    log.info(f"Saving numpy array to {path}")
    np.save(path, array)


def save_features_to_s3(array: np.ndarray, filename: str):
    key = f"features/{filename}.npy"
    log.info(f"Saving numpy array to s3: {bucket} {key}")
    array_binary = BytesIO()
    np.save(array_binary, array)
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=array_binary.getvalue(),
        ContentType="application/numpy",
    )


def save_model(model: LSHModel, model_name: str):
    if storage_env == "local":
        save_model_locally(model, model_name)
    elif storage_env == "s3":
        save_model_to_s3(model, model_name)
    else:
        raise ValueError("Unknown environment")


def save_model_locally(model: LSHModel, model_name: str):
    path = data_dir / "models" / model_name
    log.info(f"Saving model to {path}")
    model.save(path)


def save_model_to_s3(model: LSHModel, model_name: str):
    key = f"models/{model_name}.npy"
    log.info(f"Saving model to s3: {bucket} {key}")
    model_binary = BytesIO()
    model.save(model_binary)
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=model_binary.getvalue(),
        ContentType="application/numpy",
    )
