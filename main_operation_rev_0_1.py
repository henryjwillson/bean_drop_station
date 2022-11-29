'''''
Complete program for Bean Drop Stations
'''

from tkinter import *
from PIL import Image, ImageTk
import smbus
import time
import random
import datetime
import sys
import os
import subprocess
from multiprocessing import Process, Pipe
import _thread, queue
from pynput.keyboard import Key, Controller
from pynput import keyboard


import RPi.GPIO as GPIO
from gpiozero import LED
from gpiozero import Button as GPIOButton #Changing to allow tkinter Button Class and prevent clash

from examples.epd_7in5_V2_test import e_paper_display_class
from Bean_drop_station_status_attributes import Bean_drop_station_status_attributes		#Importing attributes class.
from Bean_drop_station_cup_return_class import cup_return_attributes					#Importing the cup return class
from Bean_drop_station_local_database import bean_drop_station_database					#Importing the local database class
from Bean_drop_station_error_classes import customer_error_database_entry				#Importing the customer_error_database_entry class
from beandrop_station_raspi_mqtt_communication import sms_module_serial_communication
from passlib_authentication_module import *
from cup_camera_program import *
from Frame_Sizing_Class import Frame_Sizing
main_frame_size = Frame_Sizing(1024,600)


# Setting up mqtt communication class -------------------------------------------------------------------------------------------------------------------------
mqtt_send = sms_module_serial_communication(115200, 1)

mqtt_queue = queue.Queue()

def mqtt_queue_worker():
	while True:
		#Check Sim Module is Ready:
		try:
			new_item = mqtt_queue.get()
			sim_module_status = False
			while not sim_module_status:
				sim_module_status = mqtt_send.check_sim_module_status
				if sim_module_status:
					print("Sim module ready for new mqtt publish message")
					try:
						item = new_item
						print(item)
						print(item[:2],item[2],item[3:])
						mqtt_send.send_mqtt_cup_return(item[:2],item[2],item[3:])
					except Exception as e:
						print("mqtt_queue_worker raised an exception",e)
				else:
					# Sending last sent message again
					try:
						mqtt_send.send_mqtt_cup_return(item[:2],item[2],item[3:])
					except Exception as e:
						print("mqtt_queue_worker raised an exception",e)
		except Exception as e:
			print("mqtt_queue_worker raised an exception",e)


# Image Processing For HDMI GUI--------------------------------------------------------------------------------------------------------------------------------------------

# Images must be instigated in tk after tk opened later on
# Beandrop Logo Icon
beandrop_logo = Image.open("/home/pi/Pictures/homelogo.png")
# print(beandrop_logo.size)
beandrop_logo_new_crop = beandrop_logo.crop((210, 50, 590, 430))
# beandrop_logo_new_crop.show()
beandrop_logo_new_height = 300
# integer required for resize, not a float (float is a number with decimals)
beandrop_logo_new_width = int(beandrop_logo_new_height /
                              beandrop_logo_new_crop.height * beandrop_logo_new_crop.width)
beandrop_logo_new_size = beandrop_logo_new_crop.resize(
    (beandrop_logo_new_width, beandrop_logo_new_height))
beandrop_logo_new_size.show()


# Setting up e-paper display class test -----------------------------------------------
customer_display = e_paper_display_class(50)
customer_display.home_screen_logo()
_thread.start_new_thread(customer_display.screen_updating,())

# Initialising Sound Output-------------------------------------------------------------------
cwd_retrieve = os.getcwd()      # Command to retrieve current working directory of this python program
music_directory = str(cwd_retrieve) + "/Station_GUI_Sounds" #Appends string to GUI_Sounds directory

