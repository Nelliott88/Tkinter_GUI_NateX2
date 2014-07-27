from Tkinter import *   # don't pollute namespace like this except for Tkinter
import PIL    
from PIL import ImageTk # a subpackage that must be imported explicitly

import os.path 

          
__dir__ = os.path.dirname(os.path.abspath(__file__))  
filename = os.path.join(__dir__, 'stars3.jpg')
img = PIL.Image.open(filename)
img=img.resize((600,600))

__dir__ = os.path.dirname(os.path.abspath(__file__))  
filename = os.path.join(__dir__, 'stars2.jpg')
img2 = PIL.Image.open(filename)
img2=img2.resize((600,600))


__dir__ = os.path.dirname(os.path.abspath(__file__))  
filename = os.path.join(__dir__, 'blackHole.jpg')
img3 = PIL.Image.open(filename)
img3=img3.resize((600,600))

__dir__ = os.path.dirname(os.path.abspath(__file__))  
filename = os.path.join(__dir__, 'cat1-a.gif')
img4 = PIL.Image.open(filename)

root = Tk() # create main window; must be done before using ImageTk   

tkimg1=PIL.ImageTk.PhotoImage(img)
tkimg2=PIL.ImageTk.PhotoImage(img2)
tkimg3=PIL.ImageTk.PhotoImage(img3)

#radio buttons
v= IntVar()
v.set(1)

desRad= Radiobutton(root, text='Nate Nebula...Nice' , variable=v,value=1)
waterRad= Radiobutton(root, text='Sassy Sista Stars' , variable=v,value=2)
spaceRad= Radiobutton(root, text='Billy the Big Black Hole' , variable=v,value=3)
choose=Label(root, text="Choose Background")
choose.grid(column=3, row=0)
desRad.grid(column=3, row=1)
waterRad.grid(column=3, row=2)
spaceRad.grid(column=3, row=3)

iteration = IntVar()
iteration.set(15)

## A slider to set degrees per iteration
rotation = IntVar()
rotSlider = Scale(root, variable=rotation, from_=1, to=30,
                  orient=HORIZONTAL, label='Degrees:')
rotation.set(10)
rotSlider.grid(column=0, row=0, sticky=W)
#

#
# A slider to set the resizing factor for each iteration
widthRed = DoubleVar()
wReduceSlider = Scale(root, variable=widthRed, from_=0.5, to=0.99,
                     orient=HORIZONTAL, resolution=.01, label='Width Reduction:')
widthRed.set(.95)
wReduceSlider.grid(column=0, row=1, sticky=W)
# A slider to set the resizing factor for each iteration

heightRed = DoubleVar()
hReduceSlider = Scale(root, variable=heightRed, from_=0.5, to=0.99,
                     orient=HORIZONTAL, resolution=.01, label='Height Reduction:')
heightRed.set(.95)
hReduceSlider.grid(column=0, row=2, sticky=W)



# A canvas for mouse events and image drawing
canvas = Canvas(root, height=600, width=600)
canvas.create_image(300,300, image=tkimg1)
canvas.grid(column=1, row=0, rowspan=4, sticky=W)
canvas.imglist=[] #to prevent garbage 

# A slider to set the delay speed
delay = IntVar()
delaySlider = Scale(root, variable=delay, from_=75, to=275,
                    label='Stamp Speed', length=200)
delaySlider.grid(column=2,row=0,rowspan=4)
delay.set(350)

   


# Create a text editor window for displaying information
editor = Text(root, width=10)
editor.grid(column=5, row=0, rowspan=3)

# Stamp function will get bound to the left-mouse-button-down event.
def stamp(event):
    def iterate(iterations_remaining):
        global v 
        editor.insert(END, str(v.get()))
        editor.see(END) # scroll the Text window to see the new bottom line
        if (v.get()==1):
            canvas.create_image(300,300, image=tkimg1)
        elif(v.get()==2):
            canvas.create_image(300,300, image=tkimg2)
        else:
            canvas.create_image(300,300, image=tkimg3) 
        if iterations_remaining>0:
            # Resize
            i = iteration.get() - iterations_remaining
            iterated_img = img4.resize( 
                                       ( int(width*widthRed.get()**i), 
                                         int(height*heightRed.get()**i)
                                       ) # single argument is a 2-tuple
                                     )                
                                 
            # Rotate. Using expand=True prevents cropping
            iterated_img = iterated_img.rotate(i*rotation.get(),
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
    width, height = img4.size
    iterate(iteration.get())
    
# Bind event to handler
canvas.bind('<ButtonPress-1>', stamp)

# Enter event loop
root.mainloop() 