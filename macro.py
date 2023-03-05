import pywinauto
import win32api
import win32gui
from pywinauto.application import Application
import pywinauto.mouse as mouse
import pywinauto.keyboard as keyboard
import time
from win32con import MK_LBUTTON, WM_LBUTTONDOWN, WM_LBUTTONUP, WM_ACTIVATE, WA_ACTIVE, WM_SETCURSOR


import win32gui
import win32ui
from ctypes import windll
from PIL import Image

import cv2
import numpy as np
# while True:
#     x, y = win32api.GetCursorPos()
#     print(x, y)

# app = Application(backend="win32").connect(title="LimbusCompany")

# print(app.windows())

# # dlg = app["LimbusCompany"]

# # dlg.set_focus()

# app.window(title="LimbusCompany").click(button='left', coords=(1288, 781))
# time.sleep(1)
# app.window(title="LimbusCompany").click(button='left', coords=(1146, 800))

# mouse.click(coords=(1288, 781))
# time.sleep(2)
# mouse.click(coords=(1146, 800))

# def click(x, y):
#     hWnd = win32gui.FindWindow(None, "LimbusCompany")
#     #lParam = win32api.MAKELONG(x, y)

#     # hWnd1= win32gui.FindWindowEx(hWnd, None, None, None)
#     lParam = win32gui.ScreenToClient(hWnd, (x,y))
#     # #print(lParam)
#     # print(lParam)
#     lParam = win32api.MAKELONG(lParam[0], lParam[1])
#     #lParam = win32api.MAKELONG(x, y)
    
#     #print(lParam)
#     # hWnd1= win32gui.FindWindowEx(hWnd, None, None, None)
#     #win32gui.SendMessage(hWnd, WM_ACTIVATE, WA_ACTIVE, 0)
    
#     win32gui.(hWnd, WM_LBUTTONDOWN, MK_LBUTTON, lParam)
#     time.sleep(0.5)
#     win32gui.PostMessage(hWnd, WM_LBUTTONUP, 0, lParam)

    
# print("click")
# click(1288, 781)
# time.sleep(1)
# click(1146, 800)
# click(100, 100)
# click(1288, 750)
# click(1250,750)
# click(1300, 750)
# for i in range(100):
#     for j in range(100):
#         click(i*i, j*j)

# for i in range(400,1929):
#     for j in range(400,1056):
#         click(i, j)
#         time.sleep(0.25)
# from pywinauto import Desktop

# windows = Desktop(backend="uia").windows()
# print([w.window_text() for w in windows])
# print([w.rectangle() for w in windows])

# import random

# win_x = 1288
# win_y = 781

# go_x = 1146
# go_y = 800

# win2_x = 1349
# win2_y = 777

# go2_x = 1201
# go2_y = 781

# rand_x = int(random.randrange(0, 20, 1)) - 10
# rand_y = int(random.randrange(0, 20, 1)) - 10
def click(x, y):
    pywinauto.mouse.click(button="left", coords=(x, y))
# test = 0
# while test < 20:
#     try:
#         pywinauto.mouse.click(button='left', coords=(win_x + rand_x, win_y + rand_y))
#         time.sleep(0.5)
#         pywinauto.mouse.click(button="left", coords=(go_x + rand_x, go_y + rand_y))

#         time.sleep(0.5)
#         pywinauto.mouse.click(button='left', coords=(win2_x + rand_x, win2_y + rand_y))
#         time.sleep(0.5)
#         pywinauto.mouse.click(button="left", coords=(go2_x + rand_x, go2_y + rand_y))
#         time.sleep(0.5)
#         test += 1
#     except KeyboardInterrupt:
#         break


# for _ in range(10):
#     pywinauto.mouse.click(button='left', coords=(1288, 781))
#     time.sleep(1)
#     pywinauto.mouse.click(button='left', coords=(1146, 800)) 

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

while True:
    try:
        macro_run()
        time.sleep(10)
    except KeyboardInterrupt:
        break


    