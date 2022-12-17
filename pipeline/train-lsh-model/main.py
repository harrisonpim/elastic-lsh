from datetime import datetime

import numpy as np
import typer
from src.io import load_features, save_model, yield_feature_filenames
from src.log import get_logger
from src.model import LSHModel

log = get_logger()
app = typer.Typer()


@app.command()
def main(
    n_training_vectors: int = typer.Option(
        10000, help="Number of training vectors to use"
    ),
    n_groups: int = typer.Option(
        256,
        help=(
            "Number of groups to split the features into, "
            "and therefore number of models to train"
        ),
    ),
    n_clusters: int = typer.Option(
        256, help="Number of clusters to fit within each group"
    ),
):
    timestamp = datetime.now().isoformat(timespec="seconds")
    log.info(
        f"Training LSH model with {n_training_vectors} training vectors, "
        f"{n_groups} groups, and {n_clusters} clusters"
    )
    log.info("Loading features")

    filenames = list(yield_feature_filenames())
    log.info(f"Selecting {n_training_vectors} training vectors")
    random_indices = np.random.choice(
        len(filenames), n_training_vectors, replace=False
    )
    training_filenames = [filenames[index] for index in random_indices]
    training_features = np.vstack(
        [load_features(filename) for filename in training_filenames]
    )

    log.info("Training model")
    model = LSHModel(n_groups=n_groups, n_clusters=n_clusters)
    model.fit(training_features)

    model_name = f"lsh-{timestamp}"
    log.info(f"Saving model {model_name}")
    save_model(model, model_name)


if __name__ == "__main__":
    app()
