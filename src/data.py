from typing import List

import numpy as np


def split_features(
    feature_vectors: np.ndarray, n_groups: int
) -> List[np.ndarray]:
    return np.split(feature_vectors, indices_or_sections=n_groups, axis=1)
