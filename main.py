import csv

import numpy as np
import pandas as pd
import requests


def download_data():
    csv_2022 = 'https://api.dane.gov.pl/media/resources/20220407/DOWODY_2022_Tabela_do_Danych_Publicznych_I.csv'
    csv_2021 = 'https://api.dane.gov.pl/media/resources/20220114/DOWODY_2021_Tabela_do_Danych_Publicznych_IV.csv'
    csv_2020 = 'https://api.dane.gov.pl/media/resources/20210112/DOWODY_2020_Tabela_do_Danych_Publicznych_IV.csv'
    csv_2019 = 'https://api.dane.gov.pl/media/resources/20200616/DOWODY_2019_Tabela_do_Danych_Publicznych.csv'
    list_url= [csv_2022, csv_2021, csv_2020, csv_2019]
    list_name = ['csv_2022', "csv_2021", "csv_2020", 'csv_2019']
    #print(list)

    for index, value in enumerate(list_url):
        req = requests.get(value)
        url_content = req.content

        csv_file = open(list_name[index] + '.csv', 'wb')

        csv_file.write(url_content)

        csv_file.close()

def data_for_poland(filename):
    import pandas as pd
    cols = ['l.p','WOJEWÓDZTWO','I KWARTAŁ','II KWARTAŁ','III KWARTAŁ','IV KWARTAŁ','ROK']

    df = (pd.read_csv(filename, header=None, names=cols, encoding="utf8") #open and check if has header
    [lambda x: np.ones(len(x)).astype(bool)
        if (x.iloc[0] != cols).all()
        else np.concatenate([[False], np.ones(len(x) - 1).astype(bool)])]
    )
    try:
        sum_of_poland_I_quarter = df['I KWARTAŁ'].astype(int).sum()
    except:
        print("Exception thrown. x does not exist.")
    try:
        sum_of_poland_II_quarter = df['II KWARTAŁ'].astype(int).sum()

        sum_of_poland_III_quarter = df['III KWARTAŁ'].astype(int).sum()

        sum_of_poland_IV_quarter = df['IV KWARTAŁ'].astype(int).sum()
    except:
        return sum_of_poland_I_quarter, 0, 0, 0

    return sum_of_poland_I_quarter, sum_of_poland_II_quarter, sum_of_poland_III_quarter, sum_of_poland_IV_quarter

def get_data_info():
    print("Średnia liczba dowdów osobistym w danym okresie")
    print("dostępne dane z lat od 2019 do 2022 (tylko pierwszy kwartał)")
    print('Wprowadz date w którym chcesz rozpocząćw postaci : 2019-Q1, ')
    data_start = input()
    print('Wprowadz date w którym chcesz zakończyć postaci : 2021-Q2')
    data_end = input()

    return data_start, data_end
def calculate_range(data_start, data_end):
    q1_2019_data, q2_2019_data, q3_2019_data, q4_2019_data = data_for_poland("csv_2019.csv")
    q1_2020_data, q2_2020_data, q3_2020_data, q4_2020_data = data_for_poland("csv_2020.csv")
    q1_2021_data, q2_2021_data, q3_2021_data, q4_2021_data = data_for_poland("csv_2021.csv")
    q1_2022_data, q2_2022_data, q3_2022_data, q4_2022_data = data_for_poland("csv_2022.csv")

    #print(q1_2019_data, q2_2019_data, q3_2019_data, q4_2019_data)
    #print(q1_2020_data, q2_2020_data, q3_2020_data, q4_2020_data)
    #print(q1_2021_data, q2_2021_data, q3_2021_data, q4_2021_data)
    #print(q1_2022_data, q2_2022_data, q3_2022_data, q4_2022_data)

    data = {
        "2019-Q1": q1_2019_data, '2019-Q2' : q2_2019_data, '2019-Q3' : q3_2019_data, '2019-Q4' : q4_2019_data, '2020-Q1' : q1_2020_data, '2020-Q2' : q2_2020_data, '2020-Q3' : q3_2020_data, '2020-Q4' : q4_2020_data, '2021-Q1' : q1_2021_data, '2021-Q2' : q2_2021_data,
        '2021-Q3' : q3_2021_data, '2021-Q4' : q4_2021_data , '2022-Q1' : q1_2022_data , '2022-Q2' : q2_2022_data, '2022-Q3' : q3_2022_data, '2022-Q4' : q4_2022_data
    }
    index_start = list(data.keys()).index(data_start)
    index_end = list(data.keys()).index(data_end)
    #print(index_start, index_end)
    sum_of_range = 0
    for index_start in range(index_end):
        #print(list(data.values())[index_start])
        sum_of_range = sum_of_range + list(data.values())[index_start]
    #print(sum_of_range)


    start_data_datetime = pd.to_datetime(pd.Series([data_start])) #quarter to datetime
    end_data_datetime = pd.to_datetime(pd.Series([data_end]))

    number_of_days = pd.to_datetime(end_data_datetime)- pd.to_datetime(start_data_datetime) #days between date

    return(sum_of_range / (number_of_days / np.timedelta64(1, 'D')).astype(int))


if __name__ == '__main__':
    download_data()
    data_start, data_end = get_data_info()
    ID_per_day = calculate_range(data_start, data_end)
    print("Liczba dowodow na dzien to : ", float(ID_per_day))

