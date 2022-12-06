import json
from pathlib import Path

import numpy as np
from elasticsearch import Elasticsearch
from tqdm import tqdm

from src.model import LSHModel

es = Elasticsearch(
    "http://elasticsearch:9200", basic_auth=("elastic", "password")
)

data_dir = Path("/data")
features_dir = data_dir / "raw" / "features"
model_dir = data_dir / "models"
model_path = sorted(model_dir.glob("*.npy"))[-1]
model_name = model_path.stem.replace(":", "-").lower()
model = LSHModel(path=model_path)

with open(data_dir / "raw" / "descriptions.json", "r", encoding="utf-8") as f:
    descriptions = json.load(f)

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


for file_path in tqdm(
    features_dir.glob("*.npy"), total=len(list(features_dir.glob("*.npy")))
):
    image_id = file_path.stem
    feature_vector = np.load(file_path)
    predictions = model.predict(feature_vector.reshape(1, -1))
    es.index(
        index=model_name,
        id=image_id,
        document={
            "lsh-hash": predictions,
            "description": descriptions[image_id],
        },
    )
