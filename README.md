# Stardew-Valley-Fishing-Bot
*A python 3.6 program for a fully autonomous fishing bot. Work in progress.*

It heavily depends on Opencv to understand what is happening in your screen, doing template matching and color detection to individually track the green rectangle and the little fish icon in real time.

I am not a experienced programmer, so don't expect a lot from this. The sole purpose of me posting this in GitHub is so someone can help me.

## How to help with data collecting:

To colaborate collecting data for the future neural network, you just need download **save_data.py**, go to line 267 and put your game resolution in the bbox parenthesis using this format: (0, 0, x, y). After this, you can play the game with it running on the background. 

When you finish gaming, upload the _frames.npy_ and _training_data.npy_ inside the _Data_ folder to this GitHub or send to me at _ansetti7@gmail.com_. 

As I am still learning how to do all of this, I am probably doing something wrong, so it will take a while for the projects completion.
