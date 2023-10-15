from tkinter import *
from tkinter.ttk import *
import cv2 as cv
import threading
import tkinter as tk

class ColorCalibrator:
    def __SendVideoForCalibration (self, ):
        primera = True

        while self.markingFrameForCalibration:
            img = self.tello.get_frame_read().frame
            img = self.colorDetector.MarkFrameForCalibration(img)
            cv.imshow('frame'+str(self.cont), img)
            cv.waitKey(1)
            if primera:
                self.iniciarBtn['text'] = 'Tomar valores'
                primera = False
        self.cont = self.cont + 1

    def Open (self, master, client):
        self.client = client
        self.newWindow = Toplevel(master)
        self.newWindow.title("Calibrador")
        self.newWindow.geometry("150x300")
        self.mainFrame = tk.Frame (self.newWindow)
        self.mainFrame.pack()
        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.rowconfigure(1, weight=1)
        self.mainFrame.rowconfigure(2, weight=1)



        self.iniciarBtn = tk.Button(self.mainFrame,
                            text="Iniciar calibración",
                            command=self.Iniciar)
        self.iniciarBtn.grid(row=0, column=0, padx=5, pady=5, sticky=N + S + E + W)

        self.cerrarBtn = tk.Button(self.mainFrame,
                       text="Cerrar",
                       command=self.Cerrar)
        self.cerrarBtn.grid(row=1, column=0, padx=5, pady=5, sticky=N + S + E + W)

        self.cont = 0
        valoresFrame = tk.LabelFrame (self.mainFrame, text = "Valores")
        valoresFrame.grid(row=2, column=0, padx=5, pady=5, sticky=N + S + E + W)
        valoresFrame.rowconfigure(0, weight=1)
        valoresFrame.rowconfigure(1, weight=1)
        valoresFrame.rowconfigure(2, weight=1)
        valoresFrame.rowconfigure(3, weight=1)
        valoresFrame.rowconfigure(4, weight=1)
        valoresFrame.rowconfigure(5, weight=1)
        valoresFrame.columnconfigure(0, weight=1)
        valoresFrame.columnconfigure(1, weight=1)


        tk.Button(valoresFrame,text="Yellow", bg= 'Yellow').grid(row=0, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.Yellow = Label(valoresFrame, text='?')
        self.Yellow.grid(row=0, column=1, padx=5, pady=5, sticky=N + S + E + W)


        tk.Button(valoresFrame, text="Green", bg= 'Green').grid(row=1, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.Green = Label(valoresFrame, text='?')
        self.Green.grid(row=1, column=1, padx=5, pady=5, sticky=N + S + E + W)


        tk.Button(valoresFrame, text="BlueS", bg = 'Teal').grid(row=2, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.BlueS = Label(valoresFrame, text='?')
        self.BlueS.grid(row=2, column=1, padx=5, pady=5, sticky=N + S + E + W)

        tk.Button(valoresFrame, text="BlueL", bg = 'Cyan').grid(row=3, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.BlueL = Label(valoresFrame, text='?')
        self.BlueL.grid(row=3, column=1, padx=5, pady=5, sticky=N + S + E + W)

        tk.Button(valoresFrame, text="Pink", bg = 'HotPink1').grid(row=4, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.Pink = Label(valoresFrame, text='?')
        self.Pink.grid(row=4, column=1, padx=5, pady=5, sticky=N + S + E + W)

        tk.Button(valoresFrame, text="Purple", bg = 'MediumPurple1').grid(row=5, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.Purple = Label(valoresFrame, text='?')
        self.Purple.grid(row=5, column=1, padx=5, pady=5, sticky=N + S + E + W)
        self.calibrating = False
        self.client.publish("droneCircus/cameraService/getDefaultColorValues")



    def SetValues(self, values):
        self.Yellow['text'] = values['yellow']
        self.Green['text'] = values['green']
        self.BlueS['text'] = values['blueS']
        self.BlueL['text'] = values['blueL']
        self.Pink['text'] = values['pink']
        self.Purple['text'] = values['purple']





    def Iniciar(self):
        if not self.calibrating:
            self.calibrating = True
            self.client.publish("droneCircus/cameraService/markFrameForCalibration")
            self.iniciarBtn['text'] = 'Tomar valores'
        else:
            self.client.publish("droneCircus/cameraService/getColorValues")



    def Cerrar (self):
        self.client.publish("droneCircus/cameraService/stopCalibration")
        self.newWindow.destroy()





