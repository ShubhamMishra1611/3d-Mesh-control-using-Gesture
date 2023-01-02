import cv2
import mediapipe as mp


'''
This is module is for hand tracking.
You need to place this file in you site packages folder inside blender.
Path: blender\2.93\python\lib\site-packages ---> paste this file here
'''

class TrackHand:
    def __init__(self,mode = False,max_hands = 2,model_complexity = 0,detection_confidence = 0.5,tracking_confidence = 0.5) -> None:
        self.mode = False
        self.max_hands = max_hands
        self.model_complexity = model_complexity
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(self.mode, self.max_hands,self.model_complexity,self.detection_confidence,self.tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils


    def get_hand(self,img,draw_markers = True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                if draw_markers:
                    self.mpDraw.draw_landmarks(img,hand,self.mpHand.HAND_CONNECTIONS)
        return img

    def get_position(self,img,hand_number = 0,draw = True,mark_tracker = 8):
        if mark_tracker not in list(range(0,21)): mark_tracker = 8 # if wrong value then track index finger
        land_marks = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_number]
            for id,lm in enumerate(hand.landmark):
                height,width,channel = img.shape
                c_x, c_y = int(lm.x*width),int(lm.y*height)
                land_marks.append([id, c_x, c_y])
                if mark_tracker == id:
                    cv2.circle(img,(c_x,c_y),5,(255,0,0),cv2.FILLED)
        return land_marks

def main():
    cap = cv2.VideoCapture(0)
    detector = TrackHand()
    while True:
        ret,img = cap.read()
        img = detector.get_hand(img)
        landmark_list = detector.get_position(img)
        if len(landmark_list)!=0:
            print(landmark_list[4])
        cv2.imshow("Image",img)
        cv2.waitKey(1)
        

if __name__ == "__main__":
    main()