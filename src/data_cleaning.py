'''Cleans data for datasets provided'''
import pandas as pd
import sqlite3


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
                df.rename(columns={col_name: month + '|' + str(i)},
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

def create_location_dataset():
    '''
    Creates database tables regions, local_authorities
    (p) stands for primary key
    regions:
    region_code (p)    region_name

    local_authorities
    local_authority_code (p)   local_authority_name     region_code
    '''
    letter = 'a'
    df = pd.read_excel('data/raw/raw_data.xls', sheet_name='2' +
                           letter, header=6)
    df = df.loc[:,'Region/Country code': 'Local authority name']
    df.rename(columns={'Region/Country name': 'region_name'}, inplace=True)
    df.rename(columns={'Region/Country code': 'region_code'}, inplace=True)
    df.rename(columns={'Local authority code ': 'local_authority_code'}, inplace=True) # whitespace is intentional
    df.rename(columns={'Local authority name': 'local_authority_name'}, inplace=True)
    regions = df.copy()
    regions.pop('local_authority_name')
    regions.pop('local_authority_code')
    regions.drop_duplicates(inplace=True)
    conn = sqlite3.connect('data/clean/location.db')
    df.to_sql("local_authorities", conn, if_exists="replace", index=False)
    regions.to_sql("regions", conn, if_exists="replace", index=False)
    with conn:
            conn.execute("""
        CREATE TABLE IF NOT EXISTS local_authorities (
            local_authority_code TEXT PRIMARY KEY,
            local_authority_name TEXT NOT NULL,
            region_code TEXT NOT NULL,
            FOREIGN KEY (region_code) REFERENCES regions (region_code)
        );
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS local_authorities (
            local_authority_code TEXT PRIMARY KEY,
            local_authority_name TEXT NOT NULL,
            region_code TEXT NOT NULL,
            FOREIGN KEY (region_code) REFERENCES regions (region_code)
        );
    """)
    conn.close()



def create_sample_data():
    '''Creates sample data for testing purposes'''


create_location_dataset()