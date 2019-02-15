#!/usr/bin/env python
# coding: utf-8

# In[65]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import acf, pacf, adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.statespace.sarimax import SARIMAX

#Function to plot the acf and pacf plots
def acf_plot(column,lag, column_name):
    #print the acf coorelation score
    print(acf(column,nlags=lag)[-1])
    #creating subplots
    fig = plt.figure(figsize=(12, 8))
    #plotting the acf
    ax1 = fig.add_subplot(211)
    fig = plot_acf(column, lags=lag, ax=ax1)
    #plotting the pacf
    ax2 = fig.add_subplot(212)
    fig = plot_pacf(column, lags=lag, ax=ax2)
    #adding title for both plots
    fig.suptitle(f'{column_name} Lag {lag}', fontsize=16)
    plt.show()

#code inspired by from 7.03 Advanced Timeseries Matt Brems
def sarimax_plot(train_df, test_df, train_column, test_column,
                start, end, p, d, q, S, P=0, D=0, Q=0):
    #creating the model
    sarima = SARIMAX(endog = train_column,
                     order = (p,d,q),
                     seasonal_order=(P,D,Q,S),
                     enforce_stationarity=False,
                     enforce_invertibility=False)

    # Fit SARIMA model.
    model = sarima.fit()

    # Generate predictions based on test set.

    preds = model.predict(start=start,end=end)

    # Evaluate predictions.
    mae = mean_absolute_error(test_column, preds)

    # Plot data.
    plt.figure(figsize=(10,6))
    plt.plot(train_df.index, train_column, color = 'blue')
    plt.plot(test_df.index, test_column, color = 'orange')
    plt.plot(test_df.index, preds, color = 'green')
    plt.title(label = f'Dissolved Oxygen with SARIMA({p}, {d}, {q}) x ({P}, {D}, {Q}, {S}) Predictions', fontsize=16)
    plt.legend(labels = ('Train', 'Test', 'Predicted'))
    plt.show();
    #creating a parameter dictionary to be used for evaluating model
    parameters = {'mae': mae, 'p': p, 'd': d, 'q': q, 'P': P,
                    'D': D, 'Q': Q, 'S': S}


    return parameters


#creating a sarima formula that doesnt produce a plot for each model to be used for evaluations.
def sarimax_eval(train_df, test_df, train_column, test_column,
                start, end, p, d, q, S, P=0, D=0, Q=0):
    sarima = SARIMAX(endog = train_column,
                     order = (p,d,q),              # (p, d, q)
                     seasonal_order=(P,D,Q,S),
                     enforce_stationarity=False,
                     enforce_invertibility=False)# (P, D, Q, S))

    # Fit SARIMA model.
    model = sarima.fit()

    # Generate predictions based on test set.
    preds = model.predict(start=start,end=end)

    # Evaluate predictions.
    mae = mean_absolute_error(test_column, preds)
    #creating a parameter dictionary to be used for evaluating model
    parameters = {'mae': mae, 'p': p, 'd': d, 'q': q, 'P': P,
                    'D': D, 'Q': Q, 'S': S}

    return parameters
