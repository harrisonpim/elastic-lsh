# Pipeline

Data pipeline which

- fetches a raw dataset
- extracts features
- trains a model on a subset of the data
- infers LSH hashes for all the data
- stores the hashes in an elasticsearch index