def run_sound_command(selected_command, child_pipe):
	music_time = 1
	if selected_command == "Thank_you_giant_leap_for_mankind":
		p1 = subprocess.Popen(["omxplayer -o alsa Thank_you_giant_leap_for_mankind.mp3"], cwd = music_directory, shell=True, stdin=subprocess.PIPE)
		music_time = 700
	elif selected_command == "Error_cup_overweight_excess_liquid":
		p1 = subprocess.Popen(["omxplayer -o alsa Error_cup_overweight_excess_liquid.mp3"], cwd = music_directory, shell=True, stdin=subprocess.PIPE)
		music_time = 1300
	elif selected_command == "Error_excess_weight_basic":
		p1 = subprocess.Popen(["omxplayer -o alsa Error_excess_weight_basic.mp3"], cwd = music_directory, shell=True, stdin=subprocess.PIPE)
		music_time = 700
	elif selected_command == "Error_non_bean_drop_cup":
		p1 = subprocess.Popen(["omxplayer -o alsa Error_non_bean_drop_cup.mp3"], cwd = music_directory, shell=True, stdin=subprocess.PIPE)
		music_time = 800
	elif selected_command == "Error_slieght_underweight_attatch_lid_and_sleeve":
		p1 = subprocess.Popen(["omxplayer -o alsa Error_slieght_underweight_attatch_lid_and_sleeve.mp3"], cwd = music_directory, shell=True, stdin=subprocess.PIPE)
		music_time = 800
	elif selected_command == "Error_we_cant_find_lid_press_blue_to_comfirm_loss":
		p1 = subprocess.Popen(["omxplayer -o alsa Error_we_cant_find_lid_press_blue_to_comfirm_loss.mp3"], cwd = music_directory, shell=True, stdin=subprocess.PIPE)
		music_time = 1000
	elif selected_command == "Quarantine_question_for_customer":
		p1 = subprocess.Popen(["omxplayer -o alsa Quarantine_question_for_customer.mp3"], cwd = music_directory, shell=True, stdin=subprocess.PIPE)
		music_time = 2500
	elif selected_command == "RFID_error_basic_contact_bean_drop_request":
		p1 = subprocess.Popen(["omxplayer -o alsa RFID_error_basic_contact_bean_drop_request.mp3"], cwd = music_directory, shell=True, stdin=subprocess.PIPE)
		music_time = 700
	elif selected_command == "RFID_error_place_cup_correctly_instructions":
		p1 = subprocess.Popen(["omxplayer -o alsa RFID_error_place_cup_correctly_instructions.mp3"], cwd = music_directory, shell=True, stdin=subprocess.PIPE)
		music_time = 1800
	elif selected_command == "Thank_You_Basic":
		p1 = subprocess.Popen(["omxplayer -o alsa Thank_You_Basic.mp3"], cwd = music_directory, shell=True, stdin=subprocess.PIPE)
		music_time = 300
	elif selected_command == "Thank_you_cup_saved_from_landfill_community_superstar":
		p1 = subprocess.Popen(["omxplayer -o alsa Thank_you_cup_saved_from_landfill_community_superstar.mp3"], cwd = music_directory, shell=True, stdin=subprocess.PIPE)
		music_time = 600
	elif selected_command == "Thank_You_Deposit_Returned_Ready_For_Next_Drink":
		p1 = subprocess.Popen(["omxplayer -o alsa Thank_You_Deposit_Returned_Ready_For_Next_Drink.mp3"], cwd = music_directory, shell=True, stdin=subprocess.PIPE)
		music_time = 4500
	elif selected_command == "Thank_You_One_Step_Towards_a_Healthier_Planet":
		p1 = subprocess.Popen(["omxplayer -o alsa Thank_You_One_Step_Towards_a_Healthier_Planet.mp3"], cwd = music_directory, shell=True, stdin=subprocess.PIPE)
		music_time = 700
	elif selected_command == "admin_elavator_music":
		p1 = subprocess.Popen(["omxplayer -o alsa --vol -2100 admin_elavator_music.mp3"], cwd = music_directory, shell=True, stdin=subprocess.PIPE)
		music_time = 12000
	elif selected_command == "help_instructions":
		#p1 = subprocess.run(["omxplayer -o alsa Help_Instructions.mp3 &"], cwd = music_directory, shell=True)
		p1 = subprocess.Popen(["omxplayer -o alsa Help_Instructions.mp3"], cwd = music_directory, shell=True, stdin=subprocess.PIPE)
		music_time = 4500
		
	for x in range(music_time):
		time.sleep(0.01)
		if child_pipe.poll():
			try:
				parent_msg = child_pipe.recv()
				print("parent message recieved!!!!")
				if parent_msg == "end_sound":
					keyboard = Controller()
					p1.terminate()
					p1.stdin.write(b'q')
					keyboard.press(Key.esc)
					keyboard.release(Key.esc)
					print("killed help process")
					break
			except Exception as e:
				print(e)
	sound_playback_queue.put("completed")
	child_pipe.send(True)
								 
run_sound_command_priority_dict = {
								"Thank_you_giant_leap_for_mankind":1,
								"Error_cup_overweight_excess_liquid":0,
								 "Error_excess_weight_basic":0,
								 "Error_non_bean_drop_cup":0,
								 "Error_slieght_underweight_attatch_lid_and_sleeve":0,
								 "Error_we_cant_find_lid_press_blue_to_comfirm_loss":1,
								 "Quarantine_question_for_customer":1,
								 "RFID_error_basic_contact_bean_drop_request":1,
								 "RFID_error_place_cup_correctly_instructions":0,
								 "Thank_You_Basic":1,
								 "Thank_you_cup_saved_from_landfill_community_superstar":1,
								 "Thank_You_Deposit_Returned_Ready_For_Next_Drink":1,
								 "Thank_You_One_Step_Towards_a_Healthier_Planet": 1,
								 "admin_elavator_music": 1,
								 "help_instructions":0}


sound_playback_queue = queue.Queue()

def sound_worker():
	pass
	# Hidden for commercial reasons. Uses Pipe, and queues with priority classifications to control the sound output on the bean drop station.
		
def time_from_sound_added_to_queue(sound_added_time):
	current_time = datetime_now()
	time_from_last_screen = current_time - sound_added_time
	return time_from_last_screen.total_seconds()

list_of_thank_you_messages = ["Thank_You_Basic","Thank_you_cup_saved_from_landfill_community_superstar","Thank_You_Deposit_Returned_Ready_For_Next_Drink","Thank_You_One_Step_Towards_a_Healthier_Planet","Thank_you_giant_leap_for_mankind"]

def play_random_thankyou(date_time_of_sound):
	random.shuffle(list_of_thank_you_messages)
	sound_item = (date_time_of_sound,list_of_thank_you_messages[1])
	print("Random thankyou added to sound queue...")
	sound_playback_queue.put(sound_item)
	cup_return_attributes.priority_sound_added = True

GPIO.setmode(GPIO.BCM)
# GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 21 to be input pin and set initial value to be pulled low (off)

# LS_Door = Button(17)
# timeout_signal_gpio = LED(0)
# button = Button(22)
# magnetic_lock = LED(10)
# LED_button_right = LED(11)
# LED_button_left = LED(9)

# Defining Raspi GPIO setup (I2C, SPI, UART, GPIO Zero etc)
#I2C
bus = smbus.SMBus(1)
arduino_due_address = (0x54)

Micro_controller_motor_switch = LED(4) #Relay switch to turn on motors and microcontroller power
LBag_reset_signal = GPIOButton(23)
Magnetic_lock_LED = LED(18)
#LBag_reset_button_LED = LED(5)	#Same as Left button out signal
RBag_reset_signal = GPIOButton(1)
#Rbag_reset_button = LED(7)	#Same as right button out signal
LButton1_press_signal_blue = GPIOButton(6)
LButton1_button_LED_blue = LED(5) # LBag_reset_button_LED is also connected to this output
LButton2_press_signal_orange = GPIOButton(19)
LButton2_button_LED_orange = LED(13)
RButton1_press_signal_green = GPIOButton(16)
RButton1_button_LED_green = LED(12) # Same as Rbag_reset_button
RButton2_press_signal_red = GPIOButton(21)
RButton2_button_LED_red = LED(20)
Sliding_door_limit_switch = GPIOButton(27)
Raspi_Arduino_timeout_signal = LED(22)
Raspi_blue_LED = LED(9)
Raspi_green_LED = LED(0)
Raspi_red_LED = LED(26)



