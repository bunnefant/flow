import sqlite3
from sqlite3 import Error

class UserDeviceDB:

	create_user_table = """
	CREATE TABLE IF NOT EXISTS users (
		email TEXT PRIMARY KEY,
		device_id INTEGER,
		topic_arn TEXT
	);
	"""
	create_device_table = """
	CREATE TABLE IF NOT EXISTS devices (
		device_id INTEGER PRIMARY KEY,
		status TEXT
	);
	"""

	def __init__(self, path):
		self.connection = self.create_connection(path)
		self.execute_query(self.create_user_table)
		self.execute_query(self.create_device_table)


	def create_connection(self, path):
 		connection = None
 		try:
 			connection = sqlite3.connect(path)
 			print("Connected to DB successfully")
 		except Error as e:
 			print(f"During connection to {path} DB error '{e}' occurred")

 		return connection

	def execute_query(self, query):
		cursor = self.connection.cursor()
		try:
			cursor.execute(query)
			self.connection.commit()
			print("Executed query successfully")
		except Error as e:
			print(f"During query execution error '{e}' occurred")

	def execute_read_query(self, query):
		cursor = self.connection.cursor()
		result = None
		try:
			cursor.execute(query)
			result = cursor.fetchall()
			return result
		except Error as e:
			print(f"During read query execution error '{e}' occurred")

	def add_user(self, email, device_id, topic_arn):
		query = """
		INSERT INTO
			users (email, device_id, topic_arn)
		VALUES
			('{0}', {1}, '{2}')
		""".format(email, device_id, topic_arn)
		self.execute_query(query)

	def add_device(self, device_id, status):
		query = """
		INSERT INTO
			devices (device_id, status)
		VALUES
			({0}, '{1}')
		""".format(device_id, status)
		self.execute_query(query)

	def update_device_status(self, device_id, status):
		query = """
		UPDATE
			devices
		SET
			status = '{0}'
		WHERE
			device_id = {1}
		""".format(status, device_id)
		self.execute_query(query)

	def get_topic_from_id(self, device_id):
		query = """
		SELECT
			topic_arn
		FROM
			users
		WHERE
			users.device_id = {0}
		""".format(device_id)
		return self.execute_read_query(query)

	def update(self, flag, list):
		# for adding users
		if (flag[0] == "u"):
			self.add_user(list[0], int(list[1]), list[2])
		# for adding devices
		elif (flag[0] == "d"):
			self.add_device(int(list[0]), list[1])
		# for updating device status
		elif (flag[0] == "s"):
			self.update_device_status(int(list[0]), list[1])
		# for getting topic from id
		elif (flag[0] == "t"):
			return self.get_topic_from_id(int(list[0]))

		return None


def main():
	db = UserDeviceDB("test.db")
	db.update("u", ["alex.hoerler@gatech.edu", "2554", "http:www.google.com"])
	db.update("d", ["2554", "not full"])
	print(db.update("t", ["2554"]))
	db.update("s", ["2554", "full"])
	print(db.update("t", ["2554"]))


if __name__ == "__main__":
	main()
