"""
Description
- This script downloads a dataset from Kaggle using the Kaggle API.

"""

import kagglehub

# Download latest version
path = kagglehub.dataset_download("Cornell-University/arxiv")

print("Path to dataset files:", path)