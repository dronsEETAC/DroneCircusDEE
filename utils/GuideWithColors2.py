import base64
import json
import subprocess
import threading
import time

import cv2 as cv
import numpy as np
from PIL import Image as Img
from PIL import ImageTk
import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import *
from tkinter.ttk import *

from Calibrator import Calibrator


# Define mouse callback function
def checkHSV(event, x, y, flags, param):
    global imgForCalibration
    global colorBeingCalibrated
    global yellowValue, yellowMin, yellowMax
    global redValue, redMin, redMax
    global greenValue, greenMin, greenMax
    global blueValue, blueMin, blueMax

    if event == cv.EVENT_LBUTTONDBLCLK:
        hsv = cv.cvtColor(imgForCalibration, cv.COLOR_BGR2HSV)
        if colorBeingCalibrated == 'yellow':
            value = hsv[y,x][0]
            yellowValue['text'] =  value
            if yellowMin['text'] == 'min' or int(yellowMin['text']) > value:
                yellowMin['text'] = str (value)
            if yellowMax['text'] == 'max' or int(yellowMax['text']) < value:
                yellowMax['text'] = str(value)
        if colorBeingCalibrated == 'red':
            value = hsv[y,x][0]
            redValue['text'] =  value
            if redMin['text'] == 'min' or int(redMin['text']) > value:
                redMin['text'] = str (value)
            if redMax['text'] == 'max' or int(redMax['text']) < value:
                redMax['text'] = str(value)
        if colorBeingCalibrated == 'green':
            value = hsv[y, x][0]
            greenValue['text'] = value
            if greenMin['text'] == 'min' or int(greenMin['text']) > value:
                greenMin['text'] = str(value)
            if greenMax['text'] == 'max' or int(greenMax['text']) < value:
                greenMax['text'] = str(value)
        if colorBeingCalibrated == 'blue':
            value = hsv[y, x][0]
            blueValue['text'] = value
            if blueMin['text'] == 'min' or int(blueMin['text']) > value:
                blueMin['text'] = str(value)
            if blueMax['text'] == 'max' or int(blueMax['text']) < value:
                blueMax['text'] = str(value)


def yellow ():
    global colorBeingCalibrated
    global yellowButton, redButton, greenButton, blueButton
    colorBeingCalibrated = 'yellow'
    yellowButton['text'] = 'calibrating...'
    redButton['text'] = 'calibrate'
    greenButton['text'] = 'calibrate'
    blueButton['text'] = 'calibrate'

def red ():
    global colorBeingCalibrated
    global yellowButton, redButton, greenButton, blueButton
    colorBeingCalibrated = 'red'
    yellowButton['text'] = 'calibrate'
    redButton['text'] = 'calibrating...'
    greenButton['text'] = 'calibrate'
    blueButton['text'] = 'calibrate'


def green ():
    global colorBeingCalibrated
    global yellowButton, redButton, greenButton, blueButton
    colorBeingCalibrated = 'green'
    yellowButton['text'] = 'calibrate'
    redButton['text'] = 'calibrate'
    greenButton['text'] = 'calibrating...'
    blueButton['text'] = 'calibrate'


def blue ():
    global colorBeingCalibrated
    global yellowButton, redButton, greenButton, blueButton
    colorBeingCalibrated = 'blue'
    yellowButton['text'] = 'calibrate'
    redButton['text'] = 'calibrate'
    greenButton['text'] = 'calibrate'
    blueButton['text'] = 'calibrating...'

def close():
    #cv.destroyAllWindows()
    calibrationWindow.destroy()

