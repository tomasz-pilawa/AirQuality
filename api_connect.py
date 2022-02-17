import requests
import pandas as pd
import sqlite3

pd.set_option('display.max_columns', None)

all_stations = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'


def get_stations(url_api=all_stations):
    response = requests.get(url_api)
    print(f'Response Code is: {response.status_code}')

    data_json = response.json()

    df = pd.json_normalize(data_json, sep='_')
    df = df.rename(columns={'city_commune_communeName': 'communeName', 'city_commune_districtName': 'districtName',
                            'city_commune_provinceName': 'provinceName'})

    # print(list(df.columns))   # used earlier to get column lists for renaming

    json_list = df.values.tolist()

    for entry in json_list:
        entry[2] = float(entry[2])
        entry[3] = float(entry[3])
        entry[5] = int(entry[5])

    return json_list


def populate_db_stations(data):
    conn = sqlite3.connect('air_quality.db')
    c = conn.cursor()

    c.executemany("INSERT INTO stations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", data)
    print(f"It seems like all the data has been inserted correctly")
    conn.commit()
    conn.close()

