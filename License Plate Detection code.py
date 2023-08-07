#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install opencv-python


# In[2]:


pip install pytesseract


# In[3]:


pip install imutils


# In[4]:


import cv2
import imutils
import pytesseract


# In[5]:


pytesseract.pytesseract.tesseract_cmd='C:\Program Files (x86)\Tesseract-OCR\\tesseract'


# In[6]:


def detect_license_plate_image():
    image = cv2.imread('plate2.jpg')
    image = imutils.resize(image, width=500)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
    edged = cv2.Canny(gray_image, 30, 200)
    cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    image1 = image.copy()
    cv2.drawContours(image1, cnts, -1, (0, 255, 0), 3)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
    screenCnt = None

    i = 7
    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        if len(approx) == 4:
            screenCnt = approx

        x, y, w, h = cv2.boundingRect(c)
        new_img = image[y:y + h, x:x + w]
        cv2.imwrite('./' + str(i) + '.png', new_img)
        i += 1
        break
        
        cv2.drawContours(image,[screenCnt],-1, (0, 255, 0), 3)
        cv2.imshow("image with detected license plate", image)
        

    Cropped_loc = './7.png'
    cv2.imshow('Detected License Plate', cv2.imread(Cropped_loc))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# In[7]:


def detect_license_plate_live_feed():
    video_capture = cv2.VideoCapture(0) 
    while True:
        ret, frame = video_capture.read()
        frame = imutils.resize(frame, width=500)
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
        edged = cv2.Canny(gray_image, 30, 200)
        cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        frame_copy = frame.copy()
        cv2.drawContours(frame_copy, cnts, -1, (0, 255, 0), 3)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
        screenCnt = None

       
        for c in cnts:
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
            if len(approx) == 4:
                screenCnt = approx

            x, y, w, h = cv2.boundingRect(c)
            new_img = frame[y:y + h, x:x + w]
            cv2.imshow('Detected License Plate', new_img)
            break
            
            cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 3)

        
        cv2.imshow('License Plate Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


# In[8]:


def detect_license_plate_video():
    video_capture = cv2.VideoCapture('video3.mp4')

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        frame = imutils.resize(frame, width=500)
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
        edged = cv2.Canny(gray_image, 30, 200)
        cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        frame_copy = frame.copy()
        cv2.drawContours(frame_copy, cnts, -1, (0, 255, 0), 3)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
        screenCnt = None

        for c in cnts:
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
            if len(approx) == 4:
                screenCnt = approx

            x, y, w, h = cv2.boundingRect(c)
            new_img = frame[y:y + h, x:x + w]
            cv2.imshow('Cropped License Plate', new_img)
            break
        
            cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 3)

        cv2.imshow('License Plate Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


# In[ ]:


import tkinter as tk 
from PIL import ImageTk,Image
from PIL import Image
from ipywidgets import FileUpload
from tkinter import filedialog
from tkinter.filedialog import askopenfile


root = tk.Tk()

canvas1=tk.Canvas(root,width=1000,height=1000)
canvas1.pack()
canvas1.configure(bg='cyan')

label1=tk.Label(root,text='License Plate Recognition',font=('Bold',35),bg='cyan')
canvas1.create_window(500,30,window=label1)
label2=tk.Label(root,text='Original Image',bg='orange')
canvas1.create_window(800,80,window=label2)

button1=tk.Button(root,text='Upload Image',command=lambda:upload_file())
canvas1.create_window(100,300,window=button1)
button2=tk.Button(root,text='Predict Static License Plate',command=detect_license_plate_image)
canvas1.create_window(100,350,window=button2)
button3=tk.Button(root,text='Live License Plate Detection',command=detect_license_plate_live_feed)
canvas1.create_window(100,400,window=button3)
button4=tk.Button(root,text='Upload Video',command=lambda:upload_video_file())
canvas1.create_window(100,450,window=button4)
button5=tk.Button(root,text='Predict Dynamic License Plate',command=lambda:detect_license_plate_video())
canvas1.create_window(100,500,window=button5)


label3=tk.Label(root,text='The detected License plate is loading....',bg='orange')
canvas1.create_window(800,420,window=label3)

def upload_video_file():
    f_types = [('Video Files', '*.mp4')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    if filename:
        print("Selected video file:", filename)
    else:
        print("No video file selected.")

def upload_file():
    global img
    f_types=[('Jpg Files','*.jpg')]
    filename=filedialog.askopenfilename(filetypes=f_types)
    img=ImageTk.PhotoImage(file=filename)
    img=Image.open(filename)
    img_resized=img.resize((400,300))
    img=ImageTk.PhotoImage(img_resized)
    label4=tk.Label(root,image=img)
    canvas1.create_window(750,250,window=label4)

root.mainloop()


# In[ ]:




