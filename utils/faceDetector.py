import mediapipe as mp
from cv2 import cv2
import numpy as np
import itertools


class FaceDetector:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def __prepare(self, image):
        """Prepares list of face marks
        If face is not detected, the list is empty
        The list has 468 face marks
        each landmark is composed of x, y and z. x and y are normalized to [0.0, 1.0]
        by the image width and height respectively.
        Z represents the landmark depth with the depth at center of the head being the origin,
        and the smaller the value the closer the landmark is to the camera.
        The magnitude of z uses roughly the same scale as x.
        The function returns also the image including the drawing of detected
        face marks and connecting lines"""

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.face_mesh.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if self.results.multi_face_landmarks:
            for face_landmarks in self.results.multi_face_landmarks:
                face = face_landmarks.landmark
                face_landmarks = list(
                    np.array(
                        [
                            [landmark.x, landmark.y, landmark.z, landmark.visibility]
                            for landmark in face
                        ]
                    ).flatten()
                )

            self.mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_tesselation_style(),
            )
            self.mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_contours_style(),
            )
            self.mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=self.mp_face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_iris_connections_style(),
            )

            return face_landmarks, image
        else:
            return [], image

    def get_size(self, image, face_landmarks, indexes):
        """
        This function calculate the height and width of a face part utilizing its landmarks.
        Args:
            image:          The image of person(s) whose face part size is to be calculated.
            face_landmarks: The detected face landmarks of the person whose face part size is to
                            be calculated.
            indexes:        The indexes of the face part landmarks, whose size is to be calculated.
        Returns:
            x,y:        the coordinates of the left-top corner of the rectangle containing the part of the face
            width:     The calculated width of the rectangle containing the face part of the face whose landmarks were passed.
            height:    The calculated height of the rectangle containing the face part of the face whose landmarks were passed.
            landmarks: An array of landmarks of the face part whose size is calculated.
        """

        # Retrieve the height and width of the image.
        image_height, image_width, _ = image.shape

        # Convert the indexes of the landmarks of the face part into a list.
        indexes_list = list(itertools.chain(*indexes))

        # Initialize a list to store the landmarks of the face part.
        landmarks = []

        # Iterate over the indexes of the landmarks of the face part.
        for index in indexes_list:
            # Append the landmark into the list.
            landmarks.append(
                [
                    int(face_landmarks.landmark[index].x * image_width),
                    int(face_landmarks.landmark[index].y * image_height),
                ]
            )

        # Calculate the width and height of the face part.
        x, y, width, height = cv2.boundingRect(np.array(landmarks))

        # Convert the list of landmarks of the face part into a numpy array.
        landmarks = np.array(landmarks)

        return x, y, width, height, landmarks

    def inclinacion(self, image, face_mesh_results):
        # return 'left', 'right' or 'normal' depending on the inclination of the face
        # this is deduced from the coordinates of the eyes
        # Get the indexes of the eyes
        left = self.mp_face_mesh.FACEMESH_LEFT_EYE
        right = self.mp_face_mesh.FACEMESH_RIGHT_EYE
        for face_no, face_landmarks in enumerate(
            face_mesh_results.multi_face_landmarks
        ):
            # Get the height of the face part.
            lx, ly, _, _, _ = self.get_size(image, face_landmarks, left)
            rx, ry, _, _, _ = self.get_size(image, face_landmarks, right)

            if ly > ry + 20:
                return "left"
            elif ry > ly + 20:
                return "right"
            else:
                return "normal"

    def is_open(self, image, face_mesh_results):
        """
        This function checks whether the eyes and mouth are close, open or very open
        utilizing its facial landmarks.
        Args:
            image:             The image of person(s) whose an eye or mouth is to be checked.
            face_mesh_results: The output of the facial landmarks detection on the image.

        Returns 'Very Open', 'Open' or 'Closed' for evey eye and the mouth

        """

        # Retrieve the height and width of the image.
        # image_height, image_width, _ = image.shape

        # Get the indexes of the eyes and mouth.
        lip_indexes = self.mp_face_mesh.FACEMESH_LIPS
        left_eye_indexes = self.mp_face_mesh.FACEMESH_LEFT_EYE
        right_eye_indexes = self.mp_face_mesh.FACEMESH_RIGHT_EYE

        # Iterate over the found faces.
        for face_no, face_landmarks in enumerate(
            face_mesh_results.multi_face_landmarks
        ):
            # Get the height of the whole face.
            _, _, _, face_height, _ = self.get_size(
                image, face_landmarks, self.mp_face_mesh.FACEMESH_FACE_OVAL
            )

            # Get the height of the face mouth.
            _, _, _, lip_height, _ = self.get_size(image, face_landmarks, lip_indexes)

            # Check if the face part is very open.
            if (lip_height / face_height) * 100 > 25:
                mouth = "Very Open"
            # or open
            elif (lip_height / face_height) * 100 > 15:
                mouth = "Open"
            else:
                # or closed
                mouth = "Closed"

            # the same procedure for each eye
            _, _, _, left_eye_height, _ = self.get_size(
                image, face_landmarks, left_eye_indexes
            )

            if (left_eye_height / face_height) * 100 > 5.5:
                left_eye = "Very Open"
            elif (left_eye_height / face_height) * 100 > 3:
                left_eye = "Open"
            else:
                left_eye = "Closed"

            _, _, _, right_eye_height, _ = self.get_size(
                image, face_landmarks, right_eye_indexes
            )

            if (right_eye_height / face_height) * 100 > 5.5:
                right_eye = "Very Open"
            elif (right_eye_height / face_height) * 100 > 3:
                right_eye = "Open"
            else:
                right_eye = "Closed"

        return mouth, left_eye, right_eye

    def detect(self, image, level):
        """Returns the pose made by the face"""
        face_landmarks, img = self.__prepare(image)

        code = -1
        # Make Detections
        if face_landmarks:
            mouth, left_eye, right_eye = self.is_open(image, self.results)
            inclination = self.inclinacion(image, self.results)
            if inclination == "left":
                code = 3  # east
            elif inclination == "right":
                code = 4  # west
            elif left_eye == "Closed" and mouth == "Open" and inclination == "normal":
                code = 1  # NORTH
            elif (
                left_eye == "Very Open"
                and right_eye == "Very Open"
                and mouth == "Closed"
                and inclination == "normal"
            ):
                code = 2  # south
            elif (
                left_eye == "Open"
                and right_eye == "Closed"
                and mouth == "Very Open"
                and inclination == "normal"
            ):
                code = 5  # drop

            elif (
                left_eye == "Closed"
                and right_eye == "Open"
                and mouth == "Very Open"
                and inclination == "normal"
            ):
                code = 0  # stop
            elif (
                left_eye == "Very Open"
                and right_eye == "Very Open"
                and mouth == "Very Open"
                and inclination == "normal"
            ):
                code = 6  # return
        return code, img