# --------------- Help button worker ----------------------------
def help_button_worker():
	while True:
		if LButton2_press_signal_orange.is_pressed:
			date_time_now_of_sound = datetime_now()
			sound_item = (date_time_now_of_sound,"help_instructions")
			sound_playback_queue.put(sound_item)
			cup_return_attributes.priority_sound_added = True
			time.sleep(45)
			

# Setting out global variables that need either class functions or global variables assigned-----------------------------------
# Bin A current cups
# Bin A cup capacity
# Bin B current cups
# Bin B cup capacity
# Bin Q current cups
# Bin Q cup capacity
# Last Bin used

# Datetime of last Bin A collection
# Datetime of last Bin B collection
# Datetime of last Bin Q collection

# Datetime of last bin reset
# Datetime of last micro controller reset
# Datetime of last software update
# Software_version

# Datetime of last bin error
# Last error

# Datetime of last successful cup return
# Location (Bin) of last successful return
# RFID of last successful cup return

# -- operational status of equipment --
# RFID_trolley_status
# Main_trolley_status
# Trap_door_status
# Bin A Status
# Bin B Status
# Bin C Status
# RFID_status
# Load_cell_status
	

# Initialising local database -------------------------------------------------
local_station_db = bean_drop_station_database("local_db_test.db")

# Initialising error table in local database--------------------------------------
error_db = customer_error_database_entry("local_db_test.db",10)
error_db.admin_delete_error_log_table()
error_db.create_error_table()

# Bean Drop Station Attributes Class initiation ---------------------------------
# Input import local db bean drop attributes class on initiation

Local_station_attributes_class = Bean_drop_station_status_attributes(100,0,100,0,10,0,0,0,0,0,0,0,1.0,0,0,0,"Bin_A",0,True,True,False,True,"BinATrue","ClosedTrue",True,True,True,False)

def get_local_station_db_attributes(local_db_class, attributes_class):
	attributes = local_db_class.get_bean_drop_station_attribute_values
	attributes_class.Bin_A_Capacity = attributes()[4]
	attributes_class.Bin_A_Cups = attributes()[5]
	attributes_class.Bin_B_Capacity = attributes()[6]
	attributes_class.Bin_B_Cups = attributes()[7]
	attributes_class.Bin_Q_Capacity = attributes()[8]
	attributes_class.Bin_Q_Cups = attributes()[9]
	attributes_class.Bin_A_last_collection = attributes()[10]
	attributes_class.Bin_B_last_collection = attributes()[11]
	attributes_class.Bin_Q_last_collection = attributes()[12]
	attributes_class.Last_station_reset = attributes()[13]
	attributes_class.Last_micro_controller_reset = attributes()[14]
	attributes_class.Last_software_reset = attributes()[15]
	attributes_class.software_version = attributes()[16]
	attributes_class.last_error_time = attributes()[17]
	attributes_class.last_error_code = attributes()[18]
	attributes_class.last_cup_return_time = attributes()[19]
	attributes_class.last_cup_return_bin = attributes()[20]
	attributes_class.last_rfid_returned = attributes()[21]
	attributes_class.rfid_status = attributes()[22]
	attributes_class.load_cell_status = attributes()[23]
	attributes_class.laser_status = attributes()[24]
	attributes_class.RFID_trolley_status = attributes()[25]
	attributes_class.main_trolley_status = attributes()[26]
	attributes_class.trap_door_status = attributes()[27]
	attributes_class.customer_door_status = attributes()[28]
	attributes_class.Bin_A_Status = attributes()[29]
	attributes_class.Bin_B_Status = attributes()[30]
	attributes_class.Bin_Q_Status = attributes()[31]
    
print(Local_station_attributes_class.current_status)
get_local_station_db_attributes(local_station_db, Local_station_attributes_class)
print("\n Attributes grabbed from local database \n")
print(Local_station_attributes_class.current_status)


# initialising bd_station_cup_camera_class -----------------------------------------------------------------------------
entry_port_camera = bd_station_cup_camera_class(local_station_db)


# datetime used for storage in old online databaseftr
def datetime_formatted():
		return datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')

# Datetime now version used for addition and subtraction of times		
def datetime_now():
	return datetime.datetime.now()
	
def unique_scan_action_number():
	new_time = str(datetime_now())
	variables = (new_time,"random")
	new_unique_hash = combined_variables_hash(variables)
	return new_unique_hash
	

new_date_time_now = datetime_formatted()
int_new_date_time_now = datetime_now()
setup_result = local_station_db.update_station_attribute_value("last_error_time",new_date_time_now)


get_local_station_db_attributes(local_station_db, Local_station_attributes_class)
print("\n Attributes grabbed from local database \n")
print(Local_station_attributes_class.current_status)


def half_second_timer():
	while True:
		#print("timer tick")
		time.sleep(0.5)

#---- Cup Return Attributes class initiasation ------------------------------------------

current_return_attributes = cup_return_attributes(0,0,0,0,0,False,True,0,0,0,0,0,0,"welcome to bean drop", 30, False, False, False, False, int_new_date_time_now, 1000, False, False, True) #6th value is laser result left as True until laser is implemented in arduino
test_value = current_return_attributes.main_text
print("Test value is...:",test_value)

#-----------------------------------------


### Add special time periods ------------------------------ 

quick_turnaround_time = 10

def time_from_last_rfid():
	current_time = datetime_now()
	datetimeobj=datetime.datetime.strptime(Local_station_attributes_class.last_cup_return_time,"%d-%m-%Y %H:%M:%S")
	# time_between_last_scan = current_time - Local_station_attributes_class.last_cup_return_time
	time_between_last_scan = current_time - datetimeobj
	#print("Last RFID was scanned ", time_between_last_scan.total_seconds(), " seconds ago")
	if time_between_last_scan.total_seconds() < quick_turnaround_time:
		print("use quick turnaround microcontroller moves")
		return("quick_turnaround")
	else:
		# print("use slower command if availible")
		return("normal_turnaround")
		
