import api_connect as a


def get_stations_indexes():
    data = a.get_stations()
    ids = []
    for x in data:
        ids.append(x[0])
    return sorted(ids)


indexes = get_stations_indexes()
print(indexes)
