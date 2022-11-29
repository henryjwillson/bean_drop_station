# This file contains the two error classes, cup return errors and operation errors
import sqlite3

class system_error:
	
	def __init__(self, error_code, error_name, error_text):
		self.error_code = error_code
		self.error_name = error_name
		self.error_text = error_text


# System errors list------------------------------------------------------------

#rfid errors
rfid_read_error = system_error(10, "rfid_read_error", "rfid reader failed to identify any rfid")
rfid_read_error_admin = system_error(12,"rfid_read_error_admin", "rfid reader failed to identify a rfid chip when placed by an admin under a test situation")
rfid_response_error = system_error(13, "rfid_response_error", "rfid module has failed to respond to admin commands with OKAY response")

#load cell errors
load_cell_extreme_range = system_error(20, "load_cell_extreme_range", "load cell out of expected range and limiting range")

#laser errors
laser_not_triggered = system_error(30, "laser_not_triggered", "laser sensor did not trigger during customer operation - reason unknown")
laser_not_triggered_admin = system_error(31, "laser_not_triggered_admin", "laser sensor did not trigger during admin operation when expected to trigger")

#Customer sliding door error
sliding_door_reopen_fail = system_error(40, "sliding_door_reopen_fail", "sliding door failed to leave closed limit switch or reach target open limit switch")
sliding_door_ls_fail = system_error(41, "sliding_door_ls_fail", "sliding door fails to trigger limit switch when being closed")
sliding_door_ls_fail_admin = system_error(42, "sliding_door_ls_fail_admin", "sliding door fails to trigger limit switch when being closed")

#rfid trolley error
rfid_trolley_open_ls_fail_normal = system_error(50, "rfid_trolley_open_ls_fail_normal", "rfid trolley's open limit switch failed to trigger as expected during operation")
rfid_trolley_open_ls_fail_homing = system_error(51, "rfid_trolley_open_ls_fail_homing", "rfid trolley's open limit switch failed to trigger as expected during homing operation")
rfid_trolley_closed_ls_fail_normal = system_error(52, "rfid_trolley_closed_ls_fail_normal", "rfid trolley's closed limit switch failed to trigger as expected during operation")
rfid_trolley_closed_ls_fail_homing = system_error(53, "rfid_trolley_closed_ls_fail_homing", "rfid trolley's closed limit switch failed to trigger as expected during homing operation")

#main trolley error
main_trolley_BinA_ls_fail_normal = system_error(60, "main_trolley_BinA_ls_fail_normal", "main trolley BinA limit switch failed to trigger as expected during operation")
main_trolley_BinA_ls_fail_homing = system_error(61, "main_trolley_BinA_ls_fail_homing", "main trolley BinA limit switch failed to trigger as expected during homing operation")
main_trolley_BinQ_ls_fail_normal = system_error(62, "main_trolley_BinQ_ls_fail_normal", "main trolley BinQ limit switch failed to trigger as expected during operation")
main_trolley_BinQ_ls_fail_homing = system_error(63, "main_trolley_BinQ_ls_fail_homing", "main trolley BinQ limit switch failed to trigger as expected during homing operation")
main_trolley_BinB_ls_fail_normal = system_error(64, "main_trolley_BinB_ls_fail_normal", "main trolley BinB limit switch failed to trigger as expected during operation")
main_trolley_BinB_ls_fail_homing = system_error(65, "main_trolley_BinB_ls_fail_homing", "main trolley BinB limit switch failed to trigger as expected during homing operation")

#trap door trolley
trap_door_trolley_open_ls_fail_normal = system_error(70, "trap_door_trolley_open_ls_fail_normal", "trap door trolley's open limit switch failed to trigger as expected during operation")
trap_door_trolley_open_ls_fail_homing = system_error(71, "trap_door_trolley_open_ls_fail_homing", "trap door trolley's open limit switch failed to trigger as expected during homing operation")
trap_door_trolley_closed_ls_fail_normal = system_error(72, "trap_door_trolley_closed_ls_fail_normal", "trap door trolley's open limit switch failed to trigger as expected during operation")
trap_door_trolley_closed_ls_fail_homing = system_error(73, "trap_door_trolley_closed_ls_fail_homing", "trap door trolley's open limit switch failed to trigger as expected during homing operation")

