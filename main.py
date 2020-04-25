import pandas as pd







def days_since_first_case():
    df = pd.read_csv('data/time_series_covid19_confirmed_global.csv', header=0)



def group_by_country(df):
    print(df.shape)
    df.drop('Province/State', axis=1, inplace=True)
    print(df.shape)
    for date in df.columns[3:]:
        df[date] = df.groupby(['Country/Region'])[date].transform('sum')
    df.drop_duplicates(subset=['Country/Region'], keep='first', inplace=True)
    return df



if __name__ == '__main__':
    df = pd.read_csv('data/time_series_covid19_confirmed_global.csv', header=0)
    df_country = group_by_country(df)
