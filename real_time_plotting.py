from matplotlib import pyplot as plt

x = []
y = []

for i in range(200):
    if i <= 50:
        y.append(0)
    elif (i > 50 and i <= 150):
        y.append(1)
    else:
        y.append(0)
    x.append(i)

    # Mention x and y limits to define their range
    plt.xlim(0, 200)
    plt.ylim(0, 2)
    
    # Plotting graph
    plt.plot(x, y, color = 'green')
    plt.pause(0.01)

plt.show()