'''
def setValues():
    global yellowValue, yellowMin, yellowMax
    global redValue, redMin, redMax
    global greenValue, greenMin, greenMax
    global blueValue, blueMin, blueMax
    global calibrationWindow

    values = [int(yellowMin['text']),int(yellowMax['text']), int(redMin['text']), int(redMax['text']),
              int(greenMin['text']), int(greenMax['text']), int (blueMin['text']), int(blueMax['text'])]
    print (values)
    values_json = json.dumps(values)
    print (values_json)
    client.publish ('set_hsv_values', values_json)
    cv.destroyWindow("HSV image")
    calibrationWindow.destroy()
'''
def showCalibrationResult(hsvValues):
    global imgForCalibration
    global yellowValue, yellowMin, yellowMax
    global redValue, redMin, redMax
    global greenValue, greenMin, greenMax
    global blueValue, blueMin, blueMax
    global pinkValue, pinkMin, pinkMax
    global yellowButton, redButton, greenButton, blueButton, pinkButton
    global calibrationWindow

    calibrationWindow = Toplevel(master)

    # sets the title of the
    # Toplevel widget
    calibrationWindow.title("Calibration results")

    # sets the geometry of toplevel
    calibrationWindow.geometry("200x300")
    yellowButton = tk.Button(calibrationWindow, width = 10,bg='yellow', fg="black")
    yellowButton.grid(row=0, column=0, padx=5, pady=5)
    yellowMin = tk.Label(calibrationWindow, text=str(hsvValues[0]))
    yellowMin.grid(row=0, column=1, padx=5, pady=5)
    yellowMax = tk.Label(calibrationWindow, text=str(hsvValues[1]))
    yellowMax.grid(row=0, column=2, padx=5, pady=5)

    redButton = tk.Button(calibrationWindow,width = 10, bg='red', fg="white")
    redButton.grid(row=1, column=0, padx=5, pady=5)
    redMin = tk.Label(calibrationWindow, text=str(hsvValues[8]))
    redMin.grid(row=1, column=1, padx=5, pady=5)
    redMax = tk.Label(calibrationWindow, text=str(hsvValues[9]))
    redMax.grid(row=1, column=2, padx=5, pady=5)


    greemButton = tk.Button(calibrationWindow, width = 10,  bg='green', fg="white")
    greemButton.grid(row=2, column=0, padx=5, pady=5)
    greenMin = tk.Label(calibrationWindow, text=str(hsvValues[4]))
    greenMin.grid(row=2, column=1, padx=5, pady=5)
    greenMax = tk.Label(calibrationWindow,text=str(hsvValues[5]))
    greenMax.grid(row=2, column=2, padx=5, pady=5)

    blueButton = tk.Button(calibrationWindow, width = 10, bg='blue', fg="white")
    blueButton.grid(row=3, column=0, padx=5, pady=5)
    blueMin = tk.Label(calibrationWindow, text=str(hsvValues[6]))
    blueMin.grid(row=3, column=1, padx=5, pady=5)
    blueMax = tk.Label(calibrationWindow, text=str(hsvValues[7]))
    blueMax.grid(row=3, column=2, padx=5, pady=5)

    pinkButton = tk.Button(calibrationWindow, width = 10, bg='pink', fg="black")
    pinkButton.grid(row=4, column=0, padx=5, pady=5)
    pinkMin = tk.Label(calibrationWindow, text=str(hsvValues[2]))
    pinkMin.grid(row=4, column=1, padx=5, pady=5)
    pinkMax = tk.Label(calibrationWindow, text=str(hsvValues[3]))
    pinkMax.grid(row=4, column=2, padx=5, pady=5)

    closeButton = tk.Button(calibrationWindow, text="Close", bg='grey', fg="white", command=close)
    closeButton.grid (row=5, column=0, padx=5, pady=5, columnspan = 4)



