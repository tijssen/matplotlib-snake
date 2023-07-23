"""
Matplotlib Snake
Copyright (C) 2023 Luuk Tijssen <info@luuktijssen.com>
License: CC0
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

SIZE = 20 # customize game size
LAST_KEY = KEY = None

GAME = np.zeros(2*(SIZE,)).astype(int) # square with side SIZE
POS = [2*(SIZE//2,),] # center

EAT = POS[0]

# customize figure size, colors, etc.
fig, ax = plt.subplots(figsize=2*(6.0,))
im = plt.imshow(GAME, cmap="jet", vmin=0, vmax=4)
plt.axis("off")
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
fig.canvas.manager.set_window_title("Matplotlib Snake")

def on_press(event):
    global KEY
    
    sys.stdout.flush()
    if event.key in ("up", "down", "left", "right"):
        KEY = event.key

fig.canvas.mpl_connect("key_press_event", on_press)

def init():
    im.set_data(GAME)
    return im,

def animate(i):
    # main animation loop
    # i = iteration no.: 1, 2, 3, etc.
    global KEY
    global LAST_KEY
    global EAT
    global POS
    
    # you cannot go where you came from
    # check must be done within animate loop (not in on_press)
    # otherwise keys can be changed within animation interval
    if (LAST_KEY is None
            or LAST_KEY in ("up", "down") and KEY in ("left", "right")
            or LAST_KEY in ("left", "right") and KEY in ("up", "down")):
        LAST_KEY = KEY
    
    # key = (ud, lr)
    if LAST_KEY == "up":
        key = (-1, 0)
    elif LAST_KEY == "down":
        key = (1, 0)
    elif LAST_KEY == "left":
        key = (0, -1)
    elif LAST_KEY == "right":
        key = (0, 1)
        
    # pop must come after append if snake is length 1
    POS.append(tuple(np.array(POS[-1]) + np.array(key)))
    
    # game over conditions
    game = im.get_array()
    if (len(np.unique(POS, axis=0)) < len(POS) # intersect with self
            or np.any(np.array(POS) < 0)       # out of bounds (neg)
            or np.any(np.array(POS) >= SIZE)): # out of bounds (pos)
        anim.pause() # game over
    else:
        game[POS[0]] = 0
        game[POS[-1]] = 1
        
    if EAT in POS: # snake is on food
        ax.set_title(len(POS)) # update score
        fig.canvas.draw()
        while EAT in POS: # new food not under snake
            EAT = tuple(np.random.randint(0, SIZE, 2))
        game[EAT] = 2
    else:
        POS.pop(0)

    im.set_array(game)
    return im,

anim = FuncAnimation(fig, animate, init_func=init, frames=1000000, blit=True,
    interval=50) # customize animation speed (lower = faster)
