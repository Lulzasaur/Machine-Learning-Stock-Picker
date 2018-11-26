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
from helpers import classify, preprocess_df, prediction_preprocess_df, historic_preprocess_df
from KEY import API_SECRET_KEY


SEQ_LEN=15 #number of days for a sequence to predice a 'buy' or 'sell'
FUTURE_PERIOD_PREDICT = SEQ_LEN + 1
EPOCHS=1
BATCH_SIZE=10
PCT=0.1

class MlModel:

    @staticmethod
    def clean_data(dataSet, typeData):
        
        #convert to dataframe
        df = pd.DataFrame(data=dataSet,dtype=typeData) #pct_change function only takes float data. changing type to float.

        df = df.T #transpose the data so each row is a date.

        df.rename(columns={'1. open':'open','2. high':'high','3. low':'low','4. close':'close','5. volume':'volume'},inplace=True)

        df.index.names=['date']#set date as index.

        df['future'] = df['close'].shift(FUTURE_PERIOD_PREDICT)
        df['target'] = list(map(classify, df['close'], df['future']))

        prediction_df = df[0:FUTURE_PERIOD_PREDICT]

        df.dropna(inplace=True)

        times = sorted(df.index.values)
        last_pct = sorted(df.index.values)[-int(PCT*len(times))]

        validation_main_df = df[(df.index >= last_pct)]
        main_df = df[(df.index < last_pct)]

        train_x, train_y = preprocess_df(main_df)
        validation_x, validation_y = preprocess_df(validation_main_df)
        prediction_x, prediction_y = prediction_preprocess_df(prediction_df)
        historic_prediction_x, historic_prediction_dates = historic_preprocess_df(df)

        return {
            "dataframe": df,
            "train_x": train_x,
            "train_y": train_y,
            "validation_x": validation_x,
            "validation_y": validation_y,
            "validation_main_df": validation_main_df,
            "main_df": main_df,
            "prediction_x": prediction_x,
            "prediction_y": prediction_y,
            "historic_prediction_x": historic_prediction_x,
            "historic_prediction_dates": historic_prediction_dates
        }

    @staticmethod
    def run_model(dataObject):

        model = Sequential()

        model.add(LSTM(128, input_shape=(dataObject['train_x'].shape[1:]), return_sequences=True))
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
            dataObject['train_x'], dataObject['train_y'],
            batch_size=BATCH_SIZE,
            epochs=EPOCHS,
            validation_data=(dataObject['validation_x'], dataObject['validation_y'])
            # callbacks=[tensorboard, checkpoint],
        )

        # Score model
        score = model.evaluate(dataObject['validation_x'], dataObject['validation_y'], verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])

        # Make a prediction

        predictions = model.predict(
            dataObject['prediction_x'],
            batch_size=BATCH_SIZE,
            verbose=1,
            # max_queue_size=10,
            # workers=1,
            # use_multiprocessing=True
        )

        probability = model.predict_proba(dataObject['prediction_x'])
        historic_predictions = model.predict(dataObject['historic_prediction_x'])

        return {
            'historic_predictions': historic_predictions, 
            'historic_prediction_dates': dataObject['historic_prediction_dates']
        }
