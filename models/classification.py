
import joblib
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


def perform_classification(df):
    print("\nStarting classification...")

    os.makedirs("outputs/classification", exist_ok=True)

    data = df.copy()

    features = [
        "square_feet",
        "bedrooms",
        "bathrooms",
        "latitude",
        "longitude"
    ]

    for column in features + ["price"]:
        data[column] = pd.to_numeric(
            data[column], errors="coerce"
        )

    data = data.dropna(subset=["price"])
    data = data[data["price"] > 0].copy()

    low_threshold = data["price"].quantile(1 / 3)
    high_threshold = data["price"].quantile(2 / 3)

    data["price_category"] = pd.cut(
        data["price"],
        bins=[
            float("-inf"),
            low_threshold,
            high_threshold,
            float("inf")
        ],
        labels=["Low", "Medium", "High"],
        include_lowest=True
    )

    print("Low price threshold:", round(low_threshold, 2))
    print("High price threshold:", round(high_threshold, 2))

    X = data[features]
    y = data["price_category"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    models = {
        "Decision Tree": DecisionTreeClassifier(
            max_depth=12,
            min_samples_leaf=10,
            random_state=42
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            max_depth=12,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1
        )
    }

    results = []

    for name, classifier in models.items():
        pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("classifier", classifier)
        ])

        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)

        if name == "Random Forest":
            joblib.dump(pipeline, "outputs/rent_iq_model.pkl")
            print("Random Forest model saved successfully!")

        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(
            y_test, predictions, average="weighted",
            zero_division=0
        )
        recall = recall_score(
            y_test, predictions, average="weighted",
            zero_division=0
        )
        f1 = f1_score(
            y_test, predictions, average="weighted",
            zero_division=0
        )

        results.append({
            "Model": name,
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1-score": f1
        })

        print(f"\n{name}")
        print("Accuracy:", round(accuracy, 4))
        print("Precision:", round(precision, 4))
        print("Recall:", round(recall, 4))
        print("F1-score:", round(f1, 4))

        print("\nClassification report:")
        print(classification_report(
            y_test, predictions, zero_division=0
        ))

        matrix = confusion_matrix(
            y_test, predictions,
            labels=["Low", "Medium", "High"]
        )

        plt.figure(figsize=(6, 5))
        sns.heatmap(
            matrix,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=["Low", "Medium", "High"],
            yticklabels=["Low", "Medium", "High"]
        )
        plt.title(f"{name} Confusion Matrix")
        plt.xlabel("Predicted Category")
        plt.ylabel("Actual Category")
        plt.tight_layout()

        filename = name.lower().replace(" ", "_")
        plt.savefig(
            f"outputs/classification/{filename}_confusion_matrix.png"
        )
        plt.close()

    results_df = pd.DataFrame(results)
    results_df.to_csv(
        "outputs/classification/classification_metrics.csv",
        index=False
    )

    print("\nModel comparison:")
    print(results_df.round(4).to_string(index=False))
    print("\nClassification results saved in outputs/classification/")

    return results_df
