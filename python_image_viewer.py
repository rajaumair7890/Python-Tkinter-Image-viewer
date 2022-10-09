#===========================================================Importing necessary libraries================================================

from tkinter import * # used to make app window and all the objects/widgets inside it.

from tkinter import filedialog # filedialog is used to call windows explorer file selector to select and open a file.

import pathlib # Pathlib is used to play around with system file paths using path objects.

from PIL import ImageTk, Image # Python Image Library is used to process the images.

import keyboard # keyboard library enables us to make use of our keyboard to control our app, binding keyboard keys to specified functions.

#================================================================Defining fuctions=======================================================

# ================================================================open_img() function======================================================

# global keyword variables to make their values universal beyond the scope of the fuctions they are defined in.
# filedialog method of tkinter library opens windows explorer to select an image file and return its absolute path as a string.
# pathlib.Path is used to convert the retured string from filedialog into a path object.
# pathlib parent method is used to go one step up in absolute path of our selected file (get the parent directory of our selected file).
# pathlib.Path().glob() method is used to filter all the files of the specified name and extension from our parent diectory and returns an iterable object.
# file_list variable contain the combined list of our file paths. list function is used here to convert the .glob() returned iterable object into a list.
# file_index variable contains the index of our file path in file_list.(index method is used to get the index of an object contained in the list)
# calling the display_img() function at the end.

def open_img():
    global file_list
    global file_index
    filename= filedialog.askopenfilename()
    file_path= pathlib.Path(filename)
    parent_dir= file_path.parent
    jpeg_files= pathlib.Path(parent_dir).glob('*.jpeg')
    jpg_files= pathlib.Path(parent_dir).glob("*.jpg")
    file_list= list(jpeg_files) + list(jpg_files)
    file_index= file_list.index(file_path)
    display_img()
#========================================================================================================================================

#===============================================================resize_img() function====================================================

# resize_img fuction gets an Image object as an argument, resizes it whilst maintaining the aspect ratio and returns the resized Image object back.
# working of resizing algorithm is as follow.
# Determining a fixed value for the height.(diffrent values to fit on different displays, 700 works best for me)
# calculating the height percentage of the image relative to fixed height. Image.size method returns a tuple as (width, height).
# Calculating the width to correct aspect ratio relative to height percentage we calculated earlier.
# Image.resize() method resizes the image to given width and height, and a resampling filter to maintain the quality of image.
# returns back the resized image.

def resize_img(img):
    fixed_height= 700
    height_percentage= fixed_height / float(img.size[1])
    width_size= int(float(img.size[0]) * float(height_percentage))
    resized_img= img.resize((width_size, fixed_height), resample= Image.Resampling.LANCZOS)
    return resized_img
#========================================================================================================================================

#================================================================Display_img fuction()===================================================

# making the desired variables global to use between functions
# open the image from the file_list, passes it to the resize_img function, then converting it to ImageTk object
# displaying the image on the screen through a tkinter Label widget.
# Updates the Title of our window as the Images changes.

def display_img():
    global displayed_img
    global file_list
    global my_label
    global file_index
    with Image.open(file_list[file_index]) as img:
        displayed_img= ImageTk.PhotoImage(resize_img(img))
        my_label= Label(root, image= displayed_img)
        my_label.grid(row=0, column=0, sticky=EW)
    root.title(f"Python Image Viewer>>{file_list[file_index]}<<")
#========================================================================================================================================

#=============================================================forward() function=========================================================

# event keyword is an object of keyboard library to call the fuction by keybaord keys binded to it.
# Updates the file_index variable to refer the next image in our file_list.
# calling display_img function to display the next image on screen from file_list with reference to the updated file_index.

def forward(event):
    global my_label
    global file_index
    try:
        file_index = file_index + 1
        my_label.grid_forget
        display_img()
    except IndexError:
        file_index = 0 # sets the file_index to the first image on the list when you reach the end of file_list
#========================================================================================================================================

#===============================================================backward() function======================================================

# does the same as forwrd fuction, just Updating the file_indrx to go backward in the file_list displaying previous image.

def backward(event):
    global my_label
    global file_index
    try:
        file_index = file_index - 1
        my_label.grid_forget
        display_img()
    except IndexError:
        file_index= -1 # sets the file_index to the last image on the list when you reach the very first image, keeps you looping in the file_list.
#========================================================================================================================================

# creating an instance of Tk() class initializing/creating our main window.
root = Tk() 

# setting the dimensions(width x height) for our window.
root.geometry("1366x700")

# configuring our window to recenter the contained image.
root.grid_columnconfigure(0, weight=1) 

# calling the open_img function
open_img() 

keyboard.on_press_key("right", forward) # binding Right Arrow key of our keyboard to the forward function
keyboard.on_press_key("left", backward) # binding Left Arrow key of our keyboard to the backward function

# Note: You can also bind the keyboard keys to functions using Tk().bind() method but that was not working for me due to unknown reasons.

root.mainloop() # Keeps the Window opened and loops into our program, until Close window Button is pressed.