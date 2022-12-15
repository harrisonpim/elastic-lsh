import os

from elasticsearch import Elasticsearch

from src.load import (
    count_features,
    load_features,
    load_json,
    load_model,
    get_latest_model_name,
    yield_feature_filenames,
)
from src.log import get_logger
from src.model import LSHModel

log = get_logger()

log.info("Loading Elasticsearch client")
es = Elasticsearch(
    os.environ.get("AWS_OPENSEARCH_ENDPOINT"),
    basic_auth=(
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
descriptions = load_json("descriptions.json")

log.info(f"Creating index {model_name}")
if es.indices.exists(index=model_name):
    es.indices.delete(index=model_name)

es.indices.create(
    index=model_name,
    mappings={
        "properties": {
            "lsh-hash": {"type": "keyword"},
            "description": {"type": "text", "analyzer": "english"},
        }
    },
)


total_features = count_features()
for i, filename in enumerate(yield_feature_filenames()):
    log.info(
        f"Processing feature {i + 1} of {total_features}"
        f"({i/total_features*100: .2f} %)"
    )
    try:
        feature_vector = load_features(filename)
        predictions = model.predict(feature_vector.reshape(1, -1))
    except Exception as e:
        log.error(f"Error processing feature {filename}: {e}")
        continue

    log.info(f"Indexing feature {filename}")
    try:
        es.index(
            index=model_name,
            id=filename,
            document={
                "lsh-hash": predictions,
                "description": descriptions[filename],
            },
        )
    except Exception as e:
        log.error(f"Error indexing feature {filename}: {e}")
        continue