def time_from_last_screen(last_screen_time):
	current_time = datetime_now()
	time_from_last_screen = current_time - last_screen_time
	return time_from_last_screen.total_seconds()
	
def reset_screen_timer_check_worker():
	while True:
		time_interval = 0
		while time_interval < current_return_attributes.time_on_screen:
			time.sleep(0.25)
			#print("time_interval is: ", time_interval)
			#print("Time on screen is: ",current_return_attributes.time_on_screen)
			time_interval = time_from_last_screen(current_return_attributes.last_screen_update_datetime)
		current_return_attributes.reset_GUI()
		current_return_attributes.last_screen_update_datetime = datetime_now()
		current_return_attributes.update_screen_value = True


def LED_flash(LED, flash_count, flashes_per_second):
	for repeat in range(flash_count):
		LED.on()
		time.sleep(1/flashes_per_second)
		LED.off()
		time.sleep(1/flashes_per_second)

def timeout_signal():
	print("time_out is on")
	Raspi_Arduino_timeout_signal.on()
	time.sleep(0.25)
	#time.sleep(2)		#increased in an attempt to fix the rfid section which isn't timing out...
	Raspi_Arduino_timeout_signal.off()
	print("time_out is off")

# List of micro_controller commands---------------------------------------------

# 15 - RFID Motor - Accel Stepper to limit switch (sliding door open - cup dropped through)
# 16 - RFID Motor - Accel Stepepr to limit switch (sliding door closed)
# 17 - Trolley Motor - Accel Stepper to Bin B limit switch
# 18 - Trolley Motor - Accel Stepper Bin B to Bin A limit switch (home)
# 19 - Trolley Motor - Accel Stepper Bin Q to Bin A limit switch (home)
# 20 - Trap Door Motor - Accel Stepper Open Door to limit switch
# 21 - Trap Door Motor - Accel Stepper Close Door to limit switch
# 22 - Load Cell Calibration Command 1 - Tarring Scale
# 23 - Load Cell Calibration Command 2 - Calibrate Scale
# 24 - Load Cell - Take weight measurement
# 34 - Load Cell - Take weight measurement on pre-defined scale
# 25 - RFID Motor - Homing command - Constant speed to limit switch (sliding door open - cup dropped through)
# 26 - RFID Motor - Homing command - Constant speed to limit switch (sliding door closed)
# 27 - Trolley Motor - Homing command - Constant speed to Bin B limit switch
# 28 - Trolley Motor - Homing command - Constant speed to Bin A limit switch
# 29 - Trap Door Motor - Homing command - Constant speed Open Door to limit switch
# 30 - Trap Door Motor - Homing command - Constant speed Close Door to limit switch
# 41 - Sliding_door_Motor

#-------------------------------------------------------------------------------

class micro_controller_commands:
	'''Class lays out command groups - command groups are microcontroller commands with their paired / linked commands'''
	def __init__(self, command, home_command, reverse_home_command, short_timeout, long_timeout):
		self.command = command
		self.home_command = home_command
		self.reverse_home_command = reverse_home_command
		self.short_timeout = short_timeout
		self.long_timeout = long_timeout



motor_a_right = micro_controller_commands(115, 25, 26, 400, 800)
motor_a_left = micro_controller_commands(116, 26, 25, 400, 800)
motor_b_bin_b = micro_controller_commands(17, 27, 28, 50, 80)	#original short time out was 35...
motor_b_BinB_to_BinA = micro_controller_commands(18, 28, 27, 35, 80)
motor_c_open = micro_controller_commands(20, 29, 30, 40, 100)
motor_c_close = micro_controller_commands(21, 30, 29, 40, 100)
cup_weight = micro_controller_commands(24,24,24,20,20)
cup_weight_special = micro_controller_commands(34,34,34,20,20)
tare_weight = micro_controller_commands(22,22,22,20,20)


# RFID Scanning Method
def polling():
	rfid_timeout = 0
	while True:
		rfid_timeout += 1
		if rfid_timeout >= 8:
			return False
			break
		p1 = subprocess.run(["./rfidb1-tool /dev/ttyS0 uid"],capture_output=True,cwd="/home/pi/rfidb1-tool_v1.1", shell=True) #cwd = 'current working drive' which is used instead of os.chdir = operating system. child directory #setting text=True also 'decodes' result and passes it as a string
		print(p1.stdout.decode()) #capure_output=True takes the response normally returned to console and returns it to the variable instead. stdout = standard output # .decode() method passes result out as a string eg. print(p1.stdout.decode())
		time.sleep(0.25)
		if p1.stdout.decode()[10:17] == "NTAG213":
			print("correct tag type is found...")
			
			decoded_cup_RFID = p1.stdout.decode()[35:49]
			#current_return_attributes.rfid_scanned = decoded_cup_RFID				#Old method of manually changing rfid scanned, new return_attempt_update updates the number of return attempts and the rfid just scanned
			current_return_attributes.return_attempt_update(decoded_cup_RFID)
			print("This is the new class updated rfid uid",current_return_attributes.rfid_scanned)
			print("The return attempt is:",current_return_attributes.return_attempt)
			print(decoded_cup_RFID)
			# Adding Admin Controls
			if decoded_cup_RFID == "XXX":
				return "admin"
				break
			return True
			break
			
# MicroController Queue Class
micro_controller_queue = queue.Queue()

def micro_controller_worker():
	while True:
		item = micro_controller_queue.get()
		run_micro_controller_command(item)
		micro_controller_queue.task_done()
		
