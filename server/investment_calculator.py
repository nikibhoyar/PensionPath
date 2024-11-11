import yfinance as yf
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense
import joblib

# Directory for saving models
MODEL_DIR = "saved_models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Nested list of tickers grouped by category
INVESTMENT_TICKERS = [
    # Stocks
    ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "KOTAKBANK.NS",
     "LT.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "HINDUNILVR.NS", "ASIANPAINT.NS",
     "AXISBANK.NS", "BAJFINANCE.NS", "MARUTI.NS", "M&M.NS", "SUNPHARMA.NS", "HCLTECH.NS",
     "ONGC.NS", "TITAN.NS", "ULTRACEMCO.NS", "WIPRO.NS", "ADANIGREEN.NS", "DMART.NS"],
    # Mutual Funds
    ["0P0000YENW.BO", "0P0000ZG0G.BO", "0P0000YIV3.BO"],
    # Gold ETFs
    ["GLD"],
    # Bonds
    ["TLT", "IEF", "BND", "AGG", "LQD", "HYG", "TIP", "SHY", "MUB", "BIV"],
    # Indices
    ["^GSPC", "^DJI", "^IXIC", "^RUT", "^FTSE", "^N225", "^HSI", "^GDAXI", "^FCHI", "^STOXX50E"]
]

# Function to fetch and train stock data
def fetch_stock_data(tickers):
    stock_data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5y")  # Last 5 years of data
        if not hist.empty:
            model_path = os.path.join(MODEL_DIR, f"{ticker}_lstm.pkl")
            scaler_path = os.path.join(MODEL_DIR, f"{ticker}_scaler.pkl")

            if os.path.exists(model_path) and os.path.exists(scaler_path):
                model = joblib.load(model_path)
                scaler = joblib.load(scaler_path)
                
            else:
                data = hist[['Close']].values
                scaler = MinMaxScaler(feature_range=(0,1))
                data_scaled = scaler.fit_transform(data)
                X_train = []
                y_train = []
                for i in range(60, len(data_scaled)):
                    X_train.append(data_scaled[i-60:i, 0])
                    y_train.append(data_scaled[i, 0])
                X_train, y_train = np.array(X_train), np.array(y_train)
                X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
                
                model = Sequential()
                model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
                model.add(LSTM(units=50))
                model.add(Dense(1))

                model.compile(optimizer='adam', loss='mean_squared_error')
                model.fit(X_train, y_train, epochs=1, batch_size=32)

                # Save the model and scaler
                joblib.dump(model, model_path)
                joblib.dump(scaler, scaler_path)

            # Predict future prices
            data = scaler.transform(hist[['Close']])
            X_test = []
            for i in range(60, len(data)):
                X_test.append(data[i-60:i, 0])
            X_test = np.array(X_test)
            X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
            predicted_stock_price = model.predict(X_test)
            predicted_stock_price = scaler.inverse_transform(predicted_stock_price)
            hist['Predicted'] = np.nan
            hist.iloc[60:, hist.columns.get_loc('Predicted')] = predicted_stock_price.flatten()   

            # Calculate annual return and volatility based on predicted prices
            annual_return = hist['Predicted'].pct_change().mean() * 252 * 100
            volatility = hist['Predicted'].pct_change().std() * np.sqrt(252) * 100
            beta = stock.info.get('beta', 1)
            sharpe_ratio = annual_return / volatility
            print(volatility,ticker)
            risk_profile = 'Low' if volatility < 5 else 'Medium' if volatility < 7 else 'High'

            stock_data.append({
                'ticker': ticker,
                'annual_return': annual_return,
                'volatility': volatility,
                'beta': beta,
                'sharpe_ratio': sharpe_ratio,
                'risk_profile': risk_profile
            })
    return pd.DataFrame(stock_data)

# Calculate investment strategy
def calculate_investment_strategy(retirement_age, current_age, desired_fund, monthly_investment, risk_category):
    years_to_invest = retirement_age - current_age
    n_months = years_to_invest * 12

    # Step 1: Calculate the required annual return
   
    def required_return_rate(target_value, payment, periods):
        low, high = 0, 1  # Initial bounds (0% to 100% annual return)
        tolerance = 1e-6
        while high - low > tolerance:
            guess_rate = (high + low) / 2
            monthly_rate = guess_rate / 12
            future_value_guess = payment * (((1 + monthly_rate) ** periods - 1) / monthly_rate)
            if future_value_guess < target_value:
                low = guess_rate
            else:
                high = guess_rate
        return guess_rate * 100  # Convert to annual percentage

    required_return = required_return_rate(desired_fund, monthly_investment, n_months)
    

    stock_data = []

    # Step 2: Fetch stocks and filter based on user’s risk category
    for ticker_group in INVESTMENT_TICKERS:
        data = fetch_stock_data(ticker_group)
        stock_data.append(data)
        
    df = pd.concat(stock_data, ignore_index=True)

    if risk_category == 1:  # High Risk
        df = df[(df['annual_return'] > 20) & (df['volatility'] > 7)]
    elif risk_category == 2:  # Medium Risk
        df = df[(df['annual_return'] > 10) & (df['annual_return'] <= 20) & (df['volatility'] <= 7) & (df['volatility'] >= 5)]
    elif risk_category == 3:  # Low Risk
        df = df[df['volatility'] < 5]

    # Step 3: Filter stocks with annual return less than required return
    df = df[df['annual_return'] >= required_return]
    
    if df.empty:
        return "No stocks available in the selected risk category and return requirement."

    # Sort by priority score (Sharpe ratio / volatility) for better allocations
    df['priority_score'] = df['sharpe_ratio'] / df['volatility']
    df = df.sort_values(by='priority_score', ascending=False)

    # Select top stocks
    selected_stocks = df.head(5).to_dict('records')

    # Step 4: Perform allocation based on Sharpe ratio of shortlisted stocks
    total_weight = sum(stock['sharpe_ratio'] for stock in selected_stocks)
    allocations = []
    total_future_value = 0

    for stock in selected_stocks:
        weight = (stock['sharpe_ratio'] / total_weight) if total_weight > 0 else 1 / len(selected_stocks)
        monthly_allocation = monthly_investment * weight

        # Calculate the projected future value for each stock
        annual_return_rate = stock['annual_return'] / 100
        monthly_return_rate = (1 + annual_return_rate) ** (1/12) - 1
        future_value_stock = monthly_allocation * ((1 + monthly_return_rate) ** n_months - 1) / monthly_return_rate

        total_future_value += future_value_stock

        allocations.append({
            'ticker': stock['ticker'],
            'percentage': weight * 100,
            'monthly_amount': monthly_allocation,
            'expected_return': stock['annual_return'],
            'risk_level': stock['risk_profile'],
            'projected_value': future_value_stock
        })

    # Calculate the total investment and total return
    total_invested = monthly_investment * n_months
    total_return_percentage = ((total_future_value - total_invested) / total_invested) * 100



    return {
        'required_annual_return': abs(required_return),
        'total_investment_needed': total_invested,
        'expected_future_value': total_future_value,
        'allocations': allocations,
        'years_to_invest': years_to_invest
    }
   
