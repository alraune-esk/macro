import pywinauto
from pywinauto.application import Application
import pywinauto.mouse as mouse
import pywinauto.keyboard as keyboard
import time

from ctypes import windll
from PIL import Image

import cv2
import numpy as np
import PySimpleGUI as sg
import win32gui
import win32ui
import _thread

# while True:
#     x, y = win32api.GetCursorPos()
#     print(x, y)


# import random


# rand_x = int(random.randrange(0, 20, 1)) - 10
# rand_y = int(random.randrange(0, 20, 1)) - 10



def click(x, y):
    pywinauto.mouse.click(button="left", coords=(x, y))



hwnd = win32gui.FindWindow(None, 'LimbusCompany')

# Change the line below depending on whether you want the whole window
# or just the client area. 
#left, top, right, bot = win32gui.GetClientRect(hwnd)
left, top, right, bot = win32gui.GetWindowRect(hwnd)
w = right - left
h = bot - top

template = cv2.imread('templates/winratebutton.png', 0)
threshold = 0.8


def macro_run():

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area. 
    #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
    #print (result)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        #PrintWindow Succeeded
        im.save("current.png")



    # Python program to illustrate
    # template matching

    
    # Read the main image
    img_rgb = cv2.imread("current.png")

    # Convert it to grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    
    # Read the template
    #template = cv2.imread('winratebutton.png', 0)
    
    # Store width and height of template in w and h
    #w, h = template.shape[::-1]
    
    # Perform match operations.
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    
    # Specify a threshold
    #threshold = 0.8
    
    # Store the coordinates of matched area in a numpy array
    loc = np.where(res >= threshold)

    if not(loc[0].size == 0 and loc[1].size == 0):
        

        height = loc[0][0]
        width = loc[1][0]

        click(width + 10, height + 35)
        time.sleep(1)
        click(width - 120, height + 50)
        

        # # Draw a rectangle around the matched region.
        # for pt in zip(*loc[::-1]):
        #     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
        #     # print(pt)
        #     # print(w)
        #     # print(h)  
        # # Show the final image with the matched area.
        # cv2.imshow('Detected', img_rgb)
        # cv2.waitKey(0)


def loop_macro(macro_func):
    global stop
    sleep_time = 0
    while not stop:
        print("running")
        if sleep_time >= 10:
            sleep_time = 0
            macro_func()
        time.sleep(0.5)
        sleep_time += 0.5
        window.write_event_value("loop macro", "Running {macro}".format(macro="Limbus Company Auto Battle Macro"))

    

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text("Macros")],
            [sg.Button('Auto Battle'), sg.Button('Stop')],
            [sg.Button("Exit")], [sg.Text("", size=(0, 1), key='OUTPUT')]]

# Create the Window
window = sg.Window('Limbus Company Macro', layout, grab_anywhere=True,
    resizable=True,keep_on_top=True)
# Event Loop to process "events" and get the "values" of the inputs
stop = False
while True:
    event, values = window.read()
    
    if event == "Auto Battle":
        stop = False
        window.start_thread(lambda: loop_macro(macro_run), ('-THREAD-', '-THEAD ENDED-'))

    if event == sg.WIN_CLOSED or event == "Exit": # if user closes window or clicks cancel
        stop = False
        window["OUTPUT"].update(value="Exiting")
        time.sleep(1)
        break
    if event == "Stop":
        stop = True
        window["OUTPUT"].update(value="Stopped")
    if event == "loop macro" and not stop:

        window["OUTPUT"].update(value=values["loop macro"])
    



window.close()


# while True:
#     try:
#         macro_run()
#         time.sleep(10)
#     except KeyboardInterrupt:
#         break


    