import time
import datetime


class bd_timing_class:
	'''This is a class with functions maintaining timing on the beandrop station'''

	def __init__(self, quick_turnaround_time, Bean_drop_station_status_attributes, current_return_attributes, Raspi_Arduino_timeout_signal):
		self.quick_turnaround_time = quick_turnaround_time
		self.Bean_drop_station_status_attributes = Bean_drop_station_status_attributes
		self.current_return_attributes = current_return_attributes
		self.Raspi_Arduino_timeout_signal = Raspi_Arduino_timeout_signal

	# datetime used for storage in old online database   
	def datetime_formatted(self):
		return datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
	
	# Datetime now version used for addition and subtraction of times		
	def datetime_now(self):
		return datetime.datetime.now()
	
	def half_second_timer(self):
		while True:
			#print("timer tick")
			time.sleep(0.5)

	# Function to determine micro-controller command options depending on frequency of returns
	def time_from_last_rfid(self):
		current_time = self.datetime_now()
		datetimeobj=datetime.datetime.strptime(self.Bean_drop_station_status_attributes.last_cup_return_time,"%d-%m-%Y %H:%M:%S")
		time_between_last_scan = current_time - datetimeobj
		#print("Last RFID was scanned ", time_between_last_scan.total_seconds(), " seconds ago")
		if time_between_last_scan.total_seconds() < self.quick_turnaround_time:
			print("use quick turnaround microcontroller moves")
			return("quick_turnaround")
		else:
			return("normal_turnaround")

	# Function to determine time from last updated screen	
	def time_from_last_screen(self, last_screen_time):
		current_time = self.datetime_now()
		time_from_last_screen = current_time - last_screen_time
		return time_from_last_screen.total_seconds()
	
	# Threaded worker to check for screen updates
	def reset_screen_timer_check_worker(self):
		while True:
			time_interval = 0
			while time_interval < self.current_return_attributes.time_on_screen:
				time.sleep(0.25)
				#print("time_interval is: ", time_interval)
				#print("Time on screen is: ",current_return_attributes.time_on_screen)
				time_interval = self.time_from_last_screen(self.current_return_attributes.last_screen_update_datetime)
			self.current_return_attributes.reset_GUI()
			self.current_return_attributes.last_screen_update_datetime = self.datetime_now()
			self.current_return_attributes.update_screen_value = True

	# Timeout function to help with micro-controller communication
	def timeout_signal(self):
		print("time_out is on")
		self.Raspi_Arduino_timeout_signal.on()
		time.sleep(0.25)
		self.Raspi_Arduino_timeout_signal.off()
		print("time_out is off")

	def time_from_sound_added_to_queue(self, sound_added_time):
		current_time = self.datetime_now()
		time_from_last_screen = current_time - sound_added_time
		return time_from_last_screen.total_seconds()
		
	

