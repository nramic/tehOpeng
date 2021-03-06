import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2
import cv2.cv as cv
import numpy as np
import time
import matplotlib.colors as colors

##aerial view homography
actualpts = np.zeros([5,2])
actualpts2 = np.zeros([5,2])

actualpts[0][0] = 4484
actualpts[0][1] = 281
actualpts[1][0] = 4185
actualpts[1][1] = 281
actualpts[2][0] = 4185
actualpts[2][1] = 1007
actualpts[3][0] = 4486
actualpts[3][1] = 1007
actualpts[4][0] = 4384
actualpts[4][1] = 477

actualpts2[0][0] = 4976
actualpts2[0][1] = 249
actualpts2[1][0] = 4595
actualpts2[1][1] = 254
actualpts2[2][0] = 5514
actualpts2[2][1] = 563
actualpts2[3][0] = 6311
actualpts2[3][1] = 552
actualpts2[4][0] = 5040
actualpts2[4][1] = 297

## Find homography between the views.
size = (8000,8000)
panorama = np.zeros((8000,8000, 3), np.uint8)
(homography, _) = cv2.findHomography(actualpts2, actualpts)



def drawPlayer(x,y,hm,img,r,g,b):
  tz = hm[2,0]* x  + hm[2,1]*y + hm[2,2]
  tx = hm[0,0]* x  + hm[0,1]*y + hm[0,2]
  ty =  hm[1,0]* x  + hm[1,1]*y + hm[1,2]
  tx = int(tx/tz)
  ty = int(ty/tz)
  cv2.circle(img, (tx-2503,ty),20, cv.RGB(r,g,b), thickness=cv.CV_FILLED, lineType=8, shift=0)
  return img, tx-2503, ty
      
def colorDistributionBlue(startx,starty,deltax,deltay,img):
  
  endx = int(startx)+deltax
  endy = int(starty)+deltay
  
  image = img[starty:endy,startx:endx]
  BLUE_MIN = np.array([100, 15, 50],np.uint8)
  BLUE_MAX = np.array([150, 255, 255],np.uint8)
  
  hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  frame_threshed = cv2.inRange(hsv_image, BLUE_MIN, BLUE_MAX)
  
  # cv2.imwrite('output2.jpg', frame_threshed)
  
  numBluePixel = len(frame_threshed[frame_threshed>0])
  numPixel = deltax * deltay
  ratio = float(numBluePixel) / float(numPixel)
  #print "ratio:" , ratio
  return ratio

def colorDistributionWhite(startx,starty,deltax,deltay,img):
  endx = int(startx)+deltax
  endy = int(starty)+deltay 

  image = img[starty:endy,startx:endx]
  WHITE_MIN = np.array([0,0,130],np.uint8)
  WHITE_MAX = np.array([180,25,255],np.uint8)
  
  hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  frame_threshed = cv2.inRange(hsv_image, WHITE_MIN, WHITE_MAX)

  numRedPixel = len(frame_threshed[frame_threshed>0])
  numPixel = deltax * deltay
  ratio = float(numRedPixel) / float(numPixel)
  # print "ratio:" , ratio
  return ratio

def colorDistributionGreen(startx,starty,deltax,deltay,img):
  endx = int(startx)+deltax
  endy = int(starty)+deltay 

  image = img[starty:endy,startx:endx]
  GREEN_MIN = np.array([35,115,155],np.uint8)
  GREEN_MAX = np.array([45,255,255],np.uint8)
  
  hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  frame_threshed = cv2.inRange(hsv_image, GREEN_MIN, GREEN_MAX)
  
  # cv2.imwrite('output3.jpg', frame_threshed)
  
  numRedPixel = len(frame_threshed[frame_threshed>0])
  numPixel = deltax * deltay
  ratio = float(numRedPixel) / float(numPixel)
  # print "ratio:" , ratio
  return ratio

