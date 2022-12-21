import math
import time
import tkinter as tk
import tkintermapview
from geographiclib.geodesic import Geodesic


class MapFrameClass:
    def __init__(self):
        self.father_frame = None
        self.map_frame = None
        self.drone_lat = None
        self.drone_lon = None
        self.map_widget = None
        self.geod = None
        self.ppm = None
        self.drone_x = None
        self.drone_y = None
        self.to_east = None
        self.to_west = None
        self.to_north = None
        self.to_south = None
        self.dest = None

    def build_frame(self, father_frame, position, selected_level):
        self.father_frame = father_frame
        self.map_frame = tk.Frame(father_frame)
        self.drone_lat = float(position[0])
        self.drone_lon = float(position[1])
        print("drone position ", position)

        self.map_frame.rowconfigure(0, weight=1)
        self.map_frame.columnconfigure(0, weight=1)

        dron_lab_center_point = [41.2763551, 1.9886434]

        self.map_widget = tkintermapview.TkinterMapView(
            self.map_frame, width=800, height=600, corner_radius=0
        )
        self.map_widget.grid(row=0, column=0, sticky="nesw")
        self.map_widget.set_tile_server(
            "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=20
        )
        # to center the map
        self.map_widget.set_position(dron_lab_center_point[0], dron_lab_center_point[1])
        self.map_widget.set_zoom(20)
        time.sleep(5)

        print(
            self.map_widget.canvas.winfo_reqwidth(),
            self.map_widget.canvas.winfo_reqheight(),
        )
        self.geod = Geodesic.WGS84
        self.ppm = 1 / 0.1122
        # one point (x,y) in the canvas and the corresponding position (lat,lon)
        x = 402
        y = 260
        position = [41.27638533666021, 1.9886594932540902]

        g = self.geod.Inverse(self.drone_lat, self.drone_lon, position[0], position[1])
        azimuth = 180 - float(g["azi2"])
        dist = float(g["s12"])

        # ATENCION: NO SE POR QUE AQUI TENGO QUE RESTAR EN VEZ DE SUMAR
        self.drone_x = x - math.trunc(dist * self.ppm * math.sin(math.radians(azimuth)))
        self.drone_y = y - math.trunc(dist * self.ppm * math.cos(math.radians(azimuth)))

        self.point = self.map_widget.canvas.create_oval(
            self.drone_x - 8,
            self.drone_y - 8,
            self.drone_x + 8,
            self.drone_y + 8,
            fill="blue",
        )

        # lines pointing to North, South, East and West
        point_north_x = self.drone_x + math.trunc(
            10 * self.ppm * math.sin(math.radians(180))
        )
        point_north_y = self.drone_y + math.trunc(
            10 * self.ppm * math.cos(math.radians(180))
        )
        self.to_north = self.map_widget.canvas.create_line(
            self.drone_x, self.drone_y, point_north_x, point_north_y, fill="blue"
        )

        point_east_x = self.drone_x + math.trunc(
            10 * self.ppm * math.sin(math.radians(90))
        )
        point_east_y = self.drone_y + math.trunc(
            10 * self.ppm * math.cos(math.radians(90))
        )
        self.to_east = self.map_widget.canvas.create_line(
            self.drone_x, self.drone_y, point_east_x, point_east_y, fill="yellow"
        )

        point_south_x = self.drone_x + math.trunc(
            10 * self.ppm * math.sin(math.radians(0))
        )
        point_south_y = self.drone_y + math.trunc(
            10 * self.ppm * math.cos(math.radians(0))
        )
        self.to_south = self.map_widget.canvas.create_line(
            self.drone_x, self.drone_y, point_south_x, point_south_y, fill="pink"
        )

        point_west_x = self.drone_x + math.trunc(
            10 * self.ppm * math.sin(math.radians(270))
        )
        point_west_y = self.drone_y + math.trunc(
            10 * self.ppm * math.cos(math.radians(270))
        )
        self.to_west = self.map_widget.canvas.create_line(
            self.drone_x, self.drone_y, point_west_x, point_west_y, fill="green"
        )
        dron_lab_limits = self.map_widget.set_polygon(
            [
                (41.27640750, 1.98829200),  # Index 1: Same point as index N.
                (41.27622110, 1.98836580),
                (41.27637020, 1.98906320),
                (41.27655070, 1.98899210),
                (41.27640750, 1.98829200),
            ],
            outline_color="red",
        )

        # self.map_widget.canvas.tag_raise(self.point)

        # self.map_widget.add_left_click_map_command(self.left_click_event)

        self.map_widget.canvas.bind("<ButtonPress-1>", self.click)
        if selected_level == "Medio":
            self.set_case1()
        elif selected_level == "Avanzado":
            self.set_case2()

        return self.map_frame

    def click(self, e):
        print("click:", e)
        p = self.map_widget.convert_canvas_coords_to_decimal_coords(e.x, e.y)
        print("point:", p)

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

    def set_case1(self):
        case1_fence = self.map_widget.set_polygon(
            [
                (41.27639040, 1.98845029),
                (41.27642971, 1.98849052),
                (41.27633497, 1.98878422),
                (41.27632186, 1.98874131),
                (41.27639040, 1.98845029),
            ],
            fill_color="red",
            outline_color=None,
        )

    def set_case2(self):
        case2_fence_1 = self.map_widget.set_polygon(
            [
                (41.27648111, 1.98836982),
                (41.27649320, 1.98841810),
                (41.27628659, 1.98849723),
                (41.27628155, 1.98847845),
                (41.27648111, 1.98836982),
            ],
            fill_color="red",
            outline_color=None,
        )
        case2_fence_2 = self.map_widget.set_polygon(
            [
                (41.27640552, 1.98860586),
                (41.27641257, 1.98864743),
                (41.27624325, 1.98871583),
                (41.27623720, 1.98868766),
                (41.27640552, 1.98860586),
            ],
            fill_color="red",
            outline_color=None,
        )
        case2_fence_3 = self.map_widget.set_polygon(
            [
                (41.27655469, 1.98868632),
                (41.27656376, 1.98872253),
                (41.27634807, 1.98882177),
                (41.27634101, 1.98879227),
                (41.27655469, 1.98868632),
            ],
            fill_color="red",
            outline_color=None,
        )

    def move_drone(self, position):
        print("position ", position)
        lat = float(position[0])
        lon = float(position[1])
        g = self.geod.Inverse(self.drone_lat, self.drone_lon, lat, lon)
        azimuth = 180 - float(g["azi2"])
        dist = float(g["s12"])

        newposx = self.drone_x + math.trunc(
            dist * self.ppm * math.sin(math.radians(azimuth))
        )
        newposy = self.drone_y + math.trunc(
            dist * self.ppm * math.cos(math.radians(azimuth))
        )
        print("new position ", newposx, newposy)
        self.map_widget.canvas.itemconfig(self.point, fill="red")
        self.map_widget.canvas.coords(
            self.point, newposx - 8, newposy - 8, newposx + 8, newposy + 8
        )
        self.drone_lat = lat
        self.drone_lon = lon
        self.drone_x = newposx
        self.drone_y = newposy

        self.map_widget.canvas.delete(self.to_south)
        self.map_widget.canvas.delete(self.to_east)
        self.map_widget.canvas.delete(self.to_north)
        self.map_widget.canvas.delete(self.to_west)

        # lines pointing to North, South, East and West
        point_north_x = self.drone_x + math.trunc(
            10 * self.ppm * math.sin(math.radians(180))
        )
        point_north_y = self.drone_y + math.trunc(
            10 * self.ppm * math.cos(math.radians(180))
        )
        self.to_north = self.map_widget.canvas.create_line(
            self.drone_x, self.drone_y, point_north_x, point_north_y, fill="blue"
        )

        point_east_x = self.drone_x + math.trunc(
            10 * self.ppm * math.sin(math.radians(90))
        )
        point_east_y = self.drone_y + math.trunc(
            10 * self.ppm * math.cos(math.radians(90))
        )
        self.to_east = self.map_widget.canvas.create_line(
            self.drone_x, self.drone_y, point_east_x, point_east_y, fill="yellow"
        )

        point_south_x = self.drone_x + math.trunc(
            10 * self.ppm * math.sin(math.radians(0))
        )
        point_south_y = self.drone_y + math.trunc(
            10 * self.ppm * math.cos(math.radians(0))
        )
        self.to_south = self.map_widget.canvas.create_line(
            self.drone_x, self.drone_y, point_south_x, point_south_y, fill="pink"
        )

        point_west_x = self.drone_x + math.trunc(
            10 * self.ppm * math.sin(math.radians(270))
        )
        point_west_y = self.drone_y + math.trunc(
            10 * self.ppm * math.cos(math.radians(270))
        )
        self.to_west = self.map_widget.canvas.create_line(
            self.drone_x, self.drone_y, point_west_x, point_west_y, fill="green"
        )

    def mark_at_home(self):
        self.map_widget.canvas.itemconfig(self.point, fill="blue")
