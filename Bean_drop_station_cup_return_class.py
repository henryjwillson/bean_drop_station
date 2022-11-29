''' This class holds the information about the current cup being processed '''

class cup_return_attributes:
	
	def __init__(self, rfid_scanned, last_rfid_scanned, weight_updated, weight_measured, last_weight_measured, laser_updated, laser_result, return_attempt, first_error, second_error, third_error, fourth_error, fith_error, main_text, main_text_font, white_button, green_button, blue_button, update_screen_value, last_screen_update_datetime, time_on_screen, ready_for_door_unlock, screen_pull_back_ready, priority_sound_added):
		self.rfid_scanned = rfid_scanned
		self.last_rfid_scanned = last_rfid_scanned
		self.weight_updated = weight_updated
		self.weight_measured = weight_measured
		self.last_weight_measured = last_weight_measured
		self.laser_updated = laser_updated
		self.laser_result = laser_result
		self.return_attempt = return_attempt
		self.first_error = first_error
		self.second_error = second_error
		self.third_error = third_error
		self.fourth_error = fourth_error
		self.fith_error = fith_error
		self.main_text = main_text
		self.main_text_size = main_text_font
		self.white_button = white_button
		self.green_button = green_button
		self.blue_button = blue_button
		self.update_screen_value = update_screen_value
		self.last_screen_update_datetime = last_screen_update_datetime
		self.time_on_screen = time_on_screen
		self.ready_for_door_unlock = ready_for_door_unlock
		self.screen_pull_back_ready = screen_pull_back_ready
		self.current_screen = "Home_screen"
		self.priority_sound_added = priority_sound_added
		
	def update_screen_no_rfid(self):
		#self.main_text = "Oops! we can't find your electronic tag at the bottom of your cup. Make sure your cup is placed the right way up on the green circle inside the porch. When your cup is in the right position, slide the door closed again and we'll scan the cup again"
		self.main_text = "We can't identify your Bean Drop cup \n\n\nMake sure your cup is placed the right way up on the green circle inside the porch \n\n\nWhen your cup is ready, slide the door closed again"
		self.main_text_size = "Helvetica -30"
		self.current_screen = "no_rfid_screen"
		self.time_on_screen = 20
	
	def update_screen_incorrect_rfid(self):
		self.main_text = "Looks like your cup is not a Bean Drop cup and we cannot accept it. Please remove it from the Bean Drop Station"
		self.main_text_size = "Helvetica -45"
		self.current_screen = "incorrect_rfid_screen"
		self.time_on_screen = 20
		
	def update_screen_loadcell_major_over(self):
		self.main_text = "Your cup is too heavy \n\nPlease make sure your cup is empty before returning it to the Bean Drop Station \n\nYou can empty excess liquid into the drain on the left of the Bean Drop Station"
		self.main_text_size = "Helvetica -35"
		self.current_screen = "loadcell_major_over_screen"
		self.time_on_screen = 20
		
	def update_screen_loadcell_minor_under(self):
		self.main_text = "Oops, something is wrong! \n\nPlease makesure your cup is empty and you have both your lid and heat sleeve securely attatched when returning your cup"
		self.main_text_size = "Helvetica -45"
		self.time_on_screen = 20
	
	def update_screen_loadcell_minor_under_loss(self):
		self.main_text = "We can't find your cup lid. Please make sure it is attached securely when returning your cup \n\nPress the blue button to return the cup without a lid \n"
		self.main_text_size = "Helvetica -45"
		self.blue_button = True
		self.current_screen = "loadcell_minor_under_loss_screen"
		self.time_on_screen = 20
		
	def update_screen_quarantine_request(self):
		self.main_text = "Oops we can't certify your cup at the moment, we need to take a closer look in person. Press the green button to proceed with return, we will certify you cup within 48 hours. Once certified we will return your cup deposit to your account, ready for your next drink! \n Press the blue button to cancel cup return and remove your cup from the bean drop station"
		self.main_text_size = "Helvetica -45"
		self.blue_button = True
		self.green_button = True
		self.current_screen = "quarantine_request_screen"
		self.time_on_screen = 20
		
	def update_screen_thankyou_for_returning_cup(self):
		self.main_text = "Thank you for returning your Bean Drop Cup. \nWe have returned your cup deposit to your account"
		self.main_text_size = "Helvetica -45"
		self.current_screen = "thankyou_for_returning_cup_screen"
		self.time_on_screen = 20
		
	def reset_GUI(self):
		self.main_text = "welcome to bean drop"
		self.main_text_size = "Helvetica -60"
		self.blue_button = False
		self.green_button = False
		self.white_button = False
		self.current_screen = "Home_screen"
		self.time_on_screen = 1000
		
	def return_error_codes_list(self):
		return [self.first_error, self.second_error, self.third_error, self.fourth_error, self.fith_error]
		
	def reset_error_codes_list(self):
		self.first_error = ""
		self.second_error = ""
		self.third_error = ""
		self.fourth_error = ""
		self.fith_error = ""
		
	def add_to_error_list(self, error_code):
		if self.first_error == "":
			self.first_error = error_code
		elif self.second_error == "":
			self.second_error = error_code
		elif self.third_error == "":
			self.second_error = error_code
		elif self.fourth_error == "":
			self.second_error = error_code
		elif self.fith_error == "":
			self.second_error = error_code
		
	def return_attempt_update(self, rfid_uid):
		if rfid_uid == self.rfid_scanned:
			self.return_attempt += 1
		else:
			self.return_attempt = 1
			self.reset_error_codes_list()
		self.rfid_scanned = rfid_uid
			
		
