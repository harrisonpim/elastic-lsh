from datetime import datetime
from pathlib import Path

import numpy as np
import typer

from src.data import split_features
from src.model import LSHModel

app = typer.Typer()

data_dir = Path("/data")
model_dir = data_dir / "models"
features_dir = data_dir / "raw" / "features"


@app.command()
def main(
    n_training_vectors: int = typer.Option(
        100, help="Number of training vectors to use"
    ),
    n_groups: int = typer.Option(
        32,
        help=(
            "Number of groups to split the features into, "
            "and therefore number of models to train"
        ),
    ),
    n_clusters: int = typer.Option(
        16, help="Number of clusters to fit within each group"
    ),
):
    timestamp = datetime.now().isoformat(timespec="seconds")
    features = np.vstack(
        [
            np.load(features_path)
            for features_path in features_dir.glob("*.npy")
        ]
    )

    random_indices = np.random.choice(
        features.shape[0], n_training_vectors, replace=False
    )
    training_features = features[random_indices]

    model = LSHModel(n_groups=n_groups, n_clusters=n_clusters)
    model.fit(training_features)
    model.save(model_dir / timestamp)


if __name__ == "__main__":
    app()
