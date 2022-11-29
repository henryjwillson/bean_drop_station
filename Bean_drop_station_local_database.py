'''Bean Drop Station Local DB Class'''

import sqlite3								# Used as local database for access to orders without need for connection to server network
import sys, os
import subprocess

class bean_drop_station_database:
	
	def __init__(self, database_file):
		self.database_file = database_file
	
	def create_cup_returns_table(self):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		try:
			with conn_local_db:
				c.execute("""CREATE TABLE cup_returns (
								cup_return_id integer,
								global_return_id integer,
								cup_rfid text,
								return_attempts integer,
								cup_success_code integer,
								return_datetime datetime,
								bin_section integer,
								PRIMARY KEY (cup_return_id),
								UNIQUE (global_return_id)
								)""")
				return ("New cup_returns table successfully built into ", self.database_file)
			conn_local_db.commit()
			conn_local_db.close()
		except sqlite3.Error as err:
			return ("The error in cup_returns creating table in database was: ", err)
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			
	def create_actions_table(self):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		try:
			with conn_local_db:
				c.execute("""CREATE TABLE action_log_table (
								action_id integer,
								action_code integer,
								action_text text,
								action_datetime datetime,
								PRIMARY KEY (action_id)
								)""")
				return ("New action_log_table successfully built into ", self.database_file)
		except sqlite3.Error as err:
			return ("The error in creating action_log_table in database was: ", err)
		finally:
			conn_local_db.commit()
			conn_local_db.close()
			
			
	def create_station_attribute_table(self):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		try:
			with conn_local_db:
				c.execute("""CREATE TABLE station_attribute_table (
								station_key integer,
								station_global_id integer,
								station_global_name text,
								station_nickname text,
								Bin_A_Capacity integer,
								Bin_A_Cups integer,
								Bin_B_Capacity integer,
								Bin_B_Cups integer,
								Bin_Q_Capacity integer,
								Bin_Q_Cups integer,
								Bin_A_last_collection datetime,
								Bin_B_last_collection datetime,
								Bin_Q_last_collection datetime,
								Last_station_reset datetime,
								Last_micro_controller_reset datetime,
								Last_software_reset datetime,
								software_version text, 
								last_error_time datetime,
								last_error_code integer,
								last_cup_return_time datetime,
								last_cup_return_bin text,
								last_rfid_returned varchar,
								rfid_status boolean,
								load_cell_status boolean,
								RFID_trolley_status boolean,
								laser_status boolean,
								main_trolley_status text,
								trap_door_status text,
								customer_door_status boolean,
								Bin_A_Status boolean,
								Bin_B_Status boolean,
								Bin_Q_Status boolean,
								PRIMARY KEY (station_key)
								)""")
				return ("New error_log_table successfully built into ", self.database_file)
		except sqlite3.Error as err:
			return ("The error in creating error_log_table in database was: ", err)
		finally:
			conn_local_db.commit()
			conn_local_db.close()
			
	def insert_new_cup_return(self, global_return_id, cup_rfid, return_attempts, cup_success_code, return_datetime, bin_section):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		try:
			with conn_local_db:
				c.execute("SELECT MAX(cup_return_id) FROM cup_returns")
				last_return_id = c.fetchone()
				# 0 take the first value of the turple which is returned (getting error here when applying in return statement...)
				print("Last_order_id: ", last_return_id[0])
				if last_return_id[0] == 0:
					next_return_id = 1
				elif last_return_id[0] == None:
					next_return_id = 1
				else:
					next_return_id = last_return_id[0] + 1
				print("The next order id is: ", next_return_id)
		except sqlite3.Error as err:
			print("The error in selecting Max order_id_cafe_local was: ", err)
			next_return_id = 1
		else:
			try:
				with conn_local_db:
					c.execute("""INSERT INTO cup_returns VALUES (
							:cup_return_id,
							:global_return_id,
							:cup_rfid,
							:return_attempts,
							:cup_success_code,
							:return_datetime,
							:bin_section)""", {'cup_return_id': next_return_id, 'global_return_id': global_return_id, 'cup_rfid': cup_rfid, 'return_attempts': return_attempts, 'cup_success_code': cup_success_code, 'return_datetime': return_datetime, 'bin_section': bin_section})
					print("I inserted an return with next_return_id: ", next_return_id)
					print("Last local return id was (last_return_id) used in the 'order class' object: ", last_return_id)
					print("The new local return id after update from localised db is: ",next_return_id)
					return True                                  # may need double == if this fails to update order id
			except sqlite3.Error as err:
				print("Error in inserting new cup return was: ", err)
			#print("Double check last row id: ", c.lastrowid)
		finally:
			conn_local_db.commit()
			conn_local_db.close()
			
	def insert_new_action(self, action_code, action_text, action_datetime):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		#return False
		try:
			with conn_local_db:
				c.execute("SELECT MAX(action_id) FROM action_log_table")
				last_action_id = c.fetchone()
				# 0 take the first value of the turple which is returned (getting error here when applying in return statement...)
				print("Last_order_id: ", last_action_id[0])
				if last_action_id[0] == 0:
					next_action_id = 1
				elif last_action_id[0] == None:
					next_action_id = 1
				else:
					next_action_id = last_action_id[0] + 1
				print("The next order id is: ", next_action_id)
		except sqlite3.Error as err:
			print("The error in selecting Max order_id_cafe_local was: ", err)
			next_action_id = 1
		else:
			try:
				with conn_local_db:
					c.execute("""INSERT INTO action_log_table VALUES (
							:action_id,
							:action_code,
							:action_text,
							:action_datetime)""", {'action_id': next_action_id, 'action_code': action_code, 'action_text': action_text, 'action_datetime': action_datetime})
					print("I inserted an action with action_id: ", next_action_id)
					print("Last action id was (action_id) used in the 'order class' object: ", last_action_id)
					print("The new action id after update from localised db is: ",next_action_id)
					#return True                                  # may need double == if this fails to update order id
			except sqlite3.Error as err:
				print("Error in inserting new action was: ", err)
			print("Double check last row id: ", c.lastrowid)
		finally:
			conn_local_db.commit()
			conn_local_db.close()
		
	def insert_new_station_attributes_set(self, station_global_id, station_global_name, station_nickname, Bin_A_Capacity, Bin_A_Cups, Bin_B_Capacity,
											Bin_B_Cups, Bin_Q_Capacity, Bin_Q_Cups, Bin_A_last_collection, Bin_B_last_collection, Bin_Q_last_collection,
											Last_station_reset, Last_micro_controller_reset, Last_software_reset, software_version, last_error_time,
											last_error_code, last_cup_return_time, last_cup_return_bin, last_rfid_returned, rfid_status, load_cell_status, laser_status,
											RFID_trolley_status, main_trolley_status, trap_door_status, customer_door_status, Bin_A_Status, Bin_B_Status, Bin_Q_Status):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		try:
			with conn_local_db:
				c.execute("SELECT MAX(station_key) FROM station_attribute_table")
				last_station_id = c.fetchone()
				# 0 take the first value of the turple which is returned (getting error here when applying in return statement...)
				print("station_key: ", last_station_id[0])
				if last_station_id[0] == 0:
					next_station_id = 1
				elif last_station_id[0] == None:
					next_station_id = 1
				else:
					next_station_id = last_station_id[0] + 1
				print("The next station id is: ", next_station_id)
		except sqlite3.Error as err:
			print("The error in selecting Max station_key was: ", err)
			next_station_id = 1
			return False
		else:
			try:
				with conn_local_db:
					c.execute("""INSERT INTO station_attribute_table VALUES (
							:station_key,
							:station_global_id,
							:station_global_name,
							:station_nickname,
							:Bin_A_Capacity,
							:Bin_A_Cups,
							:Bin_B_Capacity,
							:Bin_B_Cups,
							:Bin_Q_Capacity,
							:Bin_Q_Cups,
							:Bin_A_last_collection,
							:Bin_B_last_collection,
							:Bin_Q_last_collection,
							:Last_station_reset,
							:Last_micro_controller_reset,
							:Last_software_reset,
							:software_version,
							:last_error_time,
							:last_error_code,
							:last_cup_return_time,
							:last_cup_return_bin,
							:last_rfid_returned,
							:rfid_status,
							:load_cell_status,
							:laser_status,
							:RFID_trolley_status,
							:main_trolley_status,
							:trap_door_status,
							:customer_door_status,
							:Bin_A_Status,
							:Bin_B_Status,
							:Bin_Q_Status)""", {'station_key': next_station_id, 'station_global_id': station_global_id, 'station_global_name': station_global_name, 'station_nickname': station_nickname, 'Bin_A_Capacity': Bin_A_Capacity, 'Bin_A_Cups': Bin_A_Cups, 'Bin_B_Capacity': Bin_B_Capacity, 'Bin_B_Cups': Bin_B_Cups, 'Bin_Q_Capacity': Bin_Q_Capacity, 'Bin_Q_Cups': Bin_Q_Cups, 'Bin_A_last_collection': Bin_A_last_collection, 'Bin_B_last_collection': Bin_B_last_collection, 'Bin_Q_last_collection': Bin_Q_last_collection, 'Last_station_reset': Last_station_reset, 'Last_micro_controller_reset': Last_micro_controller_reset, 'Last_software_reset': Last_software_reset, 'software_version': software_version, 'last_error_time': last_error_time, 'last_error_code': last_error_code, 'last_cup_return_time': last_cup_return_time, 'last_cup_return_bin': last_cup_return_bin, 'last_rfid_returned': last_rfid_returned, 'rfid_status': rfid_status, 'load_cell_status': load_cell_status, 'laser_status':laser_status, 'RFID_trolley_status': RFID_trolley_status, 'main_trolley_status': main_trolley_status, 'trap_door_status': trap_door_status, 'customer_door_status': customer_door_status, 'Bin_A_Status': Bin_A_Status, 'Bin_B_Status': Bin_B_Status, 'Bin_Q_Status': Bin_Q_Status})
					print("I inserted an bean drop station attribute dataset with station key: ", next_station_id)
					print("Last local bean drop station attribute dataset was used in the object: ", last_station_id)
					print("The new local bean drop station attribute dataset after update from localised db is: ",next_station_id)
					return True                                  # may need double == if this fails to update order id
			except sqlite3.Error as err:
				print("Error in inserting new cup return was: ", err)
				return False
			print("Double check last row id: ", c.lastrowid)
		finally:
			conn_local_db.commit()
			conn_local_db.close()

	def update_station_attribute_value(self, attribute, new_value):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		variables = ("UPDATE station_attribute_table SET '",attribute,"' = ? WHERE `station_key` = 1;")
		execute_string = "".join(variables)
		try:
			with conn_local_db:
				c.execute(execute_string,(new_value,))
				print("I updated a bean drop station attribute, ", attribute, ": ", new_value)
				return True                                  # may need double == if this fails to update order id
		except sqlite3.Error as err:
			print("Error in inserting new cup return was: ", err)
			return False
		finally:
			conn_local_db.commit()
			conn_local_db.close()
			
	def get_bean_drop_station_attribute_values(self):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		try:
			with conn_local_db:
				c.execute("SELECT * FROM station_attribute_table WHERE `station_key` = 1;")
				return c.fetchone()                                   # may need double == if this fails to update order id
		except sqlite3.Error as err:
			print("Error in inserting new cup return was: ", err)
			return False
		finally:
			conn_local_db.close()
			
	def create_photo_database_table(self):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		try:
			with conn_local_db:
				c.execute("""CREATE TABLE cup_return_images (
						cup_return_id integer,
						cup_image_name text,
						download_status integer,
						download_date_time datetime,
						PRIMARY KEY (cup_return_id),
						UNIQUE (cup_image_name)
						)""")
				conn_local_db.commit()
				conn_local_db.close()
				print("New table successfully built into cup_return_image_database.db")
		except sqlite3.Error as err:
			print("The error in creating table in database was: ", err)
			
	def store_cup_photo(self, cup_return_id, cup_image_name):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		try:
			with conn_local_db:
				c.execute("""INSERT INTO cup_return_images VALUES (
						:cup_return_id,
						:cup_image_name,
						:download_status,
						:download_date_time)""", {'cup_return_id': cup_return_id, 'cup_image_name': cup_image_name, 'download_status': 0, 'download_date_time':""})
				print("I inserted an cup return photo into cup_return_image_database with the name: ", cup_image_name)
				return True                                  # may need double == if this fails to update order id
		except sqlite3.Error as err:
			print("Error in inserting new cup return  image was: ", err)
			return False
		finally:
			conn_local_db.commit()
			conn_local_db.close()
			
	def update_photo_download_status(self, download_status, date_time, cup_return_id):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		try:
			with conn_local_db:
				variables_set = (download_status, date_time, cup_return_id)
				update_cup_image_download_status_query = "UPDATE `cup_return_images` SET `download_status` = ? , `download_date_time` = ? WHERE `cup_image_name` = ?;"
				#UPDATE `cup_db` SET `OWNER_ID`= %s,`Number_of_uses`=`Number_of_uses`+1 ,`Last_use`=%s WHERE `RFID_UID` = %s;"
				c.execute(update_cup_image_download_status_query,(download_status, date_time, cup_return_id))
				conn_local_db.commit()
				return "update_photo_download_status completed method..."
		except Exception as err:
			print("Error in updating photo download status was: ", err)
			return False
		finally:
			conn_local_db.close()
			
	def fetchall_cup_image_table(self):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		try:
			with conn_local_db:
				c.execute("SELECT * FROM `cup_return_images`;")
				return c.fetchall()
		except Exception as err:
			print("Error in updating photo download status was: ", err)
			return False
		finally:
			conn_local_db.close()
			
	def last_cup_return_id(self):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		try:
			with conn_local_db:
				c.execute("SELECT MAX(cup_return_id) FROM cup_returns")
				last_return_id = c.fetchone()
				return last_return_id
		except Exception as err:
			print("Error finding last cup return id was: ", err)
			return False
		finally:
			conn_local_db.close()
			
	def admin_reset_cup_image_table(self):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		try:
			with conn_local_db:
				c.execute("DELETE FROM `cup_return_images`;")
				conn_local_db.commit()
		except Exception as err:
			print("Error in updating photo download status was: ", err)
			return False
		finally:
			conn_local_db.close()
			
	def create_photo_transfer_database_table(self, transfer_database_file):
		conn_local_db2 = sqlite3.connect(transfer_database_file)
		c2 = conn_local_db2.cursor()
		try:
			with conn_local_db2:
				c2.execute("""CREATE TABLE cup_return_images (
						cup_return_id integer,
						cup_image_name text,
						download_status integer,
						download_date_time datetime,
						PRIMARY KEY (cup_return_id),
						UNIQUE (cup_image_name)
						)""")
				conn_local_db2.commit()
				
				print("New table successfully built into cup_return_image_database.db")
		except sqlite3.Error as err:
			print("The error in creating table in database was: ", err)
		finally:
			conn_local_db2.close()
			
	def append_transfer_database(self, cup_return_id, cup_image_name, download_status, download_date_time, transfer_database_file):
		conn_local_db2 = sqlite3.connect(transfer_database_file)
		c2 = conn_local_db2.cursor()
		try:
			with conn_local_db2:
				c2.execute("""INSERT INTO cup_return_images VALUES (
						:cup_return_id,
						:cup_image_name,
						:download_status,
						:download_date_time)""", {'cup_return_id': cup_return_id, 'cup_image_name': cup_image_name, 'download_status': 1, 'download_date_time':download_date_time})
				print("I inserted an cup return photo into cup_return_image_database with the name: ", cup_image_name)
				return True                                  # may need double == if this fails to update order id
		# except sqlite3.Error as err:
			# print("Error in inserting new cup return  image was: ", err)
			# return False
		except sqlite3.Error as e:
			print(e)
			print("exception to table not existing was:", e)
			try:
				print("trying to create new database table...")
				self.create_photo_transfer_database_table(transfer_database_file)
				try:
					with conn_local_db2:
						c2.execute("""INSERT INTO cup_return_images VALUES (
								:cup_return_id,
								:cup_image_name,
								:download_status,
								:download_date_time)""", {'cup_return_id': cup_return_id, 'cup_image_name': cup_image_name, 'download_status': 1, 'download_date_time':download_date_time})
						print("I inserted an cup return photo into cup_return_image_database with the name: ", cup_image_name)
						return True                                  # may need double == if this fails to update order id
				except sqlite3.Error as err:
					print("Error in inserting new cup return after creating a new table was...: ", err)
					return False
			except Exception as err:
					print("Error in creating new table was..: ", err)
					return False
		finally:
			conn_local_db2.commit()
			conn_local_db2.close()
			
			
	def format_download(self):
		print("test")
		
			
	def download_camera_photos_from_bd_station(self, media_drive, date_time, transfer_database_file):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		cwd_retrieve = os.getcwd()
		picture_directory = str(cwd_retrieve) + "/Cup_photo_folder" #Appends string to GUI_Sounds directory
		try:
			with conn_local_db:
				c.execute("SELECT `cup_image_name` FROM `cup_return_images` WHERE `download_status` = 0;")
				undownloaded_photo_list = c.fetchall()
				# for images in undownloaded_photo_list:
					# print(images[0])
					# print("just printed list within list stuff....")
				print("This is the new super fetchall list of undownloaded photos",undownloaded_photo_list)
				c.execute("SELECT * FROM `cup_return_images` WHERE `download_status` = 0;")
				undownloaded_photo__details_list = c.fetchall()
				for images in undownloaded_photo__details_list:
					print(images[0])
					print(images[1])
					print(images[2])
					print(images[3])
					print("just printed all of the datails list within list stuff....")				
				
				for image in undownloaded_photo__details_list:
					#formatted_image_name = str(image)[2:-3]
					formatted_image_name = image[1]
					args_list = ["sudo cp ", formatted_image_name, " /media/pi/", media_drive, formatted_image_name]
					shell_command = ''.join([str(item) for item in args_list])
					print(shell_command)
					#p3 = subprocess.run([shell_command], cwd = picture_directory, shell=True, capture_output=True,text=True)
					p3 = subprocess.run([shell_command], cwd = picture_directory, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
					if p3.stdout != "":
						print("The standard output is: ", p3.stdout)
					print("The standard error is: ",p3.stderr)
					if p3.stderr != "":
						print("captured error below")
						print(p3.stderr)
						print("standard error above:")
						break
					elif p3.stderr == "":
						download_status_variables = (1,date_time,formatted_image_name)
						download_status_result = self.update_photo_download_status(1,date_time,formatted_image_name)
						print(download_status_result)
						setup_result = self.fetchall_cup_image_table
						print(setup_result())
						try:
							print("attempting to append to new database")
							self.append_transfer_database(image[0], formatted_image_name, 1, date_time, transfer_database_file)
						except Exception as e:
								print(e)
						# except sqlite3.DatabaseError as e:
							# print("this was a database eror with the error code:")
						#self.append_transfer_database()
					
		except Exception as e:
			print(e)
		finally:
			conn_local_db.commit()
			conn_local_db.close()
		


def insert_new_cup_return(database, global_return_id, cup_rfid, return_attempts, cup_success_code, return_datetime, bin_section):
	conn_local_db = sqlite3.connect(database)
	c = conn_local_db.cursor()
	try:
		with conn_local_db:
			c.execute("SELECT MAX(cup_return_id) FROM cup_returns")
			last_return_id = c.fetchone()
			# 0 take the first value of the turple which is returned (getting error here when applying in return statement...)
			print("Last_order_id: ", last_return_id[0])
			if last_return_id[0] == 0:
				next_return_id = 1
			elif last_return_id[0] == None:
				next_return_id = 1
			else:
				next_return_id = last_return_id[0] + 1
			print("The next order id is: ", next_return_id)
	except sqlite3.Error as err:
		return ("The error in selecting Max order_id_cafe_local was: ", err)
		next_return_id = 1
	except Exception as e:
		return e
	else:
		try:
			with conn_local_db:
				c.execute("""INSERT INTO cup_returns VALUES (
						:cup_return_id,
						:global_return_id,
						:cup_rfid,
						:return_attempts,
						:cup_success_code,
						:return_datetime,
						:bin_section)""", {'cup_return_id': next_return_id, 'global_return_id': global_return_id, 'cup_rfid': cup_rfid, 'return_attempts': return_attempts, 'cup_success_code': cup_success_code, 'return_datetime': return_datetime, 'bin_section': bin_section})
				print("I inserted an return with next_return_id: ", next_return_id)
				print("Last local return id was (last_return_id) used in the 'order class' object: ", last_return_id)
				print("The new local return id after update from localised db is: ",next_return_id)
				return True                                  # may need double == if this fails to update order id
		except sqlite3.Error as err:
			print("Error in inserting new cup return was: ", err)
		#print("Double check last row id: ", c.lastrowid)
	finally:
		conn_local_db.commit()
		conn_local_db.close()

def last_cup_return_id(database):
		conn_local_db = sqlite3.connect(database)
		c = conn_local_db.cursor()
		try:
			with conn_local_db:
				c.execute("SELECT * FROM cup_returns")
				last_return_id = c.fetchall()
				return last_return_id
		except Exception as err:
			print("Error finding last cup return id was: ", err)
			return False
		finally:
			conn_local_db.close()




def main():
	
	import datetime
	
	def datetime_formatted():
		return datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
		
	date_time_now = datetime_formatted()
	print(date_time_now)
		
	local_station_db = bean_drop_station_database("local_db_test.db")
	
	
	#----------------------------------------------
	#local_station_db.insert_new_cup_return(1236,78954,1,1,date_time_now,"A")
	#local_station_db.last_cup_return_id()
	#-------------------------------------
		
if __name__ == '__main__':
	print("INSERTING NEW CUP RETURN BELOW--------------")
	
	try:
		main()
	except KeyboardInterrupt:
		gpio.cleanup()
		sys.exit(0)