def micro_controller_worker_testing():
	while True:
		#print("I'm a micro controller worker and I'm always working")
		try:
			#item = micro_controller_queue.get() #This will block perminantly until new item in queue... For testing I am using False for blocking to raise exception immediately if nothing is in the queue
			item = micro_controller_queue.get(block=False)
			print("Micro_controller starting task")
			print(item)
			run_micro_controller_command(item)
			micro_controller_queue.task_done()
			print("Micro_controller finished task")
		except Exception as e:
			#print(e)
			# print("microntroller is waiting for new command")
			time.sleep(0.1)
		
	
def run_micro_controller_command(chosen_command):
	if chosen_command == "BinA":
		time.sleep(5)
		command_result = 1
		#command_result = intelligent_command_method_set(chosen_command)
		print("chosen_command is:" ,chosen_command)
		return command_result
	elif chosen_command == "Open_RFID_Trolley":
		command_result = intelligent_command_method(motor_a_right)
		#command_result = intelligent_command_method(motor_b_bin_b)
		return command_result
	elif chosen_command == "Close_RFID_Trolley":
		command_result = intelligent_command_method(motor_a_left)
		#command_result = intelligent_command_method(motor_b_BinB_to_BinA)
		if command_result == True:
			current_return_attributes.ready_for_door_unlock = True
			print(" successfully closed rfid trap door trolley and changed attributes to tell to relase magnetic lock")
		else:
			print(" im not changing the  magnetic lock")
		return command_result
	elif chosen_command == "BinA_to_BinQ":
		command_result = intelligent_command_method(motor_a_right)
		return command_result
	elif chosen_command == "BinA_to_BinB":
		command_result = intelligent_command_method(motor_b_bin_b)
		print("command result of Bin A to Bin B the big one is.......: ",command_result)
		if command_result == True:
			Local_station_attributes_class.main_trolley_status = "BinBTrue"
		return command_result
	elif chosen_command == "BinQ_to_BinA":
		command_result = intelligent_command_method(motor_a_right)
		return command_result
	elif chosen_command == "BinB_to_BinA":
		command_result = intelligent_command_method(motor_b_BinB_to_BinA)
		if command_result == True:
			Local_station_attributes_class.main_trolley_status = "BinATrue"
		return command_result
	elif chosen_command == "BinA_to_BinQ_slow":
		command_result = intelligent_command_method(motor_a_right)
		return command_result
	elif chosen_command == "BinA_to_BinB_slow":
		command_result = intelligent_command_method(motor_a_right)
		return command_result
	elif chosen_command == "BinQ_to_BinA_slow":
		command_result = intelligent_command_method(motor_a_right)
		return command_result
	elif chosen_command == "BinB_to_BinA_slow":
		command_result = intelligent_command_method(motor_a_right)
		return command_result
	elif chosen_command == "Open_Trap_Door":
		command_result = intelligent_command_method(motor_c_open)
		if command_result == True:
			Local_station_attributes_class.trap_door_status = "OpenTrue"
		return command_result
	elif chosen_command == "Close_Trap_Door":
		command_result = intelligent_command_method(motor_c_close)
		if command_result == True:
			Local_station_attributes_class.trap_door_status = "ClosedTrue"
		return command_result
	elif chosen_command == "HomeMotors":
		command_result = intelligent_command_method(motor_a_right)
		command_result = intelligent_command_method(motor_a_right)
		command_result = intelligent_command_method(motor_a_right)
		return command_result
	elif chosen_command == "tare":
		LED_flash(Raspi_red_LED,12,4)
		Raspi_red_LED.on()
		manual_micro_controller_command(22)
		time.sleep(2)
		Raspi_red_LED.off()
		print("Load cell tared succesfully")
		return True
	elif chosen_command == "calibrate_scale":
		LED_flash(Raspi_green_LED,12,4)
		Raspi_green_LED.on()
		manual_micro_controller_command(23)
		time.sleep(3)
		Raspi_green_LED.off()
		return command_result
	elif chosen_command == "weight_check":
		#print("Load cell weighed cup succesfully")
		command_result = weight_command(cup_weight)
		return command_result
	elif chosen_command == "double_weight_check":
		command_result = weight_command(cup_weight)
		command_result = weight_command(cup_weight_special)
		return command_result
	elif chosen_command == "estimated_weight_check":
		command_result = weight_command(cup_weight_special)
		print("estimated_weight_check result is:", command_result)
		return command_result
	elif chosen_command == "laser_check":
		command_result = manual_laser_command(51)
		current_return_attributes.laser_updated = True
		return command_result
	elif chosen_command == "laser_on":
		command_result = manual_micro_controller_command(53)
		return command_result
	elif chosen_command == "laser_off":
		command_result = manual_micro_controller_command(54)
		return command_result
	elif chosen_command == "sliding_door_motor":
		if Sliding_door_limit_switch.is_pressed:
			command_result = manual_micro_controller_command(41)
			current_return_attributes.screen_pull_back_ready = False
		else:
			command_result = manual_micro_controller_command(41)
			current_return_attributes.screen_pull_back_ready = False
		return command_result
	elif chosen_command == "sliding_door_motor_simultaneous":
		return command_result
	elif chosen_command == "delay100":
		print("sleeping for 0.1 seconds")
		time.sleep(0.1)
		print("done sleeping")
		return True
	elif chosen_command == "delay250":
		time.sleep(0.25)
		return True
	elif chosen_command == "delay500":
		time.sleep(0.5)
		return True
	elif chosen_command == "delay1000":
		time.sleep(1)
		return True
	elif chosen_command == "delay2000":
		time.sleep(2)
		return True
	elif chosen_command == "delay5000":
		print("sleeping for 5 seconds")
		time.sleep(5)
		print("done sleeping")
		return True
	# elif chosen_command[0:2] == "ITM":
		# command_result = intelligent_command_method(chosen_command[2:])
		# return command_result
	else:
		manual_micro_controller_command(chosen_command)