def colorDistributionLime(startx,starty,deltax,deltay,img):
  endx = int(startx)+deltax
  endy = int(starty)+deltay 
  
  image = img[starty:endy,startx:endx]
  LIME_MIN = np.array([32,130,190],np.uint8)
  LIME_MAX = np.array([45,255,255],np.uint8)
  
  hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  frame_threshed = cv2.inRange(hsv_image, LIME_MIN, LIME_MAX)
  
  # cv2.imwrite('output3.jpg', frame_threshed)
  
  numRedPixel = len(frame_threshed[frame_threshed>0])
  numPixel = deltax * deltay
  ratio = float(numRedPixel) / float(numPixel)
  # print "ratio:" , ratio
  return ratio

def colorDistributionRed(startx,starty,deltax,deltay,img):
  endx = int(startx)+deltax
  endy = int(starty)+deltay 
  
  image = img[starty:endy,startx:endx]
  RED_MIN = np.array([1,100,50],np.uint8)
  RED_MAX = np.array([20,255,255],np.uint8)
  
  hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  frame_threshed = cv2.inRange(hsv_image, RED_MIN, RED_MAX)
  
  # cv2.imwrite('output3.jpg', frame_threshed)
  
  numRedPixel = len(frame_threshed[frame_threshed>0])
  numPixel = deltax * deltay
  ratio = float(numRedPixel) / float(numPixel)
  # print "ratio:" , ratio
  return ratio


fgbg1 = cv2.BackgroundSubtractorMOG()
fgbg2 = cv2.BackgroundSubtractorMOG2()

w = 10
h = 10
# w:7335 h: 972
videoHeight = 972
videoWidth = 7335
videoHeightOffsetTop = 212
videoHeightOffsetBottom = 940
videoWidthOffsetLeft = 30
videoWidthOffsetRight = videoWidth

videoFrameOffset = 55

isFirstFrame = 0
frame_old = 0
corners_old = 0
corners_total = 0
corners_count = 0

cntBottomUnknown = []
cntBottomRed = []
cntBottomBlue = []
cntBottomLime = []
cntBottomGreen = []
cntBottomWhite = []


def filterContours(contours):
  contours_filtered = np.array([c for c in contours
  if (c[0,1] >= videoHeightOffsetTop and c[0,1] <= videoHeightOffsetBottom
    and c[0,0] >= videoWidthOffsetLeft and c[0,0] <= videoWidthOffsetRight
    and c[0,1] > (c[0,0] * 0.2227) - 957.61
    and c[0,1] > (c[0,0] * -0.2746) + 1029.75
    )])

  return contours_filtered

def isOnField(x,y):
  return (y >= 0 and y <= videoHeight
          and x >= 0 and x <= videoWidth
          # bottom
          and y < (x * -0.0081) + 951.7662
          # top
          and y > (x * -0.00443) + 233.7784
          # left
          and y > (x * -0.2812) + 977.4330
          # right
          and y > (x * 0.223) - 864.7794
          )

def getForeground(frame, bw = 0):

  # fgmask = fgbg1.apply(frame, learningRate=0.01)
  fgmask = fgbg2.apply(frame, learningRate=0.003)

  original = frame.copy()
  color = frame
  bw = fgmask

  normalizedMask = fgmask/255.0
  color[:,:,0] = frame[:,:,0] * normalizedMask
  color[:,:,1] = frame[:,:,1] * normalizedMask
  color[:,:,2] = frame[:,:,2] * normalizedMask

  return original, color, bw

def getExtremePoints(contour):
  leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
  rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
  topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
  bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])

  return leftmost, rightmost, topmost, bottommost


def trackPoints(previousFrame, nextFrame, old_points, canvas):

  if(len(old_points) <= 0):
    return canvas, old_points

  # calculate optical flow
  new_points, st, err = cv2.calcOpticalFlowPyrLK(previousFrame, nextFrame, 
    prevPts=old_points, nextPts=None, maxLevel=1, winSize=(10,20), flags=cv2.OPTFLOW_LK_GET_MIN_EIGENVALS)
  
  # Select good points (st = status, 1 if corner is found in the next frame)
  good_new = new_points[st==1]
  good_old = old_points[st==1]

  # drawing pink box to indicate new tracked points
  # for i in range(0,len(good_new)):
  #   x = int(good_new[i,0])
  #   y = int(good_new[i,1])
  #   cv2.circle(canvas, (x-w/2,y-h/2), 5, cv.RGB(203, 86, 194), 1)

  good_new_points = good_new.reshape(-1,1,2)

  return canvas, good_new_points


