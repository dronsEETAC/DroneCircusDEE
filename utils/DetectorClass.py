import threading
import time
import tkinter as tk
from cv2 import cv2
import paho.mqtt.client as mqtt
from PIL import Image, ImageTk

from fingerDetector import FingerDetector
from poseDetector import PoseDetector
from faceDetector import FaceDetector

from MapFrameClass import MapFrameClass
from PIL import ImageTk
from tkinter import messagebox


class DetectorClass:
    def __init__(self):
        self.father_frame = None
        self.mode = None
        self.client = None
        self.cap = None
        self.detector = None
        self.master = None
        self.top_frame = None
        self.state = None
        self.level = None
        self.easy_button = None
        self.difficult_button = None
        self.practice = None
        self.close_button = None
        self.button_frame = None
        self.set_level_button = None
        self.connect_button = None
        self.arm_button = None
        self.take_off_button = None
        self.return_home_button = None
        self.close_button2 = None
        self.bottom_frame = None
        self.map = None
        self.select_level_window = None
        self.image = None
        self.image1 = None
        self.image2 = None
        self.image3 = None
        self.bg = None
        self.bg1 = None
        self.bg2 = None
        self.bg3 = None
        self.level1_button = None
        self.level2_button = None
        self.level3_button = None
        self.direction = None
        self.selected_level = None

    def build_frame(self, father_frame, mode):
        # mode can be: fingers, face or pose
        self.father_frame = father_frame
        self.mode = mode

        # use this when simulating the system using the mosquitto broker installed in your PC
        # broker_address = "localhost"

        # use this when connecting with the RPi
        # broker_address = "10.10.10.1"

        # use pon of these when simulating the system in case you do not have a mosquitto broker installed in your PC
        # broker_address = "broker.hivemq.com"
        broker_address = "localhost"

        broker_port = 8083
        self.client = mqtt.Client("Detector", transport="websockets")
        self.client.on_message = self.on_message
        self.client.connect(broker_address, broker_port)
        self.client.loop_start()
        self.client.publish("droneCircus/gate/connectPlatform")

        self.cap = cv2.VideoCapture(0)

        if self.mode == "fingers":
            self.detector = FingerDetector()
        elif self.mode == "pose":
            self.detector = PoseDetector()
        else:
            self.detector = FaceDetector()

        self.master = tk.Frame(self.father_frame)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)

        self.top_frame = tk.LabelFrame(self.master, text="Control")
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.columnconfigure(1, weight=1)
        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.rowconfigure(1, weight=1)
        self.top_frame.rowconfigure(2, weight=1)
        self.top_frame.rowconfigure(3, weight=1)

        # state can be: initial, practising, flying, closed
        self.state = "initial"

        # level can be easy or difficult
        self.level = "easy"

        self.easy_button = tk.Button(
            self.top_frame, text="Fácil", bg="#367E18", fg="white", command=self.easy
        )
        self.easy_button.grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )
        self.difficult_button = tk.Button(
            self.top_frame,
            text="Difícil",
            bg="#CC3636",
            fg="white",
            command=self.difficult,
        )
        self.difficult_button.grid(
            row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )
        # next button to be shown when level (easy or difficult) selected
        self.practice = tk.Button(
            self.top_frame,
            text="Practica los movimientos",
            bg="#F57328",
            fg="white",
            command=self.practice_fingers,
        )
        self.close_button = tk.Button(
            self.top_frame, text="Salir", bg="#FFE9A0", fg="black", command=self.close
        )

        # frame to be shown when practise is finish and user wants to fly
        self.button_frame = tk.Frame(self.top_frame)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.rowconfigure(1, weight=1)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.columnconfigure(2, weight=1)

        self.set_level_button = tk.Button(
            self.button_frame,
            text="Set level",
            bg="#CC3636",
            fg="white",
            command=self.set_level,
        )
        self.set_level_button.grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )
        self.connect_button = tk.Button(
            self.button_frame,
            text="Connect",
            bg="#CC3636",
            fg="white",
            command=self.connect,
        )
        self.connect_button.grid(
            row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        self.arm_button = tk.Button(
            self.button_frame, text="Arm", bg="#CC3636", fg="white", command=self.arm
        )
        self.arm_button.grid(
            row=0, column=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )
        self.take_off_button = tk.Button(
            self.button_frame,
            text="Take Off",
            bg="#CC3636",
            fg="white",
            command=self.take_off,
        )
        self.take_off_button.grid(
            row=0, column=3, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        # button to be shown when flying
        self.return_home_button = tk.Button(
            self.button_frame,
            text="Retorna",
            bg="#CC3636",
            fg="white",
            command=self.return_home,
        )

        # button to be shown when the dron is back home
        self.close_button2 = tk.Button(
            self.button_frame,
            text="Salir",
            bg="#FFE9A0",
            fg="black",
            command=self.close,
        )

        self.top_frame.grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        # by defaulf, easy mode is selected
        self.bottom_frame = tk.LabelFrame(self.master, text="EASY")

        if self.mode == "fingers":
            self.image = Image.open("../assets_needed/dedos_faciles.png")
        elif self.mode == "pose":
            self.image = Image.open("../assets_needed/poses_faciles.png")
        else:
            self.image = Image.open("../assets_needed/caras_faciles.png")

        self.image = self.image.resize((400, 600), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.image)
        canvas1 = tk.Canvas(self.bottom_frame, width=400, height=600)
        canvas1.pack(fill="both", expand=True)
        canvas1.create_image(0, 0, image=self.bg, anchor="nw")

        self.bottom_frame.grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        return self.master

    def show_map(self, position):
        new_window = tk.Toplevel(self.master)
        new_window.title("Map")
        new_window.geometry("800x600")
        self.map = MapFrameClass()
        frame = self.map.build_frame(new_window, position, self.selected_level)
        frame.pack(fill="both", expand="yes", padx=10, pady=10)
        # new_window.mainloop()

    def on_message(self, cli, userdata, message):
        splited = message.topic.split("/")
        origin = splited[0]
        destination = splited[1]
        command = splited[2]

        if command == "connected":
            self.connect_button["text"] = "connected"
            self.connect_button["bg"] = "#367E18"
            self.client.subscribe(origin + "/" + destination + "/" + "homePosition")
            self.client.publish(destination + "/" + origin + "/" + "getHomePosition")

        if command == "armed":
            self.arm_button["text"] = "armed"
            self.arm_button["bg"] = "#367E18"
            self.client.subscribe(origin + "/" + destination + "/" + "armed")

        if command == "takenOff":
            self.take_off_button["text"] = "flying"
            self.take_off_button["bg"] = "#367E18"
            self.client.publish(
                destination + "/" + origin + "/" + "guideManually", "Stop"
            )
            self.state = "flying"
            # this thread will start taking images and detecting patterns to guide the drone
            x = threading.Thread(target=self.flying)
            x.start()
            self.return_home_button.grid(
                row=2,
                column=0,
                padx=5,
                columnspan=3,
                pady=5,
                sticky=tk.N + tk.S + tk.E + tk.W,
            )

        if command == "atHome":
            # the dron completed the RTL
            self.map.mark_at_home()
            messagebox.showwarning("Success", "Ya estamos en casa", parent=self.master)
            self.return_home_button.grid_forget()
            self.close_button2.grid(
                row=2,
                column=0,
                columnspan=3,
                padx=5,
                pady=5,
                sticky=tk.N + tk.S + tk.E + tk.W,
            )

            # return to the initial situation
            self.connect_button["bg"] = "#CC3636"
            self.connect_button["text"] = "Connect"
            self.arm_button["bg"] = "#CC3636"
            self.arm_button["text"] = "Arm"
            self.take_off_button["bg"] = "#CC3636"
            self.take_off_button["text"] = "TakeOff"
            self.state = "initial"

        if command == "homePosition":
            position_str = str(message.payload.decode("utf-8"))
            position = position_str.split("*")
            self.show_map(position)
            self.client.subscribe(origin + "/" + destination + "/" + "dronePosition")

        if command == "dronePosition":
            position_str = str(message.payload.decode("utf-8"))
            position = position_str.split("*")
            self.map.move_drone(position)

    def connect(self):

        print("Voy a conectar")
        # does not allow to connect if the level of difficulty is not fixed
        if self.set_level_button["bg"] == "#367E18":
            self.close_button2.grid_forget()
            self.client.subscribe("autopilotService/droneCircus/connected")
            self.client.publish("droneCircus/autopilotService/connect")
        else:
            messagebox.showwarning(
                "Error",
                "Antes de conectar debes fijar el nivel de dificultad",
                parent=self.master,
            )

    def set_level(self):
        self.select_level_window = tk.Toplevel(self.master)
        self.select_level_window.title("Select level")
        self.select_level_window.geometry("1000x300")
        select_level_frame = tk.Frame(self.select_level_window)
        select_level_frame.pack()
        select_level_frame.rowconfigure(0, weight=1)
        select_level_frame.rowconfigure(1, weight=1)
        select_level_frame.columnconfigure(0, weight=1)
        select_level_frame.columnconfigure(1, weight=1)
        select_level_frame.columnconfigure(2, weight=1)

        self.image1 = Image.open("../assets_needed/no_fence.png")
        self.image1 = self.image1.resize((320, 240), Image.ANTIALIAS)
        self.bg1 = ImageTk.PhotoImage(self.image1)
        canvas1 = tk.Canvas(select_level_frame, width=320, height=240)
        canvas1.create_image(0, 0, image=self.bg1, anchor="nw")
        canvas1.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.image2 = Image.open("../assets_needed/fence_case1.png")
        self.image2 = self.image2.resize((320, 240), Image.ANTIALIAS)
        self.bg2 = ImageTk.PhotoImage(self.image2)
        canvas2 = tk.Canvas(select_level_frame, width=320, height=240)
        canvas2.create_image(0, 0, image=self.bg2, anchor="nw")
        canvas2.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.image3 = Image.open("../assets_needed/fence_case2.png")
        self.image3 = self.image3.resize((320, 240), Image.ANTIALIAS)
        self.bg3 = ImageTk.PhotoImage(self.image3)
        canvas3 = tk.Canvas(select_level_frame, width=320, height=240)
        canvas3.create_image(0, 0, image=self.bg3, anchor="nw")
        canvas3.grid(row=0, column=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.level1_button = tk.Button(
            select_level_frame,
            text="Básico",
            bg="#CC3636",
            fg="white",
            command=self.level1,
        )
        self.level1_button.grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )
        self.level2_button = tk.Button(
            select_level_frame,
            text="Medio",
            bg="#CC3636",
            fg="white",
            command=self.level2,
        )
        self.level2_button.grid(
            row=1, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )
        self.level3_button = tk.Button(
            select_level_frame,
            text="Avanzado",
            bg="#CC3636",
            fg="white",
            command=self.level3,
        )
        self.level3_button.grid(
            row=1, column=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

    def level1(self):
        self.selected_level = "Basico"
        self.select_level_window.destroy()
        self.set_level_button["text"] = "Básico"
        self.set_level_button["bg"] = "#367E18"

    def level2(self):
        self.selected_level = "Medio"
        self.select_level_window.destroy()
        self.set_level_button["text"] = "Medio"
        self.set_level_button["bg"] = "#367E18"

    def level3(self):
        self.selected_level = "Avanzado"
        self.select_level_window.destroy()
        self.set_level_button["text"] = "Avanzado"
        self.set_level_button["bg"] = "#367E18"

    def arm(self):
        # do not allow arming if destination is not fixed
        if self.connect_button["bg"] == "#367E18":
            self.client.subscribe("autopilotService/droneCircus/armed")
            self.client.publish("droneCircus/autopilotService/armDrone")
        else:
            messagebox.showwarning(
                "Error", "Antes de armar, debes conectar", parent=self.master
            )

    def take_off(self):
        # do not allow taking off if not armed
        if self.arm_button["bg"] == "#367E18":
            self.client.subscribe("autopilotService/droneCircus/takenOff")
            self.client.subscribe("autopilotService/droneCircus/dronePosition")
            self.client.publish("droneCircus/autopilotService/takeOff")
        else:
            messagebox.showwarning(
                "Error", "Antes de despegar, debes armar", parent=self.master
            )

    def close(self):
        # this will stop the video stream thread
        self.state = "closed"
        self.cap.release()
        self.client.loop_stop()
        self.client.disconnect()
        self.father_frame.destroy()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

    def practice_fingers(self):
        if self.state == "initial":
            # start practising
            self.practice["bg"] = "#367E18"
            self.practice["text"] = "Estoy preparado. Quiero volar"
            self.state = "practising"
            # startvideo stream to practice
            x = threading.Thread(target=self.practising)
            x.start()

        elif self.state == "practising":
            # stop the video stream thread for practice
            self.state = "closed"

            self.practice.grid_forget()

            # show buttons for connect, arm and takeOff
            self.button_frame.grid(
                row=1,
                column=0,
                columnspan=2,
                padx=5,
                pady=5,
                sticky=tk.N + tk.S + tk.E + tk.W,
            )

    def easy(self):
        # show button to start practising
        self.practice.grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )
        self.close_button.grid(
            row=1, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )
        # highlight codes for easy pattern
        self.difficult_button["bg"] = "#CC3636"
        self.easy_button["bg"] = "#367E18"
        self.bottom_frame.destroy()
        self.bottom_frame = tk.LabelFrame(self.master, text="EASY")
        self.level = "easy"
        if self.mode == "fingers":
            self.image = Image.open("../assets_needed/dedos_faciles.png")
        elif self.mode == "pose":
            self.image = Image.open("../assets_needed/poses_faciles.png")
        else:
            self.image = Image.open("../assets_needed/caras_faciles.png")

        self.image = self.image.resize((400, 600), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.image)
        canvas1 = tk.Canvas(self.bottom_frame, width=400, height=600)
        canvas1.pack(fill="both", expand=True)
        canvas1.create_image(0, 0, image=self.bg, anchor="nw")

        self.bottom_frame.grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

    def difficult(self):
        # show button to start practising
        self.practice.grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )
        self.close_button.grid(
            row=1, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        # highlight codes for difficult pattern
        self.difficult_button["bg"] = "#367E18"
        self.easy_button["bg"] = "#CC3636"
        self.bottom_frame.destroy()
        self.bottom_frame = tk.LabelFrame(self.master, text="DIFFICULT")

        # we still do not have difficult patters. So we use again easy patters

        if self.mode == "fingers":
            self.image = Image.open("../assets_needed/dedos_faciles.png")
        elif self.mode == "pose":
            self.image = Image.open("../assets_needed/poses_dificiles.png")

        else:
            self.image = Image.open("../assets_needed/caras_faciles.png")

        self.image = self.image.resize((400, 600), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.image)

        canvas1 = tk.Canvas(self.bottom_frame, width=400, height=600)
        canvas1.pack(fill="both", expand=True)

        canvas1.create_image(0, 0, image=self.bg, anchor="nw")

        self.bottom_frame.grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )
        self.level = "difficult"

    def __set_direction(self, code):
        if code == 1:
            return "Norte"
        elif code == 2:
            return "Sur"
        elif code == 3:
            return "Este"
        elif code == 4:
            return "Oeste"
        elif code == 5:
            return "Drop"
        elif code == 6:
            return "Retorna"
        elif code == 0:
            return "Stop"
        else:
            return ""

    def practising(self):
        # when the user changes the pattern (new face, new pose or new fingers) the system
        # waits some time (ignore 8 video frames) for the user to stabilize the new pattern
        # we need the following variables to control this
        prev_code = -1
        cont = 0

        while self.state == "practising":
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue
            # use the selected detector to get the code of the pattern and the image with landmarks
            code, img = self.detector.detect(image, self.level)
            img = cv2.resize(img, (800, 600))
            img = cv2.flip(img, 1)

            # if user changed the pattern we will ignore the next 8 video frames
            if code != prev_code:
                cont = 4
                prev_code = code
            else:
                cont = cont - 1
                if cont < 0:
                    # the first 8 video frames of the new pattern (to be ignored) are done
                    # we can start showing new results
                    direction = self.__set_direction(code)
                    cv2.putText(
                        img,
                        direction,
                        (50, 450),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        3,
                        (0, 0, 255),
                        10,
                    )

            cv2.imshow("video", img)
            cv2.waitKey(1)
        cv2.destroyWindow("video")
        cv2.waitKey(1)

    def flying(self):

        # see comments for practising function
        prev_code = -1
        cont = 0
        # we need to know if the dron is returning to lunch to show an apropriate message
        self.returning = False

        self.direction = ""
        while self.state == "flying":
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue
            code, img = self.detector.detect(image, self.level)
            img = cv2.resize(img, (800, 600))
            img = cv2.flip(img, 1)
            if not self.returning:
                if code != prev_code:
                    cont = 8
                    prev_code = code
                else:
                    cont = cont - 1
                    if cont < 0:
                        self.direction = self.__set_direction(code)
                        go_topic = "droneCircus/autopilotService/go"
                        if code == 1:
                            # north
                            self.client.publish(go_topic, "North")
                        elif code == 2:  # south
                            self.client.publish(go_topic, "South")
                        elif code == 5:
                            self.client.publish("droneCircus/autopilotService/drop")
                            time.sleep(2)
                            self.client.publish("droneCircus/autopilotService/reset")
                        elif code == 3:  # east
                            self.client.publish(go_topic, "East")
                        elif code == 4:  # west
                            self.client.publish(go_topic, "West")
                        elif code == 6:
                            self.return_home()
                        elif code == 0:
                            self.client.publish(go_topic, "Stop")

            cv2.putText(
                img,
                self.direction,
                (50, 450),
                cv2.FONT_HERSHEY_SIMPLEX,
                3,
                (0, 0, 255),
                10,
            )
            cv2.imshow("video", img)
            cv2.waitKey(1)

        cv2.destroyWindow("video")
        cv2.waitKey(1)

    def return_home(self):
        self.returning = True
        self.direction = "Volviendo a casa"
        self.client.subscribe("droneCircus/autopilotService/go", "South")
        self.client.publish("RTL")
