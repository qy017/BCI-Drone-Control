import logging
import sys
import time
from threading import Event
import numpy as np
from scipy import signal

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E702')
DEFAULT_HEIGHT = 0.5
flying = False
deck_attached_event = Event()
logging.basicConfig(level=logging.ERROR)
duration = 10  # Total time duration in seconds
sampling_rate = 1000  # Number of samples per second (Hz)
frequency =  0.2
time = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
square_signal = signal.square(2 * np.pi * frequency * time)

def param_deck_flow(_, value_str):
    value = int(value_str)
    print(value)
    if value:
        deck_attached_event.set()
        print('Deck is attached!')
    else:
        print('Deck is NOT attached!')

def take_off_simple(scf):
    global flying
    if not flying:
        with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
            time.sleep(3)
            flying = True
            print("flying")

def land(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        mc.stop()

def main():
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
        time.sleep(1)

        if not deck_attached_event.wait(timeout=5):
            print('No flow deck detected!')
            sys.exit(1)

        take_off_simple(scf)
        time.sleep(3)
        land(scf)
        scf.cf.close_link()
        # start_time = time.time()
        # try:
        #     for t, signal_value in zip(time, signal_square):
        #         # Convert the square wave signal to a control value (thrust or velocity)
        #         # In this case, we use the signal value as desired height or thrust
        #         target_height = signal_value * 2  # Scale to control height (0 to 2 meters)

        #         # Command the drone to fly at the target height (can be extended to more control)
        #         cf.go_to([0, 0, target_height], 0.5)  # Go to target height with speed

        #         # Wait for the next control step
        #         time.sleep(time_step)

        # except KeyboardInterrupt:
        #     print("Flight interrupted.")

main()
