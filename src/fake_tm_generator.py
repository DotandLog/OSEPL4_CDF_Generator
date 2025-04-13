import numpy as np
import struct
import datetime
import random
import os
from pathlib import Path
from datetime import timedelta


def generate_tt2000_epoch(start_time=None, num_cycles=45, cycle_period_seconds=80):
    """
    Generate epoch timestamps in TT2000 format.

    Args:
        start_time: Starting datetime (default: current time)
        num_cycles: Number of cycles to generate
        cycle_period_seconds: Time between cycles in seconds

    Returns:
        List of datetime objects representing epochs
    """
    if start_time is None:
        start_time = datetime.datetime.now()

    epochs = []
    for i in range(num_cycles):
        epoch_time = start_time + timedelta(seconds=i * cycle_period_seconds)
        epochs.append(epoch_time)

    return epochs


def epoch_to_bytes(epoch):
    """
    Convert epoch datetime to bytes representation (simplified TT2000 format)
    In a real implementation, this would use proper TT2000 conversion

    Args:
        epoch: Datetime object

    Returns:
        Bytes representation of the epoch
    """
    # This is a simplified representation
    # In reality, TT2000 format would be more complex
    timestamp = int(epoch.timestamp() * 1000)  # milliseconds since epoch
    return struct.pack('>Q', timestamp)  # 8-byte big-endian unsigned long long


def generate_electron_counts(num_energy=16, num_azimuthal=7, num_incident=6, num_cycles=45):
    """
    Generate random electron count data with values from 100 to 1000

    Args:
        num_energy: Number of energy steps
        num_azimuthal: Number of azimuthal angles
        num_incident: Number of incident angles
        num_cycles: Number of cycles

    Returns:
        4D array of electron counts in order (incident, azimuthal, energy, cycle)
    """
    # Generate with values in the range 100-1000
    return np.random.randint(100, 1001, size=(num_incident, num_azimuthal, num_energy, num_cycles))


def generate_measure_energy(num_energy=16, num_cycles=45):
    """
    Generate energy values for each energy step

    Args:
        num_energy: Number of energy steps
        num_cycles: Number of cycles

    Returns:
        2D array of energy values
    """
    # Use the provided energy values
    energy_values = [100, 200, 300, 400, 500, 600, 700,
                     800, 900, 1000, 2000, 3000, 4000, 5000, 6000, 7000]

    # Create a 2D array with the same energy values for each cycle
    energy_array = np.tile(energy_values, (num_cycles, 1)).T
    return energy_array


def generate_output_hv(num_electrode=3, num_energy=16, num_incident=6, num_cycles=45):
    """
    Generate HV output values for each electrode, energy step, and incident angle

    Args:
        num_electrode: Number of electrodes
        num_energy: Number of energy steps
        num_incident: Number of incident angles
        num_cycles: Number of cycles

    Returns:
        4D array of HV output values
    """
    # Define incident angles
    incident_angles = [0, 15, 30, 45, 60, 75, 90]

    # Energy values
    energy_values = [100, 200, 300, 400, 500, 600, 700,
                     800, 900, 1000, 2000, 3000, 4000, 5000, 6000, 7000]

    # Initialize 4D array
    output_hv = np.zeros((num_electrode, num_energy, num_incident, num_cycles))

    # Fill with values according to the pattern in the document
    for energy_idx, energy in enumerate(energy_values):
        for angle_idx in range(num_incident):
            # Upper electrode is always 0
            output_hv[0, energy_idx, angle_idx, :] = 0

            # Middle electrode = energy * 0.46
            output_hv[1, energy_idx, angle_idx, :] = energy * 0.46

            # Lower electrode = energy * 0.16
            output_hv[2, energy_idx, angle_idx, :] = energy * 0.16

    return output_hv


def generate_datataking_time(epochs, num_cycles=45):
    """
    Generate data taking start times and durations

    Args:
        epochs: List of epoch datetimes
        num_cycles: Number of cycles

    Returns:
        Tuple of (start_times, durations)
    """
    # Start times are the same as epochs
    start_times = epochs

    # Durations are random between 70-75 seconds
    durations = np.random.uniform(70, 75, size=num_cycles)

    return start_times, durations


