import requests
import pandas as pd
import json
import sqlite3

pd.set_option('display.max_columns', None)

all_stations = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'


def populate_stations(url_api=all_stations):
    response = requests.get(url_api)
    print(f'Response Code is: {response.status_code}')

    data_json = response.json()

    df = pd.json_normalize(data_json, sep='_')
    df = df.rename(columns={'city_commune_communeName': 'communeName', 'city_commune_districtName': 'districtName',
                            'city_commune_provinceName': 'provinceName'})

    # print(list(df.columns))   # used earlier to get column lists for renaming

    json_list = json.loads(json.dumps(list(df.T.to_dict().values())))

    return json_list


# check if encapsulation works:
data = populate_stations()
print(data)
print(len(data))
print(data[0])