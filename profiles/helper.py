import pywinauto

def click(x, y):
    pywinauto.mouse.click(button="left", coords=(x, y))