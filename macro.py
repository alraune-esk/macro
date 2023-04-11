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
from pywinauto.keyboard import send_keys, KeySequenceError
from profiles import *
from profiles import limbus_auto

def no_double_click_time():
    return 0

win32gui.GetDoubleClickTime = no_double_click_time

def click(x, y):
    pywinauto.mouse.click(button="left", coords=(x, y))


# hwnd = win32gui.FindWindow(None, 'LimbusCompany')

# # Change the line below depending on whether you want the whole window
# # or just the client area. 
# #left, top, right, bot = win32gui.GetClientRect(hwnd)
# left, top, right, bot = win32gui.GetWindowRect(hwnd)
# w = right - left
# h = bot - top

# template = cv2.imread('templates/winratebutton.png', 0)
# comb_fin = cv2.imread("templates/aftercombat.png", 0)
# boss_fin = cv2.imread("templates/afterbossbattle.png", 0)
# threshold = 0.8


# def macro_run(mode:str):

#     hwndDC = win32gui.GetWindowDC(hwnd)
#     mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
#     saveDC = mfcDC.CreateCompatibleDC()
#     saveBitMap = win32ui.CreateBitmap()
#     saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

#     saveDC.SelectObject(saveBitMap)

#     # Change the line below depending on whether you want the whole window
#     # or just the client area. 
#     #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
#     result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
#     #print (result)

#     bmpinfo = saveBitMap.GetInfo()
#     bmpstr = saveBitMap.GetBitmapBits(True)

#     im = Image.frombuffer(
#         'RGB',
#         (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
#         bmpstr, 'raw', 'BGRX', 0, 1)

#     win32gui.DeleteObject(saveBitMap.GetHandle())
#     saveDC.DeleteDC()
#     mfcDC.DeleteDC()
#     win32gui.ReleaseDC(hwnd, hwndDC)

#     if result == 1:
#         #PrintWindow Succeeded
#         im.save("current.png")



#     # Python program to illustrate
#     # template matching

    
#     # Read the main image
#     img_rgb = cv2.imread("current.png")

#     # Convert it to grayscale
#     img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    
#     # Read the template
#     #template = cv2.imread('winratebutton.png', 0)
    
#     # Store width and height of template in w and h
#     #w, h = template.shape[::-1]
    
#     # Perform match operations.
#     res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
#     com_fin_check = cv2.matchTemplate(img_gray, comb_fin, cv2.TM_CCOEFF_NORMED)
#     boss_fin_check = cv2.matchTemplate(img_gray, boss_fin, cv2.TM_CCOEFF_NORMED)
#     # Specify a threshold
#     #threshold = 0.8
    
#     # Store the coordinates of matched area in a numpy array
#     loc = np.where(res >= threshold)
#     loc_com_fin = np.where(com_fin_check >= threshold)
#     loc_boss_fin = np.where(boss_fin_check >= threshold)


#     if not(loc[0].size == 0 and loc[1].size == 0):
        

#         height = loc[0][0]
#         width = loc[1][0]
#         #print(win32gui.GetForegroundWindow())
#         #print(hwnd)


#         #time.sleep(0.5)
#         send_keys("{VK_MENU}")
#         if mode == "TAB BACK":
#             prev_wind = win32gui.GetForegroundWindow()
#             win32gui.SetForegroundWindow(hwnd)
#         #print(win32gui.GetForegroundWindow())
#         time.sleep(0.5)
#         click(50, 50)
#         time.sleep(1)
#         click(width + 10, height + 35)
#         #time.sleep(1)
#         click(width - 120, height + 50)
#         #time.sleep(0.5)
#         time.sleep(0.1)
#         click(width + 10, height + 35)
#         click(width - 120, height + 50)
#         click(width + 10, height + 35)
#         click(width - 120, height + 50)
#         click(width + 10, height + 35)
#         click(width - 120, height + 50)
#         click(width + 10, height + 35)
#         click(width - 120, height + 50)
#         if mode == "TAB BACK":
#             win32gui.SetForegroundWindow(prev_wind)
        
#     if not(loc_com_fin[0].size == 0 and loc_com_fin[1].size == 0) and mode == "TAB BACK":

#         win32gui.SetForegroundWindow(hwnd)

#         # # Draw a rectangle around the matched region.
#         # for pt in zip(*loc[::-1]):
#         #     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
#         #     # print(pt)
#         #     # print(w)
#         #     # print(h)  
#         # # Show the final image with the matched area.
#         # cv2.imshow('Detected', img_rgb)
#         # cv2.waitKey(0)
#     if not(loc_boss_fin[0].size == 0 and loc_boss_fin[1].size == 0) and mode == "TAB BACK":
#         win32gui.SetForegroundWindow(hwnd)



def loop_macro(macro_func, mode):
    global stop
    sleep_time = 0
    while running_macros[mode]:
        print("running: ", mode)
        if sleep_time >= 10:
            sleep_time = 0
            macro_func.macro_run(mode)
        time.sleep(0.5)
        sleep_time += 0.5
        window.write_event_value("loop macro", "Running {macro}".format(macro="Limbus Company Auto Battle Macro"))

def stop_macros(macro:str=""):
    if macro:
        running_macros[macro] = False
    else:
        for keys in running_macros.items():
                running_macros[keys] = False


sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text("Macros")],
            [sg.Button('Auto Battle'), sg.Button('Stop')],
            [sg.Button("Exit")], [sg.Text("", size=(0, 1), key='OUTPUT')],
            [sg.Listbox(values=["ALWAYS FOREGROUND", "TAB BACK"], select_mode='extended', key='mode', size=(30, 6))]]

# Create the Window
window = sg.Window('Limbus Company Macro', layout, grab_anywhere=True,
    resizable=True,keep_on_top=True)
# Event Loop to process "events" and get the "values" of the inputs
stop = False
modes = ["ALWAYS FOREGROUND", "TAB BACK"]
running_macros = {}
STATE = "PAUSED"


while True:
    event, values = window.read()
    
    if event == "Auto Battle":
        STATE = "RUNNING"
        print(values["mode"])
        if not values["mode"]:
            window["OUTPUT"].update(value="No mode selected")

        else:
            stop = False
            mode = values["mode"][0]
            stop_macros()
            
            running_macros[mode] = True
            mac = limbus_auto.limbus_auto()


            window.start_thread(lambda: loop_macro(mac, mode), ('-THREAD-', '-THEAD ENDED-'))
        
    if event == sg.WIN_CLOSED or event == "Exit": # if user closes window or clicks cancel
        stop_macros()
        window["OUTPUT"].update(value="Exiting")
        time.sleep(1)
        break

    if event == "Stop":
        stop_macros()
        STATE = "PAUSED"
        window["OUTPUT"].update(value="Stopped")

    if event == "loop macro" and STATE != "PAUSED":
        window["OUTPUT"].update(value=values["loop macro"])
    

window.close()