def generate_data_quality(num_energy=16, num_azimuthal=7, num_incident=6, num_cycles=45):
    """
    Generate data quality flags

    Args:
        num_energy: Number of energy steps
        num_azimuthal: Number of azimuthal angles
        num_incident: Number of incident angles
        num_cycles: Number of cycles

    Returns:
        4D array of data quality flags
    """
    # Most data is good quality (0), with occasional issues (1-255)
    quality = np.zeros(
        (num_energy, num_azimuthal, num_incident, num_cycles), dtype=np.uint8)

    # Add some random quality issues (about 5% of the data)
    mask = np.random.random(quality.shape) < 0.05
    quality[mask] = np.random.randint(1, 256, size=np.sum(mask))

    return quality


def value_to_bytes(value, num_bytes=2, is_float=False):
    """
    Convert a value to bytes representation

    Args:
        value: Value to convert
        num_bytes: Number of bytes to use
        is_float: Whether the value is a float

    Returns:
        Bytes representation of the value
    """
    if is_float:
        if num_bytes == 4:
            return struct.pack('>f', value)  # 4-byte big-endian float
        else:
            return struct.pack('>d', value)  # 8-byte big-endian double
    else:
        if num_bytes == 1:
            return struct.pack('>B', value)  # 1-byte unsigned char
        elif num_bytes == 2:
            return struct.pack('>H', value)  # 2-byte big-endian unsigned short
        elif num_bytes == 4:
            return struct.pack('>I', value)  # 4-byte big-endian unsigned int
        elif num_bytes == 8:
            # 8-byte big-endian unsigned long long
            return struct.pack('>Q', value)


def generate_l1_cdf_hex_bitstring():
    """
    Generate a hex bitstring representing the L1 CDF data

    Returns:
        Hex bitstring
    """
    num_energy = 16
    num_azimuthal = 7
    num_incident = 6
    num_cycles = 45
    num_electrode = 3

    # Generate data
    epochs = generate_tt2000_epoch()
    electron_counts = generate_electron_counts()
    bg_counts = generate_bg_counts()  # Background count data
    measure_energy = generate_measure_energy()
    output_hv = generate_output_hv()
    start_times, durations = generate_datataking_time(epochs)
    data_quality = generate_data_quality()

    # Convert to bytes
    byte_array = bytearray()

    # Epochs (TT2000 format, 8 bytes each)
    for epoch in epochs:
        byte_array.extend(epoch_to_bytes(epoch))

    # Electron_Count (2 bytes per value)
    for i in range(num_incident):
        for a in range(num_azimuthal):
            for e in range(num_energy):
                for c in range(num_cycles):
                    byte_array.extend(value_to_bytes(
                        electron_counts[i, a, e, c], 2))

    # BG_Count (2 bytes per value)
    for i in range(num_incident):
        for a in range(num_azimuthal):
            for e in range(num_energy):
                for c in range(num_cycles):
                    byte_array.extend(value_to_bytes(bg_counts[i, a, e, c], 2))

    # Measure_Energy (4 bytes per value, float)
    for e in range(num_energy):
        for c in range(num_cycles):
            byte_array.extend(value_to_bytes(
                measure_energy[e, c], 4, is_float=True))

    # Output_HV (4 bytes per value, float)
    for el in range(num_electrode):
        for e in range(num_energy):
            for i in range(num_incident):
                for c in range(num_cycles):
                    byte_array.extend(value_to_bytes(
                        output_hv[el, e, i, c], 4, is_float=True))

    # Datataking_Time_Start (8 bytes each, TT2000 format)
    for t in start_times:
        byte_array.extend(epoch_to_bytes(t))

    # Data_Time_Duration (4 bytes each, float)
    for d in durations:
        byte_array.extend(value_to_bytes(d, 4, is_float=True))

    # Data_Quality (1 byte each)
    for e in range(num_energy):
        for a in range(num_azimuthal):
            for i in range(num_incident):
                for c in range(num_cycles):
                    byte_array.extend(value_to_bytes(
                        data_quality[e, a, i, c], 1))

    # Convert to hex string
    hex_string = byte_array.hex()

    return hex_string


def save_l1_cdf_hex_bitstring(filename):
    """
    Generate and save hex bitstring to a file

    Args:
        filename: Output filename
    """
    hex_string = generate_l1_cdf_hex_bitstring()

    # Use Path for cross-platform compatibility
    output_path = Path(filename)

    # Create parent directories if they don't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(hex_string)

    print(f"Generated hex bitstring saved to {output_path}")
    print(f"Total length: {len(hex_string) // 2} bytes")


def save_l1_cdf_binary(filename):
    """
    Generate and save binary data to a file

    Args:
        filename: Output filename
    """
    hex_string = generate_l1_cdf_hex_bitstring()
    binary_data = bytes.fromhex(hex_string)

    # Use Path for cross-platform compatibility
    output_path = Path(filename)

    # Create parent directories if they don't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'wb') as f:
        f.write(binary_data)

    print(f"Generated binary data saved to {output_path}")
    print(f"Total length: {len(binary_data)} bytes")


