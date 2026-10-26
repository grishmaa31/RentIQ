
# RentIQ: Apartment Rental Intelligence System

A machine learning project for analyzing apartment rental listings using data preprocessing, exploratory data analysis, classification, clustering, and regression.

## Project Information

- **Course:** Machine Learning Projects
- **Section:** Sec_A
- **Group:** 6

### Team Members

| Name | Student ID |
| --- | --- |
| Grishma Asvin Madhvani | 2427010434 |
| Chaitali Goyal | 2427010514 |
| Tanvi Sharma | 2427010513 |

## Problem Statement

Develop a machine learning framework for analyzing apartment rental listings that identifies meaningful rental property segments, classifies apartments based on their characteristics, and predicts property attributes such as square footage using relevant demographic, geographic, and housing features. The framework should address data quality issues, uncover underlying patterns in rental properties, and provide accurate, data-driven insights for understanding and predicting apartment characteristics and rental market behavior.

## Dataset

The project uses the Apartment for Rent Classified dataset from the UCI Machine Learning Repository (2019).

- **Dataset ID:** 555
- **DOI:** [10.24432/C5X623](https://doi.org/10.24432/C5X623)
- **Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/555/apartment+for+rent+classified)

The dataset contains apartment rental listings and associated property information. The available features are examined to determine their suitability for analysis and model development.

## Objectives

- Clean the dataset by handling missing values, duplicates, and outliers.
- Explore rental data using statistical analysis and visualizations.
- Classify apartment listings using relevant property features.
- Group similar apartments using clustering techniques.
- Predict apartment square footage using regression.
- Evaluate model performance and present the results through visualizations and an interactive dashboard.

## Methodology

The project follows these stages:

1. **Data collection:** Retrieve the dataset using `ucimlrepo`.
2. **Data preprocessing:** Handle missing values, duplicate records, outliers, and data types.
3. **Exploratory data analysis:** Study feature distributions, correlations, and relationships between apartment attributes.
4. **Classification:** Train and evaluate a supervised learning model using a defined categorical target.
5. **Clustering:** Identify groups of similar apartments based on selected features.
6. **Regression:** Predict square footage and evaluate the prediction errors.
7. **Visualization:** Present analytical results through plots and a Streamlit dashboard.

### Evaluation Metrics

| Task | Metrics |
| --- | --- |
| Classification | Accuracy, Precision, Recall, F1-score, Confusion Matrix |
| Clustering | Silhouette Score and cluster analysis |
| Regression | MAE, RMSE, R² Score |

The final model names and evaluation results should be documented after running the implemented pipeline.

## Project Structure

```text
RentIQ/
├── data/
│   ├── raw_apartments.csv
│   └── cleaned_apartments.csv
├── models/
│   ├── classification.py
│   └── clustering.py
├── outputs/
│   ├── EDA plots
│   ├── Classification metrics and confusion matrices
│   ├── Cluster results
│   └── rent_iq_model.pkl
├── app.py
├── data_cleaning.py
├── data_loader.py
├── eda.py
├── main.py
├── predict.py
├── requirements.txt
└── README.md
```

## Technologies Used

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Scikit-learn
- ucimlrepo
- Joblib
- Streamlit
- Plotly

## Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/grishmaa31/RentIQ.git
cd RentIQ
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

On Windows, activate it using:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the project

To execute the main pipeline:

```bash
python main.py
```

If the scripts support independent execution, the individual stages can also be run using:

```bash
python data_loader.py
python data_cleaning.py
python eda.py
```

### 5. Launch the dashboard

```bash
streamlit run app.py
```

### 6. Run predictions

After training and saving the required model:

```bash
python predict.py
```

## Expected Outputs

The pipeline is designed to generate:

- Raw and cleaned datasets.
- Exploratory data analysis plots.
- Classification evaluation metrics and confusion matrices.
- Cluster assignments and related visualizations.
- A serialized model saved as `outputs/rent_iq_model.pkl`.
- An interactive dashboard for supported analytical and prediction tasks.

The exact outputs depend on the implemented pipeline and the models trained.

## Conclusion

RentIQ applies machine learning techniques to apartment rental data to examine property characteristics, identify similar listings, classify apartments, and predict square footage. The project combines data preprocessing, visualization, model evaluation, and an interactive dashboard in a single workflow.

## References

1. UCI Machine Learning Repository. *Apartment for Rent Classified*. [Dataset DOI](https://doi.org/10.24432/C5X623).
2. Scikit-learn Documentation: https://scikit-learn.org/stable/
3. Pandas Documentation: https://pandas.pydata.org/docs/
4. Streamlit Documentation: https://docs.streamlit.io/
5. UCI ML Repository Python Package: https://github.com/uci-ml-repo/ucimlrepo
