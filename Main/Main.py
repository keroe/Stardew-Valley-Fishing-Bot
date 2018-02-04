import numpy as np
from matplotlib import pyplot as plt
from PIL import ImageGrab
import cv2
import time
from directkeys import ReleaseKey, PressKey, C
import pyautogui


upperBound_s1 = np.array([200, 150, 255])  # upper and lower bound for the color detection (the way I came up with to find the contour of the green rectangle)
lowerBound_s1 = np.array([130, 0, 85])

x_center_calibration_value = 10 # Makes the x coordinate of the center of the fish and of the rectangle to be in the right place


def exc_point(img_rgb):  # the image format is actually BGR because of Opencv, but I didn't bother changing all the names

    x = 105 # If I need to translate the areas of interest easily and equally
    y = 75

    #Exclamation point:
    exc_point_vertices = np.array([[(520+x,200+y), (555+x,200+y), (555+x, 155+y), (520+x, 155+y)]])
    cv2.rectangle(img_rgb, (520+x, 155+y), (555+x,200+y), (0, 255, 0), 2)

    mask = np.zeros(img_rgb.shape, dtype=np.uint8)  # diminishing the area to look for the exclamation point so it takes less resources
    channel_count = img_rgb.shape[2]
    ignore_mask_color = (255,)*channel_count
    cv2.fillPoly(mask, exc_point_vertices, ignore_mask_color)
    masked_image_exc = cv2.bitwise_and(img_rgb, mask)

    exc_point_win = masked_image_exc[150+y:205+y, 470+x:610+x]        # exclamation point window
    exc_point_win = cv2.cvtColor(exc_point_win, cv2.COLOR_BGR2GRAY)   # both images needs to be gray to do template matching

    exc_template = cv2.imread('Images\\exclamation point.png')
    exc_template = cv2.cvtColor(exc_template, cv2.COLOR_BGR2GRAY)

    w, h = exc_template.shape[::-1] 

    res = cv2.matchTemplate(exc_point_win, exc_template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.7

    loc = np.where( res >= threshold)
    located = [0]

    for pt in zip(*loc[::-1]):  # read this for loop as: if the template matched with the image, append 1 to the list. This means that, if the last item in the list is a 1, the exc point was detected
        #exc_point = cv2.rectangle(exc_point_win, pt, (pt[0] + w, pt[1] + h), (255,255,255), 1)
        located.append(1)

    if located[-1] == 1:
        exc_detected = True

    else:
        exc_detected = False
    
    located.clear()

    return exc_detected


def process_img(img_rgb):
    '''

    Now this does a hell lot of things and I wanted to break it apart, making one function for every different thing it does, but maybe later.


    See comments on each "section" to undestand what they do.   


    Reminder to self: min Windows 10 window width: 120px


    '''

    x = 105 # Serves the same purpose as the exc_point ones
    y = 75

    #================================================================================================================================================================================================

    #Green bar:
    green_bar_vertices = np.array([[(405+x,5+y), (405+x,460+y), (430+x,460+y), (430+x, 5+y)]])
    #cv2.rectangle(img_rgb, (405+x,5+y), (430+x,460+y), (0,255,0), 2)
    
    green_bar_win = img_rgb[y-5:470+y, 347+x:488+x] # This is where we will draw what the script is identifying.

    #================================================================================================================================================================================================

    #It should check before starting to fish if the energy bar is below a certain level. Easy to do, so leave to do last.

    #Energy bar: 
    #energy_bar_vertices = np.array([[(1245, 680), (1245, 690), (1265, 690), (1265, 680)]])
    #cv2.rectangle(img_rgb, (1245, 680), (1265, 690), (0,255,0), 1)

    #================================================================================================================================================================================================

    #It should also check the clock every T seconds, so it stops fishing after a defined hour. Seems easy to do too witch template matching.

    #Clock:
    #clock_vertices = np.array([[(1125, 87), (1125, 120), (1255, 120), (1255, 87)]])
    #cv2.rectangle(img_rgb, (1125, 87), (1255, 120), (0,255,0), 2)

    #================================================================================================================================================================================================


    #Green bar vision:
    vertices = np.array([[(405+x,5+y), (405+x,455+y), (430+x,455+y), (430+x, 5+y)]])
    #cv2.drawContours(img_rgb, vertices, -1, (0,255,0), 2)

    mask = np.zeros(img_rgb.shape, dtype=np.uint8)
    channel_count = img_rgb.shape[2]
    ignore_mask_color = (255,)*channel_count
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_image = cv2.bitwise_and(img_rgb, mask)

    masked_image = masked_image[y-5:470+y, 347+x:488+x]

    img_YCrCb = cv2.cvtColor(masked_image, cv2.COLOR_BGR2YCrCb)  # chose this color scheme because ir seemed to be one of the few who worked. BGR2Lab also seemed to work.
    img_green = cv2.inRange(img_YCrCb, lowerBound_s1, upperBound_s1)

    kernel = np.ones((2, 2),np.uint8)
    img_green = cv2.erode(img_green, kernel, iterations = 2) # reduces the noise formed by the green algaes at the bottom of the mini game

    #================================================================================================================================================================================================

    #Fish: this looks pretty shitty. I really want to optimize it. What to change: only if it didn't match the fish at the first try it should try again. At the moment it is always trying 2 times and I think this is stupid and is slowing everything down.
    fish_center_height = 400   #If there is no fish found in the image sets this as the height. 400 hundred is at the bottom of the mini-game because point (0, 0) is the top-left corner

    fish_template = cv2.imread('Images\\fish.png')
    fish_template = cv2.cvtColor(fish_template, cv2.COLOR_BGR2GRAY)

    #               There is 2 fish templates because if the fish was outside of the green rectangle, the first template would not match it (if threshold was reduced, there would be false positives)
    #               The only diference between the templates is that the second one is with blue background 
    
    fish_template2 = cv2.imread('Images\\fish2.png')

    fish_template2 = cv2.cvtColor(fish_template2, cv2.COLOR_BGR2GRAY)
    
    w, h = fish_template.shape[::-1]
    w2, h2 = fish_template2.shape[::-1]

    vertices_fish = np.array([[(400+x,5+y), (400+x,445+y), (425+x,445+y), (425+x, 5+y)]])
    cv2.fillPoly(mask, vertices_fish, ignore_mask_color)
    masked_image_fish = cv2.bitwise_and(img_rgb, mask)

    searching_nemo = masked_image_fish[y-5:470+y, 347+x:488+x]  # reduced area to look for fish, so less resources are used
    searching_nemo = cv2.cvtColor(searching_nemo, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(searching_nemo, fish_template, cv2.TM_CCOEFF_NORMED)
    res2 = cv2.matchTemplate(searching_nemo, fish_template2, cv2.TM_CCOEFF_NORMED)
    
    threshold = 0.5
    threshold2 = 0.5

    #Could be optmized: (draws circle over each other)
    loc = np.where( res >= threshold)

    fish_located = [0]  # This all is basically the same as trying to find the exc_point, but it also saves the fish center point

    for pt in zip(*loc[::-1]):
        fish_top = pt[1]
        fish_bot = pt[1] + h

        fish_center_height = int(np.round((fish_top + fish_bot)/2, 0))

        fish_center_point = cv2.circle(green_bar_win, (pt[0] + x_center_calibration_value + 5, fish_center_height), 17, (100, 0, 255), 2) # draws circle around fish's center

        fish_located.append(1)

    loc2 = np.where( res2 >= threshold2)

    for pt in zip(*loc2[::-1]):
        fish_top = pt[1]
        fish_bot = pt[1] + h

        fish_center_height = int(np.round((fish_top + fish_bot)/2, 0))

        fish_center_point = cv2.circle(green_bar_win, (pt[0] + x_center_calibration_value + 5, fish_center_height), 17, (100, 0, 255), 2) # draws circle around fish's center

        fish_located.append(1)

    if fish_located[-1] == 1:
        fish_detected = True

    else:  # I tried doing 'elif fish_located[-1] != 1:' but it didn't work IDK why
        fish_detected = False

    fish_located.clear()

    #================================================================================================================================================================================================

    #Finding contours of the green rectangle (always finds it + some noise):
    _, conts, hierarchy = cv2.findContours(img_green, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)

    cnt_list= []

    for cnt in conts:
        area = cv2.contourArea(cnt)

        #filter noise of those damn algaes
        if area > 25:

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

    #return 'img_green' to see what the script is seeing when finding contours

    return img_rgb, green_bar_win, fish_detected, rect_center_heigth, fish_center_height # Could make the fish_detected + fish_center_height another function (just like exc_point) and rect_center_height another one


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

    while(True):

        screen =  np.array(ImageGrab.grab(bbox=(0,40, 1280, 760))) # gets what is happening on the screen

        contour, green_bar_window, fish_detected, green_bar_height, fish_height = process_img(screen) # process every frame (would be nice if it could process every 5 or so frames, so the process becomes faster).

        exc_detected = exc_point(contour) # Contour is the img_rgb with the area of interest drawn over

        if exc_detected:

            print("exc detected")
            PressKey(C)
            time.sleep(0.1)
            ReleaseKey(C)
            time.sleep(1)

        #if fish_height != 400: # for testing height_control
        #    print(fish_height)

        print(fish_detected)
        if fish_detected:
            height_control(green_bar_height, fish_height)

        cv2.imshow('RGB Region',cv2.cvtColor(green_bar_window, cv2.COLOR_BGR2RGB)) 
        
        #This is for testing:

        #print("green: ", green_bar_height)
        #print("fish: ", fish_height)
        #cv2.imshow('YCrCb', green_vision)
        cv2.imshow('Complete',cv2.cvtColor(contour, cv2.COLOR_BGR2RGB))

        if cv2.waitKey(25) & 0xFF == ord('q'): # To close the windows
            cv2.destroyAllWindows()
            break

main()
