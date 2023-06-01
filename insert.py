import sqlite3
from pathlib import Path
from time import time

db_path = Path(__file__).parent.parent / 'temp_ui' / 'instance' / 'db.sqlite'


def db_connection_and_cursor(db_location = db_path):
	db_connection = sqlite3.connect(db_location)
	db_cursor = db_connection.cursor()
	return db_connection, db_cursor


def insert_into_db(row: dict):
	insert_query = f"""
	INSERT INTO Thermometer 
	(id, name, value, thermometer_time, database_time)
	VALUES
	('{row['device_id']}', '{row['name']}', '{row['reading']}', '{row['reading_time']}', '{int(time())}')
	"""
	


row = {}


select_query = """SELECT id FROM Thermometer"""
db_cursor.execute(select_query)
response = db_cursor.fetchall()
print(response)
