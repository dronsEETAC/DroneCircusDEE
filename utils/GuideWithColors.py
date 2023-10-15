import base64
import json
import subprocess
import threading
import time
from tkinter import messagebox

import cv2 as cv
import numpy as np
from PIL import Image as Img
from PIL import ImageTk
import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import *
from tkinter.ttk import *

from utils.ColorCalibrator import ColorCalibrator

class GuideWithColors:
    def __init__ (self):
        broker_address = "10.10.10.1"
        #broker_address = "localhost"
        broker_address = "broker.hivemq.com"

        self.client = mqtt.Client("Colors", transport="websockets")
        self.client.on_message = self.on_message
        self.client.connect(broker_address, 8000)
        self.client.loop_start()
        self.client.subscribe('cameraService/droneCircus/#')
        self.client.subscribe('autopilotService/droneCircus/#')
        self.client.subscribe('autopilotService/+/telemetryInfo')

    def BuildFrame (self, father_frame):
        self.father_frame = father_frame

        self.master = tk.Frame(self.father_frame)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=1)
        self.master.rowconfigure(3, weight=1)
        self.master.rowconfigure(4, weight=1)
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)

        self.calibrateButton = tk.Button(self.master, text="Calibrate", bg='red', fg="white", command=self.calibrate)
        self.calibrateButton.grid (row =0, column = 0, columnspan = 2, padx = 5, pady = 5, sticky=N+S+E+W)
        self.checkColorButton = tk.Button(self.master, text="Test colors", bg='red', fg="white", command=self.checkColor)
        self.checkColorButton.grid(row=0, column=2, columnspan =2, padx=5, pady=5, sticky=N + S + E + W)

        self.connectButton = tk.Button(self.master, text="Connect", bg='red', fg="white", command=self.connect)
        self.connectButton.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
        self.armButton = tk.Button(self.master, text="Arm", bg='red', fg="white", command=self.arm)
        self.armButton.grid (row =1, column = 2,columnspan=2, padx = 5, pady = 5, sticky=N+S+E+W)

        self.takeOffButton = tk.Button(self.master, text="TakeOff", bg='red', fg="white", command=self.takeOff)
        self.takeOffButton.grid (row =2, column = 0, columnspan=4, padx = 5, pady = 5, sticky=N+S+E+W)

        self.startNButton = tk.Button(self.master, text="Start North", bg='blue', fg="white", command=self.startNorth)
        self.startNButton.grid(row=3, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.startEButton = tk.Button(self.master, text="Start East", bg='yellow', fg="black", command=self.startEast)
        self.startEButton.grid(row=3, column=1, padx=5, pady=5, sticky=N + S + E + W)
        self.startWButton = tk.Button(self.master, text="Start West", bg='green', fg="white", command=self.startWest)
        self.startWButton.grid(row=3, column=2, padx=5, pady=5, sticky=N + S + E + W)
        self.startSButton = tk.Button(self.master, text="Start South", bg='pink', fg="black", command=self.startSouth)
        self.startSButton.grid(row=3, column=3, padx=5, pady=5, sticky=N + S + E + W)

        self.dropButton = tk.Button(self.master, text="Drop", bg='red', fg="white", command=self.Drop)
        self.dropButton.grid (row =4, column = 0, columnspan=4, padx = 5, pady = 5, sticky=N+S+E+W)
        self.RTLButton = tk.Button(self.master, text="RTL", bg='red', fg="white", command=self.RTL)
        self.RTLButton.grid (row =5, column = 0, columnspan=4, padx = 5, pady = 5, sticky=N+S+E+W)

        self.findingColor = False
        self.state = 'disconnected'

        return self.master

    def calibrate (self):
        self.colorCalibrator = ColorCalibrator()
        self.colorCalibrator.Open(self.master, self.client)

    def checkColor(self):
        if not self.findingColor:
            self.client.publish("droneCircus/cameraService/startFindingColor")
            self.checkColorButton['text'] = 'Stop test'
            self.findingColor = True
        else:
            self.client.publish("droneCircus/cameraService/stopFindingColor")
            self.checkColorButton['text'] = 'Stop test'
            self.findingColor = False



    def connect (self):
        self.client.publish("droneCircus/autopilotService/connect")
        self.connectButton["text"] = "connecting ..."
        self.connectButton["bg"] = "orange"

    def arm (self):
        # do not allow arming if destination is not fixed
        if self.state == "connected":
            self.armButton["bg"] = "orange"
            self.armButton["text"] = "arming ..."
            self.client.publish("droneCircus/autopilotService/armDrone")

        elif self.state == "disconnected":
            messagebox.showwarning(
                "Error", "Antes de armar, debes conectar", parent=self.master
            )
        elif self.state == "flying":
            messagebox.showwarning("Error", "Ya estas volando", parent=self.master)


    def takeOff (self):
        # do not allow taking off if not armed
        if self.state == "armed":
            self.client.publish("droneCircus/autopilotService/takeOff")
            self.takeOffButton["text"] = "taking off ..."
            self.takeOffButton["bg"] = "orange"
        elif self.state == "flying":
            messagebox.showwarning("Error", "Ya estas volando", parent=self.master)
        elif self.state == "connected" or self.state == "disconnected":
            messagebox.showwarning(
                "Error", "Antes de despegar, debes armar", parent=self.master
            )
    def going (self, direction):
        if direction == 'North':
            self.startNButton['text'] = 'Going North'
            self.startNButton['bg'] = 'blue'

            self.startSButton['text'] = ''
            self.startSButton ['bg'] = 'gray'

            self.startEButton['text'] = ''
            self.startEButton['bg'] = 'gray'

            self.startWButton['text'] = ''
            self.startWButton['bg'] = 'gray'
        elif direction == 'South':
            self.startSButton['text'] = 'Going South'
            self.startSButton['bg'] = 'pink'

            self.startNButton['text'] = ''
            self.startNButton['bg'] = 'gray'

            self.startEButton['text'] = ''
            self.startEButton['bg'] = 'gray'

            self.startWButton['text'] = ''
            self.startWButton['bg'] = 'gray'

        elif direction == 'East':
            self.startEButton['text'] = 'Going East'
            self.startEButton['bg'] = 'yellow'

            self.startNButton['text'] = ''
            self.startNButton['bg'] = 'gray'

            self.startSButton['text'] = ''
            self.startSButton['bg'] = 'gray'

            self.startWButton['text'] = ''
            self.startWButton['bg'] = 'gray'

        elif direction == 'West':
            self.startWButton['text'] = 'Going West'
            self.startWButton['bg'] = 'green'

            self.startNButton['text'] = ''
            self.startNButton['bg'] = 'gray'

            self.startEButton['text'] = ''
            self.startEButton['bg'] = 'gray'

            self.startSButton['text'] = ''
            self.startSButton['bg'] = 'gray'

    def startNorth (self):
        self.client.publish("droneCircus/autopilotService/go", "North")
        self.client.publish("droneCircus/cameraService/startFindingColor")

        self.going('North')


    def startSouth (self):
        self.client.publish("droneCircus/autopilotService/go", "South")
        self.client.publish("droneCircus/cameraService/startFindingColor")

        self.going('South')
    def startEast (self):
        self.client.publish("droneCircus/autopilotService/go", "East")
        self.client.publish("droneCircus/cameraService/startFindingColor")

        self.going('East')
    def startWest (self):
        self.client.publish("droneCircus/autopilotService/go", "West")
        self.client.publish("droneCircus/cameraService/startFindingColor")

        self.going('West')
    def Drop (self):
        pass

    def RTL(self):
        if self.state == "flying":
            self.returning = True
            self.direction = "Volviendo a casa"
            self.RTLButton["text"] = "Volviendo a casa"
            self.RTLButton["bg"] = "orange"
            self.client.publish("droneCircus/cameraService/stopFindingColor")
            self.client.publish("droneCircus/autopilotService/returnToLaunch")
        else:
            messagebox.showwarning("Error", "No estas volando", parent=self.master)

    def on_message(self,client, userdata, message):
        global cont
        global missionName
        global pictureStream
        global imgForCalibration
        global img
        global showingGWYB
        global calibration

        splited = message.topic.split("/")
        origin = splited[0]
        command = splited[2]

        if command == 'colorValues':
            values = json.loads(message.payload)
            print('recibo ', values)
            self.colorCalibrator.SetValues(values)
        if command == 'videoFrame':
            img = base64.b64decode(message.payload)
            # converting into numpy array from buffer
            npimg = np.frombuffer(img, dtype=np.uint8)
            # Decode to Original Frame
            img = cv.imdecode(npimg, 1)
            cv.imshow("Video Stream", img)
            cv.waitKey(1)
        if command == 'videoFrameWithColor':
            frameWithColor = json.loads(message.payload)
            frame = frameWithColor['frame']
            color = frameWithColor['color']
            if color == 'blueS':
                self.going('North')
            elif color == 'yellow':
                self.going ('East')
            elif color == 'pink':
                self.going ('South')
            elif color == 'green':
                self.going ('West')
            img = base64.b64decode(frame)
            # converting into numpy array from buffer
            npimg = np.frombuffer(img, dtype=np.uint8)
            # Decode to Original Frame
            img = cv.imdecode(npimg, 1)
            cv.imshow("Video Stream", img)
            cv.waitKey(1)


        if command == "telemetryInfo":
            telemetry_info = json.loads(message.payload)
            lat = telemetry_info["lat"]
            lon = telemetry_info["lon"]
            state = telemetry_info["state"]
            print ('recibo estado ', state, lat, lon)
            if state == "connected" and self.state != "connected":
                self.connectButton["text"] = "disconnect"
                self.connectButton["bg"] = "#367E18"
                #self.show_map((lat, lon))
                self.state = "connected"
            elif state == "armed":
                self.armButton["text"] = "armed"
                self.armButton["bg"] = "#367E18"
                self.state = "armed"
            elif state == "disarmed":
                self.armButton["text"] = "Arm"
                self.armButton["bg"] = "#CC3636"
                self.state = "connected"
            elif state == "flying" and self.state != "flying":
                self.takeOffButton["text"] = "flying"
                self.takeOffButton["bg"] = "#367E18"
                #self.client.publish(
                #    destination + "/" + origin + "/" + "guideManually", "Stop"
                #)
                self.state = "flying"
                # this thread will start taking images and detecting patterns to guide the drone
                '''x = threading.Thread(target=self.flying)
                x.start()
                self.return_home_button.grid(
                    row=2,
                    column=0,
                    padx=5,
                    columnspan=3,
                    pady=5,
                    sticky=tk.N + tk.S + tk.E + tk.W,
                )'''
            elif state == "flying" and self.state == "flying":
                pass
                #self.map.move_drone((lat, lon), "red")
            elif state == "returningHome":
                #self.map.move_drone((lat, lon), "brown")
                self.state = "returningHome"
                self.RTLButton["text"] = "Volviendo a casa"
                self.RTLButton["bg"] = "orange"
                self.client.publish("droneCircus/cameraService/stopFindingColor")
                print ('he hecho lo que toca')
            elif state == "onHearth":
                '''(
                state == "onHearth"
                and self.state != "onHearth"
                and self.state != "disconnected"
                ):
                # the dron completed the RTL
                self.map.mark_at_home()
                messagebox.showwarning(
                    "Success", "Ya estamos en casa", parent=self.master
                )
                self.return_home_button.grid_forget()
                '''
                print ('en casa')
                self.armButton["bg"] = "#CC3636"
                self.armButton["text"] = "Arm"
                self.takeOffButton["bg"] = "#CC3636"
                self.takeOffButton["text"] = "TakeOff"
                self.RTLButton["text"] = "RTL"
                self.RTLButton["bg"] = "#CC3636"

                self.startNButton['text'] = 'Start North'
                self.startNButton['bg'] = 'blue'

                self.startSButton['text'] = 'Start South'
                self.startSButton['bg'] = 'pink'

                self.startEButton['text'] = 'Start East'
                self.startEButton['bg'] = 'yellow'

                self.startWButton['text'] = 'Start West'
                self.startWButton['bg'] = 'green'
                self.state = "connected"
                #self.client.publish("droneCircus/monitor/stop")
