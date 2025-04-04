import struct
import json
import datetime
import numpy as np
import argparse
from pathlib import Path


class BitStringParser:
    def __init__(self):
        # Define data structure dimensions
        self.num_energy = 16
        self.num_azimuthal = 7
        self.num_incident = 6
        self.num_cycles = 45
        self.num_electrode = 3

    def bytes_to_tt2000(self, byte_data):
        """
        Convert bytes to TT2000 format (simplified representation)

        Args:
            byte_data: Bytes representation of TT2000 timestamp

        Returns:
            Datetime object and ISO format string
        """
        # In a real implementation, this would use proper TT2000 conversion
        # 8-byte big-endian unsigned long long
        timestamp_ms = struct.unpack('>Q', byte_data)[0]
        dt = datetime.datetime.fromtimestamp(timestamp_ms / 1000.0)
        return dt, dt.isoformat()

    def bytes_to_value(self, byte_data, is_float=False):
        """
        Convert bytes to value

        Args:
            byte_data: Bytes representation
            is_float: Whether the value is a float

        Returns:
            Decoded value
        """
        if is_float:
            if len(byte_data) == 4:
                # 4-byte big-endian float
                return struct.unpack('>f', byte_data)[0]
            else:
                # 8-byte big-endian double
                return struct.unpack('>d', byte_data)[0]
        else:
            if len(byte_data) == 1:
                # 1-byte unsigned char
                return struct.unpack('>B', byte_data)[0]
            elif len(byte_data) == 2:
                # 2-byte big-endian unsigned short
                return struct.unpack('>H', byte_data)[0]
            elif len(byte_data) == 4:
                # 4-byte big-endian unsigned int
                return struct.unpack('>I', byte_data)[0]
            elif len(byte_data) == 8:
                # 8-byte big-endian unsigned long long
                return struct.unpack('>Q', byte_data)[0]

    def parse_bitstring(self, hex_string):
        """
        Parse a hex bitstring into structured data

        Args:
            hex_string: Hex string representation of L1 CDF data

        Returns:
            Dictionary containing structured data
        """
        # Convert hex string to bytes
        binary_data = bytes.fromhex(hex_string)

        # Initialize result dictionary
        result = {
            "epochs": [],
            "electron_counts": [],
            "bg_counts": [],
            "measure_energy": [],
            "output_hv": [],
            "datataking_time_start": [],
            "data_time_duration": [],
            "data_quality": []
        }

        # Initialize position
        pos = 0

        # Parse EPOCH (TT2000 format, 8 bytes each)
        for c in range(self.num_cycles):
            dt, iso = self.bytes_to_tt2000(binary_data[pos:pos+8])
            result["epochs"].append({
                "cycle": c,
                "timestamp_ms": int(dt.timestamp() * 1000),
                "iso_format": iso
            })
            pos += 8

        # Parse Electron_Count (2 bytes per value)
        electron_counts = []
        for i in range(self.num_incident):
            incident_data = []
            for a in range(self.num_azimuthal):
                azimuthal_data = []
                for e in range(self.num_energy):
                    energy_data = []
                    for c in range(self.num_cycles):
                        count = self.bytes_to_value(binary_data[pos:pos+2])
                        energy_data.append(count)
                        pos += 2
                    azimuthal_data.append(energy_data)
                incident_data.append(azimuthal_data)
            electron_counts.append(incident_data)

        # Convert to a more readable format for JSON
        for i in range(self.num_incident):
            for a in range(self.num_azimuthal):
                for e in range(self.num_energy):
                    for c in range(self.num_cycles):
                        result["electron_counts"].append({
                            "incident_idx": i,
                            "azimuthal_idx": a,
                            "energy_idx": e,
                            "cycle": c,
                            "count": electron_counts[i][a][e][c]
                        })

        # Parse BG_Count (2 bytes per value)
        bg_counts = []
        for i in range(self.num_incident):
            incident_data = []
            for a in range(self.num_azimuthal):
                azimuthal_data = []
                for e in range(self.num_energy):
                    energy_data = []
                    for c in range(self.num_cycles):
                        count = self.bytes_to_value(binary_data[pos:pos+2])
                        energy_data.append(count)
                        pos += 2
                    azimuthal_data.append(energy_data)
                incident_data.append(azimuthal_data)
            bg_counts.append(incident_data)

        # Convert to a more readable format for JSON
        for i in range(self.num_incident):
            for a in range(self.num_azimuthal):
                for e in range(self.num_energy):
                    for c in range(self.num_cycles):
                        result["bg_counts"].append({
                            "incident_idx": i,
                            "azimuthal_idx": a,
                            "energy_idx": e,
                            "cycle": c,
                            "count": bg_counts[i][a][e][c]
                        })

        # Parse Measure_Energy (4 bytes per value, float)
        measure_energy = []
        for e in range(self.num_energy):
            energy_data = []
            for c in range(self.num_cycles):
                energy = self.bytes_to_value(
                    binary_data[pos:pos+4], is_float=True)
                energy_data.append(energy)
                pos += 4
            measure_energy.append(energy_data)

        # Convert to a more readable format for JSON
        for e in range(self.num_energy):
            for c in range(self.num_cycles):
                result["measure_energy"].append({
                    "energy_idx": e,
                    "cycle": c,
                    "energy_value": measure_energy[e][c]
                })

        # Parse Output_HV (4 bytes per value, float)
        output_hv = []
        for el in range(self.num_electrode):
            electrode_data = []
            for e in range(self.num_energy):
                energy_data = []
                for i in range(self.num_incident):
                    incident_data = []
                    for c in range(self.num_cycles):
                        hv = self.bytes_to_value(
                            binary_data[pos:pos+4], is_float=True)
                        incident_data.append(hv)
                        pos += 4
                    energy_data.append(incident_data)
                electrode_data.append(energy_data)
            output_hv.append(electrode_data)

        # Convert to a more readable format for JSON with electrode names
        electrode_names = ["upper", "middle", "lower"]
        for el in range(self.num_electrode):
            for e in range(self.num_energy):
                for i in range(self.num_incident):
                    for c in range(self.num_cycles):
                        result["output_hv"].append({
                            "electrode": electrode_names[el],
                            "electrode_idx": el,
                            "energy_idx": e,
                            "incident_idx": i,
                            "cycle": c,
                            "voltage": output_hv[el][e][i][c]
                        })

        # Parse Datataking_Time_Start (8 bytes each, TT2000 format)
        for c in range(self.num_cycles):
            dt, iso = self.bytes_to_tt2000(binary_data[pos:pos+8])
            result["datataking_time_start"].append({
                "cycle": c,
                "timestamp_ms": int(dt.timestamp() * 1000),
                "iso_format": iso
            })
            pos += 8

        # Parse Data_Time_Duration (4 bytes each, float)
        for c in range(self.num_cycles):
            duration = self.bytes_to_value(
                binary_data[pos:pos+4], is_float=True)
            result["data_time_duration"].append({
                "cycle": c,
                "duration_seconds": duration
            })
            pos += 4

        # Parse Data_Quality (1 byte each)
        data_quality = []
        for e in range(self.num_energy):
            energy_data = []
            for a in range(self.num_azimuthal):
                azimuthal_data = []
                for i in range(self.num_incident):
                    incident_data = []
                    for c in range(self.num_cycles):
                        quality = self.bytes_to_value(binary_data[pos:pos+1])
                        incident_data.append(quality)
                        pos += 1
                    azimuthal_data.append(incident_data)
                energy_data.append(azimuthal_data)
            data_quality.append(energy_data)

        # Convert to a more readable format for JSON
        for e in range(self.num_energy):
            for a in range(self.num_azimuthal):
                for i in range(self.num_incident):
                    for c in range(self.num_cycles):
                        result["data_quality"].append({
                            "energy_idx": e,
                            "azimuthal_idx": a,
                            "incident_idx": i,
                            "cycle": c,
                            "quality": data_quality[e][a][i][c]
                        })

        return result

    def parse_multiple_bitstrings(self, input_file):
        """
        Parse multiple bitstrings from a text file

        Args:
            input_file: Input filename containing multiple bitstrings

        Returns:
            List of dictionaries containing structured data
        """
        results = []
        current_bitstring = ""
        current_index = None

        with open(input_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith("Bitstring"):
                    # If we have a previous bitstring, parse it
                    if current_bitstring and current_index is not None:
                        print(f"Parsing Bitstring {current_index}...")
                        result = self.parse_bitstring(current_bitstring)
                        results.append({
                            "bitstring_index": current_index,
                            "data": result
                        })

                    # Start a new bitstring
                    try:
                        current_index = int(line.split()[1].replace(":", ""))
                        current_bitstring = ""
                    except (IndexError, ValueError):
                        print(
                            f"Warning: Could not parse bitstring index from line: {line}")
                        current_index = None
                        current_bitstring = ""
                elif line and current_index is not None:
                    # Add line to current bitstring
                    current_bitstring += line

        # Parse the last bitstring
        if current_bitstring and current_index is not None:
            print(f"Parsing Bitstring {current_index}...")
            result = self.parse_bitstring(current_bitstring)
            results.append({
                "bitstring_index": current_index,
                "data": result
            })

        return results

    def save_as_json(self, data, output_file):
        """
        Save parsed data as JSON

        Args:
            data: Parsed data
            output_file: Output filename
        """
        class NumpyEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                return super(NumpyEncoder, self).default(obj)

        with open(output_file, 'w') as f:
            json.dump(data, f, cls=NumpyEncoder, indent=2)

        print(f"Parsed data saved to {output_file}")

    def create_hdf5_structure(self, data, output_file):
        """
        Save parsed data as HDF5 (a more efficient format for large scientific data)

        Args:
            data: Parsed data
            output_file: Output filename
        """
        try:
            import h5py
        except ImportError:
            print(
                "h5py not installed. Please install with 'pip install h5py' to use HDF5 format.")
            return

        with h5py.File(output_file, 'w') as f:
            # For each bitstring
            for bitstring_data in data:
                bitstring_index = bitstring_data["bitstring_index"]
                bitstring_group = f.create_group(
                    f"bitstring_{bitstring_index}")

                # Process EPOCH data
                epochs_group = bitstring_group.create_group("epochs")
                epochs = bitstring_data["data"]["epochs"]
                epochs_group.create_dataset(
                    "timestamp_ms", data=[e["timestamp_ms"] for e in epochs])
                epochs_group.create_dataset("iso_format", data=[
                                            e["iso_format"] for e in epochs], dtype=h5py.special_dtype(vlen=str))

                # Process electron counts with a more efficient structure
                counts_data = np.zeros(
                    (self.num_energy, self.num_azimuthal, self.num_incident, self.num_cycles), dtype=np.int32)
                for entry in bitstring_data["data"]["electron_counts"]:
                    e, a, i, c = entry["energy_idx"], entry["azimuthal_idx"], entry["incident_idx"], entry["cycle"]
                    counts_data[e, a, i, c] = entry["count"]
                bitstring_group.create_dataset(
                    "electron_counts", data=counts_data)

                # Process background counts
                bg_counts_data = np.zeros(
                    (self.num_energy, self.num_azimuthal, self.num_incident, self.num_cycles), dtype=np.int32)
                for entry in bitstring_data["data"]["bg_counts"]:
                    e, a, i, c = entry["energy_idx"], entry["azimuthal_idx"], entry["incident_idx"], entry["cycle"]
                    bg_counts_data[e, a, i, c] = entry["count"]
                bitstring_group.create_dataset(
                    "bg_counts", data=bg_counts_data)

                # Process energy measurements
                energy_data = np.zeros(
                    (self.num_energy, self.num_cycles), dtype=np.float32)
                for entry in bitstring_data["data"]["measure_energy"]:
                    e, c = entry["energy_idx"], entry["cycle"]
                    energy_data[e, c] = entry["energy_value"]
                bitstring_group.create_dataset(
                    "measure_energy", data=energy_data)

                # Process HV output
                electrode_names = ["upper", "middle", "lower"]
                hv_data = np.zeros((self.num_electrode, self.num_energy,
                                   self.num_incident, self.num_cycles), dtype=np.float32)
                for entry in bitstring_data["data"]["output_hv"]:
                    el, e, i, c = entry["electrode_idx"], entry["energy_idx"], entry["incident_idx"], entry["cycle"]
                    hv_data[el, e, i, c] = entry["voltage"]

                hv_group = bitstring_group.create_group("output_hv")
                hv_group.create_dataset("values", data=hv_data)
                hv_group.attrs["electrode_names"] = electrode_names

                # Process data taking times
                start_times_group = bitstring_group.create_group(
                    "datataking_time_start")
                start_times = bitstring_data["data"]["datataking_time_start"]
                start_times_group.create_dataset(
                    "timestamp_ms", data=[t["timestamp_ms"] for t in start_times])
                start_times_group.create_dataset("iso_format", data=[
                                                 t["iso_format"] for t in start_times], dtype=h5py.special_dtype(vlen=str))

                # Process durations
                durations = np.array(
                    [d["duration_seconds"] for d in bitstring_data["data"]["data_time_duration"]], dtype=np.float32)
                bitstring_group.create_dataset(
                    "data_time_duration", data=durations)

                # Process data quality
                quality_data = np.zeros(
                    (self.num_energy, self.num_azimuthal, self.num_incident, self.num_cycles), dtype=np.uint8)
                for entry in bitstring_data["data"]["data_quality"]:
                    e, a, i, c = entry["energy_idx"], entry["azimuthal_idx"], entry["incident_idx"], entry["cycle"]
                    quality_data[e, a, i, c] = entry["quality"]
                bitstring_group.create_dataset(
                    "data_quality", data=quality_data)

        print(f"Parsed data saved in HDF5 format to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Parse L1 CDF hex bitstrings')
    parser.add_argument(
        'input_file', help='Input file containing hex bitstrings')
    parser.add_argument(
        '--output-format', choices=['json', 'hdf5'], default='json', help='Output format (default: json)')
    parser.add_argument(
        '--output-file', help='Output file name (default: derived from input filename)')

    args = parser.parse_args()

    # Set default output file name if not provided
    if args.output_file is None:
        input_path = Path(args.input_file)
        if args.output_format == 'json':
            args.output_file = str(input_path.with_suffix('.json'))
        else:
            args.output_file = str(input_path.with_suffix('.h5'))

    # Parse bitstrings
    parser = BitStringParser()
    parsed_data = parser.parse_multiple_bitstrings(args.input_file)

    # Save in selected format
    if args.output_format == 'json':
        parser.save_as_json(parsed_data, args.output_file)
    else:
        parser.create_hdf5_structure(parsed_data, args.output_file)


if __name__ == "__main__":
    main()
