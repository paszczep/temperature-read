import sqlite3
from pathlib import Path
import logging
from datetime import datetime
from measure import read_all_thermometers, Measure

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

db_path = Path(__file__).parent.parent / 'temp_ui' / 'instance' / 'db.sqlite'


def db_connection_and_cursor(db_location=db_path):
    db_connection = sqlite3.connect(db_location)
    db_cursor = db_connection.cursor()
    return db_connection, db_cursor


VALUE_KEYS = tuple(Measure.__annotations__.keys())



def insert_all_thermometers(input_data: list[Measure], value_keys: tuple = VALUE_KEYS):
    insert_data = [[row.__dict__[key] for key in value_keys] for row in input_data]
    insert_query = f"INSERT INTO Thermometer {str(value_keys)} VALUES ({str('?, '*len(value_keys))[:-2]})"
    insert_connection, insert_cursor = db_connection_and_cursor()
    with insert_connection:
        insert_cursor.executemany(insert_query, insert_data)
        insert_connection.commit()


def _update_query(row: Measure, update_time: str) -> str:
    update_query = f"""
        UPDATE Thermometer SET 
        device_name = '{row.device_name}', 
        temperature = '{row.temperature}', 
        measure_time = '{row.measure_time}', 
        database_time = '{update_time}' 
        WHERE device_id = {row.device_id}"""
    return update_query


def update_all_thermometers(input_data: list[Measure]):
    update_connection, update_cursor = db_connection_and_cursor()
    update_time = str(datetime.now())
    with update_connection:
        for row in input_data:
            update_query = _update_query(row, update_time)
            update_cursor.execute(update_query)
            update_connection.commit()

if __name__ == '__main__':
    thermometer_data = read_all_thermometers()
    update_all_thermometers(thermometer_data)
