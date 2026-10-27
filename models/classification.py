
import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import (
    train_test_split,
    GridSearchCV,
    StratifiedKFold
)
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
    os.makedirs("outputs", exist_ok=True)

    features = [
        "square_feet",
        "bedrooms",
        "bathrooms",
        "latitude",
        "longitude"
    ]

    required = features + ["price"]
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    data = df[required].copy()

    for column in required:
        data[column] = pd.to_numeric(
            data[column], errors="coerce"
        )

    # The target price must be valid. Missing input features can
    # be imputed by the pipeline using training data only.
    data = data.dropna(subset=["price"])
    data = data[data["price"] > 0]

    if len(data) < 50:
        raise ValueError("Not enough valid records for model training.")

    X = data[features]
    prices = data["price"]

    # Split first so category boundaries are learned from training
    # prices, not from the held-out test prices.
    X_train, X_test, price_train, price_test = train_test_split(
        X,
        prices,
        test_size=0.20,
        random_state=42
    )

    low_threshold = price_train.quantile(1 / 3)
    high_threshold = price_train.quantile(2 / 3)

    if low_threshold >= high_threshold:
        raise ValueError(
            "Price quantiles are not distinct enough to create "
            "three price categories. Review the price distribution."
        )

    bins = [
        float("-inf"),
        low_threshold,
        high_threshold,
        float("inf")
    ]
    category_names = ["Low", "Medium", "High"]

    y_train = pd.cut(
        price_train,
        bins=bins,
        labels=category_names,
        include_lowest=True
    )
    y_test = pd.cut(
        price_test,
        bins=bins,
        labels=category_names,
        include_lowest=True
    )

    if y_train.isna().any() or y_test.isna().any():
        raise ValueError(
            "Some prices were not assigned a category. "
            "Check price thresholds and category construction."
        )

    # Remove rows with missing input values from neither set:
    # the pipeline will impute them.
    print("Training records:", len(X_train))
    print("Testing records:", len(X_test))
    print("Low price threshold:", round(low_threshold, 2))
    print("High price threshold:", round(high_threshold, 2))

    # Baseline: Decision Tree.
    decision_tree = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", DecisionTreeClassifier(
            max_depth=12,
            min_samples_leaf=10,
            class_weight="balanced",
            random_state=42
        ))
    ])

    decision_tree.fit(X_train, y_train)
    dt_predictions = decision_tree.predict(X_test)

    # Improved model: search for useful Random Forest settings
    # using cross-validation on the training data only.
    rf_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", RandomForestClassifier(
            random_state=42,
            class_weight="balanced",
            n_jobs=1
        ))
    ])

    parameter_grid = {
        "classifier__n_estimators": [100, 200],
        "classifier__max_depth": [12, None],
        "classifier__min_samples_leaf": [2, 5],
        "classifier__max_features": ["sqrt", 1.0]
    }

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    search = GridSearchCV(
        estimator=rf_pipeline,
        param_grid=parameter_grid,
        scoring="f1_macro",
        cv=cv,
        n_jobs=-1,
        refit=True
    )

    print("\nTuning Random Forest with 5-fold cross-validation...")
    search.fit(X_train, y_train)

    best_model = search.best_estimator_
    rf_predictions = best_model.predict(X_test)

    print("\nBest Random Forest parameters:")
    print(search.best_params_)
    print("Best cross-validation macro F1:",
          round(search.best_score_, 4))

    # Evaluate both models on the same held-out test data.
    model_predictions = {
        "Decision Tree": dt_predictions,
        "Random Forest (Tuned)": rf_predictions
    }

    results = []

    for name, predictions in model_predictions.items():
        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(
            y_test, predictions,
            average="weighted", zero_division=0
        )
        recall = recall_score(
            y_test, predictions,
            average="weighted", zero_division=0
        )
        weighted_f1 = f1_score(
            y_test, predictions,
            average="weighted", zero_division=0
        )
        macro_f1 = f1_score(
            y_test, predictions,
            average="macro", zero_division=0
        )

        results.append({
            "Model": name,
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "Weighted F1": weighted_f1,
            "Macro F1": macro_f1
        })

        print(f"\n{name}")
        print("Accuracy:", round(accuracy, 4))
        print("Precision:", round(precision, 4))
        print("Recall:", round(recall, 4))
        print("Weighted F1:", round(weighted_f1, 4))
        print("Macro F1:", round(macro_f1, 4))

        print("\nClassification report:")
        print(classification_report(
            y_test,
            predictions,
            labels=category_names,
            zero_division=0
        ))

        matrix = confusion_matrix(
            y_test,
            predictions,
            labels=category_names
        )

        plt.figure(figsize=(6, 5))
        sns.heatmap(
            matrix,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=category_names,
            yticklabels=category_names
        )
        plt.title(f"{name} Confusion Matrix")
        plt.xlabel("Predicted Category")
        plt.ylabel("Actual Category")
        plt.tight_layout()

        filename = name.lower().replace(" ", "_").replace("(", "").replace(")", "")
        plt.savefig(
            f"outputs/classification/{filename}_confusion_matrix.png"
        )
        plt.close()

    results_df = pd.DataFrame(results)
    results_df.to_csv(
        "outputs/classification/classification_metrics.csv",
        index=False
    )

    # Save the tuned model in the exact location expected by predict.py.
    joblib.dump(best_model, "outputs/rent_iq_model.pkl")

    print("\nModel comparison:")
    print(results_df.round(4).to_string(index=False))
    print("\nSaved tuned model to outputs/rent_iq_model.pkl")
    print("Classification results saved in outputs/classification/")

    return results_df
