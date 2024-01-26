import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf
from keras.models import load_model
import streamlit as st
from datetime import date, timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Function to predict future prices
def predict_future_prices(data_scaled, model, last_100_days_scaled, start_date, days_to_predict, scaler):
    future_dates = pd.date_range(start=start_date + timedelta(days=1), periods=days_to_predict)
    future_data_scaled = last_100_days_scaled.copy()

    for _ in future_dates:
        last_100_days = future_data_scaled[-100:].reshape(1, 100, 1)
        next_day_prediction = model.predict(last_100_days)
        future_data_scaled = np.append(future_data_scaled, next_day_prediction[0, -1])

    future_data_scaled = future_data_scaled[100:].reshape(-1, 1)
    future_prices = scaler.inverse_transform(future_data_scaled)
    return pd.DataFrame({'Date': future_dates, 'Predicted Price': future_prices.flatten()})

def app():
    st.header('Stock Market Predictor')
    model = load_model("C:/Users/User/Downloads/Stock Prediction Model.keras")
    stock = st.text_input('Enter Stock Symbol', 'GOOG')
    start = '2012-01-01'
    TODAY = date.today()

    try:
        data = yf.download(stock, start, TODAY)
        if data.empty:
            st.error(f"No data found for the stock symbol: {stock}. Please try a different symbol.")
            return
    except Exception as e:
        st.error(f"An error occurred: {e}. Please try a different stock symbol.")
        return

    data_train = pd.DataFrame(data.Close[0: int(len(data)*0.80)])
    data_test = pd.DataFrame(data.Close[int(len(data)*0.80): len(data)])
    scaler = MinMaxScaler(feature_range=(0, 1))
    past_100_days = data_train.tail(100)
    data_test = pd.concat([past_100_days, data_test], ignore_index=True)
    data_test_scale = scaler.fit_transform(data_test)

    # Price vs MA50
    st.subheader('Price vs MA50')
    fig1, ax1 = plt.subplots(figsize=(10, 8))
    ax1.plot(data.Close, 'g', label='Actual Price')
    ax1.plot(data.Close.rolling(50).mean(), 'r', label='MA 50 Days')
    ax1.set_title(f'Stock Prices and 50-Day Moving Average of {stock}')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax1.legend()
    st.pyplot(fig1)

    # Price vs MA50 vs MA100
    st.subheader('Price vs MA50 vs MA100')
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    ax2.plot(data.Close, 'g', label='Actual Price')
    ax2.plot(data.Close.rolling(50).mean(), 'r', label='MA 50 Days')
    ax2.plot(data.Close.rolling(100).mean(), 'b', label='MA 100 Days')
    ax2.set_title(f'Stock Prices, 50-Day and 100-Day Moving Averages of {stock}')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Price')
    ax2.legend()
    st.pyplot(fig2)

    # Price vs MA100 vs MA200
    st.subheader('Price vs MA100 vs MA200')
    fig3, ax3 = plt.subplots(figsize=(10, 8))
    ax3.plot(data.Close, 'g', label='Actual Price')
    ax3.plot(data.Close.rolling(100).mean(), 'r', label='MA 100 Days')
    ax3.plot(data.Close.rolling(200).mean(), 'b', label='MA 200 Days')
    ax3.set_title(f'Stock Prices, 100-Day and 200-Day Moving Averages of {stock}')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Price')
    ax3.legend()
    st.pyplot(fig3)

    # Prepare and predict
    x, y = [], []
    for i in range(100, data_test_scale.shape[0]):
        x.append(data_test_scale[i-100:i])
        y.append(data_test_scale[i, 0])
    x, y = np.array(x), np.array(y)
    predict = model.predict(x)
    scale = 1 / scaler.scale_
    predict = predict * scale
    y = y * scale

    # Original Price vs Predicted Price
    st.subheader('Original Price vs Predicted Price')
    fig4, ax4 = plt.subplots(figsize=(10, 8))
    ax4.plot(predict, 'r', label='Original Price')
    ax4.plot(y, 'g', label='Predicted Price')
    ax4.set_title(f'Last 100 days data of actual and prediction chart for {stock}')
    ax4.set_xlabel('Time')
    ax4.set_ylabel('Price')
    ax4.legend()
    st.pyplot(fig4)

    # Calculate and display errors
    mae = mean_absolute_error(y, predict.flatten())
    rmse = mean_squared_error(y, predict.flatten(), squared=False)
    st.subheader('Accuracy of Predictions')
    st.write(f"Mean Absolute Error (MAE): {mae:.2f}")
    st.write(f"Root Mean Squared Error (RMSE): {rmse:.2f}")

    # Future Price Predictions
    last_date = data.index[-1]
    last_100_days_scaled = data_test_scale[-100:]
    future_predictions = predict_future_prices(data_test_scale, model, last_100_days_scaled, last_date, 30, scaler)
    st.subheader('Future Price Predictions for Next Month')
    st.write(future_predictions.set_index('Date'))
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    ax5.plot(future_predictions['Date'], future_predictions['Predicted Price'], color='blue')
    ax5.set_title('Future Stock Price Predictions')
    ax5.set_xlabel('Date')
    ax5.set_ylabel('Predicted Price')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig5)

if __name__ == '__main__':
    app()
