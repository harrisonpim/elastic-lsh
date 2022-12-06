from pathlib import Path
from typing import List, Optional, Union

import numpy as np
from sklearn.cluster import KMeans
from tqdm import tqdm


class LSHModel:
    def __init__(
        self,
        path: Optional[Union[Path, str]] = None,
        n_groups: Optional[int] = 32,
        n_clusters: Optional[int] = 16,
    ):
        if path is None and n_groups is not None and n_clusters is not None:
            self.models: List[KMeans] = None
            self.n_groups = n_groups
            self.n_clusters = n_clusters
        elif path is not None and n_groups is None and n_clusters is None:
            self.models = self.load(path)
            self.n_groups = len(self.models)
            self.n_clusters = self.models[0].n_clusters
        else:
            raise ValueError(
                "Either path or n_groups and n_clusters must be specified"
            )

    def fit(self, features: np.ndarray, verbose: bool = False) -> List[KMeans]:
        feature_groups = np.split(
            features, indices_or_sections=self.n_groups, axis=1
        )

        if verbose:
            feature_groups = tqdm(feature_groups)
        models = [
            KMeans(n_clusters=self.n_clusters).fit(feature_group)
            for feature_group in feature_groups
        ]

        self.models = models
        return models

    @staticmethod
    def encode(clusters):
        return [f"{i}-{val}" for i, val in enumerate(clusters)]

    def predict(self, features: np.ndarray, models: List[KMeans]) -> List[str]:
        feature_groups = np.split(
            features, indices_or_sections=self.n_groups, axis=1
        )

        predictions = [
            model.predict(feature_group)
            for model, feature_group in zip(models, feature_groups)
        ]
        return self.encode(predictions)

    def save(self, path: Path):
        np.save(path, self.models)

    def load(self, path: Path) -> List[KMeans]:
        return np.load(path, allow_pickle=True)
