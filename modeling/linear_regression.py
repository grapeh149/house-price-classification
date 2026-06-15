import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

from data.data_loader import *



def get_data():
    data = load_data()
    feature = data.iloc[:,1:12]
    label = data.iloc[:, -1]

    return feature, label

def normalization():
    features, labels = get_data()
    data_encoded = pd.get_dummies(features, columns=['house_type', 'legal_status', 'street', 'ward',
                                              'district'])
    scaler = StandardScaler()
    feature_scaled = scaler.fit_transform(data_encoded)

    encoder_label = LabelEncoder()
    label_encoded = encoder_label.fit_transform(labels)

    return feature_scaled, label_encoded, encoder_label

def training():
    feature_scaled, label_encoded, encoder_label = normalization()
    feature_train, feature_test, label_train, label_test = train_test_split(feature_scaled, label_encoded,
                                                                            test_size=0.25, random_state=42)
    model = LinearRegression()
    model.fit(feature_train, label_train)

    return model, feature_train, feature_test, label_train, label_test, encoder_label

def predict_LN():

    model, f_train, f_test, l_train, l_test, en_label = training()


    prediction = model.predict(f_test)


    plt.figure(figsize=(8, 6))
    plt.scatter(l_test, prediction, alpha=0.6, color='blue')


    min_val = min(np.min(l_test), np.min(prediction))
    max_val = max(np.max(l_test), np.max(prediction))
    plt.plot([min_val, max_val], [min_val, max_val], 'k--', lw=2, color='red')

    plt.xlabel("Actual value: ")
    plt.ylabel("Predict value ")
    plt.title("Linear Regression")
    plt.show()


    mse = mean_squared_error(l_test, prediction)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(l_test, prediction)
    r2 = r2_score(l_test, prediction)

    print("\n📊 Regression Metrics Report:")
    print(f"- Mean Absolute Error (MAE): ")
    print(f"- Mean Squared Error (MSE): ")
    print(f"- Root Mean Squared Error (RMSE): ")
    print(f"- R-squared (R2 Score):")



