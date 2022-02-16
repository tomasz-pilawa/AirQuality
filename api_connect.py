import requests

all_stations = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'

response = requests.get(all_stations)
print(response.status_code)

print(response.json())


