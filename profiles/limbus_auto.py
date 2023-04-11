from __init__ import Macro, register_macro
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
from helper import click



class limbus_auto(Macro):

    hwnd = win32gui.FindWindow(None, 'LimbusCompany')

    # Change the line below depending on whether you want the whole window
    # or just the client area. 
    #left, top, right, bot = win32gui.GetClientRect(hwnd)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    template = cv2.imread('templates/winratebutton.png', 0)
    comb_fin = cv2.imread("templates/aftercombat.png", 0)
    boss_fin = cv2.imread("templates/afterbossbattle.png", 0)
    threshold = 0.8

    def macro_run(self, mode:str):

        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, self.w, self.h)

        saveDC.SelectObject(saveBitMap)

        # Change the line below depending on whether you want the whole window
        # or just the client area. 
        #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
        result = windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 3)
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
        win32gui.ReleaseDC(self.hwnd, hwndDC)

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
        res = cv2.matchTemplate(img_gray, self.template, cv2.TM_CCOEFF_NORMED)
        com_fin_check = cv2.matchTemplate(img_gray, self.comb_fin, cv2.TM_CCOEFF_NORMED)
        boss_fin_check = cv2.matchTemplate(img_gray, self.boss_fin, cv2.TM_CCOEFF_NORMED)
        # Specify a threshold
        #threshold = 0.8
        
        # Store the coordinates of matched area in a numpy array
        loc = np.where(res >= self.threshold)
        loc_com_fin = np.where(com_fin_check >= self.threshold)
        loc_boss_fin = np.where(boss_fin_check >= self.threshold)


        if not(loc[0].size == 0 and loc[1].size == 0):
            

            height = loc[0][0]
            width = loc[1][0]
            #print(win32gui.GetForegroundWindow())
            #print(hwnd)


            #time.sleep(0.5)
            send_keys("{VK_MENU}")
            if mode == "TAB BACK":
                prev_wind = win32gui.GetForegroundWindow()
                win32gui.SetForegroundWindow(self.hwnd)
            #print(win32gui.GetForegroundWindow())
            time.sleep(0.5)
            click(50, 50)
            time.sleep(1)
            click(width + 10, height + 35)
            #time.sleep(1)
            click(width - 120, height + 50)
            #time.sleep(0.5)
            time.sleep(0.1)
            click(width + 10, height + 35)
            click(width - 120, height + 50)
            click(width + 10, height + 35)
            click(width - 120, height + 50)
            click(width + 10, height + 35)
            click(width - 120, height + 50)
            click(width + 10, height + 35)
            click(width - 120, height + 50)
            if mode == "TAB BACK":
                win32gui.SetForegroundWindow(prev_wind)
            
        if not(loc_com_fin[0].size == 0 and loc_com_fin[1].size == 0) and mode == "TAB BACK":
            win32gui.SetForegroundWindow(self.hwnd)

        if not(loc_boss_fin[0].size == 0 and loc_boss_fin[1].size == 0) and mode == "TAB BACK":
            win32gui.SetForegroundWindow(self.hwnd)