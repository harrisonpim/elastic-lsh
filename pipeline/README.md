# Pipeline

Data pipeline which

- fetches the [LAION-Aesthetics V2 dataset](https://laion.ai/blog/laion-aesthetics/) dataset and downloads the images, saving them to a local directory or s3
- extracts features and stores them in a local directory or s3
- trains a model on a subset of the data, saving the model to a local directory or s3
- infers LSH hashes for all the data, and stores the hashes and image captions in an elasticsearch index to be searched and compared
