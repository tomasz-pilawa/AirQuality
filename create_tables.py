import sqlite3


def create_new_table(table_name):
    conn = sqlite3.connect('air_quality.db')
    c = conn.cursor()
    c.execute('CREATE TABLE')