'''
def calibrate():
    global imgForCalibration
    global yellowValue, yellowMin, yellowMax
    global redValue, redMin, redMax
    global greenValue, greenMin, greenMax
    global blueValue, blueMin, blueMax
    global yellowButton, redButton, greenButton, blueButton
    global calibrationWindow

    calibrationWindow = Toplevel(master)

    # sets the title of the
    # Toplevel widget
    calibrationWindow.title("Calibration window")

    # sets the geometry of toplevel
    calibrationWindow.geometry("300x200")
    yellowButton = tk.Button(calibrationWindow, text="calibrate", bg='yellow', fg="black", command=yellow)
    yellowButton.grid(row=0, column=0, padx=5, pady=5)
    yellowValue = tk.Label(calibrationWindow, text="value")
    yellowValue.grid(row=0, column=1, padx=5, pady=5)
    yellowMin = tk.Label(calibrationWindow, text="min")
    yellowMin.grid(row=0, column=2, padx=5, pady=5)
    yellowMax = tk.Label(calibrationWindow, text="max")
    yellowMax.grid(row=0, column=3, padx=5, pady=5)

    redButton = tk.Button(calibrationWindow, text="calibrate", bg='red', fg="white", command=red)
    redButton.grid(row=1, column=0, padx=5, pady=5)
    redValue = tk.Label(calibrationWindow, text="value")
    redValue.grid(row=1, column=1, padx=5, pady=5)
    redMin = tk.Label(calibrationWindow, text="min")
    redMin.grid(row=1, column=2, padx=5, pady=5)
    redMax = tk.Label(calibrationWindow, text="max")
    redMax.grid(row=1, column=3, padx=5, pady=5)


    greemButton = tk.Button(calibrationWindow, text="calibrate", bg='green', fg="white", command=green)
    greemButton.grid(row=2, column=0, padx=5, pady=5)
    greenValue = tk.Label(calibrationWindow, text="value")
    greenValue.grid(row=2, column=1, padx=5, pady=5)
    greenMin = tk.Label(calibrationWindow, text="min")
    greenMin.grid(row=2, column=2, padx=5, pady=5)
    greenMax = tk.Label(calibrationWindow, text="max")
    greenMax.grid(row=2, column=3, padx=5, pady=5)

    blueButton = tk.Button(calibrationWindow, text="calibrate", bg='blue', fg="white", command=blue)
    blueButton.grid(row=3, column=0, padx=5, pady=5)
    blueValue = tk.Label(calibrationWindow, text="value")
    blueValue.grid(row=3, column=1, padx=5, pady=5)
    blueMin = tk.Label(calibrationWindow, text="min")
    blueMin.grid(row=3, column=2, padx=5, pady=5)
    blueMax = tk.Label(calibrationWindow, text="max")
    blueMax.grid(row=3, column=3, padx=5, pady=5)


    setValuesButton = tk.Button(calibrationWindow, text="set values", bg='grey', fg="white", command=setValues)
    setValuesButton.grid (row=4, column=0, padx=5, pady=5, columnspan = 4)


    cv.imshow('HSV image', imgForCalibration)
    cv.setMouseCallback('HSV image', checkHSV)
    cv.waitKey()
'''
def showVideoForCalibration (img):
    # converting into numpy array from buffer
    npimg = np.frombuffer(img, dtype=np.uint8)
    # Decode to Original Frame
    img = cv.imdecode(npimg, 1)
    # show stream in a separate opencv window
    cv.imshow("Video for calibration", img)
    cv.waitKey(0)

def showGWYB ():
    global showingGWYB
    global img

    while not showingGWYB:
        pass
    while showingGWYB:
        print ('pongo')
        # converting into numpy array from buffer
        npimg = np.frombuffer(img, dtype=np.uint8)
        # Decode to Original Frame
        img = cv.imdecode(npimg, 1)
        # show stream in a separate opencv window
        cv.imshow("Stream", img)
        cv.waitKey(1)
        time.sleep (0.02)


def on_message(client, userdata, message):
    global cont
    global missionName
    global pictureStream
    global imgForCalibration
    global img
    global showingGWYB
    global calibration
    print ('recibo ', message.topic)
    if message.topic == 'picture':

        jpg_original = base64.b64decode(message.payload)
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        image_buffer = cv.imdecode(jpg_as_np, flags=1)
        cv2image = cv.cvtColor(image_buffer, cv.COLOR_BGR2RGBA)
        if pictureStream:
            cv.imwrite(missionName +'_' + str(cont)+'.jpg',cv2image)
            cont = cont +1;
        img = Img.fromarray(cv2image)

        imgtk = ImageTk.PhotoImage(image=img)
        pictureLabel.imgtk = imgtk
        pictureLabel.configure(image=imgtk)


    if message.topic == 'dronePosition':
        print ('Heading: ', message.payload)
        positionLabel['text'] = str(message.payload.decode("utf-8"))

    if message.topic == 'ballDetected':
        img = base64.b64decode(message.payload)
        # converting into numpy array from buffer
        npimg = np.frombuffer(img, dtype=np.uint8)
        # Decode to Original Frame
        img = cv.imdecode(npimg, 1)
        # show stream in a separate opencv window
        cv.imshow("Video Stream", img)
        cv.waitKey(1)


    if message.topic == 'videoForCalibration':
       calibration.showFrame (message.payload)
       '''img = base64.b64decode(message.payload)
       # converting into numpy array from buffer
       npimg = np.frombuffer(img, dtype=np.uint8)
       # Decode to Original Frame
       img = cv.imdecode(npimg, 1)
       # show stream in a separate opencv window
       cv.imshow("Video Stream", img)
       cv.waitKey(1)'''


    '''if message.topic == 'pictureForCalibration':
        img = base64.b64decode(message.payload)
        npimg = np.frombuffer(img, dtype=np.uint8)
        # Decode to Original Frame
        imgForCalibration = cv.imdecode(npimg, 1)
        w = threading.Thread(target=calibrate)
        w.start()'''

    if message.topic == 'calibrationResult':
        print ('tengo los resultados')
        HsvValues = json.loads(message.payload)
        calibration.setCalibrationResults(HsvValues)
        '''hsvValues = json.loads(message.payload)
        w = threading.Thread(target=showCalibrationResult, args = (hsvValues,))
        w.start()'''

    if message.topic == 'videoFrame':
        calibration.showFrame(message.payload)
        '''img = base64.b64decode(message.payload)
        # converting into numpy array from buffer
        npimg = np.frombuffer(img, dtype=np.uint8)
        # Decode to Original Frame
        img = cv.imdecode(npimg, 1)
        # show stream in a separate opencv window
        calibration.showFrame2(img)
        cv.imshow("Video Stream", img)
        cv.waitKey(1)'''

    if message.topic == 'connected':
        connectButton['bg'] = 'green'
    if message.topic == 'armed':
        armButton['bg'] = 'green'
    if message.topic == 'takenOff':
        takeOffButton['bg'] = 'green'

    if message.topic == 'prevValues':
        print ('main recive pev')
        prevHsvValues = json.loads(message.payload)
        calibration.setPrevValues(prevHsvValues)


