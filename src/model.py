'''Module Containing House price prediction models'''


import pandas as pd
import numpy as np
from sklearn import linear_model


def compute_regression(province:str='E06000001', h_type:str='all'):
    '''
    Compute house price based on area and regression model on previous data
    Valid h_types (house types):
    all, detached, flats, semi-detached, tarraced
    Province corresponds to UK local authority code

    To do: Implement datasheet for uk local authority and region codes
    '''
    df = pd.read_parquet('data/clean/'+h_type+'.parquet')
    data = parse_data(df)
    reg = linear_model.LinearRegression()
    index = np.array([[i] for i in range(len(data))])
    reg.fit(index, data)

def parse_data(df:pd.DataFrame):
    '''Parses String format of dataframe into format readable for model'''
    data = df.loc[0, 'Dec|1995':'Mar|2023']
    data = data.to_numpy()
    return data

compute_regression()
