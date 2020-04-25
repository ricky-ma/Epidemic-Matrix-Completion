import pandas as pd


def load_covid_data(df):
    df.drop(columns=['Lat', 'Long', 'Province/State'], inplace=True)
    for date in df.columns[1:]:
        df[date] = df.groupby([df.columns[0]])[date].transform('sum')
    df.drop_duplicates(subset=[df.columns[0]], keep='first', inplace=True)
    df['days since first'] = 0
    df['20 days from first'] = None
    df['30 days from first'] = None
    df['40 days from first'] = None
    df['50 days from first'] = None

    for index, country in df.iterrows():
        days_since_first = -1
        total_n = 0
        for n in country[1:92]:
            if n > 0:
                days_since_first += 1
                total_n += n
                df.at[index, 'days since first'] += 1
                if days_since_first == 20:
                    df.at[index, '20 days from first'] = n
                if days_since_first == 30:
                    df.at[index, '30 days from first'] = n
                if days_since_first == 40:
                    df.at[index, '40 days from first'] = n
                if days_since_first == 50:
                    df.at[index, '50 days from first'] = n

    return df


if __name__ == '__main__':

    df_confirmed_global = pd.read_csv('data/time_series_covid19_confirmed_global.csv', header=0)
    df_confirmed_global = load_covid_data(df_confirmed_global)
    df_confirmed_global = df_confirmed_global.sort_values(by=['4/23/20', 'days since first'], ascending=False)

    df_deaths_global = pd.read_csv('data/time_series_covid19_deaths_global.csv', header=0)
    df_deaths_global = load_covid_data(df_deaths_global)
    df_deaths_global = df_deaths_global.sort_values(by=['4/23/20', 'days since first'], ascending=False)

    print(df_confirmed_global.head(10))
    print(df_deaths_global.head(10))

