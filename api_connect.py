import requests
import pandas as pd
import sqlite3

pd.set_option('display.max_columns', None)

all_stations = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'


def get_stations(url_api=all_stations):
    response = requests.get(url_api)

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


def get_stations_indexes():
    data = get_stations()
    indexes = []
    for d in data:
        indexes.append(d[0])
    return sorted(indexes)


def get_sensors(limit=1):
    indexes = get_stations_indexes()
    base_url = 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/'
    urls = []
    all_data = pd.DataFrame(
        columns=['id', 'stationId', 'param_paramName', 'param_paramFormula', 'param_paramCode', 'param_idParam'])

    if limit > len(indexes):
        limit = len(indexes)

    for index in indexes[:limit]:
        urls.append(f'{base_url}{index}')

    for url in urls:
        response = requests.get(url)
        print(url)
        print(f'Response Code is: {response.status_code}')
        data_json = response.json()
        df = pd.json_normalize(data_json, sep='_')
        all_data = pd.concat([all_data, df], ignore_index=True)

    all_data = all_data.rename(columns={'param_paramName': 'paramName', 'param_paramFormula': 'paramFormula',
                                        'param_paramCode': 'paramCode', 'param_idParam': 'idParam'})
    json_list = all_data.values.tolist()

    return json_list


def populate_db_sensors(data):
    conn = sqlite3.connect('air_quality.db')
    c = conn.cursor()

    c.executemany("INSERT INTO sensors VALUES (?, ?, ?, ?, ?, ?);", data)
    print(f"It seems like all the data has been inserted correctly")
    conn.commit()
    conn.close()


def get_sensor_indexes_from_db():
    conn = sqlite3.connect('air_quality.db')
    c = conn.cursor()
    c.execute('SELECT id FROM sensors;')
    indexes = [x[0] for x in c.fetchall()]
    conn.commit()
    conn.close()
    return indexes


def get_sensor_data(limit=1):
    indexes = get_sensor_indexes_from_db()
    base_url = 'https://api.gios.gov.pl/pjp-api/rest/data/getData/'

    all_data = pd.DataFrame(columns=['sensorId', 'dataCode', 'date', 'value'])

    if limit > len(indexes):
        limit = len(indexes)

    for index in indexes[:limit]:

        url = f'{base_url}{index}'
        print(url)
        response = requests.get(url)
        print(f'Response Code is: {response.status_code}')

        data_json = response.json()

        key = list(data_json.values())[0]
        lst = list(data_json.values())[1]

        df = pd.json_normalize(lst[1:50], sep='_')      # It returns data 62 hours back, and last one is usually NULL
        df.insert(0, 'dataCode', key)
        df.insert(0, 'sensorId', index)

        all_data = pd.concat([all_data, df], ignore_index=True)

    json_list = all_data.values.tolist()
    print(json_list)    # change to return
    # INT, STR, STR (date), FLOAT 2022-02-18 14:00:00

    testowo = json_list[0]
    print(testowo)
    for t in testowo:
        print(t)
        print(type(t))

    # all_data = all_data.rename(columns={'param_paramName': 'paramName', 'param_paramFormula': 'paramFormula',
    #                                     'param_paramCode': 'paramCode', 'param_idParam': 'idParam'})
    # json_list = all_data.values.tolist()

    # return json_list


get_sensor_data(limit=2)

