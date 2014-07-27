'''
stamper.py uses a GUI to  create a montage from 
rotated and reduced iterations of an image. 
Rotation, reduction, and iteration are entered by slider.
Rotation direction is entered by a toggling button.
The stamp is initiated by a mouseclick.

version 1 creates the GUI window with the sliders, button, and canvas.
version 2 implements the mouse-click pasting an image
version 3 implements the iterative stamping
version 4 implements animiation delays using Widget.after(delay,callback)
version 5 implements an additional GUI widget to adjust the time delay

'''
from Tkinter import *   # don't pollute namespace like this except for Tkinter
import PIL    
from PIL import ImageTk # a subpackage that must be imported explicitly

import os.path              
__dir__ = os.path.dirname(os.path.abspath(__file__))  
filename = os.path.join(__dir__, 'cat1-a.gif')

img = PIL.Image.open(filename)

root = Tk() # create main window; must be done before using ImageTk

# A slider to set degrees per iteration
rotation = IntVar()
rotSlider = Scale(root, variable=rotation, from_=1, to=30,
                  orient=HORIZONTAL, label='Degrees:')
rotation.set(10)
rotSlider.grid(column=0, row=0, sticky=W)

# A slider to set the number of iterations
iteration = IntVar()
iterSlider = Scale(root, variable=iteration, from_=2, to=15,
                   orient=HORIZONTAL, label='Iterations:')
iteration.set(10)
iterSlider.grid(column=0, row=1, sticky=W)

# A slider to set the resizing factor for each iteration
reduction = DoubleVar()
reduceSlider = Scale(root, variable=reduction, from_=0.5, to=0.99,
                     orient=HORIZONTAL, resolution=.01, label='Reduction:')
reduction.set(.95)
reduceSlider.grid(column=0, row=2, sticky=W)

# A checkbutton to toggle the direction
ccw = IntVar()
direction = Checkbutton(root, variable=ccw,
                        text='Reverse', offvalue=-1) #onvalue=1 by default
ccw.set(1)
direction.grid(column=0, row=3, sticky=W)

# A canvas for mouse events and image drawing
canvas = Canvas(root, height=600, width=600, bg='cyan')
canvas.grid(column=1, row=0, rowspan=4, sticky=W)
canvas.imglist=[] #to prevent garbage collection

# A slider to set the delay speed
delay = IntVar()
delaySlider = Scale(root, variable=delay, from_=10, to=500,
                    label='Stamp Speed', length=500)
delaySlider.grid(column=2,row=0,rowspan=4)
delay.set(350)

# Stamp function will get bound to the left-mouse-button-down event.
def stamp(event):
    def iterate(iterations_remaining):
        if iterations_remaining>0:
            # Resize
            i = iteration.get() - iterations_remaining
            iterated_img = img.resize( 
                                       ( int(width*reduction.get()**i), 
                                         int(height*reduction.get()**i)
                                       ) # single argument is a 2-tuple
                                     )                
                                 
            # Rotate. Using expand=True prevents cropping
            iterated_img = iterated_img.rotate(i*rotation.get()*ccw.get(),
                                               expand=True) 
        
            # Put alpha channel back in. It was resize that removed it.
            # But it works to put alpha back in here, or between resize and rotate.
            iterated_img = iterated_img.convert('RGBA')
    
            # Cut out the blank edges
            bounds = iterated_img.getbbox() # Returns bounding box
            iterated_img = iterated_img.crop(bounds)

            #Convert iterated image to Tk format, hang onto it, and show it
            tkimg = PIL.ImageTk.PhotoImage(iterated_img)
            canvas.imglist += [tkimg] # prevents garbage collection when stamp exits
            canvas.create_image(event.x, event.y, image=tkimg)

            # Call this handler with 1 less iteration
            # Widget.after(msec,callback function, args passed to callback)
            canvas.after(delay.get(),iterate, 
                         iterations_remaining-1) 

    # These are the first commands executed by the stamp handler:
    width, height = img.size
    iterate(iteration.get())
    
# Bind event to handler
canvas.bind('<ButtonPress-1>', stamp)

# Enter event loop
root.mainloop() 