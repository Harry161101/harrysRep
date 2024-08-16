import sqlite3
import json


def create_weather_table(database_file):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS weather_newyork")

    cursor.execute('''
        CREATE TABLE weather_newyork (
            date TEXT,
            mean_temp INT,
            precip FLOAT,
            events TEXT
        )
    ''')

    conn.commit()
    return conn, cursor

def insert_data_from_json(database_file, json_file):
    conn, cursor = create_weather_table(database_file)

    with open(json_file, 'r') as file:
        data = json.load(file)

        for date, details in data.items():
            mean_temp = details['mean_temp']
            precip = details['precip']
            events = details['events']

            precip_value = None if precip == 'T' else float(precip)

            cursor.execute('''
                INSERT INTO weather_newyork (date, mean_temp, precip, events)
                VALUES (?, ?, ?, ?)
            ''', (date, int(mean_temp), precip_value, events))

        conn.commit()

    cursor.execute('SELECT * FROM weather_newyork LIMIT 10')
    rows = cursor.fetchall()
    print("First 10 rows:")
    for row in rows:
        print(row)

    cursor.execute("SELECT * FROM weather_newyork WHERE date = '1/9/16'")
    print("\nRow with date '1/9/16':")
    print(cursor.fetchone())

    cursor.execute('SELECT COUNT(*) FROM weather_newyork')
    print("\nTotal number of rows:")
    print(cursor.fetchone()[0])

    conn.close()


insert_data_from_json('session_2.db', 'weather_newyork_dod.json')