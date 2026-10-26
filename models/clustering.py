
import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


def perform_clustering(df):
    print("\nStarting K-Means clustering...")

    os.makedirs("outputs/clustering", exist_ok=True)

    features = [
        "price",
        "square_feet",
        "bedrooms",
        "bathrooms"
    ]

    data = df[features].copy()

    for column in features:
        data[column] = pd.to_numeric(
            data[column], errors="coerce"
        )

    data = data.dropna()
    data = data[(data > 0).all(axis=1)]

    if len(data) < 3:
        raise ValueError("Not enough valid records for clustering.")

    print("Listings used:", len(data))

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    model = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(scaled_data)

    sample_size = min(5000, len(scaled_data))

    sample_data = scaled_data[:sample_size]
    sample_labels = labels[:sample_size]

    score = silhouette_score(
        sample_data,
        sample_labels
    )

    print("\nCluster sizes:")
    print(pd.Series(labels).value_counts().sort_index())

    print("\nCluster characteristics:")
    summary = data.assign(
        cluster=labels
    ).groupby("cluster").mean()

    print(summary.round(2))

    print("\nSilhouette score:", round(score, 4))

    results = data.copy()
    results["cluster"] = labels

    results.to_csv(
        "outputs/clustering/clustering_results.csv",
        index=False
    )

    plt.figure(figsize=(9, 6))
    plt.scatter(
        data["square_feet"],
        data["price"],
        c=labels,
        alpha=0.5
    )

    plt.title("RentIQ: Apartment Rental Clusters")
    plt.xlabel("Square Feet")
    plt.ylabel("Rental Price")
    plt.tight_layout()

    plt.savefig("outputs/clustering/rental_clusters.png")
    plt.close()

    print("\nClustering results saved in outputs/clustering/")
    print("Graph saved to outputs/clustering/rental_clusters.png")

    return results, model, scaler
