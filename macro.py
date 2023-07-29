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
import profiles


def no_double_click_time():
    return 0

win32gui.GetDoubleClickTime = no_double_click_time

def click(x, y):
    pywinauto.mouse.click(button="left", coords=(x, y))


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


sg.theme('DarkAmber')  

layout = [  [sg.Text("Macros")],
            [sg.Button('Auto Battle'), sg.Button('Stop')],
            [sg.Button("Exit")], [sg.Text("", size=(0, 1), key='OUTPUT')],
            [sg.Listbox(values=["ALWAYS FOREGROUND", "TAB BACK"], select_mode='extended', key='mode', size=(30, 6))]]

# Create the Window
window = sg.Window('Macro Executor', layout, grab_anywhere=True,
    resizable=True,keep_on_top=True)
# Event Loop to process "events" and get the "values" of the inputs
stop = False
modes = ["ALWAYS FOREGROUND", "TAB BACK"]
running_macros = {}
STATE = "PAUSED"
print(profiles.MACRO_REGISTRY)

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


