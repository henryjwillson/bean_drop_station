#Bean Drop Station Raspi_MQTT Communication

import serial
import time


class sms_module_serial_communication:
	
	def __init__(self, baud_rate, time_out):
		self.baud_rate = baud_rate
		self.time_out = time_out
		
	def send_mqtt_cup_return(self, return_code, return_attempts, rfid_uid):
		
		try:
			ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
		except Exception:
			ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)
		ser.reset_input_buffer()
		
		string_return_message = return_code + return_attempts + rfid_uid
		new_string_return_message_encoded = str(string_return_message).encode('utf-8')
		str_msg = new_string_return_message_encoded.hex()
		args = [str_msg, "\n"]
		comb_str = ''.join([str(item) for item in args])
		comb_encoded = comb_str.encode('utf-8')
		ser.reset_input_buffer()
		ser.write(comb_encoded)
		time.sleep(5)
		
	def check_sim_module_status():
		print("Sim status check with serial communication")
		try:
			ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
		except Exception:
			ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)
		ser.reset_input_buffer()
		
		status_msg = "status"
		comb_encoded = status_msg.encode('utf-8')
		ser.reset_input_buffer()
		ser.write(comb_encoded)
		#Finding 1 response in ser read
		sim_status = ser.readline()
		if (sim_status).decode().find("1") != -1:
			return True
		print(sim_status)
		sim_status = ser.readline()
		if (sim_status).decode().find("1") != -1:
			return True
		print(sim_status)
		sim_status = ser.readline()
		if (sim_status).decode().find("1") != -1:
			return True
		print(sim_status)
		sim_status = ser.readline()
		if (sim_status).decode().find("1") != -1:
			return True
		print(sim_status)
		
		return False
