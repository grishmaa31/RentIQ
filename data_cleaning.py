
import os
import pandas as pd


def clean_dataset(df):
    print("\nStarting data cleaning...")

    df = df.copy()
    original_rows = len(df)

    # Remove exact duplicate listings
    df = df.drop_duplicates()
    print("Duplicate rows removed:", original_rows - len(df))

    # Convert numeric columns
    numeric_columns = [
        "price",
        "square_feet",
        "bedrooms",
        "bathrooms",
        "latitude",
        "longitude"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column], errors="coerce"
            )

    # Mark invalid values as missing
    df.loc[df["price"] <= 0, "price"] = float("nan")
    df.loc[df["square_feet"] <= 0, "square_feet"] = float("nan")
    df.loc[df["bedrooms"] < 0, "bedrooms"] = float("nan")
    df.loc[df["bathrooms"] <= 0, "bathrooms"] = float("nan")

    # Validate geographic coordinate ranges
    df.loc[~df["latitude"].between(-90, 90), "latitude"] = float("nan")
    df.loc[~df["longitude"].between(-180, 180), "longitude"] = float("nan")

    # Price is required if it will be used as the target
    df = df.dropna(subset=["price"])

    # Handle missing categorical values
    for column in ["amenities", "pets_allowed", "has_photo"]:
        if column in df.columns:
            df[column] = df[column].fillna("Unknown")

    print("Rows before cleaning:", original_rows)
    print("Rows after cleaning:", len(df))
    print("\nMissing values by column:")
    print(df.isnull().sum())

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/cleaned_apartments.csv", index=False)

    print("Cleaned dataset saved to data/cleaned_apartments.csv")

    return df
