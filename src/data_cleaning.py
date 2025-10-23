'''Cleans data for datasets provided'''
import pandas as pd


def clean_data():
    '''
    Clean median house price data from ONS and convert to a .parquet
    and .csv formats
    Dataset: https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity
    /housing/datasets/medianhousepricefornationalandsubnationalgeographiesquarterly
    rollingyearhpssadataset09/current/hpssadataset9medianpricepaidforadministrativegeographies.xls
    '''
    dataset_months = ['Dec', 'Mar', 'Jun', 'Sep']
    letters = [chr(i) for i in range(ord('a'), ord('e') + 1)]
    house_type = {'a': 'all', 'b': 'detached', 'c': 'semi-detached',
                  'd': 'terraced', 'e': 'flats'}
    for letter in letters:
        df = pd.read_excel('data/raw/raw_data.xls', sheet_name='2' +
                           letter, header=6)  # Read all datasheets up to 2e
        for i in range(1995, 2024):
            for month in dataset_months:
                col_name = 'Year ending ' + month + ' ' + str(i)
                df.rename(columns={col_name: month + ' ' + str(i)},
                          inplace=True)
        df.pop('Region/Country name')
        df.pop('Local authority name')
        df.rename(columns={'Region/Country code': 'Region'}, inplace=True)
        df.rename(columns={'Local authority code ': 'Province'}, inplace=True)
        h_type = house_type[letter]
        if h_type == 'detached' or h_type == 'semi-detached':
            df = df[df['Province'] != 'E09000001']
        df = df.replace('.*:.*', pd.NA, regex=True)
        df.to_csv('data/human_readable/' + house_type[letter] + '.csv')
        df.to_parquet('data/clean/' + house_type[letter] + '.parquet')


clean_data()
