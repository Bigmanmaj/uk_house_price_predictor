'''Module Containing House price prediction models'''


import pandas as pd
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
    data = df.loc[0]
    print(data)
    reg = linear_model.LinearRegression()


compute_regression()