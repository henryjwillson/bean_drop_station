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
from Bean_drop_station_timing_class import bd_timing_class
from Bean_drop_station_sound_class import bd_sound_operation_class
from Bean_drop_station_micro_controller_commands_class import *
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
list_of_thank_you_messages = ["Thank_You_Basic","Thank_you_cup_saved_from_landfill_community_superstar","Thank_You_Deposit_Returned_Ready_For_Next_Drink","Thank_You_One_Step_Towards_a_Healthier_Planet","Thank_you_giant_leap_for_mankind"]
# Initialising bd_sound_operation_class -------------------------------------------------------------------------------------------
bds_sound = bd_sound_operation_class(music_directory, sound_playback_queue, cup_return_attributes, run_sound_command_priority_dict, list_of_thank_you_messages)

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

int_new_date_time_now = datetime_now()

#---- Cup Return Attributes class initiasation ------------------------------------------
current_return_attributes = cup_return_attributes(0,0,0,0,0,False,True,0,0,0,0,0,0,"welcome to bean drop", 30, False, False, False, False, int_new_date_time_now, 1000, False, False, True) #6th value is laser result left as True until laser is implemented in arduino
test_value = current_return_attributes.main_text
print("Test value is...:",test_value)

# intialising new bd_timing_class --------------------------------------------------------------------------------------
bd_timer = bd_timing_class(10,Local_station_attributes_class, current_return_attributes, Raspi_Arduino_timeout_signal)
	

new_date_time_now = bd_timer.datetime_formatted()
setup_result = local_station_db.update_station_attribute_value("last_error_time",new_date_time_now)


get_local_station_db_attributes(local_station_db, Local_station_attributes_class)
print("\n Attributes grabbed from local database \n")
print(Local_station_attributes_class.current_status)
	
def unique_scan_action_number():
	new_time = str(datetime_now())
	variables = (new_time,"random")
	new_unique_hash = combined_variables_hash(variables)
	return new_unique_hash

#-----------------------------------------
### Add special time periods ------------------------------ 
quick_turnaround_time = 10


# RFID Scanning Method --------------------------------------------
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
# Initialising micro_controller_methods_class
mcm = micro_controller_methods(micro_controller_queue, current_return_attributes, Local_station_attributes_class, bd_timer, Raspi_red_LED, Raspi_green_LED, Sliding_door_limit_switch, arduino_due_address, LButton1_press_signal_blue, RButton1_press_signal_green)


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
	_thread.start_new_thread(mcm.micro_controller_worker_testing,())
	_thread.start_new_thread(mcm.homing_motors_thread,())
	_thread.start_new_thread(bd_timer.half_second_timer,())
	_thread.start_new_thread(bds_sound.sound_worker,())
	_thread.start_new_thread(bd_timer.reset_screen_timer_check_worker,())
	_thread.start_new_thread(help_button_worker,())
	_thread.start_new_thread(mqtt_queue_worker,())
	_thread.start_new_thread(mcm.tare_and_calibration,())
	
	root.mainloop()