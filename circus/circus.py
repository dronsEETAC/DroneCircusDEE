import time
from tkinter import *
import tkinter as tk
from tkinter import font, simpledialog

from pygame import mixer
from tkinter import font
from PIL import Image, ImageTk
from tkvideo import tkvideo
from utils.DetectorClass import DetectorClass
from utils.ColorsNew import ColorsNew
from utils.GuideWithColors import GuideWithColors

# from ColorsClass import ColorsClass



mixer.init()
mixer.music.load("../assets_needed/circo.mp3")
mixer.music.play(10)

root = Tk()
root.geometry("700x700")

image = Image.open("../assets_needed/entrada.png")
image = image.resize((700, 500), Image.ANTIALIAS)
bg = ImageTk.PhotoImage(image)
canvas1 = Canvas(root, width=700, height=500)
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg, anchor="nw")

myFont = font.Font(family="Bernard MT Condensed", size=28, weight="bold")

"""'
def colors ():
    mixer.music.stop()
    mixer.music.load('assets_needed/aplausos.mp3')
    mixer.music.play(10)
    time.sleep(5)
    mixer.music.stop()

    newWindow = Toplevel(root)
    newWindow.title("Colores")
    newWindow.geometry("450x800")
    #color = ColorsClass()
    frame = color.buildFrame(newWindow)
    frame.pack(fill="both", expand="yes", padx=10, pady=10)
    newWindow.mainloop()
"""

def colors():
    print ('vamos')
    mixer.music.stop()
    mixer.music.load("../assets_needed/aplausos.mp3")
    mixer.music.play(10)

    new_window = Toplevel(root)
    new_window.title("Colors")
    new_window.geometry("450x600")
    guideWithColors = GuideWithColors()
    frame = guideWithColors.BuildFrame(new_window)
    mixer.music.stop()
    frame.pack(fill="both", expand="yes", padx=10, pady=10)
    new_window.mainloop()
def voice():
    mixer.music.stop()
    mixer.music.load("../assets_needed/aplausos.mp3")
    mixer.music.play(10)

    new_window = Toplevel(root)
    new_window.title("Voz")
    new_window.geometry("450x800")
    detector = DetectorClass()
    frame = detector.build_frame(new_window, "voice")
    mixer.music.stop()
    frame.pack(fill="both", expand="yes", padx=10, pady=10)
    new_window.mainloop()


def fingers():
    mixer.music.stop()
    mixer.music.load("../assets_needed/aplausos.mp3")
    mixer.music.play(10)

    new_window = Toplevel(root)
    new_window.title("Dedos")
    new_window.geometry("450x800")


    detector = DetectorClass()
    frame = detector.build_frame(new_window, "fingers")
    mixer.music.stop()
    frame.pack(fill="both", expand="yes", padx=10, pady=10)
    new_window.mainloop()


def pose():
    mixer.music.stop()
    mixer.music.load("../assets_needed/aplausos.mp3")
    mixer.music.play(10)

    new_window = Toplevel(root)
    new_window.title("Pose")
    new_window.geometry("450x800")
    detector = DetectorClass()
    frame = detector.build_frame(new_window, "pose")
    mixer.music.stop()
    frame.pack(fill="both", expand="yes", padx=10, pady=10)
    new_window.mainloop()


def faces():
    mixer.music.stop()
    mixer.music.load("../assets_needed/aplausos.mp3")
    mixer.music.play(10)

    new_window = Toplevel(root)
    new_window.title("Pose")
    new_window.geometry("450x800")
    detector = DetectorClass()
    frame = detector.build_frame(new_window, "face")
    mixer.music.stop()
    frame.pack(fill="both", expand="yes", padx=10, pady=10)
    new_window.mainloop()