def connect ():
    print ('connect')
    global client
    client.publish('connect')
    client.subscribe('connected')

def arm ():
    print ('arm')
    global client
    client.publish('arm')
    client.subscribe('armed')
def takeOff ():
    print ('take Off')
    global client
    client.publish('takeOff')
    client.subscribe('takenOff')

def showVideoStream ():
    print('show Video stream')
    global client
    client.publish('showVideoStream')

def startNorth ():
    print ('GWYB')
    global client
    client.publish('GWYB', 'North')
    client.subscribe('ballDetected')
def startSouth ():
    print ('GWYB')
    global client
    client.publish('GWYB', 'South')
    client.subscribe('ballDetected')
def startEast ():
    print ('GWYB')
    global client
    client.publish('GWYB', 'East')
    client.subscribe('ballDetected')
def startWest ():
    print ('GWYB')
    global client
    client.publish('GWYB', 'West')
    client.subscribe('ballDetected')

def stopGWYB ():
    global client
    client.publish('RTL')
    client.unsubscribe('ballDetected')
    #cv.destroyWindow('Stream')
    #cv.waitKey(0)

def startGuiding ():
    client.publish('guideManually', 'Stop')
    client.publish("bluei")
    goingButton['bg'] = 'blue'



def takePicture ():
    global client
    client.publish('takePicture')

def colorCalibration():
    global client
    global calibration
    print ('vamos a calibrar')
    #client.publish('startVideoForCalibration')
    #client.subscribe('videoForCalibration')

    newWindow = Toplevel(master)

    # sets the title of the
    # Toplevel widget
    newWindow.title("Calibration")

    # sets the geometry of toplevel
    newWindow.geometry("200x400")

    calibration = Calibrator()
    calibrationFrame= calibration.buildFrame(newWindow, client)
    calibrationFrame.pack(fill="both", expand="yes", padx=10, pady=5)

def stop ():
    #cv.destroyWindow("Video for calibration")
    client.publish('calibrate')
    client.subscribe('calibrationResult')


def Drop ():
    global client
    client.publish('drop')

def Reset ():
    global client
    client.publish('reset')

def startPictureStream ():
    global client
    global cont
    global missionName
    global pictureStream
    cont = 1
    pictureStream = True
    missionName = askstring('Mission name', 'Picture files will have this name')
    seconds = askstring('Enter seconds','Picture evey how many second?')
    client.publish('startPictureStream', seconds)


def stopPictureStream ():
    global client
    global cont
    global pictureStream
    pictureStream = False
    cont = 0
    client.publish('stopPictureStream')
'''
for n in range (0,155):
        host = "10.10.10." + str (n)
        r = subprocess.run(["ping", "-n", "1", "-w", "200", host], capture_output=True, text=True).stdout
        ls = r.split("\n")
        if 'Respuesta ' in ls[2]:
            ip = (ls[2].split(' ')[2][:-1])
            print ('encontrado ', ip)
'''
def sendYellow():
    client.publish ("yellowi")
    client.publish('ballCommand', 'yellow')
    goingButton['bg'] = 'yellow'
