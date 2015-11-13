import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2
import cv2.cv as cv
import numpy as np
import time
import matplotlib.colors as colors

      
def colorDistribution2(startx,starty,deltax,deltay,img):
  endx = int(startx)+deltax
  endy = int(starty)+deltay
  
  image = img[starty:endy,startx:endx]
  BLUE_MIN = np.array([100, 15, 50],np.uint8)
  BLUE_MAX = np.array([150, 255, 255],np.uint8)
  hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  frame_threshed = cv2.inRange(hsv_image, BLUE_MIN, BLUE_MAX)
  cv2.imwrite('output2.jpg', frame_threshed)
  hue, sat, val = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
  nonBlackHue = hue[(val>20)]
  
  numBluePixel = len(frame_threshed[frame_threshed>0])
  numPixel = deltax * deltay
  ratio = float(numBluePixel) / float(numPixel)
  #print "ratio:" , ratio
  return ratio

def colorDistributionGreen(startx,starty,deltax,deltay,img):
  endx = int(startx)+deltax
  endy = int(starty)+deltay 
  image = img[starty:endy,startx:endx]
  GREEN_MIN = np.array([35,125,170],np.uint8)
  GREEN_MAX = np.array([45,255,255],np.uint8)
  hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  frame_threshed = cv2.inRange(hsv_image, GREEN_MIN, GREEN_MAX)
  cv2.imwrite('output3.jpg', frame_threshed)
  numRedPixel = len(frame_threshed[frame_threshed>0])
  numPixel = deltax * deltay
  ratio = float(numRedPixel) / float(numPixel)
  print "ratio:" , ratio
  return ratio

def colorDistributionLime(startx,starty,deltax,deltay,img):
  endx = int(startx)+deltax
  endy = int(starty)+deltay 
  image = img[starty:endy,startx:endx]
  LIME_MIN = np.array([32,130,190],np.uint8)
  LIME_MAX = np.array([45,255,255],np.uint8)
  hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  frame_threshed = cv2.inRange(hsv_image, LIME_MIN, LIME_MAX)
  cv2.imwrite('output3.jpg', frame_threshed)
  numRedPixel = len(frame_threshed[frame_threshed>0])
  numPixel = deltax * deltay
  ratio = float(numRedPixel) / float(numPixel)
  print "ratio:" , ratio
  return ratio

def colorDistributionRed(startx,starty,deltax,deltay,img):
  endx = int(startx)+deltax
  endy = int(starty)+deltay 
  image = img[starty:endy,startx:endx]
  RED_MIN = np.array([1,100,50],np.uint8)
  RED_MAX = np.array([20,255,255],np.uint8)
  hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  frame_threshed = cv2.inRange(hsv_image, RED_MIN, RED_MAX)
  cv2.imwrite('output3.jpg', frame_threshed)
  numRedPixel = len(frame_threshed[frame_threshed>0])
  numPixel = deltax * deltay
  ratio = float(numRedPixel) / float(numPixel)
  print "ratio:" , ratio
  return ratio


def colorDistribution(startx,starty,img):
  endx = int(startx)+3
  endy = int(starty)+3
  image = img[starty-3:endy,startx-3:endx]
  hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  hue, sat, val = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
  histo = cv2.calcHist( [hsv_image], [0], None, [256], [0,256] )
  maxbin = np.argmax(histo)
  print "max:" ,maxbin
  return maxbin

##    *kernel = np.ones((3,3), np.uint8)
##    color = []
##    color.append(imgp[x][y])
##    color.append(imgp[x+1][y+1])
##    color.append(imgp[x-1][y-1])
##    color.append(imgp[x+1][y-1])
##    color.append(imgp[x-1][y+1])
  
# print "Enter the filename of the video (w/o extension)"
# print "to have its background extracted:"

# fileName = raw_input()

# cap = cv2.VideoCapture(fileName + ".mp4")
# cap = cv2.VideoCapture("football_right.mp4")
# cap = cv2.VideoCapture("Stitched_videoB.avi")


# frameHeight = int(cap.get(cv.CV_CAP_PROP_FRAME_WIDTH))
# frameWidth = int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
# frameCount = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))

# print "Height:",frameHeight
# print "Width:",frameWidth
# print "Frame Count:", frameCount


fgbg1 = cv2.BackgroundSubtractorMOG()
fgbg2 = cv2.BackgroundSubtractorMOG2()

w = 10
h = 10
# w: 8475 h: 1078
videoHeight = 1078
videoWidth = 8475
videoHeightOffsetTop = 235
videoHeightOffsetBottom = 1030
videoWidthOffsetLeft = 30
videoWidthOffsetRight = videoWidth

isFirstFrame = 0
frame_old = 0
corners_old = 0
corners_total = 0
corners_count = 0

