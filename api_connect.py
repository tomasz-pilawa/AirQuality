import requests
import pandas as pd
import json

pd.set_option('display.max_columns', None)

all_stations = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'

response = requests.get(all_stations)
print(response.status_code)

jos = response.json()

df = pd.json_normalize(jos, sep='_')
df = df.rename(columns={'city_commune_communeName': 'communeName', 'city_commune_districtName': 'districtName',
                        'city_commune_provinceName': 'provinceName'})

print(df)

print(list(df.columns))

json_list = json.loads(json.dumps(list(df.T.to_dict().values())))
print(json_list)
print(json_list[0])
