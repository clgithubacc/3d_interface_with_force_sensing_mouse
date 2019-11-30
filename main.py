from window_controller import WindowController
from sensor_input import SensorInput
import time

si=SensorInput(arduino_port='COM4')
si.start()
time.sleep(3)
print('wwwwwwwwwwwwwwwwwwwwwwwwwwwww')
wc=WindowController(si)
wc.start()
