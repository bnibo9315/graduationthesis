import socket
import base64
import sys
import time
import cv2
import numpy as np
import pyautogui
import face_recognition
import os
from PIL import Image
import shutil

MB_OK = 0x0
recognizer = cv2.face.LBPHFaceRecognizer_create()
faceCascade = cv2.CascadeClassifier(
    "haarcascade/haarcascade_frontalface_alt.xml")

mode = sys.argv[1]
count = 0
list_user = sorted(os.listdir("./database/users/"))
id = 0
name = ['None', 'Admin']
if mode == "login":
    print("Test")

    for num in range(0, len(list_user)):
        addname = list_user[num]
        name.append(addname)
        print("test")
    print(list_user)
    print(name)

    # rank = sys.argv[2]
    HOST = "192.168.1.8"  # Standard loopback interface address (localhost)
    PORT = 8081        # Port to listen on (non-privileged ports are > 1023)
    # if rank == "Admin":
    #     path = "database/admin/"
    # else:
    #     path = "database/users/"

    path = "database/train"

    def getImagesAndLabels(path):

        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        ids = []

        for imagePath in imagePaths:

            PIL_img = Image.open(imagePath).convert(
                'L')  # convert it to grayscale
            img_numpy = np.array(PIL_img, 'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = faceCascade.detectMultiScale(
                img_numpy,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y+h, x:x+w])
                ids.append(id)

        return faceSamples, ids

    print("\n[INFO] Training faces. It will take a few seconds. Wait ...")
    faces, ids = getImagesAndLabels(path)
    recognizer.train(faces, np.array(ids))

    recognizer.write('database/trainer_bin.yml')
    print("\n[INFO] {0} faces trained. Exiting Program".format(
        len(np.unique(ids))))
    print("ok")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting ", HOST, PORT)
        s.connect((HOST, PORT))
        fs = s.makefile("rb")
        while True:
            data = fsocket.readline()
            if not data:
                print("break because not data")
                break
            img = base64.standard_b64decode(data)
            imgCv = cv2.imdecode(np.asarray(
                bytearray(img), dtype=np.uint8), 1)
            gray = cv2.cvtColor(imgCv, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            for (x, y, w, h) in faces:
                cv2.rectangle(imgCv, (x, y), (x+w, y+h), (0, 255, 0), 3)
                id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                if (confidence < 60):
                    id = name[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))

                cv2.putText(
                    imgCv, str(id), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
            cv2.imshow('Add New Face Live', imgCv)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cv2.destroyAllWindows()


if mode == "register":

    print("ok")
    HOST = "192.168.1.8"  # Standard loopback interface address (localhost)
    PORT = 8081        # Port to listen on (non-privileged ports are > 1023)
    ids = sys.argv[5]
    rank = sys.argv[4]
    image_path = sys.argv[3]
    name = sys.argv[2]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting ", HOST, PORT)
        s.connect((HOST, PORT))
        fs = s.makefile("rb")
        while True:
            data = fsocket.readline()
            if not data:
                print("break because not data")
                break
            img = base64.standard_b64decode(data)
            imgCv = cv2.imdecode(np.asarray(
                bytearray(img), dtype=np.uint8), 1)
            gray = cv2.cvtColor(imgCv, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            for (x, y, w, h) in faces:
                if count == 10:
                    pathcp = image_path + name + "_" + rank + "." + ids + ".5.jpg"
                    print(pathcp)
                    target = "/home/bin9315/code/Project/TieuLuanTotNghiep/Project_FaceID_ver2/database/train"
                    pyautogui.alert('Add face success',
                                    "Notice - Author: ThanhQuangLong")
                    shutil.copy(pathcp, target)

                    sys.exit()
                    break
                else:
                    count += 1
                    name_path = image_path + name + "_" + \
                        rank + "." + ids + "." + format(count) + ".jpg"
                    cv2.imwrite(name_path, imgCv)
                    cv2.rectangle(imgCv, (x, y), (x+w, y+h),
                                  (0, 255, 0), 3)
                    cv2.putText(imgCv, name, (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
            cv2.imshow('Add New Face Live', imgCv)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cv2.destroyAllWindows()
