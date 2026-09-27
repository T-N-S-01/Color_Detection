#color detection...
import cv2
import numpy as np

image = cv2.imread("C:\\Users\\tharu\\Downloads\\Gemini_Generated_Image_bmogxwbmogxwbmog.jfif")

def empty(a):
    pass
#control
cv2.namedWindow("Trackbars")
cv2.createTrackbar("Hue Min", "Trackbars", 0, 179, empty)
cv2.createTrackbar("Hue Max", "Trackbars", 179, 179, empty)
cv2.createTrackbar("Sat Min", "Trackbars", 78, 255, empty)
cv2.createTrackbar("Sat Max", "Trackbars", 255, 255, empty)
cv2.createTrackbar("val Min", "Trackbars", 0, 255, empty)
cv2.createTrackbar("val Max", "Trackbars", 255, 255, empty)

cap = cv2.VideoCapture(1)

while True:
    ret, img = cap.read()
    if ret:
        # img = image.copy()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        h_min = cv2.getTrackbarPos("Hue Min", "Trackbars")
        h_max = cv2.getTrackbarPos("Hue Max", "Trackbars")
        s_min = cv2.getTrackbarPos("Sat Min", "Trackbars")
        s_max = cv2.getTrackbarPos("Sat Max", "Trackbars")
        v_min = cv2.getTrackbarPos("val Min", "Trackbars")
        v_max = cv2.getTrackbarPos("val Max", "Trackbars")

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])

        mask = cv2.inRange(hsv, lower, upper)
        x,y,w,h = cv2.boundingRect(mask)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.imshow("mask", mask)

        result = cv2.bitwise_and(img, img, mask=mask)
        cv2.imshow("Result", result)

        cv2.imshow("Original", img)

    else:
        break

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()