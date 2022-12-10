import json
import os
from io import BytesIO
from pathlib import Path

import boto3

compute_env = os.environ.get("COMPUTE_ENVIRONMENT")
storage_env = os.environ.get("STORAGE_ENVIRONMENT")
aws_profile = os.environ.get("AWS_PROFILE")
bucket_name = os.environ.get("S3_BUCKET_ID")
data_dir = Path(os.environ.get("DATA_DIR"))
assume_role_arn = os.environ.get("LOCAL_ROLE_ARN")

if storage_env == "s3":
    boto3.setup_default_session(profile_name=aws_profile)
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


def save_image_locally(image, filename):
    image.save(data_dir / "images" / f"{filename}.jpg")


def save_image_to_s3(image, filename):
    image_bytes = BytesIO()
    image.save(image_bytes, format="JPEG")
    s3.put_object(
        Bucket=bucket_name,
        Key=f"images/{filename}.jpg",
        Body=image_bytes.getvalue(),
        ContentType="image/jpeg",
    )


def save_json_locally(json_data, filename):
    with open(data_dir / f"{filename}.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f)


def save_json_to_s3(json_data, filename):
    s3.put_object(
        Bucket=bucket_name,
        Key=f"{filename}.json",
        Body=json.dumps(json_data).encode("utf-8"),
        ContentType="application/json",
    )


def save_image(image, filename):
    if storage_env == "local":
        save_image_locally(image, filename)
    elif storage_env == "s3":
        save_image_to_s3(image, filename)
    else:
        raise ValueError("Unknown environment")


def save_json(json_data, filename):
    if storage_env == "local":
        save_json_locally(json_data, filename)
    elif storage_env == "s3":
        save_json_to_s3(json_data, filename)
    else:
        raise ValueError("Unknown environment")
