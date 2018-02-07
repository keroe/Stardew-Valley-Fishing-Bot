import numpy as np
from PIL import ImageGrab
import cv2
import time
from directkeys import ReleaseKey, PressKey, C

upperBound_s1 = np.array([200, 150, 255])  # upper and lower bound for the color detection (the way I came up with to find the contour of the green rectangle)
lowerBound_s1 = np.array([130, 0, 85])

upperBound_fish = np.array([50, 255, 197])
lowerBound_fish = np.array([20, 215, 147])

x_center_calibration_value = 10 # Makes the x coordinate of the center of the fish and of the rectangle to be in the right place

x = 105 # If I need to translate the areas of interest easily and equally
y = 75

'''
def energy_bar(img_rgb):   #It should check before starting to fish if the energy bar is below a certain level. Easy to do, so leave to do last.

    cv2.rectangle(img_rgb, (1245, 680), (1265, 690), (0,255,0), 1)  # vertices: (1245, 680), (1245, 690), (1265, 690), (1265, 680)


def clock(img_rgb): #It should also check the clock every T seconds, so it stops fishing after a defined hour. Seems easy to do too witch template matching.

    cv2.rectangle(img_rgb, (1125, 87), (1255, 120), (0,255,0), 2)   #vertices: (1125, 87), (1125, 120), (1255, 120), (1255, 87)


def exc_point(img_rgb, exc_template, w, h):  # the image format is actually BGR because of Opencv, but I didn't bother changing all the names

    exc_detected = False

    exc_point_win = img_rgb[150+y:205+y, 470+x:610+x]        # exclamation point window
    exc_point_win = cv2.cvtColor(exc_point_win, cv2.COLOR_BGR2GRAY)   # both images needs to be gray to do template matching    

    res = cv2.matchTemplate(exc_point_win, exc_template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.8

    loc = np.where( res >= threshold)

    for pt in zip(*loc[::-1]):
        exc_point = cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0,255), 2)
        exc_detected = True

    return exc_detected
'''

def fishing_region(img_rgb, region_template_gray, w, h):  # the image format is actually BGR because of Opencv, but I didn't bother changing all the names
    
    region_detected = False
    lowestPoint = 460

    green_bar_region = img_rgb[y-5:470+y, 347+x:488+x]

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)  

    res = cv2.matchTemplate(img_gray, region_template_gray, cv2.TM_CCOEFF_NORMED)

    threshold = 0.65

    loc = np.where( res >= threshold)

    for pt in zip(*loc[::-1]):

        x1, y1 = pt[0], pt[1] #+ y_adjustment
        x2, y2 = pt[0] + w, pt[1] + h #+ y_adjustment

        region_rect = cv2.rectangle(img_rgb, (x1, y1), (x2, y2), (0, 255,255), 2)
        
        #coords_list = [y1, y2, x1 + 55, x2 - 35]
        green_bar_region = img_rgb[y1 : y2, x1 + 55 : x2 - 35]
        lowestPoint = y2

        #cv2.imshow("Green bar window", green_bar_region)
        region_detected = True
        #print("Region detected")
        break

    if not region_detected:
        print("No region")

    return region_detected, green_bar_region,lowestPoint


def fish(green_bar_win): #Fish: this looks pretty shitty. I really want to optimize it. What to change: only if it didn't match the fish at the first try it should try again. At the moment it is always trying 2 times and I think this is stupid and is slowing everything down.
   
    fish_center_height = 400   #If there is no fish found in the image sets this as the height. 400 hundred is at the bottom of the mini-game because point (0, 0) is the top-left corner
    fish_x_calibration = 0 #58

    x = 105 # If I need to translate the areas of interest easily and equally
    y = 75

    fish_detected = False

    img_HSV = cv2.cvtColor(green_bar_win, cv2.COLOR_BGR2HSV)
    img_fish = cv2.inRange(img_HSV, lowerBound_fish, upperBound_fish)

    #kernel
    #dilate/ erode

    _, conts, hierarchy = cv2.findContours(img_fish, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)

    for cnt in conts:

        area = cv2.contourArea(cnt)

        if area > 25:

            (x, y), radius = cv2.minEnclosingCircle(cnt)
            fish_center_point = (int(x + fish_x_calibration), int(y))
            fish_center_height = fish_center_point[1]
            radius = int(radius)
            fish_center_point = cv2.circle(green_bar_win, fish_center_point, 15, (100, 0, 255), 2)

            fish_detected = True

            #print('Fishy') 
            break

    if not fish_detected:
        print("No fishy")

    return fish_detected, fish_center_height, img_fish


