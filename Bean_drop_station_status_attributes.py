
'''This Python file defines the class which stores all of the relavent Bean Drop Station Attributes'''


class Bean_drop_station_status_attributes:
	'''This class defines the status of all possible attributes to the main operation of the Bean Drop Station'''
	
	def __init__(self, Bin_A_Capacity, Bin_A_Cups, Bin_B_Capacity, Bin_B_Cups, Bin_Q_Capacity, Bin_Q_Cups, Bin_A_last_collection, Bin_B_last_collection, Bin_Q_last_collection, Last_station_reset, Last_micro_controller_reset, Last_software_reset, software_version, last_error_time, last_error_code, last_cup_return_time, last_cup_return_bin, last_rfid_returned, rfid_status, load_cell_status, laser_status, RFID_trolley_status, main_trolley_status, trap_door_status, customer_door_status, Bin_A_Status, Bin_B_Status, Bin_Q_Status):
		self.Bin_A_Capacity = Bin_A_Capacity
		self.Bin_A_Cups = Bin_A_Cups
		self.Bin_B_Capacity = Bin_B_Capacity
		self.Bin_B_Cups = Bin_B_Cups
		self.Bin_Q_Capacity = Bin_Q_Capacity
		self.Bin_Q_Cups = Bin_Q_Cups
		self.Bin_A_last_collection = Bin_A_last_collection
		self.Bin_B_last_collection = Bin_B_last_collection
		self.Bin_Q_last_collection = Bin_Q_last_collection
		self.Last_station_reset = Last_station_reset
		self.Last_micro_controller_reset = Last_micro_controller_reset
		self.Last_software_reset = Last_software_reset
		self.software_version = software_version
		self.last_error_time = last_error_time
		self.last_error_code = last_error_code
		self.last_cup_return_time = last_cup_return_time
		self.last_cup_return_bin = last_cup_return_bin
		self.last_rfid_returned = last_rfid_returned
		self.rfid_status = rfid_status
		self.load_cell_status = load_cell_status
		self.laser_status = laser_status
		self.RFID_trolley_status = RFID_trolley_status
		self.main_trolley_status = main_trolley_status
		self.trap_door_status = trap_door_status
		self.customer_door_status = customer_door_status
		self.Bin_A_Status = Bin_A_Status
		self.Bin_B_Status = Bin_B_Status
		self.Bin_Q_Status = Bin_Q_Status
	
	def reset_bin_A(self, time):
		self.Bin_A_Cups = 0
		self.Bin_A_last_collection = time
		
	def reset_bin_B(self, time):
		self.Bin_B_Cups = 0
		self.Bin_B_last_collection = time
		
	def reset_bin_Q(self, time):
		self.Bin_Q_Cups = 0
		self.Bin_Q_last_collection = time

	@property
	def current_status(self):
		status_string = {'Bin_A_Capacity': self.Bin_A_Capacity,
				'Bin_A_Cups': self.Bin_A_Cups,
				'Bin_B_Capacity': self.Bin_B_Capacity,
				'Bin_B_Cups': self.Bin_B_Cups,
				'Bin_Q_Capacity': self.Bin_Q_Capacity,
				'Bin_Q_Cups': self.Bin_Q_Cups,
				'Bin_A_last_collection': self.Bin_A_last_collection,
				'Bin_B_last_collection': self.Bin_B_last_collection,
				'Bin_Q_last_collection': self.Bin_Q_last_collection,
				'Last_station_reset': self.Last_station_reset,
				'Last_micro_controller_reset': self.Last_micro_controller_reset,
				'Last_software_reset': self.Last_software_reset,
				'software_version': self.software_version,
				'last_error_time': self.last_error_time,
				'last_error_code': self.last_error_code,
				'last_cup_return_time': self.last_cup_return_time,
				'last_cup_return_bin': self.last_cup_return_bin,
				'last_rfid_returned': self.last_rfid_returned,
				'rfid_status': self.rfid_status,
				'load_cell_status': self.load_cell_status,
				'laser_status': self.laser_status,
				'RFID_trolley_status': self.RFID_trolley_status,
				'main_trolley_status': self.main_trolley_status,
				'trap_door_status': self.trap_door_status,
				'customer_door_status': self.customer_door_status,
				'Bin_A_Status': self.Bin_A_Status,
				'Bin_B_Status': self.Bin_B_Status,
				'Bin_Q_Status': self.Bin_Q_Status}
		return (str(status_string).replace(",",',\n')).replace("'","")


def main():
	test_bean_drop_station_class = Bean_drop_station_status_attributes(100,0,100,0,10,0,0,0,0,0,0,0,1.0,0,0,0,"Bin_A",0,True,True,False,True,True,True,True,True,True,True)
	print(test_bean_drop_station_class.current_status)


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		gpio.cleanup()
		sys.exit(0)
		
