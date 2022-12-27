# Drone Circus 
![gallery](https://user-images.githubusercontent.com/100842082/209651156-2c3cd627-aecb-4f25-bc12-530bbab7edde.png)

## Demo   
[Drone Engineering Ecosystem demo](https://www.youtube.com/playlist?list=PL64O0POFYjHpXyP-T063RdKRJXuhqgaXY) 

## What is Drone Circus?
Drone Circus is a front-end desktop application developed in Python and Tkinter that allows to control the drone platform in different ways (for example, with the voice or with body poses).  
It is aimed at allowing the audience participating in the exhibition to interact with the drone in a safe and fun way.


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
