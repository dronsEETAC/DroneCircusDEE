import sys
import tkinter as tk
from tkinter import messagebox
from shapely.geometry.polygon import Polygon
from shapely.geometry.point import Point
import paho.mqtt.client as mqtt
from PIL import Image, ImageTk
import time
import math
import threading
import json
from utils.MapFrameClass import MapFrameClass
import random
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


class RaceClass:
    def __init__(self):
        self.father_frame = None
        self.top_frame = None
        self.bottom_frame = None
        self.button_frame = None
        self.master = None
        self.client = None
        self.state = None
        self.selected_level = None
        self.map = None
        self.select_level_window = None
        self.select_scenario_button = None
        self.practice_button = None
        self.connect_button = None
        self.arm_button = None
        self.connected = None
        self.stopped = None
        self.close_button = None
        self.test_button = None
        self.close_button2 = None
        self.level1_button = None
        self.level2_button = None
        self.level3_button = None
        self.custom_level_button = None
        self.go_next_checkpoint = None
        self.connection_mode = None
        self.start_time = None
        self.elapsed_time = None
        self.num_points = tk.DoubleVar()
        self.score = 0

    # BUILD FRAME

    # Define main frame
    def build_frame(self, father_frame):
        self.father_frame = father_frame

        self.master = tk.Frame(self.father_frame)

        # Top Frame is shown all time

        self.top_frame = tk.LabelFrame(self.master, text="Escenario", width=430, height=600)

        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.rowconfigure(1, weight=1)
        self.top_frame.rowconfigure(2, weight=1)
        self.top_frame.rowconfigure(3, weight=1)
        self.top_frame.rowconfigure(4, weight=1)
        self.top_frame.rowconfigure(5, weight=1, minsize=300)

        self.top_frame.columnconfigure(0, minsize=430)

        self.select_scenario_button = tk.Button(
            self.top_frame, text="Selecciona el escenario", bg="#F57328", fg="white", command=self.set_level
        )
        self.select_scenario_button.grid(
            row=0, column=0, columnspan=5, padx=5, pady=5, ipadx=10, ipady=10, sticky=tk.N + tk.S + tk.E + tk.W
        )
        self.select_scenario_button.bind("<Enter>", lambda event: self.show_messages("select_scenario_button"))
        self.select_scenario_button.bind("<Leave>", lambda event: self.show_messages("N/A"))

        self.practice_button = tk.Button(
            self.top_frame, text="Practica los movimientos", bg="#F57328", fg="white", command=self.practice
        )

        self.practice_button['state'] = 'disabled'

        self.race_button = tk.Button(
            self.top_frame, text="Comienza la Carrera", bg="red", fg="white", command=self.fly
        )

        self.race_button.bind(
            "<Enter>", lambda event: self.show_messages("race_button")
        )

        self.race_button.bind(
            "<Leave>", lambda event: self.show_messages("N/A")
        )

        self.close_button = tk.Button(
            self.top_frame, text="Salir", bg="#FFE9A0", fg="black", command=self.close
        )

        self.test_button = tk.Button(
            self.top_frame, text="Test", bg="#FFE9A0", fg="black", command=self.test
        )

        self.test_slider = tk.Scale(
            self.top_frame, from_=3, to=10, orient='horizontal', variable=self.num_points, command=self.slider_changed
        )

        self.test_slider_Label = tk.Label(
            self.top_frame, text="Selecciona el numero de puntos de control:" + self.get_current_value()
        )

        # Test button to check if all 10 random checkpoints are being generated correctly, unused
        self.skip_checkpoint_button = tk.Button(
            self.top_frame, text="Siguiente punto de control", bg="#F57328", fg="white", command=self.next_checkpoint
        )

        self.connect_button = tk.Button(
            self.top_frame, text="Select Connection Mode", bg="#CC3636", fg="white", command=self.select_connection_mode,
        )

        # Button Frame to be shown when practise is finish and user wants to fly

        self.button_frame = tk.Frame(self.top_frame)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.rowconfigure(1, weight=1)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)

        self.close_button2 = tk.Button(
            self.button_frame, text="Salir", bg="#FFE9A0", fg="black", command=self.close,
        )

        # Help Frame to show help messages

        self.help_frame = tk.LabelFrame(self.master, bg="light gray", text="Help", width=430, height=200, padx=5, pady=5)

        self.help_label = tk.Label(
            self.help_frame, fg="black", bg="light gray", font=("", 12)
        )

        self.help_label.grid(
            row=0, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W
        )

        # Score Frame to be shown when race is started

        self.score_frame = tk.LabelFrame(self.master, bg="light gray", text="Scoreboard", width=430, height=200, padx=5, pady=5)

        self.score_display = tk.Label(
            self.score_frame, fg="black", bg="light gray", font=("", 24), text="0.00"
        )

        self.score_display.grid(
            row=0, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.W
        )

        self.distance_display = tk.Label(
            self.score_frame, fg="black", bg="light gray", font=("", 24), text="Distance: N/A"
        )

        self.distance_display.grid(
            row=1, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.W
        )

        self.checkpoint_count_label = tk.Label(
            self.score_frame, fg="black", bg="light gray", font=("", 24), text="Checkpoints remaining: " + str(self.num_points.get())
        )

        self.checkpoint_count_label.grid(
            row=2, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.W
        )

        # Display frames

        self.top_frame.grid(
            row=0, rowspan=5, pady=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        self.help_frame.grid(
            row=5, rowspan=5, pady=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        self.connected = False
        self.state = "disconnected"

        return self.master

    # Function to get slider value
    def get_current_value(self):
        return '{: .2f}'.format(self.num_points.get())

    # Function called each time slider is activated
    def slider_changed(self, event):
        self.test_slider_Label.config(
            text="Selecciona el numero de puntos de control:" + self.get_current_value()
        )

    # Function to display help messages
    def show_messages(self, button_name):
        if button_name == "select_scenario_button":
            self.help_label.config(
                text="Selecciona el escenario en el que quieres jugar."
            )
        elif button_name == "practice_button":
            self.help_label.config(
                text="Practica la carrera antes de conectarte al dron.\nAlcanza todos los puntos de control\nen el menor"
                     " tiempo y la mayor precisión\nposible.\nDebes seleccionar el modo de conexión\n"
                     "antes de comenzar la práctica."
            )
        elif button_name == "checkpoints_slider":
            self.help_label.config(
                text="Escoge el número de puntos de control de la carrera"
            )
        elif button_name == "exit_button":
            self.help_label.config(
                text="Salir del modo Carrera"
            )
        elif button_name == "N/A":
            self.help_label.config(
                text="Pasa el ratón por encima de los controles para ayuda"
            )
        elif button_name == "connect_button":
            self.help_label.config(
                text="Aprieta para seleccionar el modo de conexión:\n Local o Global.\n"
            )
        elif button_name == "race_button":
            self.help_label.config(
                text="Presiona para comenzar la carrera. Es necesario\n"
                     "que se esté ejecutando el Autopilot Service. La\n"
                     "carrera comienza cuando el dron esté volando.\n"
                     "Para armar y despegar hay que usar la app movil"
            )

    # Function to close race game
    def close(self):
        if self.state == "disconnected" or self.state == "practising":

            self.father_frame.destroy()

        else:
            messagebox.showwarning(
                "Error", "Antes de salir debes desconectar", parent=self.master
            )

    # Function to close final score display window
    def exit(self):
        self.score_frame.grid_forget()
        # self.score_frame.pack_forget()
        # self.help_frame.pack(fill="both")
        self.help_frame.grid(
            row=5, rowspan=5, pady=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W
        )
        self.score_window.destroy()

    # DEFINE LEVELS

    # Opens a new window to select the scenario
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
        select_level_frame.columnconfigure(3, weight=1)

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

        self.image4 = Image.open("../assets_needed/custom_fence.png")
        self.image4 = self.image4.resize((320, 240), Image.ANTIALIAS)
        self.bg4 = ImageTk.PhotoImage(self.image4)
        canvas4 = tk.Canvas(select_level_frame, width=320, height=240)
        canvas4.create_image(0, 0, image=self.bg4, anchor="nw")
        canvas4.grid(row=0, column=3, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

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

        self.custom_level_button = tk.Button(
            select_level_frame,
            text="Personalizar",
            bg= "#CC3636",
            fg="white",
            command=self.custom_level,
        )
        self.custom_level_button.grid(
            row=1, column=3, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

    # Sets selected level, closes window and displays layout
    def level1(self):
        self.selected_level = "Basico"
        self.select_level_window.destroy()
        self.select_scenario_button["text"] = "Básico"
        self.select_scenario_button["bg"] = "#367E18"
        # show button to start practising
        self.practice_button.grid(
            row=4, column=0, padx=5, pady=5, ipadx=10, ipady=10, sticky=tk.N + tk.S + tk.E + tk.W
        )
        self.practice_button.bind(
            "<Enter>", lambda event: self.show_messages("practice_button")
        )
        self.practice_button.bind(
            "<Leave>", lambda event: self.show_messages("N/A")
        )
        self.close_button.grid(
            row=5, column=0, columnspan=3, padx=5, pady=5, sticky=tk.S
        )
        self.close_button.bind(
            "<Enter>", lambda event: self.show_messages("exit_button")
        )
        self.close_button.bind(
            "<Leave>", lambda event: self.show_messages("N/A")
        )
        # self.test_button.grid(
        #     row=1, column=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        # )

        self.test_slider_Label.grid(
            row=1, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        self.test_slider.grid(
            row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        self.test_slider.bind(
            "<Enter>", lambda event: self.show_messages("checkpoints_slider")
        )

        self.test_slider.bind(
            "<Leave>", lambda event: self.show_messages("N/A")
        )

        self.connect_button.grid(
            row=3, column=0, columnspan=5, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        self.connect_button.bind(
            "<Enter>", lambda event: self.show_messages("Connect_button")
        )

        self.connect_button.bind(
            "<Leave>", lambda event: self.show_messages("N/A")
        )

    # Sets selected level, closes window and displays layout
    def level2(self):
        self.selected_level = "Medio"
        self.select_level_window.destroy()
        self.select_scenario_button["text"] = "Medio"
        self.select_scenario_button["bg"] = "#367E18"
        # show button to start practising
        self.practice_button.grid(
            row=4, column=0, padx=5, pady=5, ipadx=10, ipady=10, sticky=tk.N + tk.S + tk.E + tk.W
        )
        self.practice_button.bind(
            "<Enter>", lambda event: self.show_messages("practice_button")
        )
        self.practice_button.bind(
            "<Leave>", lambda event: self.show_messages("N/A")
        )
        self.close_button.grid(
            row=5, column=0, columnspan=3, padx=5, pady=5, sticky=tk.S + tk.E + tk.W
        )
        self.close_button.bind(
            "<Enter>", lambda event: self.show_messages("exit_button")
        )
        self.close_button.bind(
            "<Leave>", lambda event: self.show_messages("N/A")
        )
        # self.test_button.grid(
        #     row=1, column=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        # )

        self.test_slider_Label.grid(
            row=1, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        self.test_slider.grid(
            row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        self.test_slider.bind(
            "<Enter>", lambda event: self.show_messages("checkpoints_slider")
        )

        self.test_slider.bind(
            "<Leave>", lambda event: self.show_messages("N/A")
        )

        self.connect_button.grid(
            row=3, column=0, columnspan=5, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        self.connect_button.bind(
            "<Enter>", lambda event: self.show_messages("connect_button")
        )

        self.connect_button.bind(
            "<Leave>", lambda event: self.show_messages("N/A")
        )

    # Sets selected level, closes window and displays layout
    def level3(self):
        self.selected_level = "Avanzado"
        self.select_level_window.destroy()
        self.select_scenario_button["text"] = "Avanzado"
        self.select_scenario_button["bg"] = "#367E18"
        # show button to start practising
        self.practice_button.grid(
            row=4, column=0, padx=5, pady=5, ipadx=10, ipady=10, sticky=tk.N + tk.S + tk.E + tk.W
        )
        self.practice_button.bind(
            "<Enter>", lambda event: self.show_messages("practice_button")
        )
        self.practice_button.bind(
            "<Leave>", lambda event: self.show_messages("N/A")
        )
        self.close_button.grid(
            row=5, column=0, columnspan=3, padx=5, pady=5, sticky=tk.S
        )
        self.close_button.bind(
            "<Enter>", lambda event: self.show_messages("exit_button")
        )
        self.close_button.bind(
            "<Leave>", lambda event: self.show_messages("N/A")
        )
        # self.test_button.grid(
        #     row=1, column=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        # )

        self.test_slider_Label.grid(
            row=1, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        self.test_slider.grid(
            row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        self.test_slider.bind(
            "<Enter>", lambda event: self.show_messages("checkpoints_slider")
        )

        self.test_slider.bind(
            "<Leave>", lambda event: self.show_messages("N/A")
        )

        self.connect_button.grid(
            row=3, column=0, columnspan=5, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        self.connect_button.bind(
            "<Enter>", lambda event: self.show_messages("Connect_button")
        )

        self.connect_button.bind(
            "<Leave>", lambda event: self.show_messages("N/A")
        )

    # WIP: Allows to customize the scenario
    def custom_level(self):
        self.selected_level = "Personalizado"
        self.select_level_window.destroy()
        self.select_scenario_button["text"] = "Personalizado"
        self.select_scenario_button["bg"] = "#367E18"
        # show button to start practising
        self.practice_button.grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )
        self.close_button.grid(
            row=1, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

    # PRACTICE MODE

    # Creates and displays a new map window, inherited from MapFrameClass
    def show_map(self, position):
        self.new_window = tk.Toplevel(self.master)
        self.new_window.title("Map")
        self.new_window.geometry("800x600")
        self.new_window.wm_attributes('-transparentcolor', 'pink')
        self.map = MapFrameClass()
        frame = self.map.build_frame(self.new_window, position, self.selected_level)
        frame.pack(fill="both", expand="yes", padx=10, pady=10)

    # Defines obstacles and creates set of random points in the map
    def random_points(self):

        self.dronLabLimits = Polygon(
            [
                (41.2764151, 1.9882914),
                (41.2762170, 1.9883551),
                (41.2763733, 1.9890491),
                (41.2765582, 1.9889881),
            ]
        )

        self.obstacle_1 = Polygon(
            [
                (41.2764408, 1.9885938),
                (41.2764368, 1.9886494),
                (41.2763385, 1.9886407),
                (41.2763450, 1.9885878),
            ]
        )

        self.obstacle_2_1 = Polygon(
            [
                (41.2765219, 1.9888506),
                (41.2764065, 1.9888902),
                (41.2763924, 1.9888600),
                (41.2765669, 1.9887990),
            ]
        )
        self.obstacle_2_2 = Polygon(
            [
                (41.2764287, 1.9887453),
                (41.2763123, 1.9888077),
                (41.2763032, 1.9887460),
                (41.2764267, 1.9887111),
            ]
        )
        self.obstacle_2_3 = Polygon(
            [
                (41.2764569, 1.9885515),
                (41.2763461, 1.9886903),
                (41.2763274, 1.9886535),
                (41.2764473, 1.9885274),
            ]
        )

        self.top_left_corner = Polygon(
            [
                (41.2765582, 1.9882914),#not lab limit
                (41.2764151, 1.9882914),
                (41.2765582, 1.9889881),
            ]
        )

        self.top_right_corner = Polygon(
            [
                (41.2765582, 1.9889881),
                (41.2765582, 1.9890491),#not lab limit
                (41.2763733, 1.9890491),
            ]
        )

        self.bottom_left_corner = Polygon(
            [
                (41.2764151, 1.9882914),
                (41.2762170, 1.9882914),#not lab limit
                (41.2762170, 1.9883551),
            ]
        )

        self.bottom_right_corner = Polygon(
            [
                (41.2762170, 1.9883551),
                (41.2762170, 1.9890491),#not lab limit
                (41.2763733, 1.9890491),
            ]
        )

        #self.num_points = 10
        self.race_points = []
        self.timer_vector = []
        self.penalty_vector = []
        self.distance_vector = []
        self.score_vector = []

        while len(self.race_points) <= self.num_points.get()-1:

            # Generate a random x and y coordinate inside a rectangular surface
            y = random.uniform(1.9882928, 1.9890477)
            x = random.uniform(41.2762184, 41.2765568)

            self.race_point_coords = [x, y]
            self.race_point = Point(self.race_point_coords)

            # Check if the point falls within any of the avoided areas
            if self.selected_level == "Basico" \
                and self.dronLabLimits.contains(self.race_point):
                self.race_points.append(self.race_point_coords)
                # If the point doesn't fall within any of the avoided areas, add it to the list of points
            elif self.selected_level == "Medio" \
                and self.dronLabLimits.contains(self.race_point) \
                and not self.obstacle_1.contains(self.race_point):
                self.race_points.append(self.race_point_coords)
            elif self.selected_level == "Avanzado" \
                and self.dronLabLimits.contains(self.race_point) \
                and not self.obstacle_2_1.contains(self.race_point) \
                and not self.obstacle_2_2.contains(self.race_point) \
                and not self.obstacle_2_3.contains(self.race_point):
                self.race_points.append(self.race_point_coords)

    # Triggers next checkpoint
    def next_checkpoint(self):

        self.calculate_score()

        if self.checkpoint_count <= self.num_points.get():
            self.go_next_checkpoint = True

        self.timer_start = time.time()

    # Moves point for practice mode
    def movePoint(self):
        print("muevo a ", self.direction)
        bearing = None

        if self.direction == "North":
            bearing = math.radians(0)
        elif self.direction == "NorthWest":
            bearing = math.radians(315)
        elif self.direction == "NorthEast":
            bearing = math.radians(45)
        elif self.direction == "South":
            bearing = math.radians(180)
        elif self.direction == "SouthWest":
            bearing = math.radians(225)
        elif self.direction == "SouthEast":
            bearing = math.radians(135)
        elif self.direction == "East":
            bearing = math.radians(90)
        elif self.direction == "West":
            bearing = math.radians(270)
        if bearing != None:
            R = 6378.1
            d = 0.001

            lat = math.radians(self.practicePoint[0])
            lon = math.radians(self.practicePoint[1])

            lat2 = math.asin(
                math.sin(lat) * math.cos(d/R)
                + math.cos(lat) * math.sin(d/R) * math.cos(bearing)
            )

            lon2 = lon + math.atan2(
                math.sin(bearing) * math.sin(d/R) * math.cos(lat),
                math.cos(d/R) - math.sin(lat) * math.sin(lat2),
            )



            if self.selected_level == "Basico" \
                and self.dronLabLimits.contains(Point(math.degrees(lat2), math.degrees(lon2))):

                self.map.move_drone([math.degrees(lat2), math.degrees(lon2)], 'red')
                self.practicePoint = [math.degrees(lat2), math.degrees(lon2)]
                self.coords = [lat2, lon2]

            elif self.selected_level == "Medio" \
                and self.dronLabLimits.contains(Point(math.degrees(lat2), math.degrees(lon2))) \
                and not self.obstacle_1.contains(Point(math.degrees(lat2), math.degrees(lon2))):

                self.map.move_drone([math.degrees(lat2), math.degrees(lon2)], 'red')
                self.practicePoint = [math.degrees(lat2), math.degrees(lon2)]
                self.coords = [lat2, lon2]

            elif self.selected_level == "Avanzado" \
                and self.dronLabLimits.contains(Point(math.degrees(lat2), math.degrees(lon2))) \
                and not self.obstacle_2_1.contains(Point(math.degrees(lat2), math.degrees(lon2))) \
                and not self.obstacle_2_2.contains(Point(math.degrees(lat2), math.degrees(lon2))) \
                and not self.obstacle_2_3.contains(Point(math.degrees(lat2), math.degrees(lon2))):

                self.map.move_drone([math.degrees(lat2), math.degrees(lon2)], 'red')
                self.practicePoint = [math.degrees(lat2), math.degrees(lon2)]
                self.coords = [lat2, lon2]

    # Function to be called when practice button is pressed.
    def practice(self):

        # If state is disconnected practice mode starts
        if self.state == "disconnected":
            self.practice_button["bg"] = "#367E18"
            self.practice_button["text"] = "Estoy preparado. Quiero volar"
            self.select_scenario_button['state'] = 'disabled'
            self.test_slider['state'] = 'disabled'
            self.state = "practising"

            try:
                self.client = mqtt.Client("Carrera de Drones", transport="websockets")
                self.client.on_message = self.on_message
                if self.connection_mode == "global":
                    self.client.connect("broker.hivemq.com", port=8000)
                else:
                    self.client.connect("localhost", port=8000)
                self.client.subscribe("mobileApp/droneCircus/connect")
                self.client.subscribe("mobileApp/droneCircus/go")
                self.client.subscribe("mobileApp/droneCircus/checkpoint")
                print("Waiting connection")
                self.connected = "Conectado al Circo de Drones"
                self.client.publish("droneCircus/mobileApp/connect", json.dumps(self.getTestData()))
                self.client.loop_start()

            except Exception as e:
                print(f"Error:{e}")

            x = threading.Thread(target=self.practising)
            x.start()

        # If already practising, stops practice mode and shows race option
        elif self.state == "practising":
            self.state = "disconnected"

            self.practice_button.grid_forget()

            self.stop_timer_update()

            self.map.close()

            self.race_button.grid(
                row=4, column=0, padx=5, pady=5, ipadx=10, ipady=10, sticky=tk.N + tk.S + tk.E + tk.W
            )

            self.score_frame.grid_forget()
            self.help_frame.grid(
                row=5, rowspan=5, pady=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W
            )

            self.button_frame.grid(
                row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W,
            )

    # Function running whilst in practice mode
    def practising(self):
        self.direction = None
        self.go_next_checkpoint = False
        self.help_frame.pack_forget()
        # self.score_frame.pack(fill="both")
        self.score_frame.grid(
            row=5, rowspan=5, pady=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        self.practicePoint = [41.2765003, 1.9889760]
        self.checkpoint_count = 0

        self.random_points()

        self.show_map(self.practicePoint)
        self.map.show_checkpoint(self.race_points[self.checkpoint_count])

        # Poner una cuenta atras
        self.start_clock()

        # self.skip_checkpoint_button.grid(
        #     row=2, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
        # )

        #        self.client.subscribe("mobileApp/droneCircus/#")

        while self.state == "practising":

            if self.go_next_checkpoint:
                self.checkpoint_count += 1
                print("Checkpoint Count: " + str(self.checkpoint_count))
                print("Num points: " + str(self.num_points.get()))
                if self.checkpoint_count < self.num_points.get():
                    self.map.move_checkpoint(self.race_points[self.checkpoint_count])
                self.map.checkpoint_skip([math.degrees(self.coords[0]), math.degrees(self.coords[1])],
                                         self.multiplier)
                self.go_next_checkpoint = False

            if self.checkpoint_count == int(self.num_points.get()):
                print("Fin de la carrera")
                self.state = "disconnected"
                self.connected = False

                score = "Tiempo total: " + str(self.score)
                print(score)
                self.stop_timer_update()

                self.new_window.after(1650)

                self.score_window = tk.Toplevel(self.master)
                self.score_window.title("Fin de la Partida")
                self.score_window.geometry("800x600")
                score_title_frame = tk.Frame(self.score_window)
                score_title_frame.pack()
                score_title_frame.rowconfigure(0, weight=1)
                score_title_frame.columnconfigure(0, weight=1)

                self.total_score_label = tk.Label(
                    score_title_frame, fg="black", font=("", 20),
                    text="Total Score\n" + datetime.fromtimestamp(self.score).strftime('%M:%S.%f')[:-3]
                )
                self.total_score_label.grid(
                    column=0, row=0, sticky=tk.N + tk.S + tk.E + tk.W
                )

                # self.score_title = tk.Label(
                #     score_frame, fg="black", font=("", 18), text="Checkpoint\tTime\tDistance\tPenalty\tScore"
                # )
                #
                # self.score_title.grid(
                #     column=0, row=1, pady=10, padx=10, sticky=tk.N + tk.S + tk.E + tk.W
                # )

                score_frame = tk.LabelFrame(
                    score_title_frame, bg="light gray", text="Score Breakdown", height=400
                )

                checkpoint_n = ""
                time_n = ""
                distance_n = ""
                penalty_n = ""
                score_n = ""

                for i in range(int(self.num_points.get())):
                    checkpoint_n = str(checkpoint_n) + str(i + 1) + ".-\n"
                    time_n = str(time_n) + str(
                        datetime.fromtimestamp(self.timer_vector[i]).strftime('%M:%S.%f')[:-3]) + "\n"
                    distance_n = str(distance_n) + str(self.distance_vector[i]) + "\n"
                    penalty_n = str(penalty_n) + str(self.penalty_vector[i]) + "\n"
                    score_n = str(score_n) + str(
                        datetime.fromtimestamp(self.score_vector[i]).strftime('%M:%S.%f')[:-3]) + "\n"

                self.checkpoint_n_label = tk.Label(
                    score_frame, fg="black", font=("", 16), text="Checkpoint #" + "\n" + str(checkpoint_n)
                )

                self.time_label = tk.Label(
                    score_frame, fg="black", font=("", 16), text="Time" + "\n" + str(time_n)
                )

                self.distance_label = tk.Label(
                    score_frame, fg="black", font=("", 16), text="Distance" + "\n" + str(distance_n)
                )

                self.penalty_label = tk.Label(
                    score_frame, fg="black", font=("", 16), text="Penalty" + "\n" + str(penalty_n)
                )

                self.score_label = tk.Label(
                    score_frame, fg="black", font=("", 16), text="Score" + "\n" + str(score_n)
                )

                # text_var = ""

                # for i in range(int(self.num_points.get())):
                #     text_var = text_var + str(i + 1) + ".-\t" + str(datetime.fromtimestamp(self.timer_vector[i]).strftime('%M:%S.%f')[:-3]) + "\t" + str(self.distance_vector[i]) + \
                #                "\t" + str(self.penalty_vector[i]) + "\t" + str(datetime.fromtimestamp(self.score_vector[i]).strftime('%M:%S.%f')[:-3]) + "\n"

                self.checkpoint_n_label.grid(
                    column=0, row=2, pady=10, padx=10, sticky=tk.N + tk.S + tk.E + tk.W
                )

                self.time_label.grid(
                    column=1, row=2, pady=10, padx=10, sticky=tk.N + tk.S + tk.E + tk.W
                )

                self.distance_label.grid(
                    column=2, row=2, pady=10, padx=10, sticky=tk.N + tk.S + tk.E + tk.W
                )

                self.penalty_label.grid(
                    column=3, row=2, pady=10, padx=10, sticky=tk.N + tk.S + tk.E + tk.W
                )

                self.score_label.grid(
                    column=4, row=2, pady=10, padx=10, sticky=tk.N + tk.S + tk.E + tk.W
                )

                score_frame.grid(
                    column=0, row=1, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W
                )

                self.exit_btn = tk.Button(
                    score_title_frame, fg="black", text="Salir", command=self.exit
                )

                self.exit_btn.grid(
                    column=0, row=4, pady=10, padx=10, sticky=tk.N + tk.S + tk.E + tk.W
                )

                self.button_frame.grid(
                    row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W,
                )

                self.practice_button.grid_forget()
                self.score_frame.grid_forget()

                self.race_button.grid(
                    row=4, column=0, padx=5, pady=5, ipadx=10, ipady=10, sticky=tk.N + tk.S + tk.E + tk.W
                )

                self.help_frame.grid(
                    row=5, rowspan=5, pady=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W
                )

                # Aqui va el desglose de los puntos de control

                self.map.close()

    # SELECT CONNECTION MODE

    # Opens window to select between connection modes
    def select_connection_mode(self):
        if not self.connected:
            self.select_connection_mode_window = tk.Toplevel(self.master)
            self.select_connection_mode_window.title("Select connection mode")
            self.select_connection_mode_window.geometry("1200x500")
            select_connection_mode_frame = tk.Frame(self.select_connection_mode_window)
            select_connection_mode_frame.pack()
            select_connection_mode_frame.rowconfigure(0, weight=1)
            select_connection_mode_frame.rowconfigure(1, weight=1)
            select_connection_mode_frame.columnconfigure(0, weight=1)
            select_connection_mode_frame.columnconfigure(1, weight=1)

            self.image1 = Image.open("../assets_needed/connection_mode.png")
            self.image1 = self.image1.resize((2200, 450), Image.ANTIALIAS)
            self.bg1 = ImageTk.PhotoImage(self.image1)
            canvas1 = tk.Canvas(select_connection_mode_frame, width=1100, height=450)
            canvas1.create_image(0,0, image=self.bg1, anchor="nw")
            canvas1.grid(
                row=0,
                column=0,
                padx=5,
                pady=5,
                columnspan=2,
                sticky=tk.N + tk.S + tk.E + tk.W,
            )

            self.global_button = tk.Button(
                select_connection_mode_frame,
                text="Global",
                bg="#CC3636",
                fg="white",
                command=self.global_mode,
            )
            self.global_button.grid(
                row=1, column=0, padx=20, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
            )
            self.local_button = tk.Button(
                select_connection_mode_frame,
                text="Local",
                bg="#CC3636",
                fg="white",
                command=self.local_mode,
            )
            self.local_button.grid(
                row=1, column=1, padx=20, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
            )
        elif self.state != "flying":
            self.connect_button["text"] = "connect"
            self.connect_button["bg"] = ("#CC3636",)
            self.client.publish("droneCircus/autopilotService/disconnect")
            # self.cap.release()
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False
            self.state = "disconnected"
        else:
            messagebox.showwarning(
                "Error",
                "No puedes desconectar. Estas volando",
                parent=self.master,
            )

    # Sets global connection mode
    def global_mode(self):
        self.connection_mode = "global"
        self.select_connection_mode_window.destroy()
        self.practice_button['state'] = 'normal'
        #self.connect()

    # Sets local connection mode
    def local_mode(self):
        self.connection_mode = "local"
        self.select_connection_mode_window.destroy()
        self.practice_button['state'] = 'normal'
        #self.connect()

    # Unused
    def connect(self):
        #does not allow to connect if there is no scenario selected
        if self.select_scenario_button["bg"] == "#367E18":
            if self.connection_mode == "global":
                # in global mode, the external broker must be running in internet
                # and must operate with websockets
                # there are several options:
                # a public broker

                external_broker_address = "broker.hivemq.com"

                # our broker (that requires credentials)
                # external_broker_address = "classpip.upc.edu"
                # a mosquitto broker running at localhost (only in simulation mode)
                # external_broker_address = "localhost"

            else:
                # in local mode, the external broker will run always in localhost
                # (either in production or simulation mode)
                # use this when connecting with the RPi

                external_broker_address = "10.10.10.1"

                # external_broker_address = "localhost"

            external_broker_port = 8000

            self.client = mqtt.Client("Race", transport="websockets")
            self.client.on_message = self.on_message
            print("voy a conectarme al broker en modo ", self.connection_mode)
            self.client.connect(external_broker_address, external_broker_port)
            self.client.loop_start()
            self.connected = True
            self.close_button2.grid_forget()
            self.client.subscribe("autopilotService/droneCircus/#")
            self.client.subscribe("mobileApp/droneCircus/#")
            self.client.publish("droneCircus/autopilotService/connect")
            self.client.publish("droneCircus/monitor/start")
            self.connect_button["text"] = "connecting..."
            self.connect_button["bg"] = "orange"
        else:
            messagebox.showwarning(
                "Error",
                "Antes de conectar debes fijar el escenario", parent=self.master,
            )

    # FLY MODE

    def checklimits(self, position):

        lat2 = position[0]
        lon2 = position[1]

        R = 6378.1
        d = 0.003

        bearing = math.radians(self.heading)

        lat3 = math.asin(
                math.sin(lat2) * math.cos(d/R)
                + math.cos(lat2) * math.sin(d/R) * math.cos(bearing)
            )

        lon3 = lon2 + math.atan2(
                math.sin(bearing) * math.sin(d/R) * math.cos(lat2),
                math.cos(d/R) - math.sin(lat2) * math.sin(lat3),
            )

        if self.selected_level == "Basico" \
                and self.dronLabLimits.contains(Point(math.degrees(lat3), math.degrees(lon3))):
            return True

        elif self.selected_level == "Medio" \
                and self.dronLabLimits.contains(Point(math.degrees(lat3), math.degrees(lon3))) \
                and not self.obstacle_1.contains(Point(math.degrees(lat3), math.degrees(lon3))):
            return True

        elif self.selected_level == "Avanzado" \
             and self.dronLabLimits.contains(Point(math.degrees(lat3), math.degrees(lon3))) \
             and not self.obstacle_2_1.contains(Point(math.degrees(lat3), math.degrees(lon3))) \
             and not self.obstacle_2_2.contains(Point(math.degrees(lat3), math.degrees(lon3))) \
             and not self.obstacle_2_3.contains(Point(math.degrees(lat3), math.degrees(lon3))):
            return True
        else:
            return False

    # Function to be called when race button is pressed.
    def fly(self):
        # Set connection mode based on selection
        if self.connection_mode == "global":
            external_broker_address = "broker.hivemq.com"
        elif self.connection_mode == "local":
            external_broker_address = "localhost"
        else:
            external_broker_address = "10.10.10.1"

        # Start connection sequence and begin racing
        external_broker_port = 8000
        self.client = mqtt.Client("Circo de Drones", transport="websockets")
        self.client.on_message = self.on_message
        self.client.connect(external_broker_address, external_broker_port)
        self.client.loop_start()
        self.connected = True
        self.client.subscribe("mobileApp/droneCircus/race")
        self.client.subscribe("droneCircus/mobileApp/resendTelemetry")
        print("Waiting connection")
        self.connected = "Conectado al Autopiloto"
        self.client.publish("droneCircus/mobileApp/race")
        self.client.loop_start()

    # Function running whilst in race mode
    def racing(self):
        self.stopped = False
        self.direction = None
        self.go_next_checkpoint = False
        self.help_frame.pack_forget()
        # self.score_frame.pack(fill="both")
        self.score_frame.grid(
            row=5, rowspan=5, pady=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W
        )

        self.checkpoint_count = 0
        self.random_points()

        self.show_map((math.degrees(self.coords[0]), math.degrees(self.coords[1])))

        self.map.show_checkpoint(self.race_points[self.checkpoint_count])
        self.start_clock()

        while self.state == "flying":

            if not self.checklimits((self.coords[0], self.coords[1])):
                if not self.stopped:
                    self.client.publish("droneCircus/mobileApp/stop")
                    self.stopped = True

            elif self.checklimits((self.coords[0], self.coords[1])) and self.stopped:
                self.stopped = False

            if self.go_next_checkpoint:
                self.checkpoint_count += 1
                print("Checkpoint Count: " + str(self.checkpoint_count))
                print("Num points: " + str(self.num_points.get()))
                if self.checkpoint_count < self.num_points.get():
                    self.map.move_checkpoint(self.race_points[self.checkpoint_count])
                self.map.checkpoint_skip([math.degrees(self.coords[0]), math.degrees(self.coords[1])], self.multiplier)
                self.go_next_checkpoint = False

            if self.checkpoint_count == int(self.num_points.get()):
                print("Fin de la carrera")
                self.state = "disconnected"
                self.connected = False

                score = "Tiempo total: " + str(self.score)
                print(score)
                self.stop_timer_update()

                self.new_window.after(1650)

                self.score_window = tk.Toplevel(self.master)
                self.score_window.title("Fin de la Partida")
                self.score_window.geometry("800x600")
                score_title_frame = tk.Frame(self.score_window)
                score_title_frame.pack()
                score_title_frame.rowconfigure(0, weight=1)
                score_title_frame.columnconfigure(0, weight=1)

                self.total_score_label = tk.Label(
                    score_title_frame, fg="black", font=("", 20),
                    text="Total Score\n" + datetime.fromtimestamp(self.score).strftime('%M:%S.%f')[:-3]
                )
                self.total_score_label.grid(
                    column=0, row=0, sticky=tk.N + tk.S + tk.E + tk.W
                )

                # self.score_title = tk.Label(
                #     score_frame, fg="black", font=("", 18), text="Checkpoint\tTime\tDistance\tPenalty\tScore"
                # )
                #
                # self.score_title.grid(
                #     column=0, row=1, pady=10, padx=10, sticky=tk.N + tk.S + tk.E + tk.W
                # )

                score_frame = tk.LabelFrame(
                    score_title_frame, bg="light gray", text="Score Breakdown", height=400
                )

                checkpoint_n = ""
                time_n = ""
                distance_n = ""
                penalty_n = ""
                score_n = ""

                for i in range(int(self.num_points.get())):
                    checkpoint_n = str(checkpoint_n) + str(i + 1) + ".-\n"
                    time_n = str(time_n) + str(datetime.fromtimestamp(self.timer_vector[i]).strftime('%M:%S.%f')[:-3]) + "\n"
                    distance_n = str(distance_n) + str(self.distance_vector[i]) + "\n"
                    penalty_n = str(penalty_n) + str(self.penalty_vector[i]) + "\n"
                    score_n = str(score_n) + str(datetime.fromtimestamp(self.score_vector[i]).strftime('%M:%S.%f')[:-3]) + "\n"


                self.checkpoint_n_label = tk.Label(
                    score_frame, fg="black", font=("", 16), text="Checkpoint #" + "\n" + str(checkpoint_n)
                )

                self.time_label = tk.Label(
                    score_frame, fg="black", font=("", 16), text="Time" + "\n" + str(time_n)
                )

                self.distance_label  =tk.Label(
                    score_frame, fg="black", font=("", 16), text="Distance" + "\n" + str(distance_n)
                )

                self.penalty_label = tk.Label(
                    score_frame, fg="black", font=("", 16), text="Penalty" + "\n" + str(penalty_n)
                )

                self.score_label = tk.Label(
                    score_frame, fg="black", font=("", 16), text="Score" + "\n" + str(score_n)
                )

                #text_var = ""

                # for i in range(int(self.num_points.get())):
                #     text_var = text_var + str(i + 1) + ".-\t" + str(datetime.fromtimestamp(self.timer_vector[i]).strftime('%M:%S.%f')[:-3]) + "\t" + str(self.distance_vector[i]) + \
                #                "\t" + str(self.penalty_vector[i]) + "\t" + str(datetime.fromtimestamp(self.score_vector[i]).strftime('%M:%S.%f')[:-3]) + "\n"

                self.checkpoint_n_label.grid(
                    column=0, row=2, pady=10, padx=10, sticky=tk.N + tk.S + tk.E + tk.W
                )

                self.time_label.grid(
                    column=1, row=2, pady=10, padx=10, sticky=tk.N + tk.S + tk.E + tk.W
                )

                self.distance_label.grid(
                    column=2, row=2, pady=10, padx=10, sticky=tk.N + tk.S + tk.E + tk.W
                )

                self.penalty_label.grid(
                    column=3, row=2, pady=10, padx=10, sticky=tk.N + tk.S + tk.E + tk.W
                )

                self.score_label.grid(
                    column=4, row=2, pady=10, padx=10, sticky=tk.N + tk.S + tk.E + tk.W
                )

                score_frame.grid(
                    column=0, row=1, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W
                )

                self.exit_btn = tk.Button(
                    score_title_frame, fg="black", text="Salir", command=self.exit
                )

                self.exit_btn.grid(
                    column=0, row=4, pady=10, padx=10, sticky=tk.N + tk.S + tk.E + tk.W
                )

                self.button_frame.grid(
                    row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W,
                )

                # Aqui va el desglose de los puntos de control

                self.map.close()

    # Function used to test, unused
    def test(self):
        try:
            self.client = mqtt.Client("Carrera de Drones", transport="websockets")
            self.client.on_message = self.on_message
            self.client.connect("localhost", port=8000)
            self.client.subscribe("mobileApp/droneCircus/connect")
            self.client.subscribe("mobileApp/droneCircus/go")
            self.client.subscribe("mobileApp/droneCircus/checkpoint")
            print("Waiting connection")
            self.client.publish("droneCircus/mobileApp/connect")
            self.client.loop_start()
            self.connected = "Conectado al Circo de Drones"

        except Exception as e:
            print(f"Error:{e}")

    # MESSAGE MANAGEMENT

    # Get function for connected value
    def getTestData(self):

        testData = {
            'connected': self.connected
        }

        return testData

    # Get function for penalty value
    def getPenalty(self):

        penalty = {
            'penalty': str(self.multiplier)
        }

        return penalty

    # Function called whenever new mosquitto message is received
    def on_message(self, cli, userdata, message):

        # Split message in origin, destination and command
        splitted = message.topic.split("/")
        origin = splitted[0]
        destination = splitted[1]
        command = splitted [2]

        if command == "connect":
            print(origin, "connected to ", destination)
            # self.client.publish("droneCircus/mobileApp/connect", json.dumps(self.getTestData()))

        if command == "go":

            self.direction = message.payload.decode("utf-8")

            self.movePoint()
            self.distance_display.config(text="Distancia: " + str(round(self.distance(), 3)))
            print("Moviéndome al ", self.direction)

        if command == "checkpoint":

            if self.distance() < 5:
                self.next_checkpoint()
                print("Quedan ", int(self.num_points.get()) - self.checkpoint_count, "puntos de control")
                self.checkpoint_count_label.config(text="Checkpoints remaining: " + str(int(self.num_points.get()-self.checkpoint_count)))
                print("Estado: " + str(self.state))
                self.client.publish("droneCircus/mobileApp/checkpoint", json.dumps(self.getPenalty()))
            else:
                print("Estas demasiado lejos del punto de control")

        if command == "resendTelemetry":
            telemetry_info = json.loads(message.payload)
            lat = telemetry_info["lat"]
            lon = telemetry_info["lon"]
            self.heading = telemetry_info["heading"]
            self.coords = [math.radians(lat), math.radians(lon)]
            state = telemetry_info["state"]
            if state == "connected" and self.state != "connected":
                #self.show_map((lat, lon))
                self.state = "connected"
            elif state == "armed":
                self.state = "armed"
            elif state == "flying" and self.state != "flying":
                #
                self.state = "flying"
                x = threading.Thread(target=self.racing)
                x.start()
            elif state == "flying" and self.state == "flying":
                if not self.stopped:
                    self.map.move_drone((lat, lon), "red")
                self.distance_display.config(text="Distancia: " + str(round(self.distance(), 3)))
            elif state == "returningHome":
                self.map.move_drone((lat, lon), "brown")
                self.state = "returningHome"
            elif(
                state == "onHearth"
                and self.state != "onHearth"
                and self.state != "disconnected"
            ):
                self.map.mark_at_home()
                messagebox.showwarning(
                    "Success", "Ya estamos en casa", parent=self.master
                )
            self.race_button.config(
                text=self.state
            )

            print(state)

    # SCORE CALCULATION

    # Start timer from 0
    def start_clock(self):
        global timer_updating
        timer_updating = True
        self.start_time = time.time()
        self.timer_start = time.time()
        self.actual_time = 0

        print("Comienza la carrera!")
        #self.update_timer()
        x = threading.Thread(target=self.update_timer)
        x.start()

    # Pause timer
    def stop_timer_update(self):
        global timer_updating
        timer_updating = False

    # Function to be called whilst timer is running
    def update_timer(self):
        mins = 0
        while timer_updating:
            current_time = - self.timer_start + time.time()

            # if self.checkpoint_count != 0:
                #self.score_display.config(text="Time: {mins:2}:{actual_time:2.2f}".format(mins=0, actual_time=actual_time))
                #self.score_display.after(10000)
            self.actual_time = float(self.score) + (time.time() - self.start_time)
            self.score_display.config(text="Time: "+datetime.fromtimestamp(self.actual_time).strftime('%M:%S.%f')[:-3])
            #
            # else:
            #     #self.score_display.config(text="Time: {mins:2}:{current_time:2.2f}".format(mins=0, current_time=current_time))
            #     #self.score_display.after(10000)
            #     #self.score_display.after(10000, self.update_timer())
            #     self.score_display.config(text="Time: "+datetime.fromtimestamp(current_time).strftime('%M:%S.%f')[:-3])

    # Get function for elapsed timer time.
    def get_elapsed_time(self):
        if self.start_time is None:
            print( "Aun no ha empezado la carrera" )

        else:
            self.elapsed_time = time.time() - self.start_time
            self.start_time = time.time()
        #print("Tiempo: ", self.elapsed_time)
        return self.elapsed_time

    # Calculate distance to the current checkpoint
    def distance(self):
        lat1 = math.radians(self.race_points[self.checkpoint_count][0])
        lon1 = math.radians(self.race_points[self.checkpoint_count][1])

        lat2 = self.coords[0]
        lon2 = self.coords[1]

        #lat1 = math.radians(41.276337625595026)
        #lon1 = math.radians(1.9885984525481781)

        #lat2 = math.radians(41.275583720151594)
        #lon2 = math.radians(1.9872305259411154)
        #lat2 = math.radians(41.2763013415753)
        #lon2 = math.radians(1.988534079531375)

        var_lat = lat2 - lat1
        var_lon = lon2 - lon1

        a = math.sin(var_lat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(var_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = 6371000 * c #Radius of the Earth in m

        return distance

    # Calculates score time based on timer time and distance to current checkpoint and stores current stage data
    def calculate_score(self):
        distance = self.distance()

        print("Distancia: ", self.distance())

        elapsed_time = self.get_elapsed_time()

        # if self.checkpoint_count == 0:
        #     race_time = 0
        # else:
        race_time = self.score
        if distance <= 0.5:
            race_time = race_time + elapsed_time
            self.multiplier = 1
        elif 0.5 < distance <= 1:
            race_time = race_time + 1.1 * elapsed_time
            self.multiplier = 1.1
        elif 1 < distance <= 2.5:
            race_time = race_time + 1.5 * elapsed_time
            self.multiplier = 1.5
        elif 2.5 < distance <= 4:
            race_time = race_time + 1.8 * elapsed_time
            self.multiplier = 1.8
        elif 4 < distance <= 5:
            race_time = race_time + 2 * elapsed_time
            self.multiplier = 2

        self.score = race_time

        self.timer_vector.append(round(elapsed_time, 3))
        self.score_vector.append(self.score)
        self.penalty_vector.append(format(self.multiplier, '.3f'))
        self.distance_vector.append(round(distance, 3))
        print(self.score)
        return race_time

