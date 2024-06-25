# - Import packages

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import time
import datetime
import matplotlib.ticker as mticker

# - Plot function
def plot_data(file_path):
    plt.rc('font', family='serif', size=14)
    fig, ax1 = plt.subplots(figsize=(12, 6))
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("right", size="3%", pad=0.05)

    # Define the color range
    jet = plt.cm.jet
    colors = [jet(x) for x in np.linspace(1, 0.5, 256)]
    green_to_red = LinearSegmentedColormap.from_list('GreenToRed', colors, N=256)

    t = time.time()
    i = 0
    vehicle_data = {'global_times': [], 'mile_markers': [], 'speeds': []}

    for vehicle_id, global_time, v_vel, local_y in data_generator(file_path):
        vehicle_data['global_times'].append(global_time)
        vehicle_data['mile_markers'].append(local_y)
        vehicle_data['speeds'].append(v_vel)

        i += 1
        if i % 1000 == 0:
            print(f"Processed {i} lines")

    # Convert to numpy array for subsequent operations
    global_times = np.array(vehicle_data['global_times'])
    mile_markers = np.array(vehicle_data['mile_markers'])
    speeds = np.array(vehicle_data['speeds'])

    # Plot the diagram
    sc = ax1.scatter(global_times, mile_markers, c=speeds, cmap=green_to_red, vmin=0, vmax=60, s=0.1)
    plt.colorbar(sc, cax=cax).set_label('Speed (km/s)', rotation=90, labelpad=20)
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Kilometer marker")

    # Set format for the x axis
    min_time = global_times.min()
    max_time = global_times.max()
    num_ticks = 20
    ticks_loc = np.linspace(min_time, max_time, num_ticks)
    x_datetime = [datetime.datetime.fromtimestamp(ts) + datetime.timedelta(hours=9) for ts in ticks_loc]
    labels = [d.strftime('%H:%M:%S') for d in x_datetime]
    ax1.set_xticks(ticks_loc)
    ax1.set_xticklabels(labels, rotation=45)

    plt.show()

# - Operating zone
file_path = 
plot_data(file_path)