def sendPink():
    client.publish ("pinki")
    client.publish('ballCommand','pink')
    goingButton['bg'] = 'pink'
def sendGreen():
    client.publish ("greeni")
    client.publish('ballCommand',  'green')
    goingButton['bg'] = 'green'
def sendBlue():
    client.publish ("bluei")
    client.publish('ballCommand', 'blue')
    goingButton['bg'] = 'blue'
def sendRed():
    client.publish ("redi")
    client.publish('drop')
    client.publish('RTL')


#broker_address = "10.10.10.1"
broker_address = "localhost"
broker_port = 1883

client = mqtt.Client("Little ground station")
cont = 1
pictureStream = False
showingGWYB = False
master = tk.Tk()
autoPilotFrame = tk.LabelFrame (text = "Autopilot control")
autoPilotFrame.grid (row = 0, column = 0, padx = 5, pady = 5)
connectButton = tk.Button(autoPilotFrame, text="Connect", bg='red', fg="white", command=connect)
connectButton.grid (row =0, column = 0, padx = 5, pady = 5, sticky=N+S+E+W)
armButton = tk.Button(autoPilotFrame, text="Arm", bg='red', fg="white", command=arm)
armButton.grid (row =0, column = 1, padx = 5, pady = 5, sticky=N+S+E+W)
takeOffButton = tk.Button(autoPilotFrame, text="TakeOff", bg='red', fg="white", command=takeOff)
takeOffButton.grid (row =0, column = 2, padx = 5, pady = 5, sticky=N+S+E+W)
dropButton = tk.Button(autoPilotFrame, text="Drop", bg='red', fg="white", command=Drop)
dropButton.grid (row =0, column = 3, padx = 5, pady = 5, sticky=N+S+E+W)
resetServoButton = tk.Button(autoPilotFrame, text="Reset", bg='red', fg="white", command=Reset)
resetServoButton.grid (row =0, column = 4, padx = 5, pady = 5, sticky=N+S+E+W)

showVideoStreamButton = tk.Button(autoPilotFrame, text="Show video stream", bg='green', fg="white", command=showVideoStream)
showVideoStreamButton.grid (row =1, column = 0, padx = 5, pady = 5, columnspan = 5, sticky=N+S+E+W)

colorCalibrationButton = tk.Button(autoPilotFrame, text="Show colors", bg='red', fg="white", command=colorCalibration)
colorCalibrationButton.grid (row =2, column = 0, padx = 5, pady = 5, columnspan = 3, sticky=N+S+E+W)
calibrateButton = tk.Button(autoPilotFrame, text="Calibrate", bg='red', fg="white", command=stop)
calibrateButton.grid (row =2, column = 3, padx = 5, pady = 5,  columnspan = 3, sticky=N+S+E+W)

#Load an image in the script
#img= (Img.open("fiveColors.png"))

#Resize the Image using resize method
#resized_image= img.resize((150,20), Img.ANTIALIAS)
#photo= ImageTk.PhotoImage(resized_image)
GWCFrame =  tk.LabelFrame (autoPilotFrame, text = "Guide with colors")
GWCFrame.grid (row =3, column = 0, padx = 5, pady = 5, columnspan = 5, sticky=N+S+E+W)
StartNButton = tk.Button(GWCFrame, text="Start North",  bg='blue', fg="white", command=startNorth)
StartNButton.grid (row =0, column = 0, padx = 5, pady = 5, sticky=N+S+E+W)
StartEButton = tk.Button(GWCFrame, text="Start East",  bg='yellow', fg="black",command=startEast)
StartEButton.grid (row =0, column = 1, padx = 5, pady = 5, sticky=N+S+E+W)
StartWButton = tk.Button(GWCFrame, text="Start West",  bg='green', fg="white",command=startWest)
StartWButton.grid (row =0, column = 2, padx = 5, pady = 5, sticky=N+S+E+W)
StartSButton = tk.Button(GWCFrame, text="Start South",  bg='pink', fg="black",command=startSouth)
StartSButton.grid (row =0, column = 3, padx = 5, pady = 5, sticky=N+S+E+W)
stopGWYBButton = tk.Button(GWCFrame, text="RTL", bg='red', fg="white", command=stopGWYB)
stopGWYBButton.grid (row =1, column = 0, padx = 5, pady = 5, columnspan = 5, sticky=N+S+E+W)


