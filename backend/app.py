from flask import Flask, request, redirect, render_template, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from Model import MlModel
import requests
from KEY import API_SECRET_KEY

app = Flask(__name__)

BASE_URL = f'https://www.alphavantage.co/query'

def serialize_model_data(historic_pred, historic_dates):
    """Function that takes data from model and serializes it so that flask can convert
    it to JSON"""
    response_array = []
    for p, d in zip(historic_pred, historic_dates):
        data_object = {
        '0': int(p[0]*100),
        '1': int(p[1]*100),
        'date': d
        }
        response_array.append(data_object)
    
    return response_array

def serialize_dataframe(df):
     """Function that takes dataframe and serializes it so that flask can convert
    it to JSON"""
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
            'target': values[6]
        }
        response_array.append(data_object)
    
    return response_array

@app.route("/silas/<ticker>")
def getStockPrediction(ticker):
    """Depending on ticker route will make a get request to API to get data on that stock,
    pass that data into the ML model and return prediction data in JSON format to front end
    """
    api_resp = requests.get(f'{BASE_URL}',
        params={
            "function":"TIME_SERIES_DAILY",
            "symbol":f'{ticker}',
            "outputsize":'full',
            "apikey":API_SECRET_KEY
        })
    
    stock_data = api_resp.json()
    data = MlModel.clean_data(stock_data['Time Series (Daily)'],'float')
    historic_predictions = MlModel.run_model(data)

    #response will be an array of objects where each object has a key of 0, 1 and date
    #0 and 1 have probability values
    response = serialize(historic_predictions['historic_predictions'],historic_predictions['historic_prediction_dates'])

    return jsonify(response)


@app.route("/silas/<ticker>/historics")
def getHistoricPrices(ticker):
    """Route will return an array of object with historic data for specific ticker.
    Object will contain close, future, high, low, open, target and volume data"""
    
    api_resp = requests.get(f'{BASE_URL}',
    params={
        "function":"TIME_SERIES_DAILY",
        "symbol":f'{ticker}',
        "outputsize":'full',
        "apikey":API_SECRET_KEY
    })

    stock_data = api_resp.json()
    data = MlModel.clean_data(stock_data['Time Series (Daily)'],'float')
    dataframe = data['dataframe']
    response = serialize_dataframe(dataframe)

    return jsonify(response)