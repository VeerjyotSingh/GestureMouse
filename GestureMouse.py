import cv2
import mediapipe
import pyautogui
import math

captureHands = mediapipe.solutions.hands.Hands()
drawing = mediapipe.solutions.drawing_utils
camera = cv2.VideoCapture(0)
screenWidth,ScreenHeight = pyautogui.size()
x1=x2=y1=y2 = 0
while True:
    _,image = camera.read()
    imageHeight,imageWidth,_ = image.shape
    image = cv2.flip(image,1)
    rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(rgb_image, (320, 240))
    output_hands = captureHands.process(resized_image)
    all_hands = output_hands.multi_hand_landmarks
    if all_hands:
        for hand in all_hands:
            mediapipe.solutions.drawing_utils.draw_landmarks(image,hand)
            oneHandLandmarks = hand.landmark
            for id ,lm in enumerate(oneHandLandmarks):
                x = lm.x * imageWidth
                y = lm.y * imageHeight
                #print(x,y)
                
                if id == 8:
                    mouseX = int(screenWidth/imageWidth * x)
                    mouseY = int(ScreenHeight/imageHeight * y)
                    cv2.circle(image,(int(x),int(y)),10,(0,255,255))
                    pyautogui.moveTo(mouseX,mouseY)
                    x1 = x
                    y1 = y
                if id == 4: 
                    cv2.circle(image,(int(x),int(y)),10,(0,255,255))
                    x2 = x
                    y2 = y
        dist = math.sqrt((y2-y1)**2+(x2-x1)**2)
        if dist < 40:
            pyautogui.click()
            dist = -5
    cv2.imshow("Hands movement video caputre", image)
    key = cv2.waitKey(50)
    if key == 27:
        break
camera.release()
cv2.destroyAllWindows()