from flask import Flask, request, redirect, render_template, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from Model import MlModel

app = Flask(__name__)

BASE_URL = "https://api.iextrading.com/1.0"


@app.route("/silas/<ticker>")
def getStockPrediction():
    """Depending on ticker route will make a get request to API to get data on that stock,
    pass that data into the ML model and return prediction data in JSON format to front end
    """

    stock_data = requests.get(f"{BASE_URL}/stock/{ticker}/chart/5y")
    training_data = MlModel.clean_data(stock_data)
    prediction_data = MlModel.run_model(training_data)

    return prediction_data

