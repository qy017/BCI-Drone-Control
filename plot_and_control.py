import logging
import sys
import time
from threading import Event
from matplotlib import pyplot as plt
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

# Drone URI (change it to your drone's URI)
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E702')

# Constants
DEFAULT_HEIGHT = 1.0
PLOT_DURATION = 200  # Number of iterations for plotting
SLEEP_TIME = 0.01  # Time to pause between plot updates

# Initialize event to check if deck is attached
deck_attached_event = Event()

# Logging setup
logging.basicConfig(level=logging.ERROR)

# Plot data initialization
x = []
y = []

# Drone movement logic based on plot values
def control_drone_motion(scf, i, y_value):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        if y_value == 1:
            mc.forward(0.05)  # Move forward when y == 1
        else:
            mc.stop()  # Stay in place when y == 0

# Plotting and controlling drone movement
def plot_and_control(scf):
    # Initialize plot
    for i in range(PLOT_DURATION):
        if i <= 50:
            y_value = 0
        elif (i > 50 and i <= 150):
            y_value = 1
        else:
            y_value = 0
        y.append(y_value)
        x.append(i)

        # Control drone movement based on y value
        control_drone_motion(scf, i, y_value)

        # Plot data
        plt.xlim(0, PLOT_DURATION)
        plt.ylim(0, 2)
        plt.plot(x, y, color='green')
        plt.pause(SLEEP_TIME)

    plt.show()

# Check if flow deck is attached
def param_deck_flow(_, value_str):
    value = int(value_str)
    print(value)
    if value:
        deck_attached_event.set()
        print('Deck is attached!')
    else:
        print('Deck is NOT attached!')

if __name__ == '__main__':
    cflib.crtp.init_drivers()

    # Connect to the Crazyflie
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

        # Add callback for detecting flow deck
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
        time.sleep(1)

        # Wait for flow deck attachment
        if not deck_attached_event.wait(timeout=5):
            print('No flow deck detected!')
            sys.exit(1)

        # Start plotting and controlling drone motion
        plot_and_control(scf)
