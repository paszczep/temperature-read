import sqlite3
from pathlib import Path
import logging
from time import time
from measure import read_all_thermometers, Measure

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

db_path = Path(__file__).parent.parent / 'temp_ui' / 'instance' / 'db.sqlite'

VALUE_KEYS = tuple(Measure.__annotations__.keys())


def db_connection_and_cursor(db_location=db_path):
    db_connection = sqlite3.connect(db_location)
    db_cursor = db_connection.cursor()
    return db_connection, db_cursor



def insert_all_thermometers_into_db(input_data: list[dict], value_keys: tuple = VALUE_KEYS):
    insert_connection, insert_cursor = db_connection_and_cursor()
    insert_data = [[row.__dict__[key] for key in value_keys] for row in input_data]
    insert_query = f"INSERT INTO Thermometer {str(value_keys)} VALUES ({str('?, '*len(value_keys))[:-2]})"
    insert_cursor.executemany(insert_query, insert_data)
    insert_connection.commit()
    insert_connection.close()


def _update_query(row: dict, update_time: int) -> str:
    update_query = f"""
        UPDATE Thermometer SET 
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
    insert_all_thermometers_into_db(thermometer_data)
