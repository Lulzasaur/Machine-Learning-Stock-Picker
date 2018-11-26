from flask import Flask, request, redirect, render_template, jsonify, session
# from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS
from Model import MlModel
import pandas as pd
import requests
from KEY import API_SECRET_KEY


app = Flask(__name__)
CORS(app)
BASE_URL = f"https://www.alphavantage.co/query"


def serialize_model_data(historic_pred, historic_dates):
    """Function that takes data from model and serializes it so that flask can convert
    it to JSON
    >>> serialize_model_data([[0.1, 0.9],[0.9, 0.1]],['2018-10-17','2018-10-16'])
    [{'0': 10, '1': 90, 'date': '2018-10-17'}, {'0': 90, '1': 10, 'date': '2018-10-16'}]
    """
    response_array = []
    for p, d in zip(historic_pred, historic_dates):
        data_object = {"0": int(p[0] * 100), "1": int(p[1] * 100), "date": d}
        response_array.append(data_object)

    return response_array


def serialize_dataframe(df):
    """Function that takes dataframe and serializes it so that flask can convert
    it to JSON
    >>> serialize_dataframe(pd.DataFrame({'open': 216.88, 'high': 220.45, 'low': '216.6200', 'close': 218.86, 'volume': 38358933.0, 'future': 172.29, 'target': 0}, index=[2001]))
    [{'open': 216.88, 'high': 220.45, 'low': '216.6200', 'close': 218.86, 'volume': 38358933.0, 'future': 172.29, 'target': 0, 'date': 2001}]
    """
    index_values = df.index.values
    df['dates'] = index_values
    df_values = df.values.tolist()
    response_array = []
    for values in df_values:
        data_object = {
            'open': values[0],
            'high': values[1],
            'low': values[2],
            'close': values[3],
            'volume': values[4],
            'future': values[5],
            'target': values[6],
            'date': values[7]
        }
        response_array.append(data_object)

    return response_array

def get_stock_data_api(stock_ticker):
    """Make a call to API to get historic data about specific stock"""
    
    resp = requests.get(
        f"{BASE_URL}",
        params={
            "function": "TIME_SERIES_DAILY",
            "symbol": f"{stock_ticker}",
            "outputsize": "full",
            "apikey": API_SECRET_KEY,
        },
    )

    return resp.json()

@app.route("/silas/<ticker>")
def getStockPrediction(ticker):
    """Use helper function to get data for specific ticker from API and pass that data 
    into the ML model and return prediction data in JSON format to front end
    """

    stock_data = get_stock_data_api(ticker)
    data = MlModel.clean_data(stock_data["Time Series (Daily)"], "float")
    historic_predictions = MlModel.run_model(data)

    #response will be an array of objects where each object has a key of 0, 1 and date
    #0 and 1 have probability values associated with them
    response = serialize_model_data(historic_predictions['historic_predictions'],historic_predictions['historic_prediction_dates'])

    return jsonify(response)


@app.route("/silas/<ticker>/historics")
def getHistoricPrices(ticker):
    """Route will return an array of object with historic data for specific ticker.
    Object will contain close, future, high, low, open, target and volume data"""

    stock_data = get_stock_data_api(ticker)
    data = MlModel.clean_data(stock_data['Time Series (Daily)'],'float')
    dataframe = data['dataframe']
    response = serialize_dataframe(dataframe)

    return jsonify(response)
