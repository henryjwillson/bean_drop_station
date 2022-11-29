# Cup camera Bean Drop Station re

from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import os
import subprocess
import math
import logging
    #process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
# construct the argument parser and parse the arguments

class bd_station_cup_camera_class():
	
	def __init__(self,database):
		self.database = database
		
	def take_webcam_photo(self, cup_return_id):
		cwd_retrieve = os.getcwd()
		picture_directory = str(cwd_retrieve) + "/Cup_photo_folder" #Appends string to Cup_photo_folder directory
		args_list = ["fswebcam -r 1280x720 --no-banner -v -S 5 -F 5 ", cup_return_id, "_image.jpg"]				# -S is skipping frames and -F is the number of frames to combine to make a single image. Multiple frames combined to make single image avoids image capture failures which produce a single black screen
		args = ''.join([str(item) for item in args_list])
		#p1 = subprocess.run([args], cwd = picture_directory, shell=True)
		p2 = subprocess.Popen([args], cwd = picture_directory, shell=True, stdout = subprocess.PIPE)
		subprocess_return = p2.stdout.read()
		print("this is subprocess stdout: ", subprocess_return)
		
	def take_cup_photo_and_add_to_database(self):
		print("this is the last cup return id...",self.database.last_cup_return_id())
		cup_return_id = self.database.last_cup_return_id()[0] + 1
		self.take_webcam_photo(cup_return_id)
		name_builder_list = [ cup_return_id, "_image.jpg"]
		name_builder = ''.join([str(item) for item in name_builder_list])
		self.database.store_cup_photo(cup_return_id, name_builder)

def take_cup_photo():
	
	cwd_retrieve = os.getcwd()      # Command to retrieve current working directory of this python program

	success_parameter = False
	# ap =  argparse.ArgumentParser()
	# ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
							# help="path to output CSV file containing barcodes")
	# args = vars(ap.parse_args())
	
	resolution = (720, 1280)
	
	#start initialising of video reader
	print("[INFO] starting video stream...")
	# vs = VideoStream(src=0).start()
	vs = VideoStream(src=0, resolution=resolution).start()
	time.sleep(2.0)
	
	while True:
		frame = vs.read()
		frame = imutils.resize(frame, width=500)
		cv2.imshow("Barcode Scanner", frame)
		key = cv2.waitKey(1) & 0xFF
	time.sleep(10)
	csv.close()
	cv2.destroyAllWindows()
	vs.stop()

def take_webcam_photo(cup_return_id):
	cwd_retrieve = os.getcwd()
	picture_directory = str(cwd_retrieve) + "/Cup_photo_folder" #Appends string to Cup_photo_folder directory
	args_list = ["fswebcam -r 1280x720 --no-banner -v -S 5 -F 5 ", cup_return_id, "_image.jpg"]				# -S is skipping frames and -F is the number of frames to combine to make a single image. Multiple frames combined to make single image avoids image capture failures which produce a single black screen
	args = ''.join([str(item) for item in args_list])
	p2 = subprocess.Popen([args], cwd = picture_directory, shell=True, stdout = subprocess.PIPE)
	subprocess_return = p2.stdout.read()
	print("this is subprocess stdout: ", subprocess_return)
	
	
# def create_photo_database():
	# conn_local_db = sqlite3.connect('cup_return_image_database.db')
	# c = conn_local_db.cursor()
	# try:
		# with conn_local_db:
			# c.execute("""CREATE TABLE cup_return_images (
					# cup_return_id integer,
					# cup_image_name text,
					# download_status integer,
					# download_date_time datetime,
					# PRIMARY KEY (cup_return_id),
					# UNIQUE (cup_image_name)
					# )""")
			# print("New table successfully built into cup_return_image_database.db")
	# except sqlite3.Error as err:
		# print("The error in creating table in database was: ", err)
			
# def store_cup_photo(cup_return_id, cup_image_name):
	# conn_local_db = sqlite3.connect('cup_return_image_database.db')
	# c = conn_local_db.cursor()
	# try:
		# with conn_local_db:
			# c.execute("""INSERT INTO cup_return_images VALUES (
					# :cup_return_id,
					# :cup_image_name,
					# :download_status)""", {'cup_return_id': cup_return_id, 'cup_image_name': cup_image_name, 'download_status': 0)
			# print("I inserted an cup return photo into cup_return_image_database with the name: ", cup_image_name)
			# return True                                  # may need double == if this fails to update order id
	# except sqlite3.Error as err:
		# print("Error in inserting new cup return  image was: ", err)
		# return False


# def update_photo_download_status(variables)
	# conn_local_db = sqlite3.connect('cup_return_image_database.db')
	# c = conn_local_db.cursor()
	# try:
		# with conn_local_db:
			# bluehost_update_user_from_order = "UPDATE `cup_return_images` SET `download_status`= %s, `download_date_time`= %s WHERE `cup_return_id` = %s;"
			# c1.execute(update_cup_data_query,(variables))
	# except sqlite3.Error as err:
		# print("Error in updating photo download status was: ", err)
		# return False

def download_camera_photos(database, media_drive):
	cwd_retrieve = os.getcwd()
	picture_directory = str(cwd_retrieve) + "/Cup_photo_folder" #Appends string to GUI_Sounds directory
	p3 = subprocess.run(['sudo cp image3.jpg /media/pi/THE\ ORANGE\ BOX/image3.jpg'], cwd = picture_directory, shell=True)
	

def download_camera_photos_hard_drive(self, media_drive, date_time):
		conn_local_db = sqlite3.connect(self.database_file)
		c = conn_local_db.cursor()
		cwd_retrieve = os.getcwd()
		picture_directory = str(cwd_retrieve) + "/Cup_photo_folder" #Appends string to GUI_Sounds directory
		try:
			with conn_local_db:
				c.execute("SELECT `cup_image_name` FROM `cup_return_images` WHERE `download_status` = 0;")
				undownloaded_photo_list = c.fetchall()
				print(len(undownloaded_photo_list))
				for image in undownloaded_photo_list:
					formatted_image_name = str(image)[2:-3]
					args_list = ["sudo cp ", formatted_image_name, " /media/pi/", media_drive, formatted_image_name]
					shell_command = ''.join([str(item) for item in args_list])
					print(shell_command)
					p3 = subprocess.run([shell_command], cwd = picture_directory, shell=True, capture_output=True,text=True)
					print("The standard output is: ",p3.stdout)
					if p3.stdout == None or p3.stdout == "" or p3.stdout == " b''":
						print("captured standard output when its printing nothing")
					print("The standard error is: ",p3.stderr)
					if p3.stderr != None or p3.stderr != "" or p3.stderr != " b''":
						print("captured error")
						break
					download_status_variables = (1,date_time,formatted_image_name)
					download_status_result = self.update_photo_download_status(1,date_time,formatted_image_name)
					print(download_status_result)
					setup_result = self.fetchall_cup_image_table
					print(setup_result())
		except Exception as e:
			print(e)
		finally:
			conn_local_db.commit()
			conn_local_db.close()


if __name__ == "__main__":
	#take_cup_photo()
	take_webcam_photo(1)
	take_webcam_photo(2)
	take_webcam_photo(3)
	take_webcam_photo(4)
	take_webcam_photo(5)
	take_webcam_photo(7)
	take_webcam_photo(7)
	take_webcam_photo(8)
	take_webcam_photo(9)
	#download_camera_photos()
