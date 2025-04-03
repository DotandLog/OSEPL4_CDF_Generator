import json
import numpy as np
import h5py
from pathlib import Path
from spacepy import pycdf
import datetime


def compute_moments(electron_counts):
    counts_array = np.zeros((16, 7, 6, 45))
    for entry in electron_counts:
        e, a, i, c = entry["energy_idx"], entry["azimuthal_idx"], entry["incident_idx"], entry["cycle"]
        counts_array[e, a, i, c] = entry["count"]

    total_counts = np.sum(counts_array, axis=(1, 2))
    mean_counts = np.mean(counts_array, axis=(1, 2))

    return total_counts.tolist(), mean_counts.tolist()


def save_as_cdf(output_file, l2_data):
    output_file = str(output_file)  # Ensure string path for pycdf

    with pycdf.CDF(output_file, '') as cdf:
        indices = [d["bitstring_index"] for d in l2_data]
        totals = [d["total_counts_per_energy"] for d in l2_data]
        means = [d["mean_counts_per_energy"] for d in l2_data]
        epochs = [d["epochs"] for d in l2_data]
        durations = [d["durations"] for d in l2_data]

        cdf["bitstring_index"] = indices
        cdf["total_counts_per_energy"] = totals
        cdf["mean_counts_per_energy"] = means
        cdf["epoch"] = epochs
        cdf["duration"] = durations

        # Add attributes for clarity
        cdf["epoch"].attrs["UNITS"] = "ms since 1970-01-01"
        cdf["epoch"].attrs["DESCRIPTION"] = "Start time of each data cycle in milliseconds"
        cdf["duration"].attrs["UNITS"] = "seconds"
        cdf["duration"].attrs["DESCRIPTION"] = "Duration of each data cycle"

    print(f"Level-2 CDF saved to {output_file}")


def process_json_to_l2(input_path, output_path):
    with open(input_path, 'r') as f:
        data = json.load(f)

    l2_results = []
    for bitstring in data:
        electron_counts = bitstring["data"]["electron_counts"]
        total, mean = compute_moments(electron_counts)

        # 提取 epoch (以毫秒表示) 與 duration
        epoch_list = [entry["timestamp_ms"] for entry in bitstring["data"].get("datataking_time_start", [])]
        duration_list = [entry["duration_seconds"] for entry in bitstring["data"].get("data_time_duration", [])]

        l2_results.append({
            "bitstring_index": bitstring["bitstring_index"],
            "total_counts_per_energy": total,
            "mean_counts_per_energy": mean,
            "epochs": epoch_list,
            "durations": duration_list
        })

    save_as_cdf(output_path, l2_results)


def process_hdf5_to_l2(input_path, output_path):
    l2_results = []
    with h5py.File(input_path, 'r') as f:
        for bitstring_key in f.keys():
            electron_counts = f[bitstring_key]["electron_counts"][:]
            total = np.sum(electron_counts, axis=(1, 2))
            mean = np.mean(electron_counts, axis=(1, 2))

            index = int(bitstring_key.split('_')[-1])

            # Placeholder for HDF5 time if needed in future
            l2_results.append({
                "bitstring_index": index,
                "total_counts_per_energy": total.tolist(),
                "mean_counts_per_energy": mean.tolist(),
                "epochs": [0] * 45,
                "durations": [0.0] * 45
            })

    save_as_cdf(output_path, l2_results)


def convert_l1_to_l2(input_file):
    input_path = Path(input_file)
    output_file = input_path.with_name(input_path.stem + "_l2.cdf")

    if input_file.endswith(".json"):
        process_json_to_l2(input_path, output_file)
    elif input_file.endswith(".h5"):
        process_hdf5_to_l2(input_path, output_file)
    else:
        raise ValueError("Unsupported file type: must be .json or .h5")


# Example usage
convert_l1_to_l2("../input/l1_cdf_data.json")