import time
import threading
import pywinauto
import math
from enum import Enum
class ControlMode(Enum):
    D0_TEST=0
    D1_UNIFORM=1
    D2_TOPBOTTOM=2
    D2_LEFTRIGHT=3

class WindowController(threading.Thread):
    def __init__(self,sensor_obj,control_mode='1d'):
        self.windows_list=[]
        self.current_index=0
        self.current_mode='Switching'
        self.add_windows()
        threading.Thread.__init__(self)
        self.sensor_obj=sensor_obj

    def add_windows(self):
        dsk = pywinauto.Desktop(backend='uia')
        explorer = pywinauto.Application().connect(path='explorer.exe')
        self.windows_list.append(explorer.win1)
        self.windows_list.append(explorer.win2)
        self.windows_list.append(explorer.win3)
        self.windows_list.append(explorer.win4)

    def increase_index(self):
        self.current_index=(self.current_index+1)%len(self.windows_list)

    def decrease_index(self):
        self.current_index=(self.current_index-1)%len(self.windows_list)

    def run(self):
        while True:
            result=self.sensor_obj.get_input()
            if result[0]==4:
                self.increase_index()
                self.windows_list[self.current_index].set_focus()
                #sleep_time=(2000-result[4])/2000
                sleep_time=3/math.exp(6*result[4]/1400)-0.005
                if sleep_time<0:
                    sleep_time=0
                print(sleep_time,'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
                time.sleep(sleep_time)
            time.sleep(0.0001)



