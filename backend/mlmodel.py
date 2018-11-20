from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import keras
from keras.layers import LSTM
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, CuDNNLSTM, BatchNormalization
from keras import optimizers
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

BASE_URL = 'https://api.iextrading.com/1.0'
ticker = 'AAPL'
FUTURE_PERIOD_PREDICT = 5
SEQ_LEN=10
EPOCHS=5
BATCH_SIZE=20

#1##########################################################
#function to create the labels for the data.
def classify(current, future):
    if float(future) > float(current)*1.01:  # if the future price is higher than the current by 1%, that's a buy, or a 1
        return 1
    else:  # otherwise... it's a 0!
        return 0

#2#########################################################
def preprocess_df(df):
    df = df.drop("future", 1)  # don't need this anymore.

    for col in df.columns:  # go through all of the columns
        if col != "target":  # normalize all ... except for the target itself!
            df[col] = df[col].pct_change()  # pct change "normalizes" the different prices
            df.dropna(inplace=True)  # remove the nas created by pct_change
            df[col] = preprocessing.scale(df[col].values)  # scale between 0 and 1.

    df.dropna(inplace=True)  # cleanup again... jic.


    sequential_data = []  # this is a list that will CONTAIN the sequences
    prev_days = deque(maxlen=SEQ_LEN)  # These will be our actual sequences. They are made with deque, which keeps the maximum length by popping out older values as new ones come in

    for i in df.values:  # iterate over the values
        prev_days.append([n for n in i[:-1]])  # store all but the target
        if len(prev_days) == SEQ_LEN:  # make sure we have 60 sequences!
            sequential_data.append([np.array(prev_days), i[-1]])  # append those bad boys!

    random.shuffle(sequential_data)  # shuffle for good measure.

    buys = []  # list that will store our buy sequences and targets
    sells = []  # list that will store our sell sequences and targets

    for seq, target in sequential_data:  # iterate over the sequential data
        if target == 0:  # if it's a "not buy"
            sells.append([seq, target])  # append to sells list
        elif target == 1:  # otherwise if the target is a 1...
            buys.append([seq, target])  # it's a buy!

    random.shuffle(buys)  # shuffle the buys
    random.shuffle(sells)  # shuffle the sells!

    lower = min(len(buys), len(sells))  # what's the shorter length?

    buys = buys[:lower]  # make sure both lists are only up to the shortest length.
    sells = sells[:lower]  # make sure both lists are only up to the shortest length.

    sequential_data = buys+sells  # add them together
    random.shuffle(sequential_data)  # another shuffle, so the model doesn't get confused with all 1 class then the other.

    X = []
    y = []

    for seq, target in sequential_data:  # going over our new sequential data
        X.append(seq)  # X is the sequences
        y.append(target)  # y is the targets/labels (buys vs sell/notbuy)

    return np.array(X), y  # return X and y...and make X a numpy array!

#3##############################################################################
#send response to server
resp = requests.get(f'{BASE_URL}/stock/{ticker}/chart/5y')

#convert to dataframe
df = pd.DataFrame(data=resp.json())

#set date as index.
df.set_index('date',inplace=True)

df = df[['volume','high','low','vwap','close']]

df['future'] = df['close'].shift(-FUTURE_PERIOD_PREDICT)
df['target'] = list(map(classify, df['close'], df['future']))

df.dropna(inplace=True)

times = sorted(df.index.values)
last_5pct = sorted(df.index.values)[-int(0.05*len(times))]

validation_main_df = df[(df.index >= last_5pct)]
main_df = df[(df.index < last_5pct)]

train_x, train_y = preprocess_df(main_df)
validation_x, validation_y = preprocess_df(validation_main_df)

#4.######################################################################################

print(f"train data: {len(train_x)} validation: {len(validation_x)}")
print(f"Dont buys: {train_y.count(0)}, buys: {train_y.count(1)}")
print(f"VALIDATION Dont buys: {validation_y.count(0)}, buys: {validation_y.count(1)}")

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

model.add(Dense(32, activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(2, activation='softmax'))


opt = keras.optimizers.Adam(lr=0.001, decay=1e-6)

# Compile model
model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer=opt,
    metrics=['accuracy']
)


# Train model
history = model.fit(
    train_x, train_y,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=(validation_x, validation_y)
    # callbacks=[tensorboard, checkpoint],
)

print(history)

# Score model
score = model.evaluate(validation_x, validation_y, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
print('Score:', score)