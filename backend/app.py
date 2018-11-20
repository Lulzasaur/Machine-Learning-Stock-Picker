from flask import Flask, request, redirect, render_template, jsonify, session
# from flask_debugtoolbar import DebugToolbarExtension
from Model import MlModel
import requests
from KEY import API_SECRET_KEY

app = Flask(__name__)

BASE_URL = f'https://www.alphavantage.co/query'


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
    training_data = MlModel.clean_data(stock_data['Time Series (Daily)'],'float')
    prediction_data = MlModel.run_model(training_data)

    return prediction_data

