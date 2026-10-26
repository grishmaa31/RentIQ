import os
import pandas as pd
from ucimlrepo import fetch_ucirepo


def load_dataset():
    print("\nLoading apartment rental dataset...")

    apartment = fetch_ucirepo(id=555)
    df = apartment.data.features.copy()

    os.makedirs("data", exist_ok=True)

    df.to_csv("data/raw_apartments.csv", index=False)

    print("Dataset loaded successfully!")
    print("Number of rows:", df.shape[0])
    print("Number of columns:", df.shape[1])
    print("Raw dataset saved to data/raw_apartments.csv")

    return df