def process_img(img_rgb, green_bar_win):
    '''

    Draws over little window of the region of interest and finds everything of the green rectangle


    See comments on each "section" to undestand what they do.   


    Reminder to self: min Windows 10 window width: 120px


    '''

    #exclamation point ROI
    #cv2.rectangle(img_rgb, (520+x, 155+y), (555+x,200+y), (0, 255, 0), 2)  # vertices: (520+x,200+y), (555+x,200+y), (555+x, 155+y), (520+x, 155+y)]])


    #Green bar vision:
    #green_bar_win = img_rgb[y-5:470+y, 347+x:488+x] # This is where we will draw what the script is identifying.

    #vertices = np.array([[(405+x,5+y), (405+x,455+y), (430+x,455+y), (430+x, 5+y)]])
    #cv2.drawContours(img_rgb, vertices, -1, (0,255,0), 2)

    img_YCrCb = cv2.cvtColor(green_bar_win, cv2.COLOR_BGR2YCrCb)  # chose this color scheme because ir seemed to be one of the few who worked. BGR2Lab also seemed to work.
    img_green = cv2.inRange(img_YCrCb, lowerBound_s1, upperBound_s1)

    kernel = np.ones((2, 2),np.uint8)
    img_green = cv2.erode(img_green, kernel, iterations = 2) # reduces the noise formed by the green algaes at the bottom of the mini game

    #================================================================================================================================================================================================

    #Finding contours of the green rectangle (always finds it + some noise):
    _, conts, hierarchy = cv2.findContours(img_green, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)

    cnt_list= []

    for cnt in conts:
        area = cv2.contourArea(cnt)

        #filter noise of those damn algaes
        if area > 200:
            x1, y1, w, h = cv2.boundingRect(cnt)
            x2 = x1 + w                           # (x1, y1) = top-left vertex
            y2 = y1 + h                           # (x2, y2) = bottom-right vertex
            #rect = cv2.rectangle(green_bar_win, (x1, y1), (x2, y2), (255,0,0), 2) # really useful to uncomment this to debug
            cnt_list.append(cnt)

    #================================================================================================================================================================================================

    
    #Finding bottom-most/top-most points, then calculate center point:
    rect_center_heigth = 400  # Lowest point possible for the center of the rectangle if use. I think the number is wrong, needs measurement again.
    highest_point_calibration = 350 # Don't let the center point be too low

    if len(cnt_list) == 2: # if it find 2 rectangles (which happens when the fish is in the middle of the bar)

        cnt1 = cnt_list[0]  #bottom rect
        cnt2 = cnt_list[1]  #top rect

        topmost = tuple(cnt2[cnt2[:,:,1].argmin()][0]) # the topm-ost point of the top rect
        bottommost = tuple(cnt1[cnt1[:,:,1].argmax()][0]) # the bottom-most point of the bottom rect

        lowest_point = int(bottommost[1])
        highest_point = int(topmost[1])

        if highest_point > highest_point_calibration: #Dont mark/consider the floor algae on the bar as center point. Maybe unnecessary as erode and area filter have been used to remove the noise made by those algaes.
            highest_point = highest_point_calibration
            highest_point = highest_point_calibration

        rect_center_heigth = int(np.round((lowest_point + highest_point)/2, 0))

        #bot_point = cv2.circle(green_bar_win, (topmost[0] + x_center_calibration_value, highest_point), 1, (255, 255, 0), 4) # very useful to know where the bottom point is being found
        #top_point = cv2.circle(green_bar_win, (topmost[0] + x_center_calibration_value, lowest_point), 1, (255, 255, 0), 4) # very useful to know where the top point is being found
        center_point = cv2.circle(green_bar_win, (topmost[0] + x_center_calibration_value, rect_center_heigth), 3, (255, 0, 255), 5) # Draws magenta point aroud center

    if len(cnt_list) == 1: # if it find only 1 rectangle. This means that the fish is not at the bar.

        cnt1 = cnt_list[0]

        topmost = tuple(cnt1[cnt1[:,:,1].argmin()][0])
        bottommost = tuple(cnt1[cnt1[:,:,1].argmax()][0])

        lowest_point = int(bottommost[1])
        highest_point = int(topmost[1])

        if highest_point > highest_point_calibration: #Dont mark/consider the floor algae on the bar as center point. Maybe unnecessary as erode and area filter have been used to remove the noise made by those algaes.
            highest_point = highest_point_calibration

        rect_center_heigth = int(np.round((lowest_point + highest_point)/2, 0))

        #bot_point = cv2.circle(green_bar_win, (topmost[0] + x_center_calibration_value, highest_point), 1, (255, 255, 0), 4) # very useful to know where the bottom point is being found
        #top_point = cv2.circle(green_bar_win, (topmost[0] + x_center_calibration_value, lowest_point), 1, (255, 255, 0), 4) # very useful to know where the top point is being found
        center_point = cv2.circle(green_bar_win, (topmost[0] + x_center_calibration_value, rect_center_heigth), 3, (255, 0, 255), 5) # Draws magenta point aroud center
    
    #================================================================================================================================================================================================

    #return 'img_green' to see what the script is seeing when finding contours obs: will give error because the window is too small for windows to display

    return img_rgb, rect_center_heigth


