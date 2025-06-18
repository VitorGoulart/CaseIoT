import cv2
import requests

_BASE_RESOLUTION = 13
_BASE_CLOCK = 8
_BASE_QUALITY = 10

URL = "http://192.168.15.22"  # insert the IP Address of the ESP32

cap = cv2.VideoCapture(URL + ":81/stream")

resolutions = {0: "(96x96)",1: "QQVGA (160x120)", 2: "(128x128)", 3: "QCIF(176x144)", 4: "HQVGA(240x176)", 5: "(240x240)", 6: "QVGA(320x240)", 8: "CIF(400x296)", 9: "HVGA(480x320)", 10: "VGA(640x480)",
               11: "SVGA(800x600)", 12: "XGA(1024x768)", 13: "HD(1280x720)", 14: "SXGA(1280x1024)", 15: "UXGA(1600x1200)"}

classifier = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")


def set_resolution(url: str, index: int = 1):
    try:
        if index in resolutions.keys():
            requests.get(url + f"/control?var=framesize&val={index}")
        else:
            print("invalid resolution")
    except:
        print("SET_RESOLUTION: something went wrong")


def set_quality(url: str, value: int = 1):
    try:
        if 4 <= value <= 63:
            requests.get(url + f"/control?var=quality&val={value}")
        else:
            print("invalid quality")
    except:
        print("SET_QUALITY: something went wrong")


def set_clock(url: str, value: int = 1):
    try:
        if 4 <= value <= 25:
            requests.get(url + f"/control?var=xclk&val={value}")
        else:
            print("invalid clock")
    except:
        print("SET_CLOCK: something went wrong")


if __name__ == "__main__":
    set_clock(URL, _BASE_CLOCK)
    set_resolution(URL, 11)
    set_quality(URL, _BASE_QUALITY)

    while True:
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, )
                gray = cv2.equalizeHist(gray)

                faces = classifier.detectMultiScale(gray, minNeighbors=10)
                for (x, y, w, h) in faces:
                    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)

                cv2.imshow('ESP32-CAM', frame)

        key = cv2.waitKey(1)

        if key == ord('r'):
            print("Select resolution:")
            for item in reversed(resolutions.items()):
                print(f"{item[0]:>2}: {item[1]}")
            index = int(input())
            set_resolution(URL, index=index)

        elif key == ord('q'):
            quality = int(input("Select quality (4   - 63): "))
            set_quality(URL, value=quality)

        elif key == ord('c'):
            clock = int(input("Set Clock (0 - 25): "))
            set_clock(URL, clock)

        elif key == ord('f'):
            break

    cv2.destroyAllWindows()
    cap.release()
