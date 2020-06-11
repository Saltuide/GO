from tkinter import *

import pygame

import os
import sys

def donothing():
   print("kappas")

root = Tk()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)

editmenu.add_separator()

editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)

menubar.add_cascade(label="Edit", menu=editmenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

embed = Frame(root, width=640, height=480)
embed.pack()
root.resizable(width=False, height=False)
root.mainloop()

# Tell pygame's SDL window which window ID to use
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
# Show the window so it's assigned an ID.
root.update()

# Usual pygame initialization
pygame.init()

# Dimensions should match those used in the embed frame
screen = pygame.display.set_mode((640, 480))

running = True
def done():
    # global running
    # running = False
    # pygame.quit()
    root.destroy()
    exit()

root.protocol("WM_DELETE_WINDOW", done)
while running:
    # game logic goes here
    pygame.display.flip()  # (or pygame.display.update())
    root.update_idletasks()
    root.update()
pygame.quit()