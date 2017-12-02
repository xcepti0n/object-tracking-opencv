import cv2
import numpy as np

color=[]
param1 = []
param2 = []
xi,yi=0,0
cam =cv2.VideoCapture(0)
img=cam.read()[1]
print img
# mouse callback function
def unsigned(a):
    if(a<0):
        return 0
    elif( a>255 ):
        return 255
    return a

def get_coordinates(event,x,y,flags,param):
    global param1,param2,xi,yi
    if event == cv2.EVENT_LBUTTONDBLCLK:
        xi,yi=y,x
        print x,y
        print param1,param2
        
mirror=False
xx,yy=0,0
param1 = [122, 124, 151]
param2 = [192, 194, 255]
while(cam.isOpened()):
    img = cam.read()[1]
    #img_copy = np.copy(img)
    img_blurred = cv2.blur(img,(30,30))
    cv2.setMouseCallback('image',get_coordinates)
    if(not (xx == xi and yy == yi)):
        print ("coordinated changed from: ",xx,yy," to: ",xi,yi)
        xx,yy = xi,yi
        if(mirror):
            yi = abs(img_blurred.shape[1]-yi)
            yy=yi
        color = img_blurred[xi][yi]
        param1 = [unsigned(color[0]-10),unsigned(color[1]-10),unsigned(color[2]-10)]
        param2 = [unsigned(color[0]+10),unsigned(color[1]+10),unsigned(color[2]+10)]
        
    ## Do the processing
    lower = np.array(param1)    ## Convert the parameters into a form that OpenCV can understand
    upper = np.array(param2)
    hsv = cv2.cvtColor(img_blurred,cv2.COLOR_BGR2HSV)
    mask  = cv2.inRange(img_blurred, lower, upper)
    res   = cv2.bitwise_and(img_blurred, img_blurred, mask= mask)
    minVal, maxVal, minLoc, maxLoc =cv2.minMaxLoc(mask)
    if(maxLoc[0]>0 and maxLoc[1]>0):
        cv2.circle(img, maxLoc, 50, (0,0,255),  3)
    #cv2.circle(img_copy, minLoc, 50, (0,255,0), 3)
    if(mirror):
        img=cv2.flip(img,1)
    cv2.imshow('image',img)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    if(cv2.waitKey(10) & 0xFF == 102): ##ASCII value of character 'f' - for flipping image
        print ("Image Flipped")
        mirror= not mirror
    elif cv2.waitKey(10) & 0xFF == 27: ##ASCII value of ESC key
        break
cv2.destroyAllWindows()
cam.release()
