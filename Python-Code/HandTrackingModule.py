#!pip install opencv-python
#!pip install mediapipe

import cv2
import mediapipe as mp


class handDetector():
    def __init__(self, mode=False, maxHands=2, modelComplex=1, detectionCon=0.5, trackCon=0.5):
        """
        Initialize handDetector class
        :param mode: Treat the input images as a video stream or a batch of static images.
        :param maxHands: Maximum number of hand to detect.
        :param modelComplex: Complexity of hand landmark model.
        :param detectionCon: Minimum confidence value ([0.0, 1.0]) for hand
        detection to be considered successful.
        :param trackCon: Minimum confidence value ([0.0, 1.0]) for the
        hand landmarks to be considered tracked successfully.
        """
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplex
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.lmList = []
        self.fingers = []

    def findHands(self, img, draw=True):
        """
        Finds hands from a BGR-color-coded image
        :param img: Input image
        :param draw: Flag to draw the output on the image
        :return: Detected hand image with or without drawing
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        """
        Finds 21 3D hand-knuckle landmarks then put them in a list. Also finds the box
        around the hand.
        :param img: Input image.
        :param handNo: ID of hand if there are more than one hand detected.
        :param draw: Flag to draw the output on the image.
        :return: list of landmarks and a bounding box.
        """
        xList = []
        yList = []
        bbbox = []
        bboxInfo = []
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHands = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHands.landmark):
                h, w, c = img.shape
                px, py = int(lm.x * w), int(lm.y * h)
                xList.append(px)
                yList.append(py)
                self.lmList.append([px, py])
                if draw:
                    cv2.circle(img, (px, py), 5, (255, 255, 0), cv2.FILLED)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            boxW, boxH = xmax - xmin, ymax - ymin
            bbox = xmin, ymin, boxW, boxH
            cx = bbox[0] + (bbox[2] // 2)
            cy = bbox[1] + (bbox[3] // 2)
            bboxInfo = {"id": id, "bbox": bbox, "center": (cx, cy)}

            if draw:
                cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                              (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                              (0, 255, 0), 2)

        return self.lmList, bboxInfo

    def fingersUp(self):
        """
        Determines which fingers are open then return in a list.
        1 is represented open finger and 0 is for closed finger
        :return: List of up and down fingers
        """
        if self.results.multi_hand_landmarks:
            myHandType = self.handType()
            self.fingers = []
            # Thumb
            if myHandType == "Right":
                if self.lmList[self.tipIds[0]][0] < self.lmList[self.tipIds[0]-1][0]:
                    self.fingers.append(1)
                else:
                    self.fingers.append(0)
            else:
                if self.lmList[self.tipIds[0]][0] > self.lmList[self.tipIds[0]-1][0]:
                    self.fingers.append(1)
                else:
                    self.fingers.append(0)

            # Other fingers
            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][1] < self.lmList[self.tipIds[id] - 2][1]:
                    self.fingers.append(1)
                else:
                    self.fingers.append(0)
        return self.fingers


    def handType(self):
        """
        Checks if the hand is left or right
        :return: Hand type of the detected hand
        """
        if self.results.multi_hand_landmarks:
            if self.lmList[17][0] < self.lmList[3][0]:
                return "Left"
            else:
                return "Right"

