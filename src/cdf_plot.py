import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from spacepy import pycdf  
import datetime
import argparse

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
    

def plot_cdf_mult_heatmaps(folder_path, save_dir=None):
    
    """
    Load a CDF file and plot total counts per energy channel over time as log-scale heatmaps.

    Parameters:
    folder_path (str): Path contains CDF files
    save_dir (str): Path that saves image
    """
    
    cdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".cdf")]
    
    if not cdf_files:
        print("No CDF files found in the folder.")
        return
    
    for cdf_path in cdf_files:
        if 'omni' in cdf_path: 
            is_omni = True
            Electron_Flux = 'Electron_Flux_Omni'
        else: 
            is_omni = False
            Electron_Flux = 'Electron_Flux_3D'
        print(f"Processing: {os.path.basename(cdf_path)}")
        cdf = pycdf.CDF(cdf_path)        
        total_counts_all = cdf[Electron_Flux][:]  # (, 6, 7, 16, 45)
        time_data = cdf["EPOCH"][:]                           # (45,)
        cdf.close()

        if len(total_counts_all.shape) < 5:
            # print(total_counts_all.shape)
            if is_omni == False:
                x, y, num, e = total_counts_all.shape[:]
                total_counts_all = total_counts_all.reshape(1, x, y, num, e)
            # else: 
            #     x, y = total_counts_all.shape[:]
            #     total_counts_all = total_counts_all.reshape(1, x, y)

        # Convert timestamp
        time_raw = np.ravel(time_data)
        if np.max(time_raw) > 10**15:
            time_raw = time_raw / 1e6
        elif np.max(time_raw) > 10**12:
            time_raw = time_raw / 1e3
            
        time_dt = [datetime.datetime.fromtimestamp(t) for t in time_raw]
        x_start = mdates.date2num(time_dt[0])
        x_end = mdates.date2num(time_dt[-1])

        if is_omni == False:

            num_data = total_counts_all.shape[0]     # 10
            num_figs = total_counts_all.shape[1]     # 6
            num_subplots = total_counts_all.shape[2] # 7

            y_ticks = [0, 8, 15]
            y_labels = [f"Ch{ch}" for ch in y_ticks]

            for data_idx in range(num_data):
                for fig_idx in range(num_figs):
                    fig, axes = plt.subplots(num_subplots, 1, figsize=(10, 14), sharex=True, sharey=True)

                    for bit_idx in range(num_subplots):
                        ax = axes[bit_idx]
                        counts = total_counts_all[data_idx][fig_idx][bit_idx]  # shape (16, 45)

                        im = ax.imshow(counts, aspect='auto', origin='lower',
                                    extent=[x_start, x_end, 0, 16],
                                    cmap='viridis', norm=plt.cm.colors.LogNorm())

                        ax.set_ylabel(f"Bit {bit_idx}")
                        ax.set_yticks(y_ticks)
                        ax.set_yticklabels(y_labels)
                        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

                    axes[-1].set_xlabel("Time (UTC)")
                    plt.xticks(rotation=45)

                    cbar_ax = fig.add_axes([0.92, 0.1, 0.02, 0.8])
                    fig.colorbar(im, cax=cbar_ax, orientation='vertical', label="Counts (log scale)")

                    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.99, wspace=0.3, hspace=0.3)
                    plt.suptitle(f"{os.path.basename(cdf_path)} | Sample {data_idx + 1} - Plot {fig_idx + 1}", fontsize=16, y=1.02)
                    
                    
                    os.makedirs(save_dir, exist_ok=True)
                    save_path = os.path.join(save_dir, f"{os.path.basename(cdf_path)}_sample{data_idx+1}_fig{fig_idx+1}.png")
                    plt.savefig(save_path, bbox_inches='tight')
                    print(f"Saved: {save_path}")
                    plt.close()
            
        else: 
            num_data = total_counts_all.shape[0]     # 10
            # num_figs = total_counts_all.shape[1]     # 6
            num_subplots = 1 # 7

            y_ticks = [0, 8, 15]
            y_labels = [f"Ch{ch}" for ch in y_ticks]

            # for data_idx in range(num_data):
                # for fig_idx in range(num_figs):
            fig, ax = plt.subplots(num_subplots, 1, figsize=(12, 6), sharex=True, sharey=True)

            # for bit_idx in range(num_subplots):
            counts = total_counts_all  # shape (16, 45)

            im = ax.imshow(counts, aspect='auto', origin='lower',
                        extent=[x_start, x_end, 0, 16],
                        cmap='viridis', norm=plt.cm.colors.LogNorm())

            # ax.set_ylabel(f"Bit {bit_idx}")
            ax.set_yticks(y_ticks)
            ax.set_yticklabels(y_labels)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

            ax.set_xlabel("Time (UTC)")
            plt.xticks(rotation=45)

            cbar_ax = fig.add_axes([0.92, 0.1, 0.02, 0.8])
            fig.colorbar(im, cax=cbar_ax, orientation='vertical', label="Counts (log scale)")
            plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.92, wspace=0.3, hspace=0.3)

            # plt.tight_layout(rect=[0, 0, 0.9, 1])
            plt.suptitle(f"{os.path.basename(cdf_path)} | Sample Omni Plot ", fontsize=16, y=1.02)
            
            
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, f"{os.path.basename(cdf_path)}_Sample_Omni_Plot.png")
            plt.savefig(save_path, bbox_inches='tight')
            print(f"Saved: {save_path}")
                # plt.show()
            plt.close()

# test
# plot_cdf_mult_heatmaps("../input", save_dir='../output_img')
def main():
    parser = argparse.ArgumentParser(description="Plot CDF heatmaps from a CDF file.")
    parser.add_argument("--cdf_path", type=str, help="Path to the CDF file.")
    parser.add_argument("--save_dir", type=str, default=None, help="Directory to save the plots.")
    

    args = parser.parse_args()

    plot_cdf_mult_heatmaps(args.cdf_path, save_dir=args.save_dir)



if __name__ == "__main__":
    main()