def bye():
    new_window = Toplevel(root)
    new_window.title("bye")
    new_window.geometry("700x550")

    image = Image.open("../assets_needed/bye.png")
    image = image.resize((700, 450), Image.ANTIALIAS)
    bg = ImageTk.PhotoImage(image)
    canvas1 = Canvas(new_window, width=700, height=450)
    canvas1.pack(fill="both", expand=True)

    canvas1.create_image(0, 0, image=bg, anchor="nw")
    label = Label(
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
    new_window = Toplevel(root)
    new_window.title("Select")
    new_window.geometry("1200x600")
    new_window.columnconfigure(0, weight=1)
    new_window.columnconfigure(1, weight=1)
    new_window.columnconfigure(2, weight=1)
    new_window.columnconfigure(3, weight=1)
    new_window.columnconfigure(4, weight=1)
    new_window.rowconfigure(0, weight=1)
    new_window.rowconfigure(1, weight=1)
    new_window.rowconfigure(2, weight=1)

    image2 = Image.open("../assets_needed/gallery.png")
    image2 = image2.resize((1200, 500), Image.ANTIALIAS)
    bg2 = ImageTk.PhotoImage(image2)
    canvas2 = Canvas(new_window, width=1200, height=500)
    canvas2.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky=N + S + E + W)
    canvas2.create_image(0, 0, image=bg2, anchor="nw")

    voice_button = Button(
        new_window, text="Voces", height=1, bg="#367E18", fg="#FFE9A0", command=voice
    )
    voice_button.grid(row=1, column=0, padx=(10, 5), pady=5, sticky=N + S + E + W)
    voice_button["font"] = myFont

    pose_button = Button(
        new_window, text="Poses", height=1, bg="#367E18", fg="#FFE9A0", command=pose
    )
    pose_button.grid(row=1, column=1, padx=5, pady=5, sticky=N + S + E + W)
    pose_button["font"] = myFont

    fingers_button = Button(
        new_window, text="Dedos", height=1, bg="#367E18", fg="#FFE9A0", command=fingers
    )
    fingers_button.grid(row=1, column=2, padx=5, pady=5, sticky=N + S + E + W)
    fingers_button["font"] = myFont

    faces_button = Button(
        new_window, text="Caras", height=1, bg="#367E18", fg="#FFE9A0", command=faces
    )
    faces_button.grid(row=1, column=3, padx=(5, 10), pady=5, sticky=N + S + E + W)
    faces_button["font"] = myFont

    colors_button = Button(
        new_window, text="Colores", height=1, bg="#367E18", fg="#FFE9A0", command=colors
    )
    colors_button.grid(row=1, column=4, padx=(5, 10), pady=5, sticky=N + S + E + W)
    colors_button["font"] = myFont

    bye_button = Button(
        new_window, text="Salir", height=1, bg="#FFE9A0", fg="#367E18", command=bye
    )
    bye_button.grid(row=2, column=0, columnspan=5, padx=5, pady=5, sticky=N + S + E + W)
    bye_button["font"] = myFont
    new_window.mainloop()


enter_button = Button(
    root,
    text="Pasen y vean",
    height=1,
    bg="#367E18",
    fg="#FFE9A0",
    width=14,
    command=enter,
)
enter_button["font"] = myFont
enterButton_canvas = canvas1.create_window(230, 500, anchor="nw", window=enter_button)


def close():
    global sponsor
    sponsor.destroy()


def show_video():
    global sponsor
    sponsor = Toplevel(root)
    sponsor.title("Castelldefels terra de drons")
    sponsor.geometry("800x600")
    close_button = Button(
        sponsor,
        text="Cerrar",
        height=1,
        bg="green",
        fg="yellow",
        width=14,
        command=close,
    )
    close_button.pack()
    label = Label(sponsor)
    label.pack()
    player = tkvideo(
        "../assets_needed/terraDeDrons.mp4", label, loop=1, size=(800, 600)
    )
    player.play()

    root.mainloop()


show_video_button = Button(
    root,
    text="Patrocinado por ...",
    height=1,
    bg="#CC3636",
    fg="white",
    width=24,
    command=show_video,
)
myFont2 = font.Font(family="Bernard MT Condensed", size=8)
show_video_button["font"] = myFont2

# Display Buttons
show_video_button_canvas = canvas1.create_window(
    300, 600, anchor="nw", window=show_video_button
)


# Execute tkinter
root.mainloop()