# A setup to send manual command data to the arduino micro controlelr address
def manual_micro_controller_command(individual_command):
	for i in range (20):
		try:
			bus.write_byte(arduino_due_address,int(individual_command))
			command_complete = False
			while command_complete == False:
				response = bus.read_byte(arduino_due_address)
				if response == 1:
					command_complete = True
					print("manual command response was: ",response)
					return True
				if response == 2:
					command_complete = True
					print("manual command response was: ",response)
					return True
				if response == 3:
					command_complete = True
					print("manual command response was: ",response)
					return True
				if response == 4:
					command_complete = True
					print("manual command response was: ",response)
					return True
		except Exception as e:
			print("manual micro controller command produced error",e)
	return True
	
def manual_laser_command(individual_command):
	pass
    
def weight_command(command_group):
	pass
		    
				
def run_command(command_group):
	time_out_count = 0
	print("Running main command")
	for i in range (20):
		try:
			bus.write_byte(arduino_due_address,int(command_group.command))
			command_complete = False
			while command_complete == False:
				response = bus.read_byte(arduino_due_address)
				if response == 2:	#cup within correct weight range
					print("selected command ", command_group.command, " completed with response ",response)
					command_complete = True
					return True
				elif response == 1:
					command_complete = True
					print("selected command ", command_group.command, " completed with response ",response)
					return True
				elif response == 3:
					command_complete = True
					print("selected command ", command_group.command, " completed with response ",response)
					return True
				elif response == 4:
					command_complete = True
					print("selected command ", command_group.command, " completed with response ",response)
					return True
				time.sleep(0.1)
				time_out_count += 1
				if time_out_count == command_group.short_timeout:
					print("short timeout reached")
					#Sending Timeout signal and then using slow home command to slowly home
					timeout_signal()
					time_out_count = 0
					response = bus.read_byte(arduino_due_address)
					return False
					command_complete = True
		except Exception as error:
			print(error)

def run_home_command(selected_command_group):
	time_out_count = 0
	print("Running home command")
	for i in range (20):
		try:
			bus.write_byte(arduino_due_address,int(selected_command_group.home_command))
			print("home command just sent command: ", selected_command_group.home_command, ".")
			command_complete = False
			while command_complete == False:
				response = bus.read_byte(arduino_due_address)
				print(response)
				if response == 1:
					print("selected command ", selected_command_group.home_command, " completed with response ",response)
					command_complete = True
					return True
				elif response == 2:
					command_complete = False
					print("selected command ", selected_command_group.home_command, " completed with response ",response)
					return True
				time.sleep(0.1)
				time_out_count += 1
				print("time out count is: ", time_out_count)
				if time_out_count == selected_command_group.long_timeout:
					print("long timeout reached")
					#Sending Timeout signal and then using slow home command to slowly home
					timeout_signal()
					time_out_count = 0
					response = bus.read_byte(arduino_due_address)
					return False
					command_complete = True
		except Exception as error:
			print(error)
		
def run_reverse_home_command(selected_command):
	time_out_count = 0
	print("Running reverse home command")
	for i in range (20):
		try:
			bus.write_byte(arduino_due_address,int(selected_command.reverse_home_command))
			command_complete = False
			while command_complete == False:
				response = bus.read_byte(arduino_due_address)
				print(response)
				if response == 1:
					print("selected command ", selected_command.reverse_home_command, " completed with response ",response)
					command_complete = True
					return True
				elif response == 2:
					command_complete = True
					print("selected command ", selected_command.reverse_home_command, " completed with response ",response)
					return False
				time.sleep(0.1)
				time_out_count += 1
				print("time out count is: ", time_out_count)
				if time_out_count == selected_command.short_timeout:
					print("short timeout reached")
					#Sending Timeout signal and then using slow home command to slowly home
					timeout_signal()
					time_out_count = 0
					response = bus.read_byte(arduino_due_address) #Read byte to remove from buffer even though we know it will be 2
					return False
					command_complete = True
		except Exception as error:
			print(error)
				
def intelligent_command_method(command_group):
	
	print("Sending main command: ", command_group)
	try:
		result = run_command(command_group)
		print("LOOK HERE!!!! result of run command is: ",result)
		if result == True:
			return True
			pass
		else:
			#Un-jamming attempt loop x2
			for i in range (3):
				print("Unjamming attempt: ", i)
				try:
					time.sleep(3)
					result = run_home_command(command_group)
					print("result of home command is:", result)
					if result == True:
						return True
						break
					else:
						try:
							time.sleep(3)
							result = run_reverse_home_command(command_group)
							if result == True:
								pass
							else:
								continue
						except Exception as error:
							print(error)
				except Exception as error:
					print(error)
	except Exception as error:
		print(error)


#Basic Bin selection method
def Bin_selection_method():
	if time_from_last_rfid() == "quick_turnaround":
		if Bean_drop_station_status_attributes.Bin_A_Status == True:
			micro_controller_queue.put("BinA")
		else:
			micro_controller_queue.put("BinB")
	if time_from_last_rfid() == "normal_turnaround":
		if Bean_drop_station_status_attributes.Bin_B_Status == True:
			micro_controller_queue.put("BinB")
		else:
			micro_controller_queue.put("BinA")

