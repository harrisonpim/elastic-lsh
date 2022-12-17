import os

from elasticsearch import Elasticsearch
from src.io import (
    count_features,
    get_latest_model_name,
    load_features,
    load_json,
    load_model,
    yield_feature_filenames,
)
from src.log import get_logger
from src.model import LSHModel

log = get_logger()

log.info("Loading Elasticsearch client")
es = Elasticsearch(
    "https://" + os.environ.get("AWS_OPENSEARCH_ENDPOINT") + ":443",
    http_auth=(
        os.environ.get("AWS_OPENSEARCH_USERNAME"),
        os.environ.get("AWS_OPENSEARCH_PASSWORD"),
    ),
)

if os.environ.get("MODEL_NAME"):
    model_name = os.environ.get("MODEL_NAME")
else:
    model_name = get_latest_model_name()
log.info(f"Loading model {model_name}")
model_bytes = load_model(model_name)
model = LSHModel(model_bytes=model_bytes)


log.info("Loading image descriptions")
descriptions = load_json("descriptions")

index_name = model_name.replace("T", "-").replace(":", "-")
log.info(f"Creating index {index_name}")
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

es.indices.create(
    index=index_name,
    body={
        "mappings": {
            "properties": {
                "lsh-hash": {"type": "keyword"},
                "description": {"type": "text", "analyzer": "english"},
            }
        }
    },
)


total_features = count_features()
for i, filename in enumerate(yield_feature_filenames()):
    log.info(
        f"Processing feature {i + 1} of {total_features} "
        f"({i/total_features*100:.2f}%)"
    )
    try:
        feature_vector = load_features(filename)
        log.debug(f"Inferring hashes for {filename}")
        predictions = model.predict(feature_vector.reshape(1, -1))
    except Exception as e:
        log.error(f"Error processing {filename}: {e}")
        continue

    log.debug(f"Indexing hashes for {filename}")
    try:
        es.index(
            index=index_name,
            id=filename,
            body={
                "lsh-hash": predictions,
                "description": descriptions[filename],
            },
        )
    except Exception as e:
        log.error(f"Error indexing hashes for {filename}: {e}")
        continue
