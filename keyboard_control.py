import logging
import sys
import time
from threading import Event

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

from pynput import keyboard

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E702')

DEFAULT_HEIGHT = 0.5
MOVING_DISTANCE=0.5

deck_attached_event = Event()

logging.basicConfig(level=logging.ERROR)

def param_deck_flow(_, value_str):
    value = int(value_str)
    print(value)
    if value:
        deck_attached_event.set()
        print('Deck is attached!')
    else:
        print('Deck is NOT attached!')

def on_press(key,mc):
        try:
            if key.char == 'f':
                print("f pressed")
                mc.forward(MOVING_DISTANCE)
            elif key.char == 'b':
                print("b pressed")
                mc.back(MOVING_DISTANCE)
            elif key.char == 'l':
                print("l pressed")
                mc.left(MOVING_DISTANCE)
            elif key.char == 'r':
                print("r pressed")
                mc.right(MOVING_DISTANCE)
            elif key.char == 'u':
                print("u pressed")
                mc.up(MOVING_DISTANCE)
            elif key.char == 'd':
                print("d pressed")
                mc.down(MOVING_DISTANCE)
        except AttributeError:
            pass  # Handle special keys (e.g., shift, ctrl)

def on_release(key):
    if key == keyboard.Key.esc:
        print("Exiting program...")
        return False  # Stop the listener

# def forward(mc):
#     mc.forward(0.5)
#     time.sleep(1)
#     print("going forward")

# def backward(mc):
#     mc.back(0.5)
#     time.sleep(1)
#     print("going backward")


def main():
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
        time.sleep(1)

        if not deck_attached_event.wait(timeout=5):
            print('No flow deck detected!')
            sys.exit(1)

        with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:

            with keyboard.Listener(
                on_press=lambda key: on_press(key, mc),
                on_release=on_release
            ) as listener:
                listener.join()
        
main()
