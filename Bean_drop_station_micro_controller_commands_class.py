import time
import smbus
from gpiozero import LED
from gpiozero import Button as GPIOButton #Changing to allow tkinter Button Class and prevent clash

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


class micro_controller_methods:
	'''Class of functions to communicate with micro_controllers'''

	def __init__(self, micro_controller_queue, current_return_attributes, Local_station_attributes_class, bd_timing_class, Raspi_red_LED, Raspi_green_LED, Sliding_door_limit_switch, arduino_due_address, LButton1_press_signal_blue, RButton1_press_signal_green):
		self.micro_controller_queue = micro_controller_queue
		self.current_return_attributes = current_return_attributes
		self.Local_station_attributes_class = Local_station_attributes_class
		self.bd_timing_class = bd_timing_class
		self.Raspi_red_LED = Raspi_red_LED
		self.Raspi_green_LED = Raspi_green_LED
		self.Sliding_door_limit_switch = Sliding_door_limit_switch
		self.arduino_due_address = arduino_due_address
		self.LButton1_press_signal_blue = LButton1_press_signal_blue
		self.RButton1_press_signal_green = RButton1_press_signal_green

	def micro_controller_worker(self):
		while True:
			item = self.micro_controller_queue.get()
			self.run_micro_controller_command(item)
			self.micro_controller_queue.task_done()

	def run_micro_controller_command(self, chosen_command):
		if chosen_command == "BinA":
			time.sleep(5)
			command_result = 1
			print("chosen_command is:" ,chosen_command)
			return command_result
		elif chosen_command == "Open_RFID_Trolley":
			command_result = self.intelligent_command_method(motor_a_right)
			return command_result
		elif chosen_command == "Close_RFID_Trolley":
			command_result = self.intelligent_command_method(motor_a_left)
			if command_result == True:
				self.current_return_attributes.ready_for_door_unlock = True
				print(" successfully closed rfid trap door trolley and changed attributes to tell to relase magnetic lock")
			else:
				print(" im not changing the  magnetic lock")
			return command_result
		elif chosen_command == "BinA_to_BinQ":
			command_result = self.intelligent_command_method(motor_a_right)
			return command_result
		elif chosen_command == "BinA_to_BinB":
			command_result = self.intelligent_command_method(motor_b_bin_b)
			print("command result of Bin A to Bin B the big one is.......: ",command_result)
			if command_result == True:
				self.Local_station_attributes_class.main_trolley_status = "BinBTrue"
			return command_result
		elif chosen_command == "BinQ_to_BinA":
			command_result = self.intelligent_command_method(motor_a_right)
			return command_result
		elif chosen_command == "BinB_to_BinA":
			command_result = self.intelligent_command_method(motor_b_BinB_to_BinA)
			if command_result == True:
				self.Local_station_attributes_class.main_trolley_status = "BinATrue"
			return command_result
		elif chosen_command == "BinA_to_BinQ_slow":
			command_result = self.intelligent_command_method(motor_a_right)
			return command_result
		elif chosen_command == "BinA_to_BinB_slow":
			command_result = self.intelligent_command_method(motor_a_right)
			return command_result
		elif chosen_command == "BinQ_to_BinA_slow":
			command_result = self.intelligent_command_method(motor_a_right)
			return command_result
		elif chosen_command == "BinB_to_BinA_slow":
			command_result = self.intelligent_command_method(motor_a_right)
			return command_result
		elif chosen_command == "Open_Trap_Door":
			command_result = self.intelligent_command_method(motor_c_open)
			if command_result == True:
				self.Local_station_attributes_class.trap_door_status = "OpenTrue"
			return command_result
		elif chosen_command == "Close_Trap_Door":
			command_result = self.intelligent_command_method(motor_c_close)
			if command_result == True:
				self.Local_station_attributes_class.trap_door_status = "ClosedTrue"
			return command_result
		elif chosen_command == "HomeMotors":
			command_result = self.intelligent_command_method(motor_a_right)
			command_result = self.intelligent_command_method(motor_a_right)
			command_result = self.intelligent_command_method(motor_a_right)
			return command_result
		elif chosen_command == "tare":
			self.LED_flash(self.Raspi_red_LED,12,4)
			self.Raspi_red_LED.on()
			self.manual_micro_controller_command(22)
			time.sleep(2)
			self.Raspi_red_LED.off()
			print("Load cell tared succesfully")
			return True
		elif chosen_command == "calibrate_scale":
			self.LED_flash(self.Raspi_green_LED,12,4)
			self.Raspi_green_LED.on()
			self.manual_micro_controller_command(23)
			time.sleep(3)
			self.Raspi_green_LED.off()
			return command_result
		elif chosen_command == "weight_check":
			command_result = self.weight_command(cup_weight)
			return command_result
		elif chosen_command == "double_weight_check":
			command_result = self.weight_command(cup_weight)
			command_result = self.weight_command(cup_weight_special)
			return command_result
		elif chosen_command == "estimated_weight_check":
			command_result = self.weight_command(cup_weight_special)
			print("estimated_weight_check result is:", command_result)
			return command_result
		elif chosen_command == "laser_check":
			command_result = self.manual_laser_command(51)
			self.current_return_attributes.laser_updated = True
			return command_result
		elif chosen_command == "laser_on":
			command_result = self.manual_micro_controller_command(53)
			return command_result
		elif chosen_command == "laser_off":
			command_result = self.manual_micro_controller_command(54)
			return command_result
		elif chosen_command == "sliding_door_motor":
			if self.Sliding_door_limit_switch.is_pressed:
				command_result = self.manual_micro_controller_command(41)
				self.current_return_attributes.screen_pull_back_ready = False
			else:
				command_result = self.manual_micro_controller_command(41)
				self.current_return_attributes.screen_pull_back_ready = False
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
			self.manual_micro_controller_command(chosen_command)

	# A setup to send manual command data to the  micro controller address
	def manual_micro_controller_command(self, individual_command):
		for i in range (20):
			try:
				self.bus.write_byte(self.arduino_due_address,int(individual_command))
				command_complete = False
				while command_complete == False:
					response = bus.read_byte(self.arduino_due_address)
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
	
	def manual_laser_command(self, individual_command):
		pass
		
	def weight_command(self, command_group):
		pass
				
					
	def run_command(self, command_group):
		time_out_count = 0
		print("Running main command")
		for i in range (20):
			try:
				bus.write_byte(self.arduino_due_address,int(command_group.command))
				command_complete = False
				while command_complete == False:
					response = bus.read_byte(self.arduino_due_address)
					#print("Current arduino response is: ",response)
					if response == 2:	#cup within correct weight range
						print("selected command ", command_group.command, " completed with response ",response)
						command_complete = True
						return True
					elif response == 1:	#cup is significantly over weight significantly
						command_complete = True
						print("selected command ", command_group.command, " completed with response ",response)
						print("Henry you are a wally, finished with response 1 before timeout...")
						return True
					elif response == 3:	#cup is significantly over weight significantly
						command_complete = True
						print("selected command ", command_group.command, " completed with response ",response)
						return True
					elif response == 4:	#cup is significantly under weight significantly
						command_complete = True
						print("selected command ", command_group.command, " completed with response ",response)
						return True
					time.sleep(0.1)
					time_out_count += 1
					#print("time out count is: ", time_out_count)
					if time_out_count == command_group.short_timeout:
						print("short timeout reached")
						#Sending Timeout signal and then using slow home command to slowly home
						self.bd_timer_class.timeout_signal()
						time_out_count = 0
						response = bus.read_byte(self.arduino_due_address)
						return False
						command_complete = True
			except Exception as error:
				print(error)

	def run_home_command(self, selected_command_group):
		time_out_count = 0
		print("Running home command")
		for i in range (20):
			try:
				bus.write_byte(self.arduino_due_address,int(selected_command_group.home_command))
				print("home command just sent command: ", selected_command_group.home_command, ".")
				command_complete = False
				while command_complete == False:
					response = bus.read_byte(self.arduino_due_address)
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
						self.bd_timing_class.timeout_signal()
						time_out_count = 0
						response = bus.read_byte(self.arduino_due_address)
						return False
						command_complete = True
			except Exception as error:
				print(error)
			
	def run_reverse_home_command(self, selected_command):
		time_out_count = 0
		print("Running reverse home command")
		for i in range (20):
			try:
				bus.write_byte(self.arduino_due_address,int(selected_command.reverse_home_command))
				command_complete = False
				while command_complete == False:
					response = bus.read_byte(self.arduino_due_address)
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
						self.bd_timing_class.timeout_signal()
						time_out_count = 0
						response = bus.read_byte(self.arduino_due_address) #Read byte to remove from buffer even though we know it will be 2
						return False
						command_complete = True
			except Exception as error:
				print(error)
					
	def intelligent_command_method(self, command_group):
		# Combination of Commands, Reverses and Homing in combination with endstops to home gantries on axis
		pass

	def LED_flash(self, LED, flash_count, flashes_per_second):
		for repeat in range(flash_count):
			LED.on()
			time.sleep(1/flashes_per_second)
			LED.off()
			time.sleep(1/flashes_per_second)

	#Basic Bin selection method
	def Bin_selection_method(self):
		if self.bd_timing_class.time_from_last_rfid() == "quick_turnaround":
			if self.Local_station_attributes_class.Bin_A_Status == True:
				self.micro_controller_queue.put("BinA")
			else:
				self.micro_controller_queue.put("BinB")
		if self.bd_timing_class.time_from_last_rfid() == "normal_turnaround":
			if self.Local_station_attributes_class.Bin_B_Status == True:
				self.micro_controller_queue.put("BinB")
			else:
				self.micro_controller_queue.put("BinA")

	#---Advanced Bin controls - avoids final commands to bring trolley back to BinA/ Home to reduce times
	def Bin_selection_method2(self):
		
		if self.bd_timing_class.time_from_last_rfid() == "quick_turnaround":
			if self.Local_station_attributes_class.Bin_A_Status == True:								#Checking Bin A is availible
				if self.Local_station_attributes_class.main_trolley_status == "BinATrue":				#Checking Location of main trolley
					if self.Local_station_attributes_class.trap_door_status == "ClosedTrue":					#Checking status of trap_door
						print("execute quick turnaround commands to drop cups into Bin A")
						self.micro_controller_queue.put("Open_RFID_Trolley")
						self.micro_controller_queue.put("delay250")
						self.micro_controller_queue.put("Close_RFID_Trolley")
						#micro_controller_queue.put("Open_Trap_Door")
				else:																					#main trolley location is not under rfid_trolley
					print("execute quick turnaround commands to drop cups into BinA without using trap door trolley")
					self.micro_controller_queue.put("Open_RFID_Trolley")
					self.micro_controller_queue.put("delay250")
					self.micro_controller_queue.put("Close_RFID_Trolley")
			else:																						#Run commands to Bin B because Bin A is unavailible
				print("Execute standard Bin B commands because Bin A is out of operation")
				self.Bin_B_selected_command_options()
				
				
		elif self.bd_timing_class.time_from_last_rfid() == "normal_turnaround":
			if self.Local_station_attributes_class.Bin_B_Status == True:
				self.Bin_B_selected_command_options()
			else:
				if self.Local_station_attributes_class.main_trolley_status == "BinQTrue":
					if self.Local_station_attributes_class.trap_door_status == "ClosedTrue":
						#micro_controller_queue.put("BinQ_to_BinA")
						self.micro_controller_queue.put("Open_RFID_Trolley")
						self.micro_controller_queue.put("delay250")
						self.micro_controller_queue.put("Close_RFID_Trolley")
						#micro_controller_queue.put("Open_Trap_Door")
						print("run commands to collect from BinQ, then open for Bin A")
					else:
						print("run commands to collect from BinQ and keep the trap door open on way, then open rfid trolley to Bin A")
						#micro_controller_queue.put("BinQ_to_BinA")
						self.micro_controller_queue.put("Open_RFID_Trolley")
						self.micro_controller_queue.put("delay250")
						self.micro_controller_queue.put("Close_RFID_Trolley")
				elif self.Local_station_attributes_class.main_trolley_status == "BinBTrue":
					if self.Local_station_attributes_class.trap_door_status == "ClosedTrue":
						print("run commands to collect from BinB, then open at Bin A")
						#micro_controller_queue.put("BinB_to_BinA")
						self.micro_controller_queue.put("Open_RFID_Trolley")
						self.micro_controller_queue.put("delay250")
						self.micro_controller_queue.put("Close_RFID_Trolley")
						#micro_controller_queue.put("Open_Trap_Door")
					else:
						print("run commands to collect from BinB and keep the trap door open on way, then open at Bin B")
						#micro_controller_queue.put("BinB_to_BinA")
						self.micro_controller_queue.put("Open_RFID_Trolley")
						self.micro_controller_queue.put("delay250")
						self.micro_controller_queue.put("Close_RFID_Trolley")
				elif self.Local_station_attributes_class.main_trolley_status == "BinATrue":
					if self.Local_station_attributes_class.trap_door_status == "ClosedTrue":
						print("run commands to take to open to bin A")
						self.micro_controller_queue.put("Open_RFID_Trolley")
						self.micro_controller_queue.put("delay250")
						self.micro_controller_queue.put("Close_RFID_Trolley")
						#micro_controller_queue.put("Open_Trap_Door")
					else:
						print("run commands to take to open to bin A but trap door is already open")
						self.micro_controller_queue.put("Open_RFID_Trolley")
						self.micro_controller_queue.put("delay250")
						self.micro_controller_queue.put("Close_RFID_Trolley")

	def Bin_B_selected_command_options(self):
		if self.Local_station_attributes_class.main_trolley_status == "BinQTrue":
			if self.Local_station_attributes_class.trap_door_status == "ClosedTrue":
				print("run commands to collect from BinQ, then take to Bin B")
				self.micro_controller_queue.put("BinQ_to_BinA")
				self.micro_controller_queue.put("Open_RFID_Trolley")
				self.micro_controller_queue.put("delay250")
				self.micro_controller_queue.put("Close_RFID_Trolley")
				self.micro_controller_queue.put("BinA_to_BinB")
				self.micro_controller_queue.put("Open_Trap_Door")
			else:
				print("run commands to collect from BinQ and close the trap door on the way, then take to Bin B")
				self.micro_controller_queue.put("Close_Trap_Door")
				self.micro_controller_queue.put("BinQ_to_BinA")
				self.micro_controller_queue.put("Open_RFID_Trolley")
				self.m1icro_controller_queue.put("delay250")
				self.micro_controller_queue.put("Close_RFID_Trolley")
				self.micro_controller_queue.put("BinA_to_BinB")
				self.micro_controller_queue.put("Open_Trap_Door")
		elif self.Local_station_attributes_class.main_trolley_status == "BinBTrue":
			if self.Local_station_attributes_class.trap_door_status == "ClosedTrue":
				print("run commands to collect from BinB, then take to Bin B")
				self.micro_controller_queue.put("BinB_to_BinA")
				self.micro_controller_queue.put("Open_RFID_Trolley")
				self.micro_controller_queue.put("delay250")
				self.micro_controller_queue.put("Close_RFID_Trolley")
				self.micro_controller_queue.put("BinA_to_BinB")
				self.micro_controller_queue.put("Open_Trap_Door")
			else:
				print("run commands to collect from BinB and close the trap door on the way, then take to Bin B")
				self.micro_controller_queue.put("Close_Trap_Door")
				self.micro_controller_queue.put("BinB_to_BinA")
				self.micro_controller_queue.put("Open_RFID_Trolley")
				self.micro_controller_queue.put("delay250")
				self.micro_controller_queue.put("Close_RFID_Trolley")
				self.micro_controller_queue.put("BinA_to_BinB")
				self.micro_controller_queue.put("Open_Trap_Door")
		elif self.Local_station_attributes_class.main_trolley_status == "BinATrue":
			if self.Local_station_attributes_class.trap_door_status == "ClosedTrue":
				print("run commands to take to Bin B")
				self.micro_controller_queue.put("Open_RFID_Trolley")
				self.micro_controller_queue.put("delay250")
				self.micro_controller_queue.put("Close_RFID_Trolley")
				self.micro_controller_queue.put("BinA_to_BinB")
				self.micro_controller_queue.put("Open_Trap_Door")
			else:
				print("run commands to close the trap door on and then take to Bin B")
				self.micro_controller_queue.put("Close_Trap_Door")
				self.micro_controller_queue.put("Open_RFID_Trolley")
				self.micro_controller_queue.put("delay250")
				self.micro_controller_queue.put("Close_RFID_Trolley")
				self.micro_controller_queue.put("BinA_to_BinB")
				self.micro_controller_queue.put("Open_Trap_Door")
	# Above ---Advanced Bin controls - avoids final commands to bring trolley back to BinA/ Home to reduce times			

	# Thread runs in background and checks if any cups are waiting to be returned / scanned and then homes motors if needed.
	def homing_motors_thread(self):
		while True:
			time.sleep(3)
			if self.bd_timing_class.time_from_last_rfid() == "normal_turnaround":
				if self.Sliding_door_limit_switch.is_pressed:
					print("waiting to home...")
				else:
					
					if self.Local_station_attributes_class.main_trolley_status != "BinATrue":
						print(self.Local_station_attributes_class.main_trolley_status)
					# print("HOMING ------------------------------")
					if self.micro_controller_queue.empty == True and self.current_return_attributes.screen_pull_back_ready == True:
						print("opening door")
						self.micro_controller_queue.put("sliding_door_motor")
					if self.Local_station_attributes_class.trap_door_status == "OpenTrue":
						print("Homeing Trap Door")
						self.micro_controller_queue.put("Close_Trap_Door")
						for i in range(20):
							if self.Local_station_attributes_class.trap_door_status == "OpenTrue":
								time.sleep(1)
								
					if self.Local_station_attributes_class.main_trolley_status == "BinQTrue":
						print("Homing to Bin A from Bin Q")
						self.micro_controller_queue.put("BinB_to_BinA")
						for i in range(20):
							if self.Local_station_attributes_class.main_trolley_status == "BinQTrue":
								time.sleep(1)
		
					elif self.Local_station_attributes_class.main_trolley_status == "BinBTrue":
						print("Homing to Bin A from Bin B")
						self.micro_controller_queue.put("BinB_to_BinA")
						for i in range(20):
							if self.Local_station_attributes_class.main_trolley_status == "BinBTrue":
								time.sleep(1)

	def tare_and_calibration(self):
		pass
	
	def micro_controller_worker_testing(self):
		while True:
			try:
				#item = micro_controller_queue.get() #This will block perminantly until new item in queue... For testing I am using False for blocking to raise exception immediately if nothing is in the queue
				item = self.micro_controller_queue.get(block=False)
				print("Micro_controller starting task")
				print(item)
				self.run_micro_controller_command(item)
				self.micro_controller_queue.task_done()
				print("Micro_controller finished task")
			except Exception as e:
				time.sleep(0.1)