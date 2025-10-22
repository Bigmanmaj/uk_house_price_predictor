import pandas as pd

def clean_data():
    dataset_months = ['Dec', 'Mar', 'Jun', 'Sep']
    letters = [chr(i) for i in range(ord('a'), ord('e') + 1)]
    house_type = {'a' : 'all', 'b' : 'detached', 'c' : 'semi-detached', 'd' : 'terraced', 'e' : 'flats'}
    for letter in letters:
        df = pd.read_excel('data/raw/raw_data.xls', sheet_name='2'+letter, header=6) # read all datasheets up to 2e
        for i in range(1995, 2024):
            for month in dataset_months:
                col_name = 'Year ending ' + month + ' ' + str(i)
                df.rename(columns={col_name : month + ' ' + str(i)}, inplace=True)

        df.pop('Region/Country name')
        df.pop('Local authority name')

        df.rename(columns={'Region/Country code' : 'Region'}, inplace=True)
        df.rename(columns={'Local authority code ' : 'Province'}, inplace=True)

        if house_type[letter] == 'detached' or house_type[letter] == 'semi-detached':
            df = df[df['Province'] != 'E09000001']

        df = df.replace('.*:.*', pd.NA, regex=True)

        df.to_csv('data/human_readable/' + house_type[letter] + '.csv')
        df.to_parquet('data/clean/' + house_type[letter] + '.parquet')

        ''' 
        Todo: 
        - delete detached and semi detached from city of london enteries (E09000001)
        - write in N/A instead of : 
        '''

clean_data()