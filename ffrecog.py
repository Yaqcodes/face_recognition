"""
ALGORITH:
- My code should open the webcam using cv2
- On a livestream, capture faces frame by frame
- Find faces in frame and identify them
- When the person is identified, close the stream and display the image with a box on their face
- Welcome the identified person
- Click a button to close and identify again?
- Open livestream
- REPEAT
"""

import os
import sys
import time

import numpy as np
import cv2
import pickle
import face_recognition
from PIL import Image, ImageDraw, ImageFont
import pyttsx3


def main():
    # main function

    # directory with images of known people
    known_dir = os.path.join(os.getcwd(), './img/known/')

    people = train(known_dir)

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        people[key] for key in people
    ]
    known_face_names = [
        key for key in people
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    # display a wait screen before opening video stream
    display_wait_screen(os.path.join(os.getcwd(), "img/wait_image.jpg"))

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # Face recognition algorithm using known face encodings on each frame of the unknown video stream
    # detect the person, determinant times out of samples times before greeting them
    detected = []
    determinant = 5
    samples = 7
    while True:
        print(detected)
        if len(detected) == samples:
            detected.clear()

        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        print(small_frame)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []

            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                    # greet a recognised person only if he is detected determinant timesyy
                    if detected.count(name) >= determinant:
                        greet(name, known_dir, place=True)
                        detected.clear()
                        # display_wait_screen(f"{known_dir}{name}")

                # append name to determined array of recognized faces
                detected.append(name)

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 0), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


# Train model
def train(known_people):
    # This function takes as an argument, the path of the known people and returns a dictionary of the people's names
    # mapped to their face locations

    print("Training model....")

    # dictionary mapping people in known directory to their face encodings
    people = dict()

    # loop through every .jpg or .png image in known directory
    for file in os.listdir(known_people):
        if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".JPG"):
            person_name = file[:-4]
            print(f"Training on {person_name}")
            image_path = f"{known_people}{file}"
            person_image = face_recognition.load_image_file(image_path)
            people[person_name] = face_recognition.face_encodings(person_image)[0]
        else:
            continue
    print("\nDone Training!")

    return people


def display_wait_screen(path):
    # This function takes as an argument the path 2 an img to be displayed on the wait screen and displays a wait screen
    if os.path.exists(path):
        wait_image = cv2.imread(path)
        cv2.imshow("Loading...", wait_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(f"No such image at {path}")
        raise FileNotFoundError


def greet(name, known_dir, place=True):
    # This function takes as an argument, the name of the person to be greeted
    # if the place argument is true, welcome them to NCAIR, else do not
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 150)
    sound = f"Hello {name}. Welcome to Neatdah World Creativity and Innovation Day 2022!" if place else "Hello" + name
    engine.say(sound)
    engine.runAndWait()


if __name__ == "__main__":
    main()
