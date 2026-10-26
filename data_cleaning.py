
import os
import pandas as pd


def clean_dataset(df):
    print("\nStarting data cleaning...")

    df = df.copy()

    original_rows = len(df)

    df = df.drop_duplicates()

    print("Duplicate rows removed:", original_rows - len(df))

    numeric_columns = [
        "price",
        "square_feet",
        "bedrooms",
        "bathrooms",
        "latitude",
        "longitude"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["price"] = df["price"].where(df["price"] > 0)
    df["square_feet"] = df["square_feet"].where(
        df["square_feet"] > 0
    )
    df["bedrooms"] = df["bedrooms"].where(df["bedrooms"] >= 0)
    df["bathrooms"] = df["bathrooms"].where(df["bathrooms"] > 0)

    df = df.dropna(subset=["price", "bedrooms", "bathrooms"])

    for column in ["bedrooms", "bathrooms"]:
        df[column] = df[column].fillna(df[column].median())

    for column in ["amenities", "pets_allowed", "has_photo"]:
        df[column] = df[column].fillna("Unknown")

    print("Rows before cleaning:", original_rows)
    print("Rows after cleaning:", len(df))
    print("Remaining missing values:", df.isnull().sum().sum())

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/cleaned_apartments.csv", index=False)

    print("Cleaned dataset saved to data/cleaned_apartments.csv")

    return df