#Server communication errors
network_connection_failure = system_error(81, "network_connection_failure", "Failed to connect to mobile network")
wifi_connection_failure = system_error(81, "wifi_connection_failure", "Failed to connect to wifi network")
credential_server_failure = system_error(82, "credential_server_failure", "credentials failed to authorise when attempting to connect to database server")
information_transfer_server_failure = system_error(83, "information_transfer_server_failure", "unexpected unknown error occured when transfering data to external server")


class customer_error_database_entry:
	
	def __init__(self, database_file, bean_drop_station_id):
		self.database_file = database_file
		self.bean_drop_station_id = bean_drop_station_id
		self.no_error_code = 10
		self.no_rfid_code = 11
		self.unrecognised_rfid_code = 12
		self.slight_under_weight_code = 20
		self.large_under_weight_code = 21
		self.slight_over_weight_code = 22
		self.large_over_weight_code = 23
		self.Laser_triggered_low_cup_height_code = 30
		self.Laser_low_slight_under_weight_code = 31
		self.Laser_low_large_under_weight_code = 32
		self.Laser_low_slight_over_weight_code = 33
		self.Laser_low_large_over_weight_code = 34
		
	def laser_error_list(self):
		return [self.Laser_triggered_low_cup_height_code, self.Laser_low_slight_under_weight_code, self.Laser_low_large_under_weight_code, self.Laser_low_slight_over_weight_code, self.Laser_low_large_over_weight_code]
		
	def create_error_table(self):
		conn_local_db2 = sqlite3.connect(self.database_file)
		c2 = conn_local_db2.cursor()
		try:
			with conn_local_db2:
				c2.execute("""CREATE TABLE error_log_table (
								error_log_id integer,
								error_code integer,
								action_code integer,
								error_datetime datetime,
								PRIMARY KEY (error_log_id)
								)""")
				return ("New error_log_table successfully built into ", self.database_file)
		except sqlite3.Error as err:
			return ("The error in creating error_log_table in database was: ", err)
		finally:
			conn_local_db2.commit()
			conn_local_db2.close()
			
	def admin_reset_error_log_table(self):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		try:
			with conn_local_db:
				c.execute("DELETE FROM `error_log_table`;")
				conn_local_db.commit()
		except Exception as err:
			print("Error in updating photo download status was: ", err)
			return False
		finally:
			conn_local_db.close()
			
	def admin_delete_error_log_table(self):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		try:
			with conn_local_db:
				c.execute("DROP TABLE `error_log_table`;")
				conn_local_db.commit()
		except Exception as err:
			print("Error in updating photo download status was: ", err)
			return False
		finally:
			conn_local_db.close()
			
	def fetch_entire_error_log_table(self):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		try:
			with conn_local_db:
				c.execute("SELECT * FROM `error_log_table`;")
				error_logs = c.fetchall()
				return error_logs
		except Exception as err:
			print("Error in updating photo download status was: ", err)
			return False
		finally:
			conn_local_db.close()
			
	def insert_new_error_log(self, error_code, action_code, error_datetime):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		#return False
		try:
			with conn_local_db:
				c.execute("SELECT MAX(error_log_id) FROM error_log_table")
				last_error_log_id = c.fetchone()
				# 0 take the first value of the turple which is returned (getting error here when applying in return statement...)
				print("Last error_log_id: ", last_error_log_id[0])
				if last_error_log_id[0] == 0:
					next_error_log_id = 1
				elif last_error_log_id[0] == None:
					next_error_log_id = 1
				else:
					next_error_log_id = last_error_log_id[0] + 1
				print("The next order id is: ", next_error_log_id)
		except sqlite3.Error as err:
			print("The error in selecting Max order_id_cafe_local was: ", err)
			self.create_error_table()
			next_error_log_id = 1
		else:
			try:
				with conn_local_db:
					c.execute("""INSERT INTO error_log_table VALUES (
							:error_log_id,
							:error_code,
							:action_code,
							:error_datetime)""", {'error_log_id': next_error_log_id, 'error_code': error_code, 'action_code': action_code, 'error_datetime': error_datetime})
					print("I inserted an error with error_log_id: ", next_error_log_id)
					print("Last error id was (error_log_id) used in the 'order class' object: ", last_error_log_id)
					print("The new error id after update from localised db is: ",next_error_log_id)
					#return True                                  # may need double == if this fails to update order id
			except sqlite3.Error as err:
				print("Error in inserting new error was: ", err)
			print("Double check last row id: ", c.lastrowid)
		finally:
			conn_local_db.commit()
			conn_local_db.close()
			
	def no_error(self, unique_entry_code, error_datetime):
		self.insert_new_error_log(1, unique_entry_code, error_datetime)
		
	def no_rfid(self, unique_entry_code, error_datetime):
		self.insert_new_error_log(10, unique_entry_code, error_datetime)
		
	def unrecognised_rfid(self, unique_entry_code, error_datetime):
		self.insert_new_error_log(11, unique_entry_code, error_datetime)
		
	def slight_under_weight(self, unique_entry_code, error_datetime):
		self.insert_new_error_log(20, unique_entry_code, error_datetime)
		
	def large_under_weight(self, unique_entry_code, error_datetime):
		self.insert_new_error_log(21, unique_entry_code, error_datetime)
		
	def slight_over_weight(self, unique_entry_code, error_datetime):
		self.insert_new_error_log(22, unique_entry_code, error_datetime)
		
	def large_over_weight(self, unique_entry_code, error_datetime):
		self.insert_new_error_log(23, unique_entry_code, error_datetime)
	
	def Laser_triggered_low_cup_height(self, unique_entry_code, error_datetime):
		self.insert_new_error_log(30, unique_entry_code, error_datetime)
		
	def Laser_low_slight_under_weight(self, unique_entry_code, error_datetime):
		self.insert_new_error_log(31, unique_entry_code, error_datetime)
		
	def Laser_low_large_under_weight(self, unique_entry_code, error_datetime):
		self.insert_new_error_log(32, unique_entry_code, error_datetime)
		
	def Laser_low_slight_over_weight(self, unique_entry_code, error_datetime):
		self.insert_new_error_log(33, unique_entry_code, error_datetime)
		
	def Laser_low_large_over_weight(self, unique_entry_code, error_datetime):
		self.insert_new_error_log(34, unique_entry_code, error_datetime)
	
	
		




def main():
	
	import datetime
	
	def datetime_formatted():
		return datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
	
	print(rfid_trolley_closed_ls_fail_normal.error_name)
	print(laser_not_triggered.error_text)
	
	test_database = customer_error_database_entry("local_db_test.db",10)
	# test_database.admin_delete_error_log_table()
	# test_database.admin_reset_error_log_table()
	
	# test_database.create_error_table()
	
	# latest_time = datetime_formatted()
	# test_database.no_rfid(21, latest_time)
	
	# latest_time = datetime_formatted()
	# test_database.unrecognised_rfid(22, latest_time)
	
	# latest_time = datetime_formatted()
	# test_database.slight_under_weight(23, latest_time)
	
	# latest_time = datetime_formatted()
	# test_database.Laser_triggered_low_cup_height(24, latest_time)
	
	all_errors_list = test_database.fetch_entire_error_log_table()
	for error in all_errors_list:
		print(error)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		gpio.cleanup()
		sys.exit(0)
