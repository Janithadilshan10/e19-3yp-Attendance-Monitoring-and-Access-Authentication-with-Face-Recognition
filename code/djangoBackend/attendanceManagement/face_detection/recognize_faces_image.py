import face_recognition
import pickle
import cv2
from django.conf import settings
import os


encodings_path = os.path.join(settings.MEDIA_ROOT, "encodings.pickle")
detection_method = "hog"  # or "hog"


def recognize_face(image_path):
    print("[INFO] loading faces and embeddings...")
    # load the known faces and embeddings
    data = pickle.loads(open(encodings_path, "rb").read())
    # load the input image and convert it from BGR to RGB
    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # detect the (x, y)-coordinates of the bounding boxes corresponding
    # to each face in the input image, then compute the facial embeddings
    # for each face
    print("[INFO] compute the facial embeddings...")
    boxes = face_recognition.face_locations(rgb, model=detection_method)
    encodings = face_recognition.face_encodings(rgb, boxes)
    # initialize the list of names for each face detected
    names = []

    print("[INFO] recognizing faces...")
    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"
        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            # loop over the matched indexes and maintain a count for
            # each recognized face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            # determine the recognized face with the largest number of
            # votes (note: in the event of an unlikely tie Python will
            # select first entry in the dictionary)
            name = max(counts, key=counts.get)

        # update the list of names
        names.append(name)

    print("[INFO] returning values...")
    name_arr = []
    # loop over the recognized faces
    for name in names:
        # print the name of the recognized face
        name_arr.append(name)

    return name_arr