def generate_bg_counts(num_energy=16, num_azimuthal=7, num_incident=6, num_cycles=45):
    """
    Generate random background count data with values from 0 to 100

    Args:
        num_energy: Number of energy steps
        num_azimuthal: Number of azimuthal angles
        num_incident: Number of incident angles
        num_cycles: Number of cycles

    Returns:
        4D array of background counts in order (incident, azimuthal, energy, cycle)
    """
    # Generate with values in the range 0-100
    return np.random.randint(0, 101, size=(num_incident, num_azimuthal, num_energy, num_cycles))


def generate_multiple_bitstrings(count, output_file):
    """
    Generate multiple hex bitstrings and save them to a text file

    Args:
        count: Number of bitstrings to generate
        output_file: Output filename
    """
    # Use Path for cross-platform compatibility
    output_path = Path(output_file)

    # Create parent directories if they don't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        for i in range(count):
            print(f"Generating bitstring {i+1}/{count}...")
            hex_string = generate_l1_cdf_hex_bitstring()
            f.write(f"Bitstring {i+1}:\n")
            f.write(hex_string)
            f.write("\n\n")

    print(f"Generated {count} hex bitstrings saved to {output_path}")


def main():
    # Generate 10 bitstrings and save to text file
    generate_multiple_bitstrings(10, "input/l1_cdf_data_10samples.txt")

    # Optional: Save a single sample as binary
    # save_l1_cdf_binary("input/l1_cdf_data_sample.bin")

    # Sample analysis of the data structure
    print("\nData Structure Analysis:")
    print("------------------------")

    num_energy = 16
    num_azimuthal = 7
    num_incident = 6
    num_cycles = 45
    num_electrode = 3

    # Epochs: 45 * 8 bytes = 360 bytes
    epoch_size = num_cycles * 8
    print(f"Epochs: {num_cycles} cycles * 8 bytes = {epoch_size} bytes")

    # Electron_Count: 16 * 7 * 6 * 45 * 2 bytes = 60,480 bytes
    electron_count_size = num_energy * num_azimuthal * num_incident * num_cycles * 2
    print(
        f"Electron_Count: {num_energy} * {num_azimuthal} * {num_incident} * {num_cycles} * 2 bytes = {electron_count_size} bytes")

    # BG_Count: 16 * 7 * 6 * 45 * 2 bytes = 60,480 bytes
    bg_count_size = num_energy * num_azimuthal * num_incident * num_cycles * 2
    print(
        f"BG_Count: {num_energy} * {num_azimuthal} * {num_incident} * {num_cycles} * 2 bytes = {bg_count_size} bytes")

    # Measure_Energy: 16 * 45 * 4 bytes = 2,880 bytes
    measure_energy_size = num_energy * num_cycles * 4
    print(
        f"Measure_Energy: {num_energy} * {num_cycles} * 4 bytes = {measure_energy_size} bytes")

    # Output_HV: 3 * 16 * 6 * 45 * 4 bytes = 51,840 bytes
    output_hv_size = num_electrode * num_energy * num_incident * num_cycles * 4
    print(
        f"Output_HV: {num_electrode} * {num_energy} * {num_incident} * {num_cycles} * 4 bytes = {output_hv_size} bytes")

    # Datataking_Time_Start: 45 * 8 bytes = 360 bytes
    start_time_size = num_cycles * 8
    print(
        f"Datataking_Time_Start: {num_cycles} * 8 bytes = {start_time_size} bytes")

    # Data_Time_Duration: 45 * 4 bytes = 180 bytes
    duration_size = num_cycles * 4
    print(
        f"Data_Time_Duration: {num_cycles} * 4 bytes = {duration_size} bytes")

    # Data_Quality: 16 * 7 * 6 * 45 * 1 byte = 30,240 bytes
    data_quality_size = num_energy * num_azimuthal * num_incident * num_cycles * 1
    print(
        f"Data_Quality: {num_energy} * {num_azimuthal} * {num_incident} * {num_cycles} * 1 byte = {data_quality_size} bytes")

    # Total: sum of all sizes
    total_size = epoch_size + electron_count_size + bg_count_size + measure_energy_size + \
        output_hv_size + start_time_size + duration_size + data_quality_size
    print(f"Total size: {total_size} bytes = {total_size / 1024:.2f} KB")


if __name__ == "__main__":
    main()
