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
    With specific ranges for energy_idx 6 and 7 at certain incident angles:
    - For incident_idx 5: values range from 750-1000
    - For incident_idx 4: values range from 500-750

    Args:
        num_energy: Number of energy steps
        num_azimuthal: Number of azimuthal angles
        num_incident: Number of incident angles
        num_cycles: Number of cycles

    Returns:
        4D array of electron counts in order (incident, azimuthal, energy, cycle)
    """
    # Generate base array with values in the range 100-1000
    electron_counts = np.random.randint(100, 1001, size=(
        num_incident, num_azimuthal, num_energy, num_cycles))

    # Apply special ranges for specific indices
    # For incident_idx 5 (last incident angle), energy_idx 6 and 7: range 750-1000
    for a in range(num_azimuthal):
        for c in range(num_cycles):
            electron_counts[5, a, 6, c] = np.random.randint(750, 1001)
            electron_counts[5, a, 7, c] = np.random.randint(750, 1001)

    # For incident_idx 4, energy_idx 6 and 7: range 500-750
    for a in range(num_azimuthal):
        for c in range(num_cycles):
            electron_counts[4, a, 6, c] = np.random.randint(500, 751)
            electron_counts[4, a, 7, c] = np.random.randint(500, 751)

    return electron_counts


def generate_electron_counts_setting1(num_energy=16, num_azimuthal=7, num_incident=6, num_cycles=45):
    """
    Generate electron count data with Setting 1:
    垂直角度5 (incident_idx 4): 水平7個方向都在能階7和8的欄位用500~750，其他能階值用0~500
    垂直角度6 (incident_idx 5): 水平7個方向都在能階7和8的欄位用750~1000，其他能階值用0~500
    垂直角度1~4 (incident_idx 0-3): 所有值全部都用100~500
    
    Args:
        num_energy: Number of energy steps
        num_azimuthal: Number of azimuthal angles
        num_incident: Number of incident angles
        num_cycles: Number of cycles
        
    Returns:
        4D array of electron counts in order (incident, azimuthal, energy, cycle)
    """
    # Initialize array
    electron_counts = np.zeros((num_incident, num_azimuthal, num_energy, num_cycles), dtype=np.int32)
    
    # 垂直角度1~4 (incident_idx 0-3): 所有值都用100~500
    for incident_idx in range(4):  # incident_idx 0-3
        for a in range(num_azimuthal):
            for e in range(num_energy):
                for c in range(num_cycles):
                    electron_counts[incident_idx, a, e, c] = np.random.randint(100, 501)
    
    # 垂直角度5 (incident_idx 4): 先設定基礎值0~500，然後特別設定能階7和8
    for a in range(num_azimuthal):
        for e in range(num_energy):
            for c in range(num_cycles):
                if e in [6, 7]:  # 能階7和8 (index 6,7 對應 700eV, 800eV)
                    electron_counts[4, a, e, c] = np.random.randint(500, 751)
                else:  # 其他能階用0~500
                    electron_counts[4, a, e, c] = np.random.randint(0, 501)
    
    # 垂直角度6 (incident_idx 5): 先設定基礎值0~500，然後特別設定能階7和8
    for a in range(num_azimuthal):
        for e in range(num_energy):
            for c in range(num_cycles):
                if e in [6, 7]:  # 能階7和8
                    electron_counts[5, a, e, c] = np.random.randint(750, 1001)
                else:  # 其他能階用0~500
                    electron_counts[5, a, e, c] = np.random.randint(0, 501)
    
    return electron_counts


def generate_electron_counts_setting2(num_energy=16, num_azimuthal=7, num_incident=6, num_cycles=45):
    """
    Generate electron count data with Setting 2:
    水平角度4 (azimuthal_idx 3):
      - 垂直角度1 (incident_idx 0) 在能階7和8用750~1000，其他能階用100~500
      - 垂直角度2 (incident_idx 1) 在能階7和8用500~750，其他能階用100~500
    水平角度3,5 (azimuthal_idx 2,4):
      - 垂直角度1 (incident_idx 0) 在能階7和8用500~750，其他能階用100~500
      - 垂直角度2 (incident_idx 1) 在能階7和8用500~750，其他能階用100~500
    剩下的水平角度 (azimuthal_idx 0,1,5,6):
      - 在能階7和8用100~500
    
    Args:
        num_energy: Number of energy steps
        num_azimuthal: Number of azimuthal angles
        num_incident: Number of incident angles
        num_cycles: Number of cycles
        
    Returns:
        4D array of electron counts in order (incident, azimuthal, energy, cycle)
    """
    # Initialize with all values 100-500
    electron_counts = np.random.randint(100, 501, size=(num_incident, num_azimuthal, num_energy, num_cycles))
    
    for c in range(num_cycles):
        for energy_idx in [6, 7]:  # 能階7和8
            
            # 水平角度4 (azimuthal_idx 3)
            azimuthal_idx = 3
            # 垂直角度1 (incident_idx 0): 能階7和8用750~1000
            electron_counts[0, azimuthal_idx, energy_idx, c] = np.random.randint(750, 1001)
            # 垂直角度2 (incident_idx 1): 能階7和8用500~750
            electron_counts[1, azimuthal_idx, energy_idx, c] = np.random.randint(500, 751)
            
            # 水平角度3 (azimuthal_idx 2)
            azimuthal_idx = 2
            # 垂直角度1 (incident_idx 0): 能階7和8用500~750
            electron_counts[0, azimuthal_idx, energy_idx, c] = np.random.randint(500, 751)
            # 垂直角度2 (incident_idx 1): 能階7和8用500~750
            electron_counts[1, azimuthal_idx, energy_idx, c] = np.random.randint(500, 751)
            
            # 水平角度5 (azimuthal_idx 4)
            azimuthal_idx = 4
            # 垂直角度1 (incident_idx 0): 能階7和8用500~750
            electron_counts[0, azimuthal_idx, energy_idx, c] = np.random.randint(500, 751)
            # 垂直角度2 (incident_idx 1): 能階7和8用500~750
            electron_counts[1, azimuthal_idx, energy_idx, c] = np.random.randint(500, 751)
            
            # 剩下的水平角度 (azimuthal_idx 0,1,5,6): 在能階7和8用100~500
            # 這些位置已經在初始化時設為100~500，不需要額外處理
    
    return electron_counts


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


def create_hex_bitstring_from_data(epochs, electron_counts, bg_counts, measure_energy, 
                                 output_hv, start_times, durations, data_quality):
    """
    Create hex bitstring from data components
    
    Args:
        epochs, electron_counts, bg_counts, measure_energy, output_hv, start_times, durations, data_quality
        
    Returns:
        Hex bitstring
    """
    num_energy = 16
    num_azimuthal = 7
    num_incident = 6
    num_cycles = 45
    num_electrode = 3
    
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
                    byte_array.extend(value_to_bytes(electron_counts[i, a, e, c], 2))

    # BG_Count (2 bytes per value)
    for i in range(num_incident):
        for a in range(num_azimuthal):
            for e in range(num_energy):
                for c in range(num_cycles):
                    byte_array.extend(value_to_bytes(bg_counts[i, a, e, c], 2))

    # Measure_Energy (4 bytes per value, float)
    for e in range(num_energy):
        for c in range(num_cycles):
            byte_array.extend(value_to_bytes(measure_energy[e, c], 4, is_float=True))

    # Output_HV (4 bytes per value, float)
    for el in range(num_electrode):
        for e in range(num_energy):
            for i in range(num_incident):
                for c in range(num_cycles):
                    byte_array.extend(value_to_bytes(output_hv[el, e, i, c], 4, is_float=True))

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
                    byte_array.extend(value_to_bytes(data_quality[e, a, i, c], 1))

    # Convert to hex string
    hex_string = byte_array.hex()
    return hex_string


def generate_l1_cdf_hex_bitstring():
    """
    Generate a hex bitstring representing the L1 CDF data (Original method)

    Returns:
        Hex bitstring
    """
    # Generate data
    epochs = generate_tt2000_epoch()
    electron_counts = generate_electron_counts()
    bg_counts = generate_bg_counts()  # Background count data
    measure_energy = generate_measure_energy()
    output_hv = generate_output_hv()
    start_times, durations = generate_datataking_time(epochs)
    data_quality = generate_data_quality()

    return create_hex_bitstring_from_data(epochs, electron_counts, bg_counts, measure_energy, 
                                        output_hv, start_times, durations, data_quality)


def generate_l1_cdf_hex_bitstring_setting1():
    """
    Generate a hex bitstring representing the L1 CDF data with Setting 1
    
    Returns:
        Hex bitstring
    """
    # Generate data with Setting 1
    epochs = generate_tt2000_epoch()
    electron_counts = generate_electron_counts_setting1()
    bg_counts = generate_bg_counts()  # Background count data
    measure_energy = generate_measure_energy()
    output_hv = generate_output_hv()
    start_times, durations = generate_datataking_time(epochs)
    data_quality = generate_data_quality()

    return create_hex_bitstring_from_data(epochs, electron_counts, bg_counts, measure_energy, 
                                        output_hv, start_times, durations, data_quality)


def generate_l1_cdf_hex_bitstring_setting2():
    """
    Generate a hex bitstring representing the L1 CDF data with Setting 2
    
    Returns:
        Hex bitstring
    """
    # Generate data with Setting 2
    epochs = generate_tt2000_epoch()
    electron_counts = generate_electron_counts_setting2()
    bg_counts = generate_bg_counts()  # Background count data
    measure_energy = generate_measure_energy()
    output_hv = generate_output_hv()
    start_times, durations = generate_datataking_time(epochs)
    data_quality = generate_data_quality()

    return create_hex_bitstring_from_data(epochs, electron_counts, bg_counts, measure_energy, 
                                        output_hv, start_times, durations, data_quality)


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


def generate_multiple_bitstrings(count, output_file):
    """
    Generate multiple hex bitstrings and save them to a text file (Original method)

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


