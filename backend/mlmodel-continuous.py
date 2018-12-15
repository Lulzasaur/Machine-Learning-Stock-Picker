from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
import keras
from keras.layers import LSTM
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, CuDNNLSTM, BatchNormalization
from keras import optimizers
from keras.optimizers import Adam, RMSprop
from tensorflow.keras.callbacks import TensorBoard 
from tensorflow.keras.callbacks import ModelCheckpoint, ModelCheckpoint
from tensorflow.contrib.rnn import *
import tensorflow as tf
from collections import deque
import time
import random
import numpy as np
import pandas as pd
import keras.backend as K
import requests
from KEY import API_SECRET_KEY

ticker = 'SPY'
BASE_URL = f'https://www.alphavantage.co/query'
SEQ_LEN=30 #number of days for a sequence to produce a 'buy' or 'sell'
SHIFT_FUTURE = 1
FUTURE_PERIOD_PREDICT = SEQ_LEN
EPOCHS=10
BATCH_SIZE=10
PCT=0.05

#function to create the labels for the data.
def percent_change_classify(current, future):
    return (float(future)-float(current))/float(current)  # if the future price is higher than the current by 1%, that's a buy, or a 1

def preprocess_df(df):

    df = df.drop("future", 1)  # don't need this anymore.
    scaler = MinMaxScaler()

    sequential_data = []  # this is a list that will CONTAIN the sequences
    prev_days = deque(maxlen=SEQ_LEN)  # These will be our actual sequences. They are made with deque, which keeps the maximum length by popping out older values as new ones come in
    predictions = []
    prediction_pointer = 0

    for i in df.values:  # iterate over the values
        prev_days.append([n for n in i[:-1]])  # store all but the target
        predictions.append(i[-1])
        if len(prev_days) == SEQ_LEN:  # make sure we have SEQ_LEN sequences!
            sequential_data.append([scaler.fit_transform(np.array(prev_days)), predictions[prediction_pointer]])  # append those bad boys!
            prediction_pointer = prediction_pointer+1

    # random.shuffle(sequential_data)  # shuffle for good measure.

    #above code constructs a list of "sequential" data (of SEQ_LEN long). the list will be fed
    #into the ML model

    X = []
    y = []

    for seq, target in sequential_data:  # going over our new sequential data
        X.append(seq)  # X is the sequences
        y.append(target)  # y is the targets/labels (buys vs sell/notbuy)

    return np.array(X), y  # return X and y...and make X a numpy array!

#send response to server
resp = requests.get(f'{BASE_URL}',
        params={
            "function":"TIME_SERIES_DAILY",
            "symbol":f'{ticker}',
            "outputsize":'full',
            "apikey":API_SECRET_KEY
        })

respData = resp.json()

#convert to dataframe
df = pd.DataFrame(data=respData['Time Series (Daily)'],dtype='float') #pct_change function only takes float data. changing type to float.

df = df.T #transpose the data so each row is a date.

df.rename(columns={'1. open':'open','2. high':'high','3. low':'low','4. close':'close','5. volume':'volume'},inplace=True)

df.index.names=['date']#set date as index.

df['future'] = df['close'].shift(SHIFT_FUTURE)
df['target'] = list(map(percent_change_classify, df['close'], df['future']))

prediction_df = df[0:FUTURE_PERIOD_PREDICT]

df.dropna(inplace=True)

times = sorted(df.index.values)
last_pct = sorted(df.index.values)[-int(PCT*len(times))]

validation_main_df = df[(df.index >= last_pct)]
main_df = df[(df.index < last_pct)]

train_x, train_y = preprocess_df(main_df)
validation_x, validation_y = preprocess_df(validation_main_df)
prediction_x, prediction_y = preprocess_df(prediction_df)

historic_prediction_x, historic_prediction_y = preprocess_df(df)

print('DFs *********************')
print('historic_prediction_x',historic_prediction_x)
print('historic_prediction_y',historic_prediction_y[0:10])
print('DFs *********************')

#model *************************

model = Sequential()

model.add(LSTM(128, input_shape=(train_x.shape[1:]), return_sequences=True))
model.add(Dropout(0.2))
model.add(BatchNormalization())

model.add(LSTM(128, return_sequences=True))
model.add(Dropout(0.1))
model.add(BatchNormalization())

model.add(LSTM(128))
model.add(Dropout(0.2))
model.add(BatchNormalization())

model.add(Dense(32))
model.add(Dropout(0.2))

model.add(Dense(1))

# Compile model

model.compile(optimizer=RMSprop(lr=0.005),loss='mean_squared_error')

# Train model
history = model.fit(
    train_x, train_y,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=(validation_x, validation_y)
    # callbacks=[tensorboard, checkpoint],
)

# print('history',history.history)

# Score model
score = model.evaluate(validation_x, validation_y, verbose=0)
print('Score: ',score)

# Make a prediction

predictions = model.predict(
    prediction_x,
    batch_size=BATCH_SIZE,
    verbose=1,
)

print('Current Prediction: ',predictions)

# probability = model.predict_proba(prediction_x)
historic_predictions = model.predict(historic_prediction_x)

print('Historic Predictions:',historic_predictions[0:10])