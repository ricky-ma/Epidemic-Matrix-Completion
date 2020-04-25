import pandas as pd


def load_covid_data(df):
    df.drop(columns=['Lat', 'Long', 'Province/State'], inplace=True)
    for date in df.columns[1:]:
        df[date] = df.groupby([df.columns[0]])[date].transform('sum')
    df.drop_duplicates(subset=[df.columns[0]], keep='first', inplace=True)
    df['Days since first'] = 0
    for index, country in df.iterrows():
        for date in country[1:]:
            if date > 0:
                df.at[index, 'Days since first'] += 1
    return df


if __name__ == '__main__':

    df_confirmed_global = pd.read_csv('data/time_series_covid19_confirmed_global.csv', header=0)
    df_confirmed_global = load_covid_data(df_confirmed_global)
    df_confirmed_global = df_confirmed_global.sort_values(by=['4/23/20', 'Days since first'], ascending=False)

    df_deaths_global = pd.read_csv('data/time_series_covid19_deaths_global.csv', header=0)
    df_deaths_global = load_covid_data(df_deaths_global)
    df_deaths_global = df_deaths_global.sort_values(by=['4/23/20', 'Days since first'], ascending=False)

    print(df_confirmed_global.head(10))
    print(df_deaths_global.head(10))