def generate_multiple_bitstrings_with_settings(count_per_setting, output_file):
    """
    Generate multiple hex bitstrings with different settings and save them to a single text file
    
    Args:
        count_per_setting: Number of bitstrings to generate per setting
        output_file: Output filename
    """
    # Use Path for cross-platform compatibility
    output_path = Path(output_file)
    
    # Create parent directories if they don't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        bitstring_counter = 1
        
        # Generate bitstrings with Setting 1
        for i in range(count_per_setting):
            print(f"Generating Setting 1 bitstring {i+1}/{count_per_setting}...")
            hex_string = generate_l1_cdf_hex_bitstring_setting1()
            f.write(f"Bitstring {bitstring_counter} (Setting 1):\n")
            f.write(hex_string)
            f.write("\n\n")
            bitstring_counter += 1
        
        # Generate bitstrings with Setting 2
        for i in range(count_per_setting):
            print(f"Generating Setting 2 bitstring {i+1}/{count_per_setting}...")
            hex_string = generate_l1_cdf_hex_bitstring_setting2()
            f.write(f"Bitstring {bitstring_counter} (Setting 2):\n")
            f.write(hex_string)
            f.write("\n\n")
            bitstring_counter += 1
    
    total_count = count_per_setting * 2
    print(f"Generated {total_count} hex bitstrings ({count_per_setting} per setting) saved to {output_path}")


