from datetime import datetime

import numpy as np
import typer

from src.load import load_features, yield_feature_filenames
from src.model import LSHModel
from src.save import save_model
from src.log import get_logger

log = get_logger()
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
    log.info(
        f"Training LSH model with {n_training_vectors} training vectors, "
        f"{n_groups} groups, and {n_clusters} clusters"
    )
    log.info("Loading features")
    features = np.vstack(
        [load_features(filename) for filename in yield_feature_filenames]
    )

    log.info("Selecting training vectors")
    random_indices = np.random.choice(
        features.shape[0], n_training_vectors, replace=False
    )
    training_features = features[random_indices]

    log.info("Training model")
    model = LSHModel(n_groups=n_groups, n_clusters=n_clusters)
    model.fit(training_features)

    model_name = f"lsh-{timestamp}"
    log.info(f"Saving model {model_name}")
    save_model(model, model_name)


if __name__ == "__main__":
    app()