def filterCorners(corners):
  corners_filtered = np.array([c for c in corners
  if (c[0,1] >= videoHeightOffsetTop and c[0,1] <= videoHeightOffsetBottom
    and c[0,0] >= videoWidthOffsetLeft and c[0,0] <= videoWidthOffsetRight
    and c[0,1] > (c[0,0] * 0.2227) - 957.61
    and c[0,1] > (c[0,0] * -0.2746) + 1029.75
    )])

  return corners_filtered

def filterContours(contours):
  # corners = np.array
  contours_filtered = np.array([c for c in contours
  if (c[0,1] >= videoHeightOffsetTop and c[0,1] <= videoHeightOffsetBottom
    and c[0,0] >= videoWidthOffsetLeft and c[0,0] <= videoWidthOffsetRight
    and c[0,1] > (c[0,0] * 0.2227) - 957.61
    and c[0,1] > (c[0,0] * -0.2746) + 1029.75
    )])

  return contours_filtered

def getForeground(frame, bw = 0):

  # fgmask = fgbg1.apply(frame, learningRate=0.01)
  fgmask = fgbg2.apply(frame, learningRate=0.005)

  original = frame.copy()
  color = frame
  bw = fgmask

  normalizedMask = fgmask/255.0
  color[:,:,0] = frame[:,:,0] * normalizedMask
  color[:,:,1] = frame[:,:,1] * normalizedMask
  color[:,:,2] = frame[:,:,2] * normalizedMask

  return original, color, bw


print "Skipping First 50 frames"



# for fr in range(0,frameCount-1):
for fr in range(100,500):
# for fr in range(0,0):
# for fr in range(0, 1440):

  frame = cv2.imread("pics/final"+`fr`+".jpg",cv2.IMREAD_COLOR)
  # _, frame = cap.read()

  original, foreColor, foreBW = getForeground(frame.copy())
  
  # cv2.imshow('frame', result)
  # cv2.waitKey(1)
  # continue

  if(isFirstFrame < 1 and fr < 150):
    # cv2.imshow('frame', original)
    # cv2.waitKey(1)
    continue

  # print "start find contours"
  # # frame_old = cv2.cvtColor(foreColor, cv2.COLOR_BGR2GRAY)
  # # corners = cv2.goodFeaturesToTrack(frame_old, minDistance=35,
  # #   maxCorners = 1000, qualityLevel=0.08, blockSize=9, useHarrisDetector=0, k=0.04)

  # ret,thresh = cv2.threshold(foreBW,127,255,0)
  # contours,hierarchy = cv2.findContours(thresh, cv.CV_RETR_TREE, cv.CV_CHAIN_APPROX_TC89_L1)
  
  # # cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
  # # cv2.imshow('frame', frame_old)

  # cntBottom = []
  # for cnt in contours:
  #   area = cv2.contourArea(cnt)
    
  #   x, y = tuple(cnt[cnt[:,:,1].argmax()][0])
  #   # print x,"-",y,":",area

  #   if((y > 300 and area < 100) or (y > 400 and area < 180) or (area < 100)):
  #    continue
  #   # cv2.rectangle(thresh, (x,y), (x+5,y+5), cv.RGB(255,0,0), 1)
  #   cntBottom.append([x,y])

  # contours_filtered = filterContours(cntBottom)

  # for cpt in contours_filtered:
  #   x = cpt[0]
  #   y = cpt[1]
  #   cv2.rectangle(original, (x,y), (x+5,y+5), cv.RGB(255,0,0), 1)

  # corners_old = filterCorners(cntBottom)
  # # corners_old = corners

  # for i in range(0,len(corners_old)):
  #   x = int(corners_old[i,0,0])
  #   y = int(corners_old[i,0,1])
  #   cv2.rectangle(original, (x-w/2,y-h/2), (x+w/2,y+h/2), cv.RGB(255, 0, 0), 1)

  # cv2.line(frame, (videoWidthOffsetLeft, videoHeightOffsetTop), (videoWidthOffsetRight, videoHeightOffsetTop), cv.RGB(255,0,0), 1)
  # cv2.line(frame, (videoWidthOffsetLeft,videoHeightOffsetBottom), (videoWidthOffsetRight, videoHeightOffsetBottom), cv.RGB(255,0,0), 1)
  # cv2.line(frame, (0,videoHeightOffsetBottom), (3750, 0), cv.RGB(255,0,0), 1)
  # cv2.line(frame, (4300, 0), (videoWidthOffsetRight, videoHeightOffsetBottom-100), cv.RGB(255,0,0), 1)

  # cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
  # cv2.imwrite("thresh.jpg", thresh)
  # cv2.imwrite("original.jpg", original)
  # cv2.imshow('frame', original)
  # continue

  if(isFirstFrame < 1 or corners_count < 21 or fr % 4 == 0):

    startTime = time.time()

    ret,thresh = cv2.threshold(foreBW,127,255,0)
    
    kernel = np.ones((1,1), 'uint8')
    dilated = cv2.dilate(np.array(thresh, dtype='uint8'), kernel)
    contours,hierarchy = cv2.findContours(dilated, cv.CV_RETR_TREE, cv.CV_CHAIN_APPROX_SIMPLE)
    #contours,hierarchy = cv2.findContours(thresh, cv.CV_RETR_TREE, cv.CV_CHAIN_APPROX_SIMPLE)
    
    cntBottom = []
    for cnt in contours:
      area = cv2.contourArea(cnt)     
      x, y = tuple(cnt[cnt[:,:,1].argmax()][0])
      # print x,"-",y,":",area

      if((y > 300 and area < 100) or (y > 400 and area < 180) or (area < 100)):
       continue
      # cv2.rectangle(thresh, (x,y), (x+5,y+5), cv.RGB(255,0,0), 1)
      cntBottom.append([[x,y]])