def generate_multiple_bitstrings_with_settings_separate(count_per_setting, output_dir="input"):
    """
    Generate multiple hex bitstrings with different settings and save them to separate text files
    
    Args:
        count_per_setting: Number of bitstrings to generate per setting
        output_dir: Output directory for files
    """
    # Use Path for cross-platform compatibility
    output_path = Path(output_dir)
    
    # Create parent directories if they don't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Generate Setting 1 bitstrings
    setting1_file = output_path / "l1_cdf_data_setting1.txt"
    with open(setting1_file, 'w') as f:
        for i in range(count_per_setting):
            print(f"Generating Setting 1 bitstring {i+1}/{count_per_setting}...")
            hex_string = generate_l1_cdf_hex_bitstring_setting1()
            f.write(f"Bitstring {i+1} (Setting 1):\n")
            f.write(hex_string)
            f.write("\n\n")
    
    print(f"Generated {count_per_setting} Setting 1 bitstrings saved to {setting1_file}")
    
    # Generate Setting 2 bitstrings
    setting2_file = output_path / "l1_cdf_data_setting2.txt"
    with open(setting2_file, 'w') as f:
        for i in range(count_per_setting):
            print(f"Generating Setting 2 bitstring {i+1}/{count_per_setting}...")
            hex_string = generate_l1_cdf_hex_bitstring_setting2()
            f.write(f"Bitstring {i+1} (Setting 2):\n")
            f.write(hex_string)
            f.write("\n\n")
    
    print(f"Generated {count_per_setting} Setting 2 bitstrings saved to {setting2_file}")
    print(f"Total: {count_per_setting * 2} bitstrings in 2 separate files")


