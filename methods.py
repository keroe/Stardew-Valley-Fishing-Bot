import numpy as np
from PIL import ImageGrab
import cv2
import time
from directkeys import ReleaseKey, PressKey, C

def fishing_region(img_gray, region_template_gray, w, h):

    region_detected = False
    
    res = cv2.matchTemplate(img_gray, region_template_gray, cv2.TM_CCOEFF_NORMED)

    threshold = 0.65

    loc = np.where( res >= threshold)

    for pt in zip(*loc[::-1]):

        x1, y1 = pt[0], pt[1]
        x2, y2 = pt[0] + w, pt[1] + h
        
        coords_list = [y1, y2, x1 + 55, x2 - 35]
       
        region_detected = True
        print("Region detected")
        break

    if not region_detected:
        print("No region")

    return region_detected, coords_list



def main():


	
    while(True):

        screen =  np.array(ImageGrab.grab(bbox=(0,40, 1280, 760))) # gets what is happening on the screen
        
        fishing_started, green_bar_window = fishing_region(screen, region_template_gray, wr, hr)

        cv2.imshow('RGB Region',cv2.cvtColor(green_bar_window, cv2.COLOR_BGR2RGB))        

main()