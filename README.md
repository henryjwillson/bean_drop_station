# Bean Drop Station
The Bean Drop Station is a 'smart bin' that is able to identify, sort and reject cups as part of cup return process in the Bean Drop Process Cycle. Customers return used Bean Drop Cups to the Bean Drop Stations to credit their accounts with a cup refund deposit.

It uses a combination of sensors including; cameras, load cells, rfid scanners and light sensors to identify cups being returned. The Bean Drop station is designed to reject cups that are not part of the system and quarantine cups that are damaged or have items missing such as cup lids. Linear motion is used to sort the cups being returned into different sections/compartments in the internal bin storage, so allow easy sorting and collection by Bean Drop employees later on. The Bean Drop Station also uses a combination of screens (LCD and e-paper displays), buttons and sound to communicate and interact with customers. The Bean Drop stations are fully independent solutions which can run on battery power indefinately and communicate using cellular networks and the mqtt protocol. 

![image](https://user-images.githubusercontent.com/60620955/204916464-642912cd-fed9-4803-8e49-97bc802efb88.png)

# Project Requirements
- Hardware (electrical & mechanical) test and selection
- Circuit Diagram & PCB Designs
- 3D CAD model and profile drawings for construction
- Construction of Bean Drop Station
- Micro-controller software development
  - motor controllers
  - sensor integration
  - mqtt sim communication
- Single board computer software development (GUI, Sound output, 
  - customer GUI / HMI
  - employee GUI / HMI
  - Sound Output
  - slave / master communication with micro-controller
  - Database integration
- Operational Deployment

## Hardware (electrical & mechanical) test and selection
Over a 2 year development cycle electronic hardware and mechnical hardware were tested continously in preparation for installation in a community and 

## Single board computer development
A single board computer was used as the main unit to control the Bean Drop station. It acted as a Master communicating via I2C communcation protocol and serial communication to a number of micro-controllers. Interfaced with LCD Screens and e-paper displays, a number of switches/buttons and determined communications to be sent to database. The main program was written in python.
### Python Libraries
- cv2
- datetime
- imutils
- logging
- math
- multiprocessing
- os
- passlib.context
- PIL
- pynput
- random
- serial
- smbus
- sqlite3
- subprocess
- sys
- _thread
- time
- tkinter

## Micro Controller Development
A number of micro controllers were used communicating via I2C communcation protocol and serial communication. Micro-controllers controlled motors, load cells, ldr laser modules, sim communication, limit switches, led's.
### C++ Libraries
- AccelStepper.h
- ATOM_DTU_NB.h
- HX711.h
- M5Atom.h
- wire.h

## Hidden / Removed Code
The Bean Drop Station is a fundamental part of the Bean Drop Process Cycle and as such represents an important commercial asset. Code shown is limited for commercial sensitivity.
Software to run and control the Bean Drop Stations for Bean Drop Ltd

![image](https://user-images.githubusercontent.com/60620955/204917291-f91ba700-42d8-4160-a878-b4316647276a.png)
![image](https://user-images.githubusercontent.com/60620955/205096841-1c13d319-3900-439b-bbfb-26462329aea0.png)

