import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from spacepy import pycdf  
import datetime

def plot_cdf_heatmap(cdf_path):
    """
    Load a CDF file and plot total counts per energy channel over time as log-scale heatmaps.

    Parameters:
    cdf_path (str): Path to the CDF file
    """

    # Load CDF file
    cdf = pycdf.CDF(cdf_path)
    total_counts_all = cdf["total_counts_per_energy"][:]  # Shape: (10, 16, 45)
    time_data = cdf["epoch"][:]                           # Shape: (10, 45)
    cdf.close()

    # Use time from the first bitstring (assuming all have the same time axis)
    time_raw = np.ravel(time_data[0])

    # Convert from microseconds or milliseconds to seconds if necessary
    if np.max(time_raw) > 10**15:
        time_raw = time_raw / 1e6
    elif np.max(time_raw) > 10**12:
        time_raw = time_raw / 1e3

    # Convert to datetime format
    time_dt = [datetime.datetime.utcfromtimestamp(t) for t in time_raw]
    x_start = mdates.date2num(time_dt[0])
    x_end = mdates.date2num(time_dt[-1])

    # Create subplots for each bitstring
    fig, axes = plt.subplots(10, 1, figsize=(10, 14), sharex=True, sharey=True)

    # Y-axis ticks and labels
    y_ticks = [0, 8, 15]
    y_labels = [f"Ch{ch}" for ch in y_ticks]

    for i, ax in enumerate(axes):
        counts = total_counts_all[i]  # Shape: (16, 45)

        im = ax.imshow(counts, aspect='auto', origin='lower',
                       extent=[x_start, x_end, 0, 16],
                       cmap='viridis', norm=plt.cm.colors.LogNorm())

        ax.set_ylabel(f"Bit {i}")
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_labels)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    # Set x-axis label for the bottom plot
    axes[-1].set_xlabel("Time (UTC)")
    plt.xticks(rotation=45)

    # Add a shared colorbar
    cbar_ax = fig.add_axes([0.92, 0.1, 0.02, 0.8])
    fig.colorbar(im, cax=cbar_ax, orientation='vertical', label="Counts (log scale)")

    # Layout and title
    plt.tight_layout(rect=[0, 0, 0.9, 1])
    plt.suptitle("Total Counts per Energy Channel (Log Heatmap)", fontsize=16, y=1.02)
    plt.show()
    
# test
# plot_cdf_heatmap("../input/l1_cdf_data_l2.cdf")