#---Advanced Bin controls - avoids final commands to bring trolley back to BinA/ Home to reduce times
def Bin_selection_method2():
	
	if time_from_last_rfid() == "quick_turnaround":
		if Local_station_attributes_class.Bin_A_Status == True:								#Checking Bin A is availible
			if Local_station_attributes_class.main_trolley_status == "BinATrue":				#Checking Location of main trolley
				if Local_station_attributes_class.trap_door_status == "ClosedTrue":					#Checking status of trap_door
					print("execute quick turnaround commands to drop cups into Bin A")
					micro_controller_queue.put("Open_RFID_Trolley")
					micro_controller_queue.put("delay250")
					micro_controller_queue.put("Close_RFID_Trolley")
					#micro_controller_queue.put("Open_Trap_Door")
			else:																					#main trolley location is not under rfid_trolley
				print("execute quick turnaround commands to drop cups into BinA without using trap door trolley")
				micro_controller_queue.put("Open_RFID_Trolley")
				micro_controller_queue.put("delay250")
				micro_controller_queue.put("Close_RFID_Trolley")
		else:																						#Run commands to Bin B because Bin A is unavailible
			print("Execute standard Bin B commands because Bin A is out of operation")
			Bin_B_selected_command_options()
			
			
	elif time_from_last_rfid() == "normal_turnaround":
		if Local_station_attributes_class.Bin_B_Status == True:
			Bin_B_selected_command_options()
		else:
			if Local_station_attributes_class.main_trolley_status == "BinQTrue":
				if Bean_drop_station_status_attributes.trap_door_status == "ClosedTrue":
					#micro_controller_queue.put("BinQ_to_BinA")
					micro_controller_queue.put("Open_RFID_Trolley")
					micro_controller_queue.put("delay250")
					micro_controller_queue.put("Close_RFID_Trolley")
					#micro_controller_queue.put("Open_Trap_Door")
					print("run commands to collect from BinQ, then open for Bin A")
				else:
					print("run commands to collect from BinQ and keep the trap door open on way, then open rfid trolley to Bin A")
					#micro_controller_queue.put("BinQ_to_BinA")
					micro_controller_queue.put("Open_RFID_Trolley")
					micro_controller_queue.put("delay250")
					micro_controller_queue.put("Close_RFID_Trolley")
			elif Local_station_attributes_class.main_trolley_status == "BinBTrue":
				if Local_station_attributes_class.trap_door_status == "ClosedTrue":
					print("run commands to collect from BinB, then open at Bin A")
					#micro_controller_queue.put("BinB_to_BinA")
					micro_controller_queue.put("Open_RFID_Trolley")
					micro_controller_queue.put("delay250")
					micro_controller_queue.put("Close_RFID_Trolley")
					#micro_controller_queue.put("Open_Trap_Door")
				else:
					print("run commands to collect from BinB and keep the trap door open on way, then open at Bin B")
					#micro_controller_queue.put("BinB_to_BinA")
					micro_controller_queue.put("Open_RFID_Trolley")
					micro_controller_queue.put("delay250")
					micro_controller_queue.put("Close_RFID_Trolley")
			elif Local_station_attributes_class.main_trolley_status == "BinATrue":
				if Local_station_attributes_class.trap_door_status == "ClosedTrue":
					print("run commands to take to open to bin A")
					micro_controller_queue.put("Open_RFID_Trolley")
					micro_controller_queue.put("delay250")
					micro_controller_queue.put("Close_RFID_Trolley")
					#micro_controller_queue.put("Open_Trap_Door")
				else:
					print("run commands to take to open to bin A but trap door is already open")
					micro_controller_queue.put("Open_RFID_Trolley")
					micro_controller_queue.put("delay250")
					micro_controller_queue.put("Close_RFID_Trolley")
			
			
def Bin_B_selected_command_options():
	if Local_station_attributes_class.main_trolley_status == "BinQTrue":
		if Local_station_attributes_class.trap_door_status == "ClosedTrue":
			print("run commands to collect from BinQ, then take to Bin B")
			micro_controller_queue.put("BinQ_to_BinA")
			micro_controller_queue.put("Open_RFID_Trolley")
			micro_controller_queue.put("delay250")
			micro_controller_queue.put("Close_RFID_Trolley")
			micro_controller_queue.put("BinA_to_BinB")
			micro_controller_queue.put("Open_Trap_Door")
		else:
			print("run commands to collect from BinQ and close the trap door on the way, then take to Bin B")
			micro_controller_queue.put("Close_Trap_Door")
			micro_controller_queue.put("BinQ_to_BinA")
			micro_controller_queue.put("Open_RFID_Trolley")
			micro_controller_queue.put("delay250")
			micro_controller_queue.put("Close_RFID_Trolley")
			micro_controller_queue.put("BinA_to_BinB")
			micro_controller_queue.put("Open_Trap_Door")
	elif Local_station_attributes_class.main_trolley_status == "BinBTrue":
		if Local_station_attributes_class.trap_door_status == "ClosedTrue":
			print("run commands to collect from BinB, then take to Bin B")
			micro_controller_queue.put("BinB_to_BinA")
			micro_controller_queue.put("Open_RFID_Trolley")
			micro_controller_queue.put("delay250")
			micro_controller_queue.put("Close_RFID_Trolley")
			micro_controller_queue.put("BinA_to_BinB")
			micro_controller_queue.put("Open_Trap_Door")
		else:
			print("run commands to collect from BinB and close the trap door on the way, then take to Bin B")
			micro_controller_queue.put("Close_Trap_Door")
			micro_controller_queue.put("BinB_to_BinA")
			micro_controller_queue.put("Open_RFID_Trolley")
			micro_controller_queue.put("delay250")
			micro_controller_queue.put("Close_RFID_Trolley")
			micro_controller_queue.put("BinA_to_BinB")
			micro_controller_queue.put("Open_Trap_Door")
	elif Local_station_attributes_class.main_trolley_status == "BinATrue":
		if Local_station_attributes_class.trap_door_status == "ClosedTrue":
			print("run commands to take to Bin B")
			micro_controller_queue.put("Open_RFID_Trolley")
			micro_controller_queue.put("delay250")
			micro_controller_queue.put("Close_RFID_Trolley")
			micro_controller_queue.put("BinA_to_BinB")
			micro_controller_queue.put("Open_Trap_Door")
		else:
			print("run commands to close the trap door on and then take to Bin B")
			micro_controller_queue.put("Close_Trap_Door")
			micro_controller_queue.put("Open_RFID_Trolley")
			micro_controller_queue.put("delay250")
			micro_controller_queue.put("Close_RFID_Trolley")
			micro_controller_queue.put("BinA_to_BinB")
			micro_controller_queue.put("Open_Trap_Door")
# Above ---Advanced Bin controls - avoids final commands to bring trolley back to BinA/ Home to reduce times			