def height_control(green_bar_height, fish_height):  #This works like shit
    
    calibratrion_value = 10  # Because the response to pressing C is immediate and releasing it is not, the fish should not be at the center of the green rectangle, but instead a little bit higher than it.

    if green_bar_height - calibratrion_value > fish_height: # because the point (0,0) is the top-left corner, a higher y coordinate represents a point closer to the bottom of the monitor screen.
        PressKey(C)
        time.sleep(0.15)
        ReleaseKey(C)
        #print("pressed")

    elif green_bar_height - calibratrion_value < fish_height:
        ReleaseKey(C)
        #time.sleep(0.05)
        #print("released")

    elif green_bar_height - calibratrion_value == fish_height:
        #print("Looks fine")
        pass


def main():

    exc_template = cv2.imread('Images\\exclamation point.png')
    exc_template_gray = cv2.cvtColor(exc_template, cv2.COLOR_BGR2GRAY)
    we, he = exc_template_gray.shape[::-1]

    region_template = cv2.imread('Images\\fishing region 3.png')
    region_template_gray = cv2.cvtColor(region_template, cv2.COLOR_BGR2GRAY)
    wr, hr = region_template_gray.shape[::-1]

    exc_detected_recently = False

    last_time = time.time()

    while(True):

        exc_detected = False

        screen =  np.array(ImageGrab.grab(bbox=(0,40, 1280, 760))) # gets what is happening on the screen

        #print('Frame took {} ms'.format(np.round((time.time()-last_time)*1000, 2)))
        #print('FPS: ', np.round(1/(time.time()-last_time), 1))

        last_time = time.time()
        
        fishing_started, green_bar_window, floor_height = fishing_region(screen, region_template_gray, wr, hr)

        if fishing_started:

            contour, green_bar_height = process_img(screen, green_bar_window) # process every frame (would be nice if it could process every 5 or so frames, so the process becomes faster).
            
            fish_detected, fish_height, searching_nemo = fish(green_bar_window)

            d_rect_fish = fish_height - green_bar_height # if result is + : fish is below the green bar, if result is - : fish is above the green bar
            d_rect_floor = floor_height - green_bar_height # always +
            c_pressed = 1

            data = [d_rect_fish, d_rect_floor, c_pressed] # example c pressed: [231, 456, 1]. c not pressed: [231, 456, 0]
            print("R/Fish: ", data[0], "R/Floor", data[1])
            #cv2.imshow('Complete',cv2.cvtColor(contour, cv2.COLOR_BGR2RGB))

        cv2.imshow('RGB Region',cv2.cvtColor(green_bar_window, cv2.COLOR_BGR2RGB))
              

        if cv2.waitKey(25) & 0xFF == ord('q'): # To close the windows
            cv2.destroyAllWindows()
            break

main()