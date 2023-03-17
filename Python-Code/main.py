#!pip install opencv-python

import cv2
import time
import HandTrackingModule as HTM
import SerialModule as SM

pTime = 0
cap = cv2.VideoCapture(0)
detector = HTM.handDetector(detectionCon=0.8, maxHands=1)
mySerial = SM.SerialObject("COM3", 9600, 1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Detect landmarks
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    if lmList:
        fingers = detector.fingersUp()
        print(fingers)
        mySerial.sendData(fingers)

    # Display
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS : {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break