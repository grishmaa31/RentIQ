
import joblib
import pandas as pd


def predict_price_category(square_feet, bedrooms, bathrooms, latitude, longitude):
    model = joblib.load("outputs/rent_iq_model.pkl")

    apartment = pd.DataFrame([{
        "square_feet": square_feet,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "latitude": latitude,
        "longitude": longitude
    }])

    prediction = model.predict(apartment)

    return prediction[0]


if __name__ == "__main__":
    print("\n===== RentIQ Apartment Price Predictor =====")

    square_feet = float(input("Enter apartment size (sq. ft.): "))
    bedrooms = float(input("Enter number of bedrooms: "))
    bathrooms = float(input("Enter number of bathrooms: "))
    latitude = float(input("Enter latitude: "))
    longitude = float(input("Enter longitude: "))

    if square_feet <= 0 or bedrooms < 0 or bathrooms <= 0:
        print("Invalid input. Please enter valid apartment details.")
    elif not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        print("Invalid latitude or longitude.")
    else:
        result = predict_price_category(
            square_feet,
            bedrooms,
            bathrooms,
            latitude,
            longitude
        )

        print("\nPredicted Price Category:", result)
