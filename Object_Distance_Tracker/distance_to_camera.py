import numpy as np
import cv2

detected = 1 
def find_edge(image):
	# convert the image to grayscale, blur it, and detect edges
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)	
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 35, 125)
	return edged

def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth

focalLength = 600 # in pixels 
KNOWN_WIDTH = 9.05

cap = cv2.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
 
    # Our operations on the frame come here
    edged = find_edge(frame)
    (cnts, _)  = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) == 0 : 
    	continue 
    print cnts 
    c = max(cnts, key = cv2.contourArea)
    marker = cv2.minAreaRect(c)
    inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
    box = np.int0(cv2.cv.BoxPoints(marker))
    cv2.drawContours(frame , [box], -1, (0, 255, 0), 2)
    cv2.putText(frame, "%.2fft" % (inches / 12),
		(frame.shape[1] - 200, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
		2.0, (0, 255, 0), 3)
    cv2.imshow("image", frame )
    if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()