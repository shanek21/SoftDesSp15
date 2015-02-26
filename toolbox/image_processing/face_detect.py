""" Experiment with face detection and image filtering using OpenCV """

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
#face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascades_frontalface_alt.xml')
#face_cascade = cv2.CascadeClassifier('/home/skelly1/OpenCV/opencv-2.4.10/data/haarcascades/haarcascades_frontalface_alt.xml')
face_cascade = cv2.CascadeClassifier('/home/skelly1/opencv-2.4.10/data/haarcascades/haarcascade_frontalface_alt.xml')
kernel = np.ones((21,21),'uint8')

while(True):
	ret, frame = cap.read()
	faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
	for (x,y,w,h) in faces:
		cv2.circle(frame, (int(x+w/2+w*.2), int(y+h/2+h*.)), 20, (0, 255, 30), -1)
		cv2.circle(frame, (int(x+w/2-w*.2), int()), 20, (0, 255, 30), -1)
		# frame[y:y+h,x:x+w,:] = cv2.dilate(frame[y:y+h,x:x+w,:], kernel)
		# cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))
	# Display the resulting frame
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()