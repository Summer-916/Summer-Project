# - Import packages

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import time
import datetime
import matplotlib.ticker as mticker

# - Read in data

def data_generator(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 12:
                vehicle_id = int(parts[0])
                global_time = int(parts[3]) / 1000 
                v_vel = float(parts[11]) * 0.681818 
                local_y = float(parts[5]) / 5280  
                lane_id = int(parts[13])
                yield vehicle_id, global_time, v_vel, local_y, lane_id

# - Plot function

def plot_lane_data(lane_id, lane_data):
    plt.rc('font', family='serif', size=14)
    fig, ax1 = plt.subplots(figsize=(10, 3))
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("right", size="3%", pad=0.05)

    # Define the color range
    jet = plt.cm.jet
    colors = [jet(x) for x in np.linspace(1, 0.5, 256)]
    green_to_red = LinearSegmentedColormap.from_list('GreenToRed', colors, N=256)

    global_times = np.array(lane_data['global_times'])
    mile_markers = np.array(lane_data['mile_markers'])
    speeds = np.array(lane_data['speeds'])

    # Plot the diagram
    sc = ax1.scatter(global_times, mile_markers, c=speeds, cmap=green_to_red, vmin=0, vmax=80, s=1)
    plt.colorbar(sc, cax=cax).set_label('Speed (mph)', rotation=90, labelpad=20)
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Mile marker")
    ax1.set_title(f'Lane {lane_id} Trajectory')

    # Set format for the x axis
    min_time = global_times.min()
    max_time = global_times.max()
    num_ticks = 10
    ticks_loc = np.linspace(min_time, max_time, num_ticks)
    x_datetime = [datetime.datetime.fromtimestamp(ts) + datetime.timedelta(hours=9) for ts in ticks_loc]
    labels = [d.strftime('%H:%M:%S') for d in x_datetime]
    ax1.set_xticks(ticks_loc)
    ax1.set_xticklabels(labels, rotation=45)

    # Show the diagram
    plt.show()

# - main function, plot diagram by the lane ID 
def plot_data(file_path):
    lane_data = {}

    for vehicle_id, global_time, v_vel, local_y, lane_id in data_generator(file_path):
        if lane_id not in lane_data:
            lane_data[lane_id] = {'global_times': [], 'mile_markers': [], 'speeds': []}
        lane_data[lane_id]['global_times'].append(global_time)
        lane_data[lane_id]['mile_markers'].append(local_y)
        lane_data[lane_id]['speeds'].append(v_vel)

    # plot diagram for each lane
    for lane_id, data in lane_data.items():
        plot_lane_data(lane_id, data)
    print('Finish!')

# - Operating zone
file_path = 
plot_data(file_path)