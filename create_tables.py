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
    provinceName TEXT);
    ''')
    conn.commit()
    conn.close()


def create_table_sensors():
    conn = sqlite3.connect('air_quality.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensors (
    id INTEGER,
    stationId INTEGER,
    paramName TEXT,
    paramFormula TEXT,
    paramCode TEXT,
    idParam INTEGER);
    ''')
    conn.commit()
    conn.close()


def create_table_sensor_data():
    conn = sqlite3.connect('air_quality.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensorData (
    sensorId INTEGER NOT NULL,
    dataCode TEXT NOT NULL,
    date TEXT NOT NULL,
    value REAL,
    UNIQUE (sensorId, dataCode, date));
    ''')

create_table_sensor_data()