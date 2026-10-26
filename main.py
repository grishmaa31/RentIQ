from models.classification import perform_classification
from models.clustering import perform_clustering
from data_loader import load_dataset
from data_cleaning import clean_dataset
from eda import perform_eda


def main():
    print("=" * 45)
    print("RentIQ - Apartment Rental Intelligence System")
    print("=" * 45)

    print("\nStep 1: Dataset loading")
    df = load_dataset()

    print("\nStep 2: Data cleaning")
    cleaned_df = clean_dataset(df)

    print("\nStep 3: Exploratory data analysis")
    perform_eda(cleaned_df)

    print("\nRentIQ data preparation completed!")

    print("\nStep 4: K-Means clustering")
    cluster_results, clustering_model, scaler = perform_clustering(
        cleaned_df
    )

    print("\nStep 5: Classification")
    classification_results = perform_classification(cleaned_df)


if __name__ == "__main__":
    main()