def print_data_structure_analysis():
    """
    Print data structure analysis
    """
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


def print_settings_summary():
    """
    Print summary of specialized settings
    """
    print("\nSpecialized Settings Summary:")
    print("=" * 50)
    print("Original Setting:")
    print("  - incident_idx 5, energy_idx 6&7: 750-1000")
    print("  - incident_idx 4, energy_idx 6&7: 500-750")
    print("  - other positions: 100-1000")
    print()
    print("Setting 1 - 垂直角度基準:")
    print("  - 垂直角度5 (incident_idx 4): 水平7個方向在能階7和8用500~750，其他能階用0~500")
    print("  - 垂直角度6 (incident_idx 5): 水平7個方向在能階7和8用750~1000，其他能階用0~500")
    print("  - 垂直角度1~4 (incident_idx 0-3): 所有值都用100~500")
    print()
    print("Setting 2 - 水平角度基準:")
    print("  - 水平角度4 (azimuthal 3):")
    print("    * 垂直角度1 (incident 0): 能階7和8用750~1000，其他能階用100~500")
    print("    * 垂直角度2 (incident 1): 能階7和8用500~750，其他能階用100~500")
    print("  - 水平角度3,5 (azimuthal 2,4):")
    print("    * 垂直角度1 (incident 0): 能階7和8用500~750，其他能階用100~500")
    print("    * 垂直角度2 (incident 1): 能階7和8用500~750，其他能階用100~500")
    print("  - 剩下的水平角度 (azimuthal 0,1,5,6): 能階7和8用100~500")
    print("  - 其他位置: 用100~500")
    print()
    print("索引對照:")
    print("  - 垂直角度 (incident angles): 1-6 對應 index 0-5")
    print("  - 水平角度 (azimuthal angles): 1-7 對應 index 0-6")
    print("  - 能階 (energy levels): 7,8 對應 index 6,7 (700eV, 800eV)")


def main():
    """
    Main function with options for different generation modes
    """
    print("OSEPL4 Bitstring Generator")
    print("=" * 30)
    print("1. Generate original bitstrings (10 samples)")
    print("2. Generate specialized setting bitstrings (5 per setting, separate files)")
    print("3. Generate specialized setting bitstrings (5 per setting, combined file)")
    print("4. Generate all types")
    print("5. Show settings summary only")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        # Generate original bitstrings
        generate_multiple_bitstrings(10, "input/l1_cdf_data_10samples.txt")
        print_data_structure_analysis()
        
    elif choice == "2":
        # Generate specialized setting bitstrings in separate files
        generate_multiple_bitstrings_with_settings_separate(5, "input")
        print_settings_summary()
        
    elif choice == "3":
        # Generate specialized setting bitstrings in combined file
        generate_multiple_bitstrings_with_settings(5, "input/l1_cdf_data_specialized_settings.txt")
        print_settings_summary()
        
    elif choice == "4":
        # Generate all types
        generate_multiple_bitstrings(10, "input/l1_cdf_data_10samples.txt")
        generate_multiple_bitstrings_with_settings_separate(5, "input")
        print_data_structure_analysis()
        print_settings_summary()
        
    elif choice == "5":
        # Show settings summary only
        print_settings_summary()
        
    else:
        print("Invalid choice. Running default (original bitstrings)...")
        generate_multiple_bitstrings(10, "input/l1_cdf_data_10samples.txt")
        print_data_structure_analysis()


if __name__ == "__main__":
    main()