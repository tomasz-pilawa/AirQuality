import sqlite3

columns_stations = ['id', 'stationName', 'gegrLat', 'gegrLon', 'addressStreet', 'city_id', 'city_name', 'communeName',
                    'districtName', 'provinceName']


def create_table_stations():
    conn = sqlite3.connect('air_quality.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stations (
    id INTEGER,
    stationName TEXT,
    gegrLat REAL,
    gegrLon REAL,
    addressStreet TEXT,
    city_id INTEGER,
    city_name TEXT,
    communeName TEXT,
    districtName TEXT,
    provinceName TEXT,
    ''')
    conn.commit()
    conn.close()
