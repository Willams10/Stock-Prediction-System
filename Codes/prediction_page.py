import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf
from keras.models import load_model
import streamlit as st
from datetime import date, timedelta

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
    model = load_model(r"C:\Users\User\Downloads\Stock Prediction Model.keras")
    st.header('Stock Market Predictor')

    stock=st.text_input('Enter Stock Symbol', 'GOOG')
    start = '2012-01-01'
    TODAY = date.today()
    
    
    try:
        data = yf.download(stock, start, TODAY)
        if data.empty:
            st.error(f"No data found for the stock symbol: {stock}. Please try a different symbol.")
            return  # Exit the function if no data is found
    except Exception as e:
        st.error(f"An error occurred: {e}. Please try a different stock symbol.")
        return  # Exit the function if an exception occurs
    st.subheader('Stock Data')
    st.write(data)

    data_train = pd.DataFrame(data.Close[0: int(len(data)*0.80)])
    data_test =  pd.DataFrame(data.Close[int(len(data)*0.80): len(data)])

    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0,1))

    pas_100_days = data_train.tail(100)
    data_test = pd.concat([pas_100_days, data_test], ignore_index=True)
    data_test_scale = scaler.fit_transform(data_test)

    tab1, tab2, tab3 = st.tabs(["Price vs MA50", "Price vs MA50 vs MA100", "Price vs MA100 vs MA200"])
    
    with tab1:
        st.subheader('Price vs MA50')
        ma_50_days =  data.Close.rolling(50).mean()
        fig1 = plt.figure(figsize=(10,8))
        plt.plot(data.Close, 'g', label='Actual Price')
        plt.plot(ma_50_days, 'r', label='MA 50 Days')
        plt.title(f'Stock Prices and 50-Day Moving Average of {stock}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        st.pyplot(fig1)
        
    with tab2:
        st.subheader('Price vs MA50 vs MA100')
        ma_100_days =  data.Close.rolling(100).mean()
        fig2 = plt.figure(figsize=(10,8))
        plt.plot(data.Close, 'g', label='Actual Price')
        plt.plot(ma_50_days, 'r', label='MA 50 Days')
        plt.plot(ma_100_days, 'b', label='MA 100 Days')
        plt.title(f'Stock Prices, 50-Day and 100-Day Moving Averages of {stock}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        st.pyplot(fig2)

    with tab3:
        st.subheader('Price vs MA100 vs MA200')
        ma_200_days =  data.Close.rolling(200).mean()
        fig3 = plt.figure(figsize=(10,8))
        plt.plot(data.Close, 'g', label='Actual Price')
        plt.plot(ma_100_days, 'r', label='MA 100 Days')
        plt.plot(ma_200_days, 'b', label='MA 200 Days')
        plt.title(f'Stock Prices, 100-Day and 200-Day Moving Averages of {stock}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        st.pyplot(fig3)

    x = []
    y = []

    for i in range(100, data_test_scale.shape[0]):
        x.append(data_test_scale[i-100:i])
        y.append(data_test_scale[i,0])

    x,y = np.array(x), np.array(y)

    predict =  model.predict(x)
    scale = 1/scaler.scale_

    predict = predict * scale
    y = y * scale

    st.subheader('Orginal Price vs Predicted Price')
    fig4 = plt.figure(figsize=(10,8))
    plt.title(f'Last 100 days data of actual and prediction chart for {stock}')
    plt.plot(predict, 'r', label = 'Original Price')
    plt.plot(y,'g', label='Predicted Price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
    st.pyplot(fig4)
    
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    # Calculate MAE
    mae = mean_absolute_error(y, predict.flatten())

    # Calculate RMSE
    rmse = mean_squared_error(y, predict.flatten(), squared=False)

    # Display the errors
    st.subheader('Accuracy of Predictions')
    st.write(f"Mean Absolute Error (MAE): {mae:.2f}")
    st.write(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    

    dates = data.index[int(len(data)*0.80):]
    dates = dates[:len(predict)]

    # Create a new DataFrame for comparison
    comparison_df = pd.DataFrame({'Date': dates, 'Actual Price': y.flatten(), 'Predicted Price': predict.flatten()})
    comparison_df.set_index('Date', inplace=True)

    # Display the DataFrame
    st.subheader('Comparison of Actual and Predicted Prices')
    st.write(comparison_df)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(comparison_df['Actual Price'], label='Actual Price', color='green')
    ax.plot(comparison_df['Predicted Price'], label='Predicted Price', color='red')

    # Formatting the plot
    ax.set_title('Stock Price Prediction')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    ax.xaxis.set_major_locator(mdates.MonthLocator())  # Set major ticks format
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)

    # Plotting Histograms
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

    # Histogram for Actual Prices
    axes[0].hist(comparison_df['Actual Price'], bins=50, color='green', alpha=0.7)
    axes[0].set_title('Histogram of Actual Prices')
    axes[0].set_xlabel('Price')
    axes[0].set_ylabel('Frequency')

    # Histogram for Predicted Prices
    axes[1].hist(comparison_df['Predicted Price'], bins=50, color='red', alpha=0.7)
    axes[1].set_title('Histogram of Predicted Prices')
    axes[1].set_xlabel('Price')
    axes[1].set_ylabel('Frequency')
    plt.tight_layout()
    st.pyplot(fig)
    
    
    past_100_days = data_train.tail(100)
    final_data_test = pd.concat([past_100_days, data_test], ignore_index=True)
    final_data_test_scaled = scaler.transform(final_data_test)
    
    
    # Predict the next 30 days (1 month)
    days_to_predict = 30
    last_date = data.index[-1]
    last_100_days_scaled = final_data_test_scaled[-100:]

    future_predictions = predict_future_prices(final_data_test_scaled, model, last_100_days_scaled, last_date, days_to_predict, scaler)

    # Display the future predictions
    st.subheader('Future Price Predictions for Next Month')
    st.write(future_predictions.set_index('Date'))

    # Plotting Future Predictions
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(future_predictions['Date'], future_predictions['Predicted Price'], color='blue')
    ax.set_title('Future Stock Price Predictions')
    ax.set_xlabel('Date')
    ax.set_ylabel('Predicted Price')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)