##      rect = cv2.minAreaRect(cnt)
##      box = cv2.cv.BoxPoints(rect)
##      box = np.int0(box)
##      cv2.drawContours(original,[box],0,(0,100,255),2)
      x,y,w2,h2 = cv2.boundingRect(cnt)
      cv2.rectangle(original,(x,y),(x+w2,y+h2),(255,0,255),2)
      moments = cv2.moments(cnt)  
      if moments['m00']!=0:
        cx = int(moments['m10']/moments['m00'])
        cy = int(moments['m01']/moments['m00'])      
        colorval = colorDistribution2(x,y,w2,h2,foreColor)
        colorval2 = colorDistributionRed(x,y,w2,h2,foreColor)
        colorvalLime = colorDistributionLime(x,y,w2,h2,foreColor)
        colorvalGreen = colorDistributionGreen(x,y,w2,h2,foreColor)
        #colorval = colorDistribution(cx,cy,foreColor)
##        print "x: " ,cx," y: ",cy," hue: ", colorval
##        cv2.rectangle(original, (cx,cy), (cx+10,cy+10), cv.RGB(25,15,50), 1)
        
        if(colorval >0.01):
          cv2.rectangle(original, (cx,cy), (cx+10,cy+10), cv.RGB(255,0,0), 1)
        elif(colorval2>0.05):
          cv2.rectangle(original, (cx,cy), (cx+10,cy+10), cv.RGB(0,0,255), 1)
        elif(colorvalLime>0.05):
          cv2.rectangle(original, (cx,cy), (cx+10,cy+10), cv.RGB(255,255,255), 1)
        elif(colorvalGreen>0.05):
          cv2.rectangle(original, (cx,cy), (cx+10,cy+10), cv.RGB(0,255,0), 1)
          
    # print "corners:\n", np.array(cntBottom, dtype='f')
    
    contours_filtered = filterContours(np.array(cntBottom, dtype='f'))

    # find corners in the first frame
    frame_old = cv2.cvtColor(foreColor, cv2.COLOR_BGR2GRAY)
    # corners = cv2.goodFeaturesToTrack(frame_old, minDistance=35,
      # maxCorners = 1000, qualityLevel=0.08, blockSize=9, useHarrisDetector=0, k=0.04)
    # corners_old = filterCorners(corners)

    corners_old = contours_filtered
    corners_count = len(corners_old)
    corners_total = corners_count

    print "finished find contours: ", time.time() - startTime, "(sec)"

    isFirstFrame = 1;
  
  cv2.imwrite("out.jpg",original)
  if(isFirstFrame > 0 and isFirstFrame <= 0):

    frame_gray = cv2.cvtColor(foreColor, cv2.COLOR_BGR2GRAY)
    
    # print "corners:\n", corners_old

    # calculate optical flow
    corners, st, err = cv2.calcOpticalFlowPyrLK(frame_old, frame_gray, 
      prevPts=corners_old, nextPts=None, maxLevel=1, winSize=(10,20), flags=cv2.OPTFLOW_LK_GET_MIN_EIGENVALS)
    
    # Select good points (st = status, 1 if corner is found in the next frame)
    good_new = corners[st==1]
    good_old = corners_old[st==1]


    for i in range(0,len(good_new)):
      x = int(good_new[i,0])
      y = int(good_new[i,1])
      cv2.rectangle(original, (x-w/2,y-h/2), (x+w/2,y+h/2), cv.RGB(0, 0, 255), 1)

    for i in range(0,len(good_old)):
      x = int(good_old[i,0])
      y = int(good_old[i,1])
      cv2.rectangle(original, (x-w/2,y-h/2), (x+w/2,y+h/2), cv.RGB(255, 0, 0), 1)

    cv2.imwrite("out.jpg",original)
    #cv2.imshow('frame', original)
    cv2.waitKey(1)


    # Now update the previous frame and previous points
    frame_old = frame_gray.copy()
    corners_old = good_new.reshape(-1,1,2)
    corners_count = len(corners_old)


print "End"
cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()