print "Skipping First ",videoFrameOffset," frames"



for fr in range(0,7200):
  pitch = cv2.imread("pitch.jpg")
  frame = cv2.imread("pics/final"+`fr`+".jpg",cv2.IMREAD_COLOR)
  
  original, foreColor, foreBW = getForeground(frame.copy())

  print "Frame",fr

  canvas = original

  # Debug
  # if(isFirstFrame < 1 and fr < 88):
  #   continue

  # cv2.line(canvas, (94, 951), (7332, 892), cv.RGB(255,0,0), 1)
  # cv2.line(canvas, (2722, 212), (4809, 203), cv.RGB(255,0,0), 1)
  # cv2.line(canvas, (94,951), (2722, 212), cv.RGB(255,0,0), 1)
  # cv2.line(canvas, (4809, 203), (7332, 770), cv.RGB(255,0,0), 1)


  # ret,thresh = cv2.threshold(foreBW,127,255,0)
  
  # kernel = np.ones((1,1), 'uint8')
  # dilated = cv2.dilate(np.array(thresh, dtype='uint8'), kernel)
  # contours,hierarchy = cv2.findContours(dilated, cv.CV_RETR_TREE, cv.CV_CHAIN_APPROX_SIMPLE)
  
  # cntBottomUnknown = []
  # cntBottomRed = []
  # cntBottomBlue = []
  # cntBottomLime = []
  # cntBottomGreen = []
  # cntBottomWhite = []

  # for cnt in contours:
  #   area = cv2.contourArea(cnt)     
  #   bottomX, bottomY = tuple(cnt[cnt[:,:,1].argmax()][0])

  #   # print x,"-",y,":",area

  #   # skip small contour area
  #   if((bottomY > 300 and area < 100) or (bottomY > 400 and area < 180) or (area < 100)):
  #    continue
    
  #   # skip contour that is not on the field
  #   if(isOnField(bottomX, bottomY) <= 0):
  #     continue

  #   cv2.rectangle(canvas, (bottomX-5, bottomY-5), (bottomX+5,bottomY+5), cv.RGB(255,0,0), 1)


  # cv2.imwrite("out.jpg",original)
  # # cv2.imshow('frame', canvas)
  # cv2.waitKey(1)
  # continue


  # Actual Code
  if(isFirstFrame < 1 and fr < videoFrameOffset):
    canvas = cv2.resize(canvas, (0,0), fx = 0.5, fy =0.7)
    pitch = cv2.resize(pitch, (0,0), fx = 0.5, fy =0.5)

    canvas_w = len(canvas[0,:])
    canvas_h = len(canvas[:,0])
    pitch_w = len(pitch[0,:])
    pitch_h = len(pitch[:,0])
    pitch_offset = canvas_w/2 - pitch_w/2
    pitch_wEnd = pitch_offset +pitch_w
    total_h = canvas_h + pitch_h

    enlarged = np.zeros((total_h,canvas_w,3))
    enlarged[0:canvas_h, 0:canvas_w] = canvas
    enlarged[canvas_h:total_h, pitch_offset:pitch_wEnd] = pitch
    cv2.imwrite("enlarge/enlarged"+`fr`+".jpg", enlarged)
    continue

  startTime = time.time()

  if(isFirstFrame < 1 or fr % 6 == 0):

    ret,thresh = cv2.threshold(foreBW,127,255,0)
    
    kernel = np.ones((1,1), 'uint8')
    dilated = cv2.dilate(np.array(thresh, dtype='uint8'), kernel)
    contours,hierarchy = cv2.findContours(dilated, cv.CV_RETR_TREE, cv.CV_CHAIN_APPROX_SIMPLE)
    
    cntBottomUnknown = []
    cntBottomRed = []
    cntBottomBlue = []
    cntBottomLime = []
    cntBottomGreen = []
    cntBottomWhite = []

    for cnt in contours:
      
      area = cv2.contourArea(cnt)     
      bottomX, bottomY = tuple(cnt[cnt[:,:,1].argmax()][0])

      # print x,"-",y,":",area

      # skip small contour area
      if((bottomY > 300 and area < 100) or (bottomY > 400 and area < 180) or (bottomY > 700 and area < 250) or (area < 100)):
       continue
      
      # skip contour that is not on the field
      if(isOnField(bottomX, bottomY) <= 0):
        continue


      boundX, boundY, boundW, boundH = cv2.boundingRect(cnt)

      # draw bounding box
      # cv2.rectangle(canvas,(boundX, boundY),(boundX+boundW, boundY+boundH),(255,0,255),2)
      
      moments = cv2.moments(cnt)  

      if moments['m00']!=0:
        cx = int(moments['m10']/moments['m00'])
        cy = int(moments['m01']/moments['m00'])      

        colorvalBlue = colorDistributionBlue(boundX, boundY, boundW, boundH, foreColor)
        colorvalRed = colorDistributionRed(boundX, boundY, boundW, boundH, foreColor)
        colorvalLime = colorDistributionLime(boundX, boundY, boundW, boundH, foreColor)
        colorvalGreen = colorDistributionGreen(boundX, boundY, boundW, boundH, foreColor)
        colorvalWhite = colorDistributionWhite(boundX, boundY, boundW, boundH, foreColor)
        
        if(colorvalWhite>0.05):
        
          # cv2.rectangle(canvas, (cx,cy), (cx+10,cy+10), cv.RGB(0,255,0), 1)
          cntBottomWhite.append([[bottomX, bottomY]])

        elif(colorvalBlue > 0.04):
          
          # cv2.rectangle(canvas, (cx,cy), (cx+10,cy+10), cv.RGB(255,0,0), 1)
          cntBottomBlue.append([[bottomX, bottomY]])
        
        elif(colorvalRed > 0.05):
        
          # cv2.rectangle(canvas, (cx,cy), (cx+10,cy+10), cv.RGB(0,0,255), 1)
          cntBottomRed.append([[bottomX, bottomY]])

        elif(colorvalLime>0.05):
        
          # cv2.rectangle(canvas, (cx,cy), (cx+10,cy+10), cv.RGB(255,255,255), 1)
          cntBottomLime.append([[bottomX, bottomY]])

       # elif(colorvalGreen>0.05):
       
       #   # cv2.rectangle(canvas, (cx,cy), (cx+10,cy+10), cv.RGB(0,255,0), 1)
       #   cntBottomGreen.append([[bottomX, bottomY]])

        else:

          # cv2.rectangle(canvas, (cx,cy), (cx+10,cy+10), cv.RGB(0,0,0), 1)
          cntBottomUnknown.append([[bottomX, bottomY]])

    
    cntBottomUnknown = np.array(cntBottomUnknown, dtype='f')
    cntBottomRed = np.array(cntBottomRed, dtype='f')
    cntBottomBlue = np.array(cntBottomBlue, dtype='f')
    cntBottomLime = np.array(cntBottomLime, dtype='f')
    cntBottomGreen = np.array(cntBottomGreen, dtype='f')
    cntBottomWhite = np.array(cntBottomWhite, dtype='f')

    frame_old = cv2.cvtColor(foreColor, cv2.COLOR_BGR2GRAY)
    # corners = cv2.goodFeaturesToTrack(frame_old, minDistance=35,
      # maxCorners = 1000, qualityLevel=0.08, blockSize=9, useHarrisDetector=0, k=0.04)
    # corners_old = filterCorners(corners)

    isFirstFrame = 1;
  

  if(isFirstFrame > 0):

    frame_gray = cv2.cvtColor(foreColor, cv2.COLOR_BGR2GRAY)
    

    # red players
    canvas, newPoints = trackPoints(frame_old, frame_gray, cntBottomRed, canvas)
    cntBottomRed = newPoints.copy()
    hm = homography

    if(len(cntBottomRed) > 0):

      # red team players on field
      playersRed = []
      for pt in cntBottomRed[:,0,:]:
        x = int(pt[0])
        y = int(pt[1])
        cv2.rectangle(canvas, (x-5, y-5), (x+5,y+5), cv.RGB(255,0,0), cv.CV_FILLED)
        pitchCopy = pitch.copy()
        pitchCopy, px, py = drawPlayer(x,y,homography,pitchCopy,255,0,0)
        playersRed.append([[px, py]])

      playersRed = np.array(playersRed, dtype='f')

      # blue team offside line
      leftmost = tuple(playersRed[playersRed[:,:,0].argmin()][0])
      x = int(leftmost[0])
      y = int(leftmost[1])
      cv2.line(pitch, (x, 0), (x, len(pitch[0,:])), cv.RGB(255, 255, 0), 10)

      # red team players on pitch
      for pt in cntBottomRed[:,0,:]:
        x = int(pt[0])
        y = int(pt[1])
        pitch, px, py = drawPlayer(x,y,homography,pitch,255,0,0)


    # blue players
    canvas, newPoints = trackPoints(frame_old, frame_gray, cntBottomBlue, canvas)
    cntBottomBlue = newPoints.copy()
  
    if(len(cntBottomBlue) > 0):

      # blue team players on field
      playersBlue = []
      for pt in cntBottomBlue[:,0,:]:
        x = int(pt[0])
        y = int(pt[1])
        cv2.rectangle(canvas, (x-5, y-5), (x+5,y+5), cv.RGB(0,0,255), cv.CV_FILLED)
        pitchCopy = pitch.copy()
        pitchCopy, px, py = drawPlayer(x,y,homography,pitchCopy,0,0,255)
        playersBlue.append([[px, py]])

      playersBlue = np.array(playersBlue, dtype='f')
      
      # red team offside line
      rightmost = tuple(playersBlue[playersBlue[:,:,0].argmax()][0])
      x = int(rightmost[0])
      y = int(rightmost[1])
      cv2.line(pitch, (x, 0), (x, len(pitch[0,:])), cv.RGB(255, 255, 0), 10)

      # blue team players on pitch
      for pt in cntBottomBlue[:,0,:]:
        x = int(pt[0])
        y = int(pt[1])
        pitch, px, py = drawPlayer(x,y,homography,pitch,0,0,255)


    # green players
    # canvas, newPoints = trackPoints(frame_old, frame_gray, cntBottomGreen, canvas)
    # cntBottomGreen = newPoints.copy()

    # if(len(cntBottomGreen) > 0):
    #   for pt in cntBottomGreen[:,0,:]:
    #     x = int(pt[0])
    #     y = int(pt[1])
    #     cv2.rectangle(canvas, (x-5, y-5), (x+5,y+5), cv.RGB(0,255,0), cv.CV_FILLED)
    #     pitch,_, _ = drawPlayer(x,y,homography,pitch,0,255,0)


    # lime players
    canvas, newPoints = trackPoints(frame_old, frame_gray, cntBottomLime, canvas)
    cntBottomLime = newPoints.copy()

    if(len(cntBottomLime) > 0):
      for pt in cntBottomLime[:,0,:]:
        x = int(pt[0])
        y = int(pt[1])
        cv2.rectangle(canvas, (x-5, y-5), (x+5,y+5), cv.RGB(203, 86, 194), cv.CV_FILLED )
        pitch,_, _ = drawPlayer(x,y,homography,pitch,203, 86, 194)
    

    # white players
    canvas, newPoints = trackPoints(frame_old, frame_gray, cntBottomWhite, canvas)
    cntBottomWhite = newPoints.copy()

    if(len(cntBottomWhite) > 0):

      redGK = 0

      potentialRedGK = []
      potentialRedGKPitch = []
      for pt in cntBottomWhite[:,0,:]:
        x = int(pt[0])
        y = int(pt[1])
        pitchCopy = pitch.copy()
        pitchCopy, px, py = drawPlayer(x,y,homography,pitchCopy,255,255,255)

        potentialRedGK.append([[x,y]])
        potentialRedGKPitch.append([[px, py]])

      potentialRedGK = np.array(potentialRedGK)
      potentialRedGKPitch = np.array(potentialRedGKPitch)

      if(len(potentialRedGKPitch) > 0 and redGK <= 0):
        redGK = 1
        leftmost = tuple(potentialRedGK[potentialRedGKPitch[:,:,0].argmin()][0])
        x = int(leftmost[0])
        y = int(leftmost[1])
        cv2.rectangle(canvas, (x-5, y-5), (x+5,y+5), cv.RGB(255,255,255), cv.CV_FILLED)
        pitch, px, py = drawPlayer(x,y,homography,pitch,255,255,255)


    # black players    
    canvas, newPoints = trackPoints(frame_old, frame_gray, cntBottomUnknown, canvas)
    cntBottomUnknown = newPoints.copy()

    if(len(cntBottomUnknown) > 0):
      blueGK = 0

      potentialBlueGK = []
      potentialBlueGKPitch = []
      for pt in cntBottomUnknown[:,0,:]:
        x = int(pt[0])
        y = int(pt[1])
        pitchCopy = pitch.copy()
        pitchCopy, px, py = drawPlayer(x,y,homography,pitchCopy,0,0,0)

        if(px<=1980 and px>=1687 and py>=283 and py<=1007):
          # potential goal keeper
          potentialBlueGK.append([[x,y]])
          potentialBlueGKPitch.append([[px, py]])

      potentialBlueGK = np.array(potentialBlueGK)
      potentialBlueGKPitch = np.array(potentialBlueGKPitch)

      if(len(potentialBlueGKPitch) > 0 and blueGK <= 0):
        blueGK = 1
        rightmost = tuple(potentialBlueGK[potentialBlueGKPitch[:,:,0].argmax()][0])
        x = int(rightmost[0])
        y = int(rightmost[1])
        cv2.rectangle(canvas, (x-5, y-5), (x+5,y+5), cv.RGB(0,0,0), cv.CV_FILLED)
        pitch, px, py = drawPlayer(x,y,homography,pitch,0,0,0)


    # Now update the previous frame
    frame_old = frame_gray.copy()


  #cv2.line(canvas, (94, 951), (7332, 892), cv.RGB(255,0,0), 1)
  #cv2.line(canvas, (2722, 212), (4809, 203), cv.RGB(255,0,0), 1)
  #cv2.line(canvas, (94,951), (2722, 212), cv.RGB(255,0,0), 1)
  #cv2.line(canvas, (4809, 203), (7332, 770), cv.RGB(255,0,0), 1)

  canvas = cv2.resize(canvas, (0,0), fx = 0.5, fy =0.7)
  pitch = cv2.resize(pitch, (0,0), fx = 0.5, fy =0.5)

  canvas_w = len(canvas[0,:])
  canvas_h = len(canvas[:,0])
  pitch_w = len(pitch[0,:])
  pitch_h = len(pitch[:,0])
  pitch_offset = canvas_w/2 - pitch_w/2
  pitch_wEnd = pitch_offset +pitch_w
  total_h = canvas_h + pitch_h

  enlarged = np.zeros((total_h,canvas_w,3))
  enlarged[0:canvas_h, 0:canvas_w] = canvas
  enlarged[canvas_h:total_h, pitch_offset:pitch_wEnd] = pitch
  #cv2.imwrite("out.jpg", canvas)
  #cv2.imwrite("transform/"+`fr`+".jpg",pitch)
  cv2.imwrite("enlarge/enlarged"+`fr`+".jpg", enlarged)
  print "finished: ", time.time() - startTime, "(sec)"
  # cv2.imshow('frame', canvas)
  cv2.waitKey(1)

print "End"
cv2.waitKey(0)

# cap.release()
cv2.destroyAllWindows()



