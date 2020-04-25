import pandas as pd
import math
import matrix_completion


def load_covid_data(file):
    df = pd.read_csv(file, header=0)
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


def load_indicator_data(file):
    df = pd.read_csv(file, header=2)
    df['indicator'] = None
    # get most recent indicator number
    for index, country in df.iterrows():
        for year in country[4:65]:
            if not math.isnan(year):
                df.at[index, 'indicator'] = year
    return df[['Country Name', 'Indicator Code', 'indicator']]


def load_all_data():
    covid_confirmed = load_covid_data('data/time_series_covid19_confirmed_global.csv')
    covid_deaths = load_covid_data('data/time_series_covid19_deaths_global.csv')
    comm_diseases = load_indicator_data('data/API_SH.DTH.COMM.ZS_DS2_en_csv_v2_988974.csv')
    noncomm_diseases = load_indicator_data('data/API_SH.DYN.NCOM.ZS_DS2_en_csv_v2_1004480.csv')
    safe_water = load_indicator_data('data/API_SH.H2O.SMDW.ZS_DS2_en_csv_v2_1006819.csv')
    physicians = load_indicator_data('data/API_SH.MED.PHYS.ZS_DS2_en_csv_v2_993645.csv')
    sanitation = load_indicator_data('data/API_SH.STA.SMSS.ZS_DS2_en_csv_v2_1007680.csv')
    smoking = load_indicator_data('data/API_SH.PRV.SMOK_DS2_en_csv_v2_1004458.csv')
    hygiene = load_indicator_data('data/API_SH.STA.HYGN.ZS_DS2_en_csv_v2_1007351.csv')
    life_expect = load_indicator_data('data/API_SP.DYN.LE00.IN_DS2_en_csv_v2_988752.csv')
    pop_65up = load_indicator_data('data/API_SP.POP.65UP.TO.ZS_DS2_en_csv_v2_988979.csv')
    pop_1564 = load_indicator_data('data/API_SP.POP.1564.TO.ZS_DS2_en_csv_v2_988895.csv')
    return covid_confirmed, covid_deaths, comm_diseases, noncomm_diseases, safe_water, physicians, sanitation, \
        smoking, hygiene, life_expect, pop_65up, pop_1564


if __name__ == '__main__':

    # load data from JHU covid csvs and world bank - world development indicators
    covid_confirmed, covid_deaths, comm_diseases, noncomm_diseases, safe_water, physicians, sanitation, \
        smoking, hygiene, life_expect, pop_65up, pop_1564 = load_all_data()

    # create main matrix, add covid and indicator data
    M = pd.DataFrame()
    M['Country/Region'] = covid_confirmed['Country/Region']
    M['30 days from first case'] = covid_confirmed['30 days from first']
    M['30 days from first death'] = covid_deaths['30 days from first']
    for ind_data in [comm_diseases, noncomm_diseases, safe_water, physicians, sanitation, \
        smoking, hygiene, life_expect, pop_65up, pop_1564]:
        M[ind_data['Indicator Code'][0]] = ind_data['indicator']

    # drop countries so that M is numerical
    countries = M['Country/Region']
    M.drop(columns=['Country/Region'], inplace=True)

    # run matrix completion
    M_complete = matrix_completion.complete(M.to_numpy())
    # print(M_complete)
