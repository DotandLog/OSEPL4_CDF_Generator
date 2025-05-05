import struct
import json
import datetime
import numpy as np
import argparse
import os
from pathlib import Path


class BitStringParser:
    def __init__(self):
        # Define data structure dimensions according to the image specification
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

        # Initialize result dictionary with global attributes from the image
        result = {
            "global_attributes": {
                "Project": "A-ESA science payload",
                "Discipline": "lunar surface plasma environment",
                "Data_type": "L1 > Level 1 uncalibrated count data",  # Updated as per image
                "Descriptor": "A-ESA",
                "File_naming_convention": "source_datatype_descriptor",
                "Data_version": "V01",
                "PI_name": "Lin, Shin-Fa / Chang, Tzu-Fang",
                "PI_affiliation": "TASA / NCKU",
                "TEXT": "All-Sky Electrostatic Analyze (10eV ~ 10KeV)",
                "Instrument_type": "Particles (space)",
                "Logical_source": "AESA_L1",  # Updated as per image
                "Logical_file_id": f"AESA_L1_{datetime.datetime.now().strftime('%Y%m%d')}_v01",
                "Logical_source_description": "Level 1 uncalibrated count data for 10eV ~ 10KeV electron distribution on the lunar surface",
                "Time_resolution": "Cycle period ~ 80 s",
                "Rules_of_use": "TBD",
                "Generated_by": "TASA / NCKU",
                "Generation_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "Acknowledgement": "TBD",
                "LINK_TEXT": "TBD",
                "LINK_TITLE": "TBD"
            },
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

        # Use Path for cross-platform compatibility
        input_path = Path(input_file)

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        with open(input_path, 'r', encoding='utf-8') as f:
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

        # Use Path for cross-platform compatibility
        output_path = Path(output_file)

        # Create parent directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, cls=NumpyEncoder, indent=2)

        print(f"Parsed data saved to {output_path}")

    def generate_cdf_directly(self, data, output_dir):
        """
        Generate CDF files directly from bitstring data according to the image specification

        Args:
            data: Parsed data
            output_dir: Output directory for CDF files
        """
        try:
            import spacepy.pycdf as cdf
        except ImportError:
            print(
                "Error: spacepy.pycdf not installed. Please install with 'pip install spacepy'")
            print("Note: SpacePy requires CDF library. See installation guide at: https://spacepy.github.io/install.html")
            return

        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Process each bitstring
        for bitstring_data in data:
            bitstring_index = bitstring_data["bitstring_index"]
            data_values = bitstring_data["data"]

            # Get the date from the first epoch for filename
            first_epoch_iso = data_values["epochs"][0]["iso_format"]
            date_str = first_epoch_iso.split('T')[0].replace('-', '')

            # Create CDF file
            cdf_file_path = output_path / \
                f"AESA_L1_{date_str}_bitstring_{bitstring_index}_v01.cdf"

            print(f"Generating CDF file for Bitstring {bitstring_index}...")

            # Create a new CDF file
            with cdf.CDF(str(cdf_file_path), '') as cdf_file:
                # Set global attributes strictly according to the image
                cdf_file.attrs["Project"] = "A-ESA science payload"
                cdf_file.attrs["Discipline"] = "lunar surface plasma environment"
                cdf_file.attrs["Data_type"] = "L1 > Level 1 uncalibrated count data"
                cdf_file.attrs["Descriptor"] = "A-ESA"
                cdf_file.attrs["File_naming_convention"] = "source_datatype_descriptor"
                cdf_file.attrs["Data_version"] = "V01"
                cdf_file.attrs["PI_name"] = "Lin, Shin-Fa / Chang, Tzu-Fang"
                cdf_file.attrs["PI_affiliation"] = "TASA / NCKU"
                cdf_file.attrs["TEXT"] = "All-Sky Electrostatic Analyze (10eV ~ 10KeV)"
                cdf_file.attrs["Instrument_type"] = "Particles (space)"
                cdf_file.attrs["Logical_source"] = "AESA_L1"
                cdf_file.attrs["Logical_file_id"] = f"AESA_L1_{date_str}_v01"
                cdf_file.attrs["Logical_source_description"] = "Level 1 uncalibrated count data for 10eV ~ 10KeV electron distribution on the lunar surface"
                cdf_file.attrs["Time_resolution"] = "Cycle period ~ 80 s"
                cdf_file.attrs["Rules_of_use"] = "TBD"
                cdf_file.attrs["Generated_by"] = "TASA / NCKU"
                cdf_file.attrs["Generation_date"] = datetime.datetime.now().strftime(
                    "%Y-%m-%d")
                cdf_file.attrs["Acknowledgement"] = "TBD"
                cdf_file.attrs["LINK_TEXT"] = "TBD"
                cdf_file.attrs["LINK_TITLE"] = "TBD"

                # Create variables according to the image

                # EPOCH (1 X 45)
                epoch_ms = [e["timestamp_ms"] for e in data_values["epochs"]]
                # Convert to CDF_TIME_TT2000 format
                cdf_file.new('EPOCH', epoch_ms, type=cdf.const.CDF_TIME_TT2000)

                # Electron_Count (16 x 7 x 6 x 45) - note dimensions match the image
                electron_counts = np.zeros(
                    (self.num_energy, self.num_azimuthal, self.num_incident, self.num_cycles), dtype=np.int32)
                for entry in data_values["electron_counts"]:
                    i, a, e, c = entry["incident_idx"], entry["azimuthal_idx"], entry["energy_idx"], entry["cycle"]
                    # Reshape to match the image specification
                    electron_counts[e, a, i, c] = entry["count"]

                cdf_file.new('Electron_Count', electron_counts,
                             type=cdf.const.CDF_INT4)

                # BG_Count (16 x 7 x 6 x 45) - note dimensions match the image
                bg_counts = np.zeros(
                    (self.num_energy, self.num_azimuthal, self.num_incident, self.num_cycles), dtype=np.int32)
                for entry in data_values["bg_counts"]:
                    i, a, e, c = entry["incident_idx"], entry["azimuthal_idx"], entry["energy_idx"], entry["cycle"]
                    # Reshape to match the image specification
                    bg_counts[e, a, i, c] = entry["count"]

                cdf_file.new('BG_Count', bg_counts, type=cdf.const.CDF_INT4)

                # Measure_Energy (16 x 45)
                energy_values = np.zeros(
                    (self.num_energy, self.num_cycles), dtype=np.float32)
                for entry in data_values["measure_energy"]:
                    e, c = entry["energy_idx"], entry["cycle"]
                    energy_values[e, c] = entry["energy_value"]

                cdf_file.new('Measure_Energy', energy_values,
                             type=cdf.const.CDF_FLOAT)

                # Output_HV (3 x 16 x 6 x 45)
                output_hv = np.zeros((self.num_electrode, self.num_energy,
                                     self.num_incident, self.num_cycles), dtype=np.float32)
                for entry in data_values["output_hv"]:
                    el, e, i, c = entry["electrode_idx"], entry["energy_idx"], entry["incident_idx"], entry["cycle"]
                    output_hv[el, e, i, c] = entry["voltage"]

                cdf_file.new('Output_HV', output_hv, type=cdf.const.CDF_FLOAT)

                # Datataking_Time_Start (1 x 45)
                start_times_ms = [t["timestamp_ms"]
                                  for t in data_values["datataking_time_start"]]
                # Reshape as 1 x 45 array to match the image
                start_times_reshaped = np.array(
                    start_times_ms).reshape(1, self.num_cycles)
                cdf_file.new('Datataking_Time_Start',
                             start_times_reshaped, type=cdf.const.CDF_TIME_TT2000)

                # Data_Time_Duration (1 x 45)
                durations = np.array(
                    [d["duration_seconds"] for d in data_values["data_time_duration"]], dtype=np.float32)
                # Reshape as 1 x 45 array to match the image
                durations_reshaped = durations.reshape(1, self.num_cycles)
                cdf_file.new('Data_Time_Duration',
                             durations_reshaped, type=cdf.const.CDF_FLOAT)

                # Data_Quality (16 x 7 x 6 x 45)
                data_quality = np.zeros(
                    (self.num_energy, self.num_azimuthal, self.num_incident, self.num_cycles), dtype=np.uint8)
                for entry in data_values["data_quality"]:
                    e, a, i, c = entry["energy_idx"], entry["azimuthal_idx"], entry["incident_idx"], entry["cycle"]
                    data_quality[e, a, i, c] = entry["quality"]

                cdf_file.new('Data_Quality', data_quality,
                             type=cdf.const.CDF_UINT1)

            print(f"CDF file generated: {cdf_file_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Parse OSEPL4 L1 CDF hex bitstrings and generate CDF directly')
    parser.add_argument(
        'input_file', help='Input file containing hex bitstrings')
    parser.add_argument(
        '--output-json', default='parsed_data.json', help='Output JSON filename')
    parser.add_argument('--output-cdf-dir', default='./cdf_files',
                        help='Output directory for CDF files')
    parser.add_argument('--json-only', action='store_true',
                        help='Only generate JSON, skip CDF')
    parser.add_argument('--cdf-only', action='store_true',
                        help='Only generate CDF, skip JSON')

    args = parser.parse_args()

    # Check if input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return

    # Parse bitstrings
    parser = BitStringParser()
    try:
        parsed_data = parser.parse_multiple_bitstrings(args.input_file)

        # Save as JSON if not cdf-only
        if not args.cdf_only:
            parser.save_as_json(parsed_data, args.output_json)

        # Generate CDF files directly if not json-only
        if not args.json_only:
            parser.generate_cdf_directly(parsed_data, args.output_cdf_dir)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
