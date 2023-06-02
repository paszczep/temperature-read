import sqlite3
from pathlib import Path
from time import time
from measure import read_all_thermometers

db_path = Path(__file__).parent.parent / 'temp_ui' / 'instance' / 'db.sqlite'


def db_connection_and_cursor(db_location=db_path):
    db_connection = sqlite3.connect(db_location)
    db_cursor = db_connection.cursor()
    return db_connection, db_cursor


def insert_all_into_db(input_data: list[dict]):
    insert_connection, insert_cursor = db_connection_and_cursor()
    insert_time = int(time())
    insert_data = [(row['device_id'], row['name'], row['value'], row['device_time'], insert_time) for row in input_data]
    insert_query = "INSERT INTO Thermometer (id, name, value, thermometer_time, database_time) VALUES (?, ?, ?, ?, ?)"
    insert_cursor.executemany(insert_query, insert_data)
    insert_connection.commit()
    insert_connection.close()


def _update_query(row: dict, update_time: int) -> str:
    update_query = f"""UPDATE Thermometer SET 
        name = '{row['name']}', 
        value = '{row['value']}', 
        thermometer_time = '{row['device_time']}', 
        database_time = '{update_time}' 
        WHERE id = {row['device_id']}"""
    return update_query


def update_db(input_data: list[dict]):
    update_connection, update_cursor = db_connection_and_cursor()
    update_time = int(time())
    for row in input_data:
        update_query = _update_query(row, update_time)
        update_cursor.execute(update_query)
        update_connection.commit()
    update_connection.close()


if __name__ == '__main__':
    thermometer_data = read_all_thermometers()
    update_db(thermometer_data)
