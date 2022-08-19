from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import serial
import string
#import pandas as pd
import csv
from datetime import datetime, time
import time #comment out afterwards

#converting sensor number to wavelength
wavelength = np.array(range(1,289))
wavelength = 3.068464691e2 + 2.707179585 * wavelength -1.45040638e-3 * wavelength**2 -4.596809405e-6 * wavelength**3 - 3.105844784e-9 * wavelength**4 + 2.269126371e-11 * wavelength**5
wavelength = np.round(wavelength, decimals=2)
print(wavelength.size) 

"""
def reset_array(a : tuple):
    for x in a:
        x = np.empty([])
    print(a) 
"""

def reset_array(a : tuple):
    x = ((np.array([])),) * len(a)
    return x
#data pack of arduino in the following format -> "Sensor number, Filtered Sensor value \n" 
abc = np.zeros(10,)
cde = np.zeros(5,)
print("before",abc)
print(cde)
test = np.array([])
(abc, cde, test) = reset_array(a = (abc, cde, test))

print("after",abc)
print(test)

#global variable
"""
target_wavelength_data = np.array([]) 
target_sensor = 4
time_stamp = np.array([])
csv_file = "test.csv"


#initalize Serial communcation
arduinoData = serial.Serial("com8",115200)
start_time = datetime.now()


while 1: #replace with a function to NOT stop root.mainloop() running
    n_sensor = 0
    current_data = np.array([])
    
    while n_sensor != 288:
        #while to value should be get_data()
        while (arduinoData.inWaiting()==0):
            pass
        packet = arduinoData.readline()
        packet = str(packet,"utf-8")
        packet = packet.strip()
        packet = packet.split(',')
        n_sensor = int(packet[0])
        value = int(packet[1])

        if n_sensor == 1:
            time_passed = (datetime.now()-start_time).total_seconds()
            time_stamp = np.append(time_stamp, time_passed)
            current_data = np.append(current_data, time_passed)

        if n_sensor == target_sensor:
            target_wavelength_data = np.append(target_wavelength_data, value)
        current_data = np.append(current_data, value)

    with open(csv_file,'a', newline='') as f:
        w = csv.writer(f)
        w.writerow(current_data)
    print("end")
"""