# Thread runs in background and checks if any cups are waiting to be returned / scanned and then homes motors if needed.
def homing_motors_thread():
	while True:
		time.sleep(3)
		if time_from_last_rfid() == "normal_turnaround":
			if Sliding_door_limit_switch.is_pressed:
				print("waiting to home...")
			else:
				
				if Local_station_attributes_class.main_trolley_status != "BinATrue":
					print(Local_station_attributes_class.main_trolley_status)
				# print("HOMING ------------------------------")
				if micro_controller_queue.empty == True and current_return_attributes.screen_pull_back_ready == True:
					print("opening door")
					micro_controller_queue.put("sliding_door_motor")
				if Local_station_attributes_class.trap_door_status == "OpenTrue":
					print("Homeing Trap Door")
					micro_controller_queue.put("Close_Trap_Door")
					for i in range(20):
						if Local_station_attributes_class.trap_door_status == "OpenTrue":
							time.sleep(1)
							
				if Local_station_attributes_class.main_trolley_status == "BinQTrue":
					print("Homing to Bin A from Bin Q")
					micro_controller_queue.put("BinB_to_BinA")
					for i in range(20):
						if Local_station_attributes_class.main_trolley_status == "BinQTrue":
							time.sleep(1)
	
				elif Local_station_attributes_class.main_trolley_status == "BinBTrue":
					print("Homing to Bin A from Bin B")
					micro_controller_queue.put("BinB_to_BinA")
					for i in range(20):
						if Local_station_attributes_class.main_trolley_status == "BinBTrue":
							time.sleep(1)
							

def tare_and_calibration():
	while True:
		time.sleep(0.5)
		if LButton1_press_signal_blue.is_pressed and RButton1_press_signal_green.is_pressed:
			time.sleep(1)
			if LButton1_press_signal_blue.is_pressed and RButton1_press_signal_green.is_pressed:
				time.sleep(1)
				if LButton1_press_signal_blue.is_pressed and RButton1_press_signal_green.is_pressed:
					time.sleep(0.5)
					if LButton1_press_signal_blue.is_pressed and RButton1_press_signal_green.is_pressed:
						# micro_controller_queue.put("tare")
						# micro_controller_queue.put("calibrate_scale")
						micro_controller_queue.put("tare")
						time.sleep(3)						
						micro_controller_queue.put("calibrate_scale")
						time.sleep(5)


# Main loop which checks to see if a customer has closed the door of the Bean Drop Station. Thread the entire sliding door interaction loop
def sliding_door_initiation_loop():
	while True:
		Micro_controller_motor_switch.on()
		Magnetic_lock_LED.off()
		micro_controller_queue.put("laser_check")
		micro_controller_queue.put("estimated_weight_check")
		time.sleep(0.5)
		if Sliding_door_limit_switch.is_pressed:
			current_return_attributes.laser_updated = False
			current_return_attributes.weight_updated = False
			#Scan time and unique scan number -------------------------------------
			scan_time = datetime_now()
			temp_unique_scan_number = unique_scan_action_number()
			#----------------------------------------------------------------------
			Magnetic_lock_LED.on()
			_thread.start_new_thread(entry_port_camera.take_cup_photo_and_add_to_database, ())
			micro_controller_queue.put("weight_check")
			micro_controller_queue.put("laser_check")
			rfid_check = polling()
			if rfid_check == "admin":	# Employees can scan special rfid tags to access the Admin mode
				sound_item = (scan_time, "admin_elavator_music")
				sound_playback_queue.put(sound_item)
				Magnetic_lock_LED.off()
				micro_controller_queue.put("sliding_door_motor")
				current_return_attributes.screen_pull_back_ready = True
				current_return_attributes.ready_for_door_unlock = False
				time.sleep(2)
				break
			if rfid_check == False:
				rfid_check = polling()	# Double Check polling.
			if rfid_check == True:
				pass
				# Main operational code for sorting, and processing cups hidden due to commerial sensitivity
				# Code uses RFID, Laser Diodes and Load Cell results to sort, process and instigate commands to return the cup.
				# These include identification of damaged cups, missing items, incorrect returns along with successful returns.
				# Commands also include customer interaction with GUI via both HDMI screens or E-paper Displays, sound/voice communication
				# via the Speakers embedded into the Bean Drop Station.
				# Commands, Errors and all returns are logged into the local database and communicated to main servers via MQTT communication protocol and a cellular SIM module.
	
        					





# Setting up Tkinter GUI Frame Class ----------------------------------------------------------------------

class Welcome_page(Frame):
	pass
	# Hidden due to commercial sensitivity



if __name__ == '__main__':
	root = Tk()
	root.geometry('1024x600+0+0')
	root.title('App Window')
	#root.attributes('-type', 'dock') # Removes title bar, must use focus_force

	# must instigate after Tk called. Rest of resize can occur ealier in program
	beandrop_logo_new_size = ImageTk.PhotoImage(beandrop_logo_new_size)	
	#------------------------------------------------------------------------------------------------------
	
	# Initialising micro_controller------------------------------------------------------------------------
	Micro_controller_motor_switch.on()
	
	# Starting session with tare and calibration of scale -------------------------------------------------
	micro_controller_queue.put("tare")
	time.sleep(3)
	micro_controller_queue.put("calibrate_scale")
	time.sleep(5)
	
	# Launching Tkinter GUI and background threads -------------------------------------------------------
	Welcome_page(root)
	_thread.start_new_thread(sliding_door_initiation_loop,())
	_thread.start_new_thread(micro_controller_worker_testing,())
	_thread.start_new_thread(homing_motors_thread,())
	_thread.start_new_thread(half_second_timer,())
	_thread.start_new_thread(sound_worker,())
	_thread.start_new_thread(reset_screen_timer_check_worker,())
	_thread.start_new_thread(help_button_worker,())
	_thread.start_new_thread(mqtt_queue_worker,())
	_thread.start_new_thread(tare_and_calibration,())
	
	root.mainloop()