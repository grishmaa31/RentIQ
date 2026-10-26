
import os
import matplotlib.pyplot as plt
import seaborn as sns


def perform_eda(df):
    print("\nStarting Exploratory Data Analysis...")

    os.makedirs("outputs/eda", exist_ok=True)

    print("\nRental price statistics:")
    print(df["price"].describe())

    print("\nApartment size statistics:")
    print(df["square_feet"].describe())

    print("\nBedroom counts:")
    print(df["bedrooms"].value_counts().sort_index())

    plt.figure(figsize=(8, 5))
    sns.histplot(
        df["price"].dropna().clip(
            upper=df["price"].quantile(0.99)
        ),
        bins=40
    )
    plt.title("Distribution of Apartment Rental Prices")
    plt.xlabel("Rental Price")
    plt.ylabel("Number of Listings")
    plt.tight_layout()
    plt.savefig("outputs/eda/price_distribution.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.histplot(
        df["square_feet"].dropna().clip(
            upper=df["square_feet"].quantile(0.99)
        ),
        bins=40
    )
    plt.title("Distribution of Apartment Sizes")
    plt.xlabel("Square Feet")
    plt.ylabel("Number of Listings")
    plt.tight_layout()
    plt.savefig("outputs/eda/size_distribution.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.countplot(x=df["bedrooms"].dropna().astype(int))
    plt.title("Apartment Listings by Number of Bedrooms")
    plt.xlabel("Bedrooms")
    plt.ylabel("Number of Listings")
    plt.tight_layout()
    plt.savefig("outputs/eda/bedroom_distribution.png")
    plt.close()

    plot_df = df[["price", "square_feet"]].dropna()

    plot_df = plot_df[
        (plot_df["price"] > 0) &
        (plot_df["square_feet"] > 0)
    ]

    plot_df = plot_df.sample(
        n=min(5000, len(plot_df)),
        random_state=42
    )

    plt.figure(figsize=(8, 5))
    sns.scatterplot(
        data=plot_df,
        x="square_feet",
        y="price",
        alpha=0.5
    )
    plt.title("Rental Price vs Apartment Size")
    plt.xlabel("Square Feet")
    plt.ylabel("Rental Price")
    plt.tight_layout()
    plt.savefig("outputs/eda/price_vs_size.png")
    plt.close()

    print("\nEDA completed!")
    print("Graphs saved in outputs/eda/")

    return df
