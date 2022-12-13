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
    data_dir = Path(os.environ.get("DATA_DIR"))


def load_image(filename: str):
    if storage_env == "local":
        return load_image_locally(filename)
    elif storage_env == "s3":
        return load_image_from_s3(filename)
    else:
        raise ValueError("Unknown environment")


def load_image_locally(filename: str):
    path = data_dir / "raw" / "images" / f"{filename}.jpg"
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
        raise ValueError("Unknown environment")


def yield_image_filenames_locally():
    for path in (data_dir / "raw" / "images").iterdir():
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
        raise ValueError("Unknown environment")


def count_images_locally():
    return len(list((data_dir / "raw" / "images").iterdir()))


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
        raise ValueError("Unknown environment")


def load_features_locally(filename: str):
    path = data_dir / "raw" / "features" / f"{filename}.npy"
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
        raise ValueError("Unknown environment")


def yield_features_filenames_locally():
    for path in (data_dir / "raw" / "features").iterdir():
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
        raise ValueError("Unknown environment")


def count_features_locally():
    return len(list((data_dir / "raw" / "features").iterdir()))


def count_features_from_s3():
    paginator = s3.get_paginator("list_objects_v2")
    count = 0
    for page in paginator.paginate(Bucket=bucket, Prefix="features"):
        count += len(page["Contents"])
    return count


def load_model(model_name: str):
    if storage_env == "local":
        return load_model_locally(model_name)
    elif storage_env == "s3":
        return load_model_from_s3(model_name)
    else:
        raise ValueError("Unknown environment")


def load_model_locally(model_name: str):
    path = data_dir / "models" / f"{model_name}.npy"
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
        raise ValueError("Unknown environment")


def load_json_locally(filename: str):
    path = data_dir / f"{filename}.json"
    log.info(f"Loading json from {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_json_from_s3(filename: str):
    key = f"{filename}.json"
    log.info(f"Loading json from s3: {bucket} {key}")
    return json.loads(s3.get_object(Bucket=bucket, Key=key)["Body"].read())
