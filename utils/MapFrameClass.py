import math
import threading
import time
import tkinter as tk
import tkintermapview
from geographiclib.geodesic import Geodesic
from PIL import Image, ImageTk


class ComputeCoords:
    def __init__(self):
        self.geod = Geodesic.WGS84
        self.ppm = 1 / 0.1122
        # one point (x,y) in the canvas and the corresponding position (lat,lon)
        self.refCoord = [651, 279]
        self.refPosition = [41.2763748, 1.9889669]


    def convert(self, position):
        g = self.geod.Inverse(
            float(position[0]),
            float(position[1]),
            self.refPosition[0],
            self.refPosition[1],
        )
        azimuth = 180 - float(g["azi2"])
        dist = float(g["s12"])

        # ATENCION: NO SE POR QUE AQUI TENGO QUE RESTAR EN VEZ DE SUMAR
        x = self.refCoord[0] - math.trunc(
            dist * self.ppm * math.sin(math.radians(azimuth))
        )
        y = self.refCoord[1] - math.trunc(
            dist * self.ppm * math.cos(math.radians(azimuth))
        )
        return x, y


class MapFrameClass:
    def __init__(self):
        self.next_checkpoint_map = None
        self.father_frame = None
        self.map_frame = None
        self.drone_lat = None
        self.drone_lon = None
        self.map_widget = None
        self.geod = None
        self.ppm = None
        self.drone_x = None
        self.drone_y = None
        self.checkpoint_x = None
        self.checkpoint_y = None
        self.to_east = None
        self.to_west = None
        self.to_north = None
        self.to_south = None
        self.dest = None
        self.gif0_frames = []
        self.gif1_frames = []
        self.gif2_frames = []
        self.gif3_frames = []
        self.gif4_frames = []
        self.frame_count = -1
        self.current_frame = None

    def build_frame(self, father_frame, position, selected_level):
        self.father_frame = father_frame
        self.map_frame = tk.Frame(father_frame)
        self.converter = ComputeCoords()
        self.drone_lat = float(position[0])
        self.drone_lon = float(position[1])

        self.map_frame.rowconfigure(0, weight=1)
        self.map_frame.columnconfigure(0, weight=1)

        if selected_level == "Basico":
            self.image = Image.open("../assets_needed/caso1.png")
        elif selected_level == "Medio":
            self.image = Image.open("../assets_needed/caso2.png")
        else:
            self.image = Image.open("../assets_needed/caso3.png")

        self.image = self.image.resize((800, 600), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(self.map_frame, width=800, height=600)
        self.canvas.grid(row=0, column=0, sticky="nesw")
        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")

        self.ppm = 1 / 0.1122

        self.drone_x, self.drone_y = self.converter.convert(position)

        self.point = self.canvas.create_oval(
            self.drone_x - 8,
            self.drone_y - 8,
            self.drone_x + 8,
            self.drone_y + 8,
            fill="blue",
        )

        # lines pointing to North, South, East and West
        point_north_x = self.drone_x + math.trunc(
            5 * self.ppm * math.sin(math.radians(180))
        )
        point_north_y = self.drone_y + math.trunc(
            5 * self.ppm * math.cos(math.radians(180))
        )
        self.to_north = self.canvas.create_line(
            self.drone_x, self.drone_y, point_north_x, point_north_y, fill="blue"
        )
        self.N = self.canvas.create_text(
            point_north_x,
            point_north_y,
            fill="yellow",
            text="N",
            font=("Helvetica 18 bold"),
        )

        point_east_x = self.drone_x + math.trunc(
            5 * self.ppm * math.sin(math.radians(90))
        )
        point_east_y = self.drone_y + math.trunc(
            5 * self.ppm * math.cos(math.radians(90))
        )
        self.to_east = self.canvas.create_line(
            self.drone_x, self.drone_y, point_east_x, point_east_y, fill="yellow"
        )

        self.E = self.canvas.create_text(
            point_east_x,
            point_east_y,
            fill="yellow",
            text="E",
            font=("Helvetica 18 bold"),
        )

        point_south_x = self.drone_x + math.trunc(
            5 * self.ppm * math.sin(math.radians(0))
        )
        point_south_y = self.drone_y + math.trunc(
            5 * self.ppm * math.cos(math.radians(0))
        )
        self.to_south = self.canvas.create_line(
            self.drone_x, self.drone_y, point_south_x, point_south_y, fill="pink"
        )
        self.S = self.canvas.create_text(
            point_south_x,
            point_south_y,
            fill="yellow",
            text="S",
            font=("Helvetica 18 bold"),
        )

        point_west_x = self.drone_x + math.trunc(
            5 * self.ppm * math.sin(math.radians(270))
        )
        point_west_y = self.drone_y + math.trunc(
            5 * self.ppm * math.cos(math.radians(270))
        )
        self.to_west = self.canvas.create_line(
            self.drone_x, self.drone_y, point_west_x, point_west_y, fill="green"
        )

        self.W = self.canvas.create_text(
            point_west_x,
            point_west_y,
            fill="yellow",
            text="W",
            font=("Helvetica 18 bold"),
        )
        self.message = None

        x = threading.Thread(target=self.ready_gifs())
        x.start()


        return self.map_frame

    def putText(self, message):
        if self.message in self.canvas.find_all():
            self.canvas.delete(self.message)
        self.message = self.canvas.create_text(
            400, 500, fill="yellow", text=message, font=("Helvetica 30 bold")
        )

    """
    def set_destination(self, position):
        position[0] = 41.2763108
        position[1] = 1.9883282

        g = self.geod.Inverse(
            self.drone_lat, self.drone_lon, float(position[0]), float(position[1])
        )

        azimuth = 180 - float(g["azi2"])
        dist = float(g["s12"])
        print("*****", dist, azimuth)

        dest_x = self.drone_x + math.trunc(
            dist * self.ppm * math.sin(math.radians(azimuth))
        )
        dest_y = self.drone_y + math.trunc(
            dist * self.ppm * math.cos(math.radians(azimuth))
        )

        self.dest = self.map_widget.canvas.create_oval(
            dest_x - 8, dest_y - 8, dest_x + 8, dest_y + 8, fill="green"
        )
    """

    def move_drone(self, position, color):
        self.drone_x, self.drone_y = self.converter.convert(position)

        self.canvas.itemconfig(self.point, fill=color)

        self.canvas.coords(
            self.point,
            self.drone_x - 8,
            self.drone_y - 8,
            self.drone_x + 8,
            self.drone_y + 8,
        )
        self.drone_lat = float(position[0])
        self.drone_lon = float(position[1])

        self.canvas.delete(self.to_south)
        self.canvas.delete(self.to_east)
        self.canvas.delete(self.to_north)
        self.canvas.delete(self.to_west)

        self.canvas.delete(self.N)
        self.canvas.delete(self.E)
        self.canvas.delete(self.S)
        self.canvas.delete(self.W)

        # lines pointing to North, South, East and West
        point_north_x = self.drone_x + math.trunc(
            5 * self.ppm * math.sin(math.radians(180))
        )
        point_north_y = self.drone_y + math.trunc(
            5 * self.ppm * math.cos(math.radians(180))
        )
        self.to_north = self.canvas.create_line(
            self.drone_x, self.drone_y, point_north_x, point_north_y, fill="blue"
        )
        self.N = self.canvas.create_text(
            point_north_x,
            point_north_y,
            fill="yellow",
            text="N",
            font=("Helvetica 18 bold"),
        )

        point_east_x = self.drone_x + math.trunc(
            5 * self.ppm * math.sin(math.radians(90))
        )
        point_east_y = self.drone_y + math.trunc(
            5 * self.ppm * math.cos(math.radians(90))
        )
        self.to_east = self.canvas.create_line(
            self.drone_x, self.drone_y, point_east_x, point_east_y, fill="yellow"
        )

        self.E = self.canvas.create_text(
            point_east_x,
            point_east_y,
            fill="yellow",
            text="E",
            font=("Helvetica 18 bold"),
        )

        point_south_x = self.drone_x + math.trunc(
            5 * self.ppm * math.sin(math.radians(0))
        )
        point_south_y = self.drone_y + math.trunc(
            5 * self.ppm * math.cos(math.radians(0))
        )
        self.to_south = self.canvas.create_line(
            self.drone_x, self.drone_y, point_south_x, point_south_y, fill="pink"
        )
        self.S = self.canvas.create_text(
            point_south_x,
            point_south_y,
            fill="yellow",
            text="S",
            font=("Helvetica 18 bold"),
        )

        point_west_x = self.drone_x + math.trunc(
            5 * self.ppm * math.sin(math.radians(270))
        )
        point_west_y = self.drone_y + math.trunc(
            5 * self.ppm * math.cos(math.radians(270))
        )
        self.to_west = self.canvas.create_line(
            self.drone_x, self.drone_y, point_west_x, point_west_y, fill="green"
        )

        self.W = self.canvas.create_text(
            point_west_x,
            point_west_y,
            fill="yellow",
            text="W",
            font=("Helvetica 18 bold"),
        )

    def mark_at_home(self):
        self.canvas.itemconfig(self.point, fill="blue")

    # DRONE CIRCUS RACE MODE

    # Function to show chekpoints
    def show_checkpoint(self, position):
        self.checkpoint_x, self.checkpoint_y = self.converter.convert(position)

        self.checkpoint = self.canvas.create_oval(
            self.checkpoint_x - 8,
            self.checkpoint_y - 8,
            self.checkpoint_x + 8,
            self.checkpoint_y + 8,
            fill="yellow",
        )

    # Function to pre-load gif frames for animations
    def ready_gifs(self):

        gif0_image = Image.open("../assets_needed/Best_checkpoint2.gif")
        gif1_image = Image.open("../assets_needed/Good_checkpoint2.gif")
        gif2_image = Image.open("../assets_needed/Medium_checkpoint2.gif")
        gif3_image = Image.open("../assets_needed/Bad_checkpoint2.gif")
        gif4_image = Image.open("../assets_needed/Worst_checkpoint2.gif")

        for r in range(0, gif0_image.n_frames):
            gif0_image.seek(r)
            self.gif0_frames.append(gif0_image.copy().resize((150, 150)))

        for r in range(0, gif1_image.n_frames):
            gif1_image.seek(r)
            self.gif1_frames.append(gif1_image.copy().resize((150, 150)))

        for r in range(0, gif2_image.n_frames):
            gif2_image.seek(r)
            self.gif2_frames.append(gif2_image.copy().resize((150, 150)))

        for r in range(0, gif3_image.n_frames):
            gif3_image.seek(r)
            self.gif3_frames.append(gif3_image.copy().resize((150, 150)))

        for r in range(0, gif4_image.n_frames):
            gif4_image.seek(r)
            self.gif4_frames.append(gif4_image.copy().resize((150, 150)))

        self.frame_delay = 125

        self.gif_canvas_image = tk.Label(self.canvas, background='pink')
        self.gif_canvas_image.pack()

    # Function called when chekpoint is reached
    def checkpoint_skip(self, position, multiplier):
        self.next_checkpoint_map = True

        print("Next checkpoint: " + str(self.next_checkpoint_map))

        self.play_gif(position, multiplier)

    # Displays gif animation based on penalty multiplier
    def play_gif(self, position, multiplier):
        print("Playing")
        self.gif_x, self.gif_y = self.converter.convert(position)

        while self.next_checkpoint_map is True:
            if self.frame_count >= len(self.gif0_frames) - 1:
                self.canvas.delete(image)
                self.frame_count = -1
                self.next_checkpoint_map = False

            else:
                self.frame_count += 1

                # Checkpoint Animation Logic

                if multiplier == 1:
                    self.current_frame = ImageTk.PhotoImage(self.gif0_frames[self.frame_count])
                    image = self.canvas.create_image(int(self.gif_x), int(self.gif_y), image=self.current_frame)
                    print(self.frame_count)

                elif multiplier == 1.1:
                    self.current_frame = ImageTk.PhotoImage(self.gif1_frames[self.frame_count])
                    image = self.canvas.create_image(int(self.gif_x), int(self.gif_y), image=self.current_frame)
                    print(self.frame_count)

                elif multiplier == 1.5:
                    self.current_frame = ImageTk.PhotoImage(self.gif2_frames[self.frame_count])
                    image = self.canvas.create_image(int(self.gif_x), int(self.gif_y), image=self.current_frame)
                    print(self.frame_count)

                elif multiplier == 1.8:
                    self.current_frame = ImageTk.PhotoImage(self.gif3_frames[self.frame_count])
                    image = self.canvas.create_image(int(self.gif_x), int(self.gif_y), image=self.current_frame)
                    print(self.frame_count)

                elif multiplier == 2:
                    self.current_frame = ImageTk.PhotoImage(self.gif4_frames[self.frame_count])
                    image = self.canvas.create_image(int(self.gif_x), int(self.gif_y), image=self.current_frame)
                    print(self.frame_count)

                self.canvas.after(self.frame_delay)

    # Unused test function
    def show_precision(self, lat, lon, color, duration):
        self.circle_x = math.degrees(lat)
        self.circle_y = math.degrees(lon)

        self.position = [self.circle_x, self.circle_y]

        self.circle_1_x, self.circle_1_y = self.converter.convert(self.position)

        frame_delay = 0
        #
        #
        # self.circle = self.canvas.create_oval(
        #     self.circle_1_x + 20,
        #     self.circle_1_y + 20,
        #     self.circle_1_x - 20,
        #     self.circle_1_y - 20,
        #     outline="green",
        #
        #     #fill="green",
        #     width=6,
        # )



        #self.canvas.after(3000)

        # opacity_decrement = 1.0 / (duration/100)
        #
        # for i in range(duration//100):
        #     opacity = 1.0 - (i * opacity_decrement)
        #     self.canvas.itemconfig(self.circle, outline=f"gray{opacity*100:.0f}")
        #     self.canvas.update()
        #     self.canvas.after(100)

        #self.canvas.delete(self.circle)

    # Function to show next checkpoint
    def move_checkpoint(self, position):
        self.checkpoint_x, self.checkpoint_y = self.converter.convert(position)

        self.canvas.coords(
            self.checkpoint,
            self.checkpoint_x - 8,
            self.checkpoint_y - 8,
            self.checkpoint_x + 8,
            self.checkpoint_y + 8,
        )

    # Function to close map
    def close(self):
        self.father_frame.destroy()
