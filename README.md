# Drone Circus 
![software-arch](https://user-images.githubusercontent.com/32190349/155320787-f8549148-3c93-448b-b79a-388623ca5d3f.png)

## Demo   
[Drone Engineering Ecosystem demo](https://www.youtube.com/playlist?list=PL64O0POFYjHpXyP-T063RdKRJXuhqgaXY) 

## What is drone Circus?
The Drone Circus is an intuitive way to use your hands to control the drone without the need of typing anything. 
You can control the drone by means of the software Mission Planner, where you can download it 
[here](https://ardupilot.org/planner/docs/mission-planner-installation.html).
To run it, you'll need:
- Run the CameraController module  found in [here](https://github.com/dronsEETAC/CameraControllerDEE)
- Run the LEDsController module found in [here](https://github.com/dronsEETAC/LEDsControllerDEE)
- Run the AutopilotController module found in [here](https://github.com/dronsEETAC/DroneAutopilotDEE) 
- Run the Gate module found in [here](https://github.com/dronsEETAC/GateDEE) 
(remember to use an interpreter of Python 2.X for the Autopilot, otherwise it won't work)
- Run the DroneCircus (this repository)

## Installing the needed packages for the circus

1) You can download all the needed libraries in a virtual environment:

`python3 -m venv /path/to/new/virtual/environment`

2) And then install the libraries:

`pip install -r requirements.txt`

If you want to install all the libraries locally, don't create a virtual environment and just use command 2)


Then, you must run the LEDs module, the Autopilot module, the Camera module and the gate module.
When they are all running (remember to run the autopilot in a different window with a Python interpreter 2.X),
then run the Circus.


## Example and tutorials

The basics of MQTT can be found here:   
[MQTT](https://www.youtube.com/watch?v=EIxdz-2rhLs)

This is a good example to start using MQTT (using a public broker):    
[Example](https://www.youtube.com/watch?v=kuyCd53AOtg)
