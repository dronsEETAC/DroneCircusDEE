import time
import tkinter as tk
from tkinter import font
from pygame import mixer
from PIL import Image, ImageTk
from tkvideo import tkvideo
from utils.DetectorClass import DetectorClass

# from ColorsClass import ColorsClass

mixer.init()
mixer.music.load("../assets_needed/circo.mp3")
mixer.music.play(10)

root = tk.Tk()
root.geometry("800x800")

image = Image.open("../assets_needed/entrada.png")
image = image.resize((800, 600), Image.ANTIALIAS)
bg = ImageTk.PhotoImage(image)
canvas1 = tk.Canvas(root, width=800, height=600)
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg, anchor="nw")

myFont = font.Font(family="Bernard MT Condensed", size=28, weight="bold")


def applause_music():
    mixer.music.stop()
    mixer.music.load("../assets_needed/aplausos.mp3")
    mixer.music.play(10)
    time.sleep(5)
    mixer.music.stop()


def new_window(name, type):
    new_window = tk.Toplevel(root)
    new_window.title(name)
    new_window.geometry("450x800")
    if type == "colors":
        color = ColorsClass()
        frame = color.build_frame(new_window, type)
        frame.pack(fill="both", expand="yes", padx=10, pady=10)
        new_window.mainloop()
    else:
        detector = DetectorClass()
        frame = detector.build_frame(new_window, type)
        frame.pack(fill="both", expand="yes", padx=10, pady=10)
        new_window.mainloop()


def colors():
    applause_music()
    new_window("Colores", "colors")


def fingers():
    applause_music()
    new_window("Dedos", "fingers")


def pose():
    applause_music()
    new_window("Pose", "pose")


def faces():
    applause_music()
    new_window("Pose", "face")


def bye():
    new_window = tk.Toplevel(root)
    new_window.title("bye")
    new_window.geometry("800x700")

    image = Image.open("../assets_needed/bye.png")
    image = image.resize((800, 600), Image.ANTIALIAS)
    bg = ImageTk.PhotoImage(image)
    canvas1 = tk.Canvas(new_window, width=800, height=600)
    canvas1.pack(fill="both", expand=True)

    canvas1.create_image(0, 0, image=bg, anchor="nw")
    label = tk.Label(
        new_window,
        text="Gracias por su visita",
        height=2,
        width=20,
        bg="white",
        fg="#367E18",
    )
    label["font"] = myFont
    label.pack()
    new_window.mainloop()


def enter():
    mixer.music.stop()
    mixer.music.load("../assets_needed/redoble.mp3")  # Loading Music File
    mixer.music.play(10)
    new_window = tk.Toplevel(root)
    new_window.title("Select")
    new_window.geometry("1400x800")
    new_window.columnconfigure(0, weight=1)
    new_window.columnconfigure(1, weight=1)
    new_window.columnconfigure(2, weight=1)
    new_window.columnconfigure(3, weight=1)
    new_window.rowconfigure(0, weight=1)
    new_window.rowconfigure(1, weight=1)
    new_window.rowconfigure(2, weight=1)

    image2 = Image.open("../assets_needed/gallery.png")
    image2 = image2.resize((1400, 600), Image.ANTIALIAS)
    bg2 = ImageTk.PhotoImage(image2)
    canvas2 = tk.Canvas(new_window, width=1400, height=600)
    canvas2.grid(
        row=0, column=0, columnspan=4, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
    )
    canvas2.create_image(0, 0, image=bg2, anchor="nw")

    colors_button = tk.Button(
        new_window, text="Colores", height=1, bg="#367E18", fg="#FFE9A0", command=colors
    )
    colors_button.grid(
        row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
    )
    colors_button["font"] = myFont
    pose_button = tk.Button(
        new_window, text="Poses", height=1, bg="#367E18", fg="#FFE9A0", command=pose
    )
    pose_button.grid(row=1, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)
    pose_button["font"] = myFont
    fingers_button = tk.Button(
        new_window, text="Dedos", height=1, bg="#367E18", fg="#FFE9A0", command=fingers
    )
    fingers_button.grid(
        row=1, column=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
    )
    fingers_button["font"] = myFont
    faces_button = tk.Button(
        new_window, text="Caras", height=1, bg="#367E18", fg="#FFE9A0", command=faces
    )
    faces_button.grid(row=1, column=3, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)
    faces_button["font"] = myFont

    bye_button = tk.Button(
        new_window, text="Salir", height=1, bg="#FFE9A0", fg="#367E18", command=bye
    )
    bye_button.grid(
        row=2, column=0, columnspan=4, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W
    )
    bye_button["font"] = myFont
    new_window.mainloop()


enter_button = tk.Button(
    root,
    text="Pasen y vean",
    height=1,
    bg="#367E18",
    fg="#FFE9A0",
    width=14,
    command=enter,
)
enter_button["font"] = myFont
enter_button_canvas = canvas1.create_window(280, 620, anchor="nw", window=enter_button)


def close():
    global sponsor
    sponsor.destroy()


def show_video():
    global sponsor
    sponsor = tk.Toplevel(root)
    sponsor.title("Castelldefels terra de drons")
    sponsor.geometry("1200x900")
    close_button = tk.Button(
        sponsor,
        text="Cerrar",
        height=1,
        bg="green",
        fg="yellow",
        width=14,
        command=close,
    )
    close_button.pack()
    label = tk.Label(sponsor)
    label.pack()
    player = tkvideo("../assets_needed/terraDeDrons.mp4", label, loop=1, size=(1200, 900))
    player.play()

    root.mainloop()


show_video_button = tk.Button(
    root,
    text="Patrocinado por ...",
    height=1,
    bg="#CC3636",
    fg="white",
    width=24,
    command=show_video,
)
my_font2 = tk.font.Font(family="Bernard MT Condensed", size=8)
show_video_button["font"] = my_font2

# Display Buttons
show_video_button_canvas = canvas1.create_window(
    340, 700, anchor="nw", window=show_video_button
)


# Execute tkinter
root.mainloop()