GuideManuallyFrame =  tk.LabelFrame (autoPilotFrame, text = "Guide manually")
GuideManuallyFrame.grid (row =4, column = 0, padx = 5, pady = 5, columnspan = 5, sticky=N+S+E+W)

guideManuallyButton = tk.Button(GuideManuallyFrame, text="start", bg='red', fg="white", command=startGuiding)
guideManuallyButton.grid (row =0, column = 0, padx = 5, pady = 5, columnspan = 5, sticky=N+S+E+W)
sendBlueButton = tk.Button(GuideManuallyFrame, text="Go North", bg='blue', fg="white", command=sendBlue)
sendBlueButton.grid (row =1, column = 0, padx = 5, pady = 5, sticky=N+S+E+W)
sendYellowButton = tk.Button(GuideManuallyFrame, text="Go East", bg='yellow', fg="black", command=sendYellow)
sendYellowButton.grid (row =1, column = 1, padx = 5, pady = 5, sticky=N+S+E+W)
sendGreenButton = tk.Button(GuideManuallyFrame, text="Go West", bg='green', fg="white", command=sendGreen)
sendGreenButton.grid (row =1, column = 2, padx = 5, pady = 5, sticky=N+S+E+W)
sendOrangeButton = tk.Button(GuideManuallyFrame, text="Go South", bg='pink', fg="white", command=sendPink)
sendOrangeButton.grid (row =1, column = 3, padx = 5, pady = 5, sticky=N+S+E+W)
sendRedButton = tk.Button(GuideManuallyFrame, text="Drop&RTL", bg='red', fg="white", command=sendRed)
sendRedButton.grid (row =1, column = 4, padx = 5, pady = 5, sticky=N+S+E+W)
goingButton = tk.Button(GuideManuallyFrame, text="direction", bg='grey', fg="white")
goingButton.grid (row =2, column = 0, padx = 5, pady = 5,columnspan = 5, sticky=N+S+E+W)


cameraFrame = tk.LabelFrame (text = "Camera control")
cameraFrame.grid (row = 0, column = 1, padx = 5, pady = 5)
takePictureButton = tk.Button(cameraFrame, text="Take picture", bg='red', fg="white", command=takePicture)
takePictureButton.grid (row =0, column = 0, padx = 5, pady = 5)
startPictureStreamButton = tk.Button(cameraFrame, text="Start picture stream", bg='red', fg="white", command=startPictureStream)
startPictureStreamButton.grid (row =0, column = 1, padx = 5, pady = 5)
stopPictureStreamButton = tk.Button(cameraFrame, text="Stop picture stream", bg='red', fg="white", command=stopPictureStream)
stopPictureStreamButton.grid (row =0, column = 2, padx = 5, pady = 5)

pictureLabel = tk.Label(cameraFrame, text='Picture will be shown here')
pictureLabel.grid(row=1, column=0, columnspan = 3)

def showRed():
    client.publish('red')


def showGreen():
    client.publish('green')


def showBlue():
    client.publish('blue')

def clearLEDs():
    client.publish('clear')

LEDsFrame = tk.LabelFrame (text = "LEDs control")
LEDsFrame.grid (row = 0, column = 2, padx = 5, pady = 5)
redButton = tk.Button(LEDsFrame, text="Red", bg='red', fg="white", command=showRed)
redButton.grid (row =0, column = 0, padx = 5, pady = 5)
greenButton = tk.Button(LEDsFrame, text="Green", bg='green', fg="white", command=showGreen)
greenButton.grid (row =0, column = 1, padx = 5, pady = 5)
blueButton = tk.Button(LEDsFrame, text="Blue", bg='blue', fg="white", command=showBlue)
blueButton.grid (row =0, column = 2, padx = 5, pady = 5)
clearButton = tk.Button(LEDsFrame, text="Clear", bg='grey', fg="white", command=clearLEDs)
clearButton.grid (row =1, column = 0, padx = 5, pady = 5, columnspan = 3, sticky=N+S+E+W)


#broker_address ="broker.hivemq.com"

client.on_message = on_message
client.connect(broker_address, broker_port)

client.loop_start()
client.subscribe('dronePosition')
client.subscribe('picture')
client.subscribe('videoFrame')

master.mainloop()
