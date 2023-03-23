import subprocess
import time
from pynput.keyboard import Key, Controller
from multiprocessing import Process, Pipe
import random


class bd_sound_operation_class:
	'''This is a class with functions maintaining sound operation on the Bean Drop Station'''

	def __init__(self, music_directory, sound_playback_queue, current_return_attributes_class, run_sound_command_priority_dict, list_of_thank_you_messages):
		self.music_directory = music_directory
		self.sound_playback_queue = sound_playback_queue
		self.current_return_attributes_class = current_return_attributes_class
		self.run_sound_command_priority_dict = run_sound_command_priority_dict
		self.list_of_thank_you_messages = list_of_thank_you_messages

	def run_sound_command(self,selected_command, child_pipe):
		music_time = 1
		if selected_command == "Thank_you_giant_leap_for_mankind":
			p1 = subprocess.Popen(["omxplayer -o alsa Thank_you_giant_leap_for_mankind.mp3"], cwd = self.music_directory, shell=True, stdin=subprocess.PIPE)
			music_time = 700
		elif selected_command == "Error_cup_overweight_excess_liquid":
			p1 = subprocess.Popen(["omxplayer -o alsa Error_cup_overweight_excess_liquid.mp3"], cwd = self.music_directory, shell=True, stdin=subprocess.PIPE)
			music_time = 1300
		elif selected_command == "Error_excess_weight_basic":
			p1 = subprocess.Popen(["omxplayer -o alsa Error_excess_weight_basic.mp3"], cwd = self.music_directory, shell=True, stdin=subprocess.PIPE)
			music_time = 700
		elif selected_command == "Error_non_bean_drop_cup":
			p1 = subprocess.Popen(["omxplayer -o alsa Error_non_bean_drop_cup.mp3"], cwd = self.music_directory, shell=True, stdin=subprocess.PIPE)
			music_time = 800
		elif selected_command == "Error_slieght_underweight_attatch_lid_and_sleeve":
			p1 = subprocess.Popen(["omxplayer -o alsa Error_slieght_underweight_attatch_lid_and_sleeve.mp3"], cwd = self.music_directory, shell=True, stdin=subprocess.PIPE)
			music_time = 800
		elif selected_command == "Error_we_cant_find_lid_press_blue_to_comfirm_loss":
			p1 = subprocess.Popen(["omxplayer -o alsa Error_we_cant_find_lid_press_blue_to_comfirm_loss.mp3"], cwd = self.music_directory, shell=True, stdin=subprocess.PIPE)
			music_time = 1000
		elif selected_command == "Quarantine_question_for_customer":
			p1 = subprocess.Popen(["omxplayer -o alsa Quarantine_question_for_customer.mp3"], cwd = self.music_directory, shell=True, stdin=subprocess.PIPE)
			music_time = 2500
		elif selected_command == "RFID_error_basic_contact_bean_drop_request":
			p1 = subprocess.Popen(["omxplayer -o alsa RFID_error_basic_contact_bean_drop_request.mp3"], cwd = self.music_directory, shell=True, stdin=subprocess.PIPE)
			music_time = 700
		elif selected_command == "RFID_error_place_cup_correctly_instructions":
			p1 = subprocess.Popen(["omxplayer -o alsa RFID_error_place_cup_correctly_instructions.mp3"], cwd = self.music_directory, shell=True, stdin=subprocess.PIPE)
			music_time = 1800
		elif selected_command == "Thank_You_Basic":
			p1 = subprocess.Popen(["omxplayer -o alsa Thank_You_Basic.mp3"], cwd = self.music_directory, shell=True, stdin=subprocess.PIPE)
			music_time = 300
		elif selected_command == "Thank_you_cup_saved_from_landfill_community_superstar":
			p1 = subprocess.Popen(["omxplayer -o alsa Thank_you_cup_saved_from_landfill_community_superstar.mp3"], cwd = self.music_directory, shell=True, stdin=subprocess.PIPE)
			music_time = 600
		elif selected_command == "Thank_You_Deposit_Returned_Ready_For_Next_Drink":
			p1 = subprocess.Popen(["omxplayer -o alsa Thank_You_Deposit_Returned_Ready_For_Next_Drink.mp3"], cwd = self.music_directory, shell=True, stdin=subprocess.PIPE)
			music_time = 4500
		elif selected_command == "Thank_You_One_Step_Towards_a_Healthier_Planet":
			p1 = subprocess.Popen(["omxplayer -o alsa Thank_You_One_Step_Towards_a_Healthier_Planet.mp3"], cwd = self.music_directory, shell=True, stdin=subprocess.PIPE)
			music_time = 700
		elif selected_command == "admin_elavator_music":
			p1 = subprocess.Popen(["omxplayer -o alsa --vol -2100 admin_elavator_music.mp3"], cwd = self.music_directory, shell=True, stdin=subprocess.PIPE)
			music_time = 12000
		elif selected_command == "help_instructions":
			#p1 = subprocess.run(["omxplayer -o alsa Help_Instructions.mp3 &"], cwd = music_directory, shell=True)
			p1 = subprocess.Popen(["omxplayer -o alsa Help_Instructions.mp3"], cwd = self.music_directory, shell=True, stdin=subprocess.PIPE)
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
		self.sound_playback_queue.put("completed")
		child_pipe.send(True)

	def play_random_thankyou(self, date_time_of_sound):
		random.shuffle(self.list_of_thank_you_messages)
		sound_item = (date_time_of_sound,self.list_of_thank_you_messages[1])
		print("Random thankyou added to sound queue...")
		self.sound_playback_queue.put(sound_item)
		self.current_return_attributes_class.priority_sound_added = True
	
	def sound_worker(self):
		sound_queue_list = []
		next_sound_ready = True
		while True:
			#print("trying to get next sound item")
			try:
				if parent_conn.poll():
					print("parent connection poll has found an answer to recieve")
					sound_finished = parent_conn.recv()
					print("parent connection recieved: ", sound_finished)
				if sound_finished == True:
					next_sound_ready = True
					sound_finished = False
					print("next_sound_ready is ", next_sound_ready, " and sound_finished is now back to ", sound_finished)
			except Exception as e:
				#print("exception in polling", e)
				pass
				#next_sound_ready = False
			
			if not sound_queue_list: #list is empty if true
					pass #print("sound list is empty")
			else:
				#print("list is not empty")
				#print("the next sound is....:", next_sound_ready)
		
				if next_sound_ready == True:
					parent_conn, child_conn = Pipe()
					p = Process(target = self.run_sound_command, args = (sound_queue_list[0], child_conn))
					p.start()
					sound_queue_list.pop(0)	#removes item just playing
					#_thread.start_new_thread()
					self.current_return_attributes_class.priority_sound_added = False
					next_sound_ready = False
			
			
			try:
				item = self.sound_playback_queue.get(block=False)
				time.sleep(0.1)
				if item == "completed":
					print("FOUND COMPLETED ITEM IN SOUND QUEUE INDICATING A PRIORITY SOUND HAS BEEN ADDED")
					next_sound_ready = True
				if item != "completed":
					print("First part of item in sound queue is the datetime: ", item[0], "Second part of item in sound queue: ", item[1])
					sound_arg = item[1]
					if self.run_sound_command_priority_dict.get(sound_arg) == 1:
						print("PRIORITY SOUND FOUND!!!!!")
						sound_queue_list.clear()  #clears dictionary
						next_sound_ready = True
						try:
							print("TRIED TO TERMINATE PROCESS HERE!!!!!!")
							parent_conn.send("end_sound")
							#print("TRIED TO TERMINATE PROCESS HERE!!!!!!")
							#p.terminate()
						except Exception as e:
							print(e)
					if len(sound_queue_list) > 1:
						sound_queue_list.pop(0) # removing long lists of thankyou messages...
					sound_queue_list.append(item[1])
					print("New sound added to sound queue:", item[1], " list length is: ", len(sound_queue_list), sound_queue_list)
			
			except Exception as e:
				pass