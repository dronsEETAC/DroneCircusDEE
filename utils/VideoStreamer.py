import cv2

import paho.mqtt.client as mqtt

import cv2 as cv2
import numpy as np
import base64

class VideoStreamer:
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connection OK")
        else:
            print("Bad connection")

    def on_disconnect(self, client, userdata, rc):
        print("disconnected OK")
        self.client.loop_stop()

    def on_message(self, cli, userdata, message):
        command = message.topic
        if command == 'videoFrame':
            image = base64.b64decode(bytes(message.payload.decode("utf-8"), "utf-8"))
            npimg = np.frombuffer(image, dtype=np.uint8)
            image = cv2.imdecode(npimg, 1)
            img = cv2.resize(image, (300, 400))
            self.img = cv2.flip(img, 1)
            self.imageReady = True



    def __init__(self, source):
        self.img = 0
        self.source = source
        self.imageReady = False

        if source == 'laptopCamera':
            self.cap = cv2.VideoCapture(0)
        else:
            client = mqtt.Client("VideoService", transport="websockets")


            client.username_pw_set(
                "dronsEETAC", "mimara1456."
            )
            client.connect("classpip.upc.edu", 8000)
            print('Connected to classpip.upc.edu:8000')

            client.on_message = self.on_message  # Callback function executed when a message is received
            client.on_connect = self.on_connect
            client.on_disconnect = self.on_disconnect
            client.max_queued_messages_set(1)
            client.max_inflight_messages_set(1)

            client.subscribe('videoFrame')
            print('Waiting connection')

            client.loop_start()

    def getFrame (self):
        if self.source == 'laptopCamera':
            success, image = self.cap.read()
            img = cv2.resize(image, (400, 300))
            img = cv2.flip(img, 1)
            return success,img
        else:
            return self.imageReady,self.img

    def disconnect (self):
        if self.source == 'mobileCamera':
            self.client.disconnect()
        else:
            self.cap.release()
