"""
PROJECTIVE DISTORTION CORRECTOR
University of the Philippines Diliman
CoE 197 M-THY (1st semester, A.Y. 22-23)

Note:
The program uses opencv for transforming an image file into an array of BGR tuples, 
as well as for rescaling (which also take cares of the interpolation) and displaying the image. 
It does not use opencv functions to correct projective distortions. 
These corrections are done manually using Numpy for linear algebra calculations.

Tkinter is used for the GUI, with the support of PIL for reading jpeg/png images.
"""

from tkinter import *
from PIL import ImageTk, Image
import cv2 as cv
import numpy as np

# Initializing the global variables
click_i = 0
x = [0,0,0,0]
y = [0,0,0,0]

def display_coordinates(event):
    global click_i, x, y 
    
    if click_i < 4:
        x[click_i] = event.x
        y[click_i] = event.y
        myLabel['text']=f'x: {event.x}    y: {event.y}'
        myCanvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, outline='red', fill='red')
        click_i += 1
        if click_i in [2,3]:
            myCanvas.create_line(x[click_i-2], y[click_i-2], x[click_i-1], y[click_i-1], dash = (3,3), fill='red')
        elif click_i == 4:
            # print(x)        # REMOVE
            # print(y)        # REMOVE
            myCanvas.create_line(x[0], y[0], x[3], y[3], dash = (3,3), fill='red')
            myCanvas.create_line(x[2], y[2], x[3], y[3], dash = (3,3), fill='red')
            myLabel['text']='Press calculate BELOW'
            myButton['state']=NORMAL
            
def calculate():
    img = cv.imread(path)
    scale = screen_height/img.shape[0]
    (height, width) = img.shape[:2]
    dimensions = (int(scale*width), int(scale*height))

    # when scaling down images, interpolation = cv.INTER_AREA is better.
    # on the other hand, cv.CUBIC_AREA is better when scaling up images.
    if scale <= 1:
        img_resized = cv.resize(img, dimensions, interpolation = cv.INTER_AREA)
    else:
        img_resized = cv.resize(img, dimensions, interpolation = cv.INTER_CUBIC)
    
    cv.imshow('Image resized', img_resized)        # REMOVE
    
    # INPUT TRANSFORMATION CALCULATIONS BELOW


root = Tk()
root.title('Projective distortion corrector')

# Sizing the GUI relative to the user's SCREEN DIMENSIONS
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f'{screen_width}x{screen_height}')

path = 'D:\Python\CoE_197_MP1\image.jpg'
my_img = ImageTk.PhotoImage(Image.open(path).resize((int(screen_width/2),int(screen_height))))

myCanvas = Canvas(root, width=screen_width/2, height=screen_height)
myCanvas.create_image(0,0, image=my_img, anchor=NW)
myCanvas.bind('<Button-1>', display_coordinates)
myLabel = Label(bd=4, relief='solid', font='Times 22 bold', bg='white', fg='black')
myLabel['text']='Select 4 points by clicking the image on the left'
myButton = Button(root, text = 'Calculate', state=DISABLED, command=calculate)
myCanvas.grid(row=0, column=0, rowspan=2)
myLabel.grid(row=0, column=1)
myButton.grid(row=1,column=1)

root.mainloop()
