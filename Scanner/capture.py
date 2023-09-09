import cv2
from requests import post
from time import sleep

cap = cv2.VideoCapture(0)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()

data = None
while True:
    _, img = cap.read()

    data, bbox, _ = detector.detectAndDecode(img)
    # check if there is a QRCode in the image
    if data:
        capturedQR = data
        jsonData = {'Code': data}
        r = post('http://127.0.0.1:8000/api/validate/',
                 headers={'Content-Type': 'application/json'},
                 json=jsonData)
        if r.status_code == 200:
            print('ACCESS GRANTED')
        else:
            print('ACCESS DENIED')
        sleep(2)

