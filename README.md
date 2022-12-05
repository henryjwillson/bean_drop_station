# Bean Drop Station
The Bean Drop Station is a 'smart bin' that is able to identify, sort and reject cups as part of cup return process in the Bean Drop Process Cycle. Customers return used Bean Drop Cups to the Bean Drop Stations to credit their accounts with a cup refund deposit.

It uses a combination of sensors including; cameras, load cells, rfid scanners and light sensors to identify cups being returned. The Bean Drop station is designed to reject cups that are not part of the system and quarantine cups that are damaged or have items missing such as cup lids. Linear motion is used to sort the cups being returned into different sections/compartments in the internal bin storage, so allow easy sorting and collection by Bean Drop employees later on. The Bean Drop Station also uses a combination of screens (LCD and e-paper displays), buttons and sound to communicate and interact with customers. The Bean Drop stations are fully independent solutions which can run on battery power indefinately and communicate using cellular networks and the mqtt protocol. 

![image](https://user-images.githubusercontent.com/60620955/204916464-642912cd-fed9-4803-8e49-97bc802efb88.png)

# Project Requirements
- Hardware (electrical & mechanical) test and selection
- Circuit Diagram & PCB Designs
- 3D CAD model and profile drawings for construction
- Construction of Bean Drop Station
- Single board computer software development 
  - customer GUI / HMI
  - employee GUI / HMI
  - Sound Output
  - slave / master communication with micro-controller
  - Database integration
- Micro-controller software development
  - motor controllers
  - sensor integration
  - mqtt sim communication
- Operational Deployment

## Hardware (electrical & mechanical) test and selection
Over a 2 year development cycle electronic hardware and mechnical hardware were tested continously in preparation for installation in a community and daily public interaction. Components were tested robustly to meet a number of criteria, including reliability, accuracy, energy efficiency and cost. 

## Circuit Diagram & PCB Designs
Circuit diagrams were produced as part of the full design cycle, and PCB's manufactured to increase ease of component integration. PCB's were designed with best practice in mind and designed around components and pcb connectors which had been robustly tested.

## 3D CAD model and profile drawings for construction
3D models were produced for all custom components and for the Bean Drop station as a whole. Components were added to the model before installation enabling identification of issues before installation. The model includes a number of technical profile drawings to allow easy manufacture and assembly of bean drop stations.

## Construction of Bean Drop Station
The construction of the Bean Drop Station has been designed and constructed in a way that allows easy maintenance, a crucial component as the Bean Drop stations will remain permenantly out in the field without the ability to transfer them back into a workshop. The construction is split into removable modules allowing easy construction and easy in field maintenance.

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

## Operational Deployment
Bean Drop station was successfully installed and operational as part of a public COP26 summit sustainability festival at EdgeHill University with students and staff alike allowed and encouraged to interact and demo the bean drop station. 

## Hidden / Removed Code
The Bean Drop Station is a fundamental part of the Bean Drop Process Cycle and as such represents an important commercial asset. Code shown is limited for commercial sensitivity.
Software to run and control the Bean Drop Stations for Bean Drop Ltd

![image](https://user-images.githubusercontent.com/60620955/204917291-f91ba700-42d8-4160-a878-b4316647276a.png)
![image](https://user-images.githubusercontent.com/60620955/205096841-1c13d319-3900-439b-bbfb-26462329aea0.png)

