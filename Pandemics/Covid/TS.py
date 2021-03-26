import pandas as pd
import numpy as np
import datetime
from statsmodels.tsa.arima.model import ARIMA
from django.db import connection


def prediction_model_counries(entry):
    with connection.cursor() as cursor:
        cursor.execute(entry)
        data = cursor.fetchall()
    date = []
    value = []
    length = len(data)
    today_val = data[len(data)-1][1]
    today_date = data[len(data)-1][0]
    for i in range(length):
        date.append(data[i][0])
        value.append(data[i][1])
    date.remove(today_date)
    value.remove(today_val)
    entry_data = {'Date': date, 'For Prediction': value}

    df = pd.DataFrame(entry_data)

    df['Date'] = pd.DatetimeIndex(df['Date'])

    df['For Prediction'] = pd.to_numeric(df['For Prediction'])
    df.set_index('Date', inplace=True)
    after_drop = df[(df != 0).all(1)]    # this will drop all rows having zeros but have to specify column i.e 1

    cases = after_drop['For Prediction']

    cases.reset_index()

    class Prediction:

        def __init__(self, cases, today_val, order):
            self.cases = cases
            self.today_val = today_val
            self.order = order

        def arima_model(self, time_series, step=5):
            for i in range(step):
                model = ARIMA(time_series.astype(float), order=self.order)  # error occured here pandas data has been cast to numpy dtype obj so chnage it to float as values will be string, so once we convert all values to float then we can append
                model_fit = model.fit()
                forecast = model_fit.forecast()
                input_data = np.asarray(str(forecast)[7:14])
                time_series.loc[time_series.last_valid_index() + datetime.timedelta(days=1)] = input_data
                time_series.sort_index()
            return time_series

        def fitted_vals_arima(self):
            model_ARIMA = ARIMA(self.cases.astype(float),
                                order=self.order)
            ARIMA_fit = model_ARIMA.fit()
            fitted_cases = ARIMA_fit.fittedvalues

            latest_date = self.cases.last_valid_index() + datetime.timedelta(days=1)

            actual_cases = self.arima_model(self.cases, step=6)

            fitted_values_cases = self.arima_model(fitted_cases, step=6)

            actual_cases_float = float(actual_cases.loc[latest_date])
            pred_cases_float = float(fitted_values_cases.loc[latest_date])
            self.today_val = float(self.today_val)

            print("today_val : " + str(self.today_val) + "prediction :" + str(pred_cases_float))
            try:
                error = float(abs((self.today_val - pred_cases_float) * 100) / self.today_val)
                error_pred = abs(error - 100)
            except ZeroDivisionError:
                error_pred = 0

            print("today_val : " + str(self.today_val) + "actual :" + str(actual_cases_float))
            try:
                error = float(abs((self.today_val - actual_cases_float) * 100) / self.today_val)
                error_actual = abs(error - 100)
            except ZeroDivisionError:
                error_actual = 0

            if error_actual > error_pred:
                return error_actual, actual_cases.loc[latest_date:]
            else:
                return error_pred, fitted_values_cases.loc[latest_date:]

    obj = Prediction(cases, today_val, (1, 1, 1))
    today_pred1, future_five1 = obj.fitted_vals_arima()

    print(data[length-1])
    print(today_val)

    return today_pred1, future_five1


def prediction_model_states(entry, today_val, today_date):
    date = []
    value = []
    for i in entry:
        date.append(i['date'])
        value.append(i['total_cases'])
    entry_data = {'Date': date, 'For Prediction': value}

    df = pd.DataFrame(entry_data)
    df.to_csv("test.csv")

    df['Date'] = pd.DatetimeIndex(df['Date'])
    print("fhfghf", df.head())
    df['For Prediction'] = pd.to_numeric(df['For Prediction'])
    df.set_index('Date', inplace=True)

    cases = df['For Prediction']

    class Prediction:

        def __init__(self, cases, today_val, order):
            self.cases = cases
            self.today_val = today_val
            self.order = order

        def arima_model(self, time_series, step=5):
            for i in range(step):
                model = ARIMA(time_series.astype(float),
                              order=self.order)
                model_fit = model.fit()
                forecast = model_fit.forecast()
                input_data = np.asarray(str(forecast)[7:14])
                time_series.loc[time_series.last_valid_index() + datetime.timedelta(days=1)] = input_data
                time_series.sort_index()
            return time_series

        def fitted_vals_arima(self):
            # ARIMA model
            model_ARIMA = ARIMA(self.cases.astype(float),
                                order=self.order)
            ARIMA_fit = model_ARIMA.fit()
            fitted_cases = ARIMA_fit.fittedvalues

            latest_date = self.cases.last_valid_index() + datetime.timedelta(days=1)

            actual_cases = self.arima_model(self.cases, step=6)

            fitted_values_cases = self.arima_model(fitted_cases, step=6)

            actual_cases_float = float(actual_cases.loc[latest_date])
            pred_cases_float = float(fitted_values_cases.loc[latest_date])
            self.today_val = float(self.today_val)

            print("today_val : " + str(self.today_val) + "prediction :" + str(pred_cases_float))
            try:
                error = float(abs((self.today_val - pred_cases_float) * 100) / self.today_val)
                error_pred = abs(error - 100)
            except ZeroDivisionError:
                error_pred = 0

            print("today_val : " + str(self.today_val) + "actual :" + str(actual_cases_float))
            try:
                error = float(abs((self.today_val - actual_cases_float) * 100) / self.today_val)
                error_actual = abs(error - 100)
            except ZeroDivisionError:
                error_actual = 0

            if error_actual > error_pred:
                return error_actual, actual_cases.tail(6)
            else:
                return error_pred, fitted_values_cases.tail(6)

    obj = Prediction(cases, today_val, (1, 1, 1))
    today_pred1, future_five1 = obj.fitted_vals_arima()

    return today_pred1, future_five1
