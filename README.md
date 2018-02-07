# Stardew-Valley-Fishing-Bot
*A python 3.6 program for a fully autonomous fishing bot. Work in progress.*


It heavily depends Opencv to understand what is going on in your screen, doing template matching and color detection to individually track the little green rectangle, the little fish icon and the exclamation point in the mini game. I am not a experienced programmer, so don't expect a lot from this. The sole purpose of me posting this in GitHub is so someone can help me.

## How to setup Stardew Valley for this to work and steps necessary to run the script:
                      
First change the resolution to 1280x720. It only works in this resolution for now so my computer can handle it. This script does noy work if the game is on the background or minimized. Now run the "Main.py" code, move your character to the margin of any water-body, press "c" with the fishing rod selected and enjoy.

## How it works:
*(Comments in the code have every step explained)*
                             
1: grabs what is on the screen with ImageGrab.

_needs to be updated just ignore all below this line_

2: runs the function 'process_img' (creates a little window with the region of interest, does template matching in this window to look for fish, finds the green rectangle by color).

3: tries to find the exclamation point (exc_point) that shows that something got into the fishing pole. When it finds the exc_point it automactilly presses C so it always catch on time.

4: waits for some time and tries to find a fish icon in the screen. If it finds it means it was "HIT", if not, you need to throw the bait again for the loop to restart.

5: if it was "HIT" (found fish) it will try to control to height of the green rectangle so it stays at the same height of the fish. However this works very poorly and it worked for me 1 time in 20~ tries, and only because the fish stayed motionless in his starting position.
