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
from KEY import API_SECRET_KEY

SEQ_LEN=10 #number of days for a sequence to predice a 'buy' or 'sell'
FUTURE_PERIOD_PREDICT = SEQ_LEN + 1
EPOCHS=1
BATCH_SIZE=10
PCT=0.1


def classify(current, future):
    if float(future) > float(current)*1.01:  # if the future price is higher than the current by 1%, that's a buy, or a 1
        return 1
    else:  # otherwise... it's a 0!
        return 0



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
        if len(prev_days) == SEQ_LEN:  # make sure we have SEQ_LEN sequences!
            sequential_data.append([np.array(prev_days), i[-1]])  # append those bad boys!

    random.shuffle(sequential_data)  # shuffle for good measure.

    #above code constructs a list of "sequential" data (of SEQ_LEN long). the list will be fed
    #into the ML model

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


def prediction_preprocess_df(df):
    df = df.drop("future", 1)  # don't need this anymore.

    for col in df.columns:  # go through all of the columns
        if col != "target":  # normalize all ... except for the target itself!
            df[col] = df[col].pct_change()  # pct change "normalizes" the different prices
            # df.dropna(inplace=True)  # remove the nas created by pct_change
            df[col] = preprocessing.scale(df[col].values)  # scale between 0 and 1.

    df.dropna(inplace=True)  # cleanup again... jic.

    sequential_data = []  # this is a list that will CONTAIN the sequences
    prev_days = deque(maxlen=FUTURE_PERIOD_PREDICT-1)  # These will be our actual sequences. They are made with deque, which keeps the maximum length by popping out older values as new ones come in

    for i in df.values:  # iterate over the values
        prev_days.append([n for n in i[:-1]])  # store all but the target
        if len(prev_days) == FUTURE_PERIOD_PREDICT-1:  # make sure we have SEQ_LEN sequences!
            sequential_data.append([np.array(prev_days), i[-1]])  # append those bad boys!

    X = []
    y = []

    for seq, target in sequential_data:  # going over our new sequential data
        X.append(seq)  # X is the sequences
        y.append(target)  # y is the targets/labels (buys vs sell/notbuy)

    return np.array(X), y  # return X and y...and make X a numpy array!

def historic_preprocess_df(df):

    df = df.drop("future", 1)  # don't need this anymore.

    for col in df.columns:  # go through all of the columns
        if col != "target":  # normalize all ... except for the target itself!
            df[col] = df[col].pct_change()  # pct change "normalizes" the different prices
            # df.dropna(inplace=True)  # remove the nas created by pct_change
            df[col] = preprocessing.scale(df[col].values)  # scale between 0 and 1.

    df.dropna(inplace=True)  # cleanup again... jic.

    sequential_data = []  # this is a list that will CONTAIN the sequences
    prev_days = deque(maxlen=FUTURE_PERIOD_PREDICT-1)  # These will be our actual sequences. They are made with deque, which keeps the maximum length by popping out older values as new ones come in

    index_values = df.index.values

    df['dates'] = index_values

    df.drop('target',axis=1,inplace=True)

    for i in df.values:  # iterate over the values
        prev_days.append([n for n in i[:-1]])  # store all but the target
        if len(prev_days) == FUTURE_PERIOD_PREDICT-1:  # make sure we have SEQ_LEN sequences!
            sequential_data.append([ np.array(prev_days), i[-1]])  # append those bad boys!

    print(len(sequential_data))
    X = [] #list of all the values being processed by the ML - what the ML uses to make a prediction
    y = [] #list of all the dates

    for seq, dates in sequential_data:  # going over our new sequential data
        # z.append(index)
        X.append(seq)  # X is the sequences
        y.append(dates)  # y is the targets/labels (buys vs sell/notbuy)

    return np.array(X), y  # return X and y...and make X a numpy array!

