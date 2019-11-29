import pyfirmata
import time
import threading


class SensorInput(threading.Thread):
    def __init__(self, arduino_port='COM3', force_diff_threshold=200, uniform_pressing_threshold=500):
        board = pyfirmata.Arduino(arduino_port)
        it = pyfirmata.util.Iterator(board)
        it.start()
        self.fsul = board.get_pin('a:0:i')
        self.fsur = board.get_pin('a:1:i')
        self.fsbl = board.get_pin('a:2:i')
        self.fsbr = board.get_pin('a:3:i')
        self.forces = [-1, -1, -1, -1]
        self.force_diff_threshold = force_diff_threshold
        self.uniform_pressing_threshold = uniform_pressing_threshold
        threading.Thread.__init__(self)

    def run(self):
        while True:
            fsreadings = [self.fsul.read(), self.fsur.read(), self.fsbl.read(), self.fsbr.read()]
            self.forces = [int(v / 900 * 2000) for v in fsreadings]
            time.sleep(0.1)

    def get_input(self):
        force_diff = [self.forces[i] - self.forces[3] for i in range(3)]
        exceed_threshold = [abs(i) > self.force_diff_threshold for i in force_diff]
        if not (exceed_threshold[0] or exceed_threshold[1] or exceed_threshold[2]) and self.forces[
            0] > self.uniform_pressing_threshold:
            pattern = 0  # Uniform
        elif exceed_threshold[0] and not (exceed_threshold[1] or exceed_threshold[2]):
            pattern = 1  # Upper Left
        elif exceed_threshold[1] and not (exceed_threshold[0] or exceed_threshold[2]):
            pattern = 2  # Upper Right
        elif exceed_threshold[2] and not (exceed_threshold[0] or exceed_threshold[1]):
            pattern = 3  # Bottom Left
        elif exceed_threshold[0] and exceed_threshold[1] and exceed_threshold[2]:
            pattern = 4  # Bottom Right
        else:
            pattern = 5

        return str(pattern) + ' ' + ' '.join(str(i) for i in self.forces)
