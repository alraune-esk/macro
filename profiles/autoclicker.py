from __init__ import Macro, register_macro

import time
from helper import click, clickOnSpot

class autoclicker(Macro):

    def macro_run(self, mode:str):

        clickOnSpot()

        if mode == "delay":
            time.sleep(0.5)

