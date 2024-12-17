import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib import pyplot as plt
from scipy import signal

duration = 10  # Total time duration in seconds
sampling_rate = 1000  # Number of samples per second (Hz)
frequency =  0.2
time = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
square_signal = signal.square(2 * np.pi * frequency * time)

with open('signal.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(square_signal)

plt.plot(time, square_signal)
plt.xlabel('Time (s)')
plt.ylabel('Signal Value')
plt.title('Square Wave')
plt.grid(True)
plt.show()
# signal = np.array(np.zeros((10)))
# signal[3:7]=1
# print(signal)
# # # Step 2: Save the grid as a CSV file


# time = np.arange(1, 11)
# # print(time)
# plt.plot(time,signal)
# plt.show()
