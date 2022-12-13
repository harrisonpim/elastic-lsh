from datetime import datetime
from pathlib import Path

import numpy as np
import typer

from src.load import load_features, yield_features_filenames
from src.model import LSHModel
from src.save import save_model

app = typer.Typer()


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
        [load_features(filename) for filename in yield_features_filenames]
    )

    random_indices = np.random.choice(
        features.shape[0], n_training_vectors, replace=False
    )
    training_features = features[random_indices]

    model = LSHModel(n_groups=n_groups, n_clusters=n_clusters)
    model.fit(training_features)

    save_model(model, f"lsh-{timestamp}")


if __name__ == "__main__":
    app()
