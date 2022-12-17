import json
import os
from io import BytesIO
from pathlib import Path

import boto3
import numpy as np
from botocore.exceptions import ClientError
from PIL import Image

from .log import get_logger
from .model import LSHModel

log = get_logger()


storage_env = os.environ.get("STORAGE_ENVIRONMENT")
bucket = os.environ.get("AWS_S3_BUCKET_ID")
boto3.setup_default_session(profile_name=os.environ.get("AWS_PROFILE", None))
session = {"s3": boto3.client("s3")}
if os.environ.get("AWS_LOCAL_ROLE_ARN"):
    sts = boto3.client("sts")
    credentials = sts.assume_role(
        RoleArn=os.environ.get("AWS_LOCAL_ROLE_ARN"),
        RoleSessionName="local-session"
    )["Credentials"]
    session["s3"] = boto3.client(
        "s3",
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )

data_dir = Path("/data").absolute()
data_dir.mkdir(parents=True, exist_ok=True)
image_dir = data_dir / "images"
image_dir.mkdir(parents=True, exist_ok=True)
feature_dir = data_dir / "features"
feature_dir.mkdir(parents=True, exist_ok=True)
model_dir = data_dir / "models"
model_dir.mkdir(parents=True, exist_ok=True)


def get_s3_client(s3=session["s3"]):
    try:
        s3.head_bucket(Bucket=bucket)
    except ClientError:
        log.debug("Session expired, refreshing")
        sts = boto3.client("sts")
        credentials = sts.assume_role(
            RoleArn=os.environ.get("AWS_LOCAL_ROLE_ARN"),
            RoleSessionName="local-session"
        )["Credentials"]
        s3 = boto3.client(
            "s3",
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
        )
        session["s3"] = s3
    return s3


def save_image(image: Image, filename: str):
    if storage_env == "local":
        save_image_locally(image, filename)
    elif storage_env == "s3":
        save_image_to_s3(image, filename)
    else:
        raise ValueError(f"Unknown environment: {storage_env}")


def save_image_locally(image: Image, filename: str):
    path = image_dir / f"{filename}.jpg"
    log.debug(f"Saving image to {path}")
    image.save(path)


def save_image_to_s3(image: Image, filename: str):
    s3 = get_s3_client()
    key = f"images/{filename}.jpg"
    log.debug(f"Saving image to s3: {bucket} {key}")
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
        raise ValueError(f"Unknown environment: {storage_env}")


def save_json_locally(json_data: dict, filename: str):
    path = data_dir / f"{filename}.json"
    log.debug(f"Saving json to {path}")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(json_data, f)


def save_json_to_s3(json_data: dict, filename: str):
    s3 = get_s3_client()
    key = f"{filename}.json"
    log.debug(f"Saving JSON to s3: {bucket} {key}")
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
        raise ValueError(f"Unknown environment: {storage_env}")


def save_features_locally(array: np.ndarray, filename: str):
    path = feature_dir / f"{filename}.npy"
    log.debug(f"Saving numpy array to {path}")
    np.save(path, array, allow_pickle=True)


def save_features_to_s3(array: np.ndarray, filename: str):
    s3 = get_s3_client()
    key = f"features/{filename}.npy"
    log.debug(f"Saving numpy array to s3: {bucket} {key}")
    array_binary = BytesIO()
    np.save(array_binary, array, allow_pickle=True)
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
        raise ValueError(f"Unknown environment: {storage_env}")


def save_model_locally(model: LSHModel, model_name: str):
    path = model_dir / model_name
    log.debug(f"Saving model to {path}")
    model.save(path)


def save_model_to_s3(model: LSHModel, model_name: str):
    s3 = get_s3_client()
    key = f"models/{model_name}.npy"
    log.debug(f"Saving model to s3: {bucket} {key}")
    model_binary = BytesIO()
    model.save(model_binary)
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=model_binary.getvalue(),
        ContentType="application/numpy",
    )


def load_image(filename: str):
    if storage_env == "local":
        return load_image_locally(filename)
    elif storage_env == "s3":
        return load_image_from_s3(filename)
    else:
        raise ValueError(f"Unknown environment: {storage_env}")


def load_image_locally(filename: str):
    path = image_dir / f"{filename}.jpg"
    log.debug(f"Loading image from {path}")
    return Image.open(path)


def load_image_from_s3(filename: str):
    s3 = get_s3_client()
    key = f"images/{filename}.jpg"
    log.debug(f"Loading image from s3: {bucket} {key}")
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
    s3 = get_s3_client()
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
    s3 = get_s3_client()
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
    log.debug(f"Loading numpy array from {path}")
    return np.load(path, allow_pickle=True)


def load_features_from_s3(filename: str):
    s3 = get_s3_client()
    key = f"features/{filename}.npy"
    log.debug(f"Loading numpy array from s3: {bucket} {key}")
    return np.load(
        BytesIO(s3.get_object(Bucket=bucket, Key=key)["Body"].read()),
        allow_pickle=True
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
    s3 = get_s3_client()
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
    s3 = get_s3_client()
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
    s3 = get_s3_client()
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
    log.debug(f"Loading model from {path}")
    return np.load(path, allow_pickle=True)


def load_model_from_s3(model_name: str):
    s3 = get_s3_client()
    key = f"models/{model_name}.npy"
    log.debug(f"Loading model from s3: {bucket} {key}")
    return np.load(
        BytesIO(
            s3.get_object(Bucket=bucket, Key=key)["Body"].read(),
            allow_pickle=True
        )
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
    log.debug(f"Loading json from {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_json_from_s3(filename: str):
    s3 = get_s3_client()
    key = f"{filename}.json"
    log.debug(f"Loading json from s3: {bucket} {key}")
    return json.loads(s3.get_object(Bucket=bucket, Key=key)["Body"].read())
