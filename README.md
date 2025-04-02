# OSEPL4 CDF Generator
## Installation
- **Python Version:**  3.12.9 or higher
```bash
# Clone the repository
git clone https://github.com/yourusername/osepl4-parser.git

# Install dependencies
pip install -r requirements.txt
```
## OSEPL4 Bitstring Parser
This tool parses hex bitstrings generated for the OSEPL4 project and converts them into structured data formats for further processing and analysis. The tool supports both JSON and HDF5 output formats, which can later be used to generate CDF (Common Data Format) files for scientific analysis.

### Usage

#### Parsing Bitstrings

```bash
# Parse bitstrings and output as JSON (default)
python src/parser.py input/l1_cdf_data.txt

# Parse bitstrings and output as HDF5
python src/parser.py l1_cdf_data.txt --output-format hdf5

# Specify custom output file
python parser.py l1_cdf_data.txt --output-file my_parsed_data.json
```

### Output JSON Structure

The parser outputs a JSON file with the following structure:

```json
[
  {
    "bitstring_index": 1,
    "data": {
      "epochs": [
        {
          "cycle": 0,
          "timestamp_ms": 1712180634000,
          "iso_format": "2025-04-02T21:10:34"
        },
        ...
      ],
      "electron_counts": [
        {
          "energy_idx": 0,
          "azimuthal_idx": 0,
          "incident_idx": 0,
          "cycle": 0,
          "count": 327
        },
        ...
      ],
      "bg_counts": [
        {
          "energy_idx": 0,
          "azimuthal_idx": 0,
          "incident_idx": 0,
          "cycle": 0,
          "count": 241
        },
        ...
      ],
      "measure_energy": [
        {
          "energy_idx": 0,
          "cycle": 0,
          "energy_value": 100.0
        },
        ...
      ],
      "output_hv": [
        {
          "electrode": "upper",
          "electrode_idx": 0,
          "energy_idx": 0,
          "incident_idx": 0,
          "cycle": 0,
          "voltage": 0.0
        },
        {
          "electrode": "middle",
          "electrode_idx": 1,
          "energy_idx": 0,
          "incident_idx": 0,
          "cycle": 0,
          "voltage": 46.0
        },
        {
          "electrode": "lower",
          "electrode_idx": 2,
          "energy_idx": 0,
          "incident_idx": 0,
          "cycle": 0,
          "voltage": 16.0
        },
        ...
      ],
      "datataking_time_start": [
        {
          "cycle": 0,
          "timestamp_ms": 1712180634000,
          "iso_format": "2025-04-02T21:10:34"
        },
        ...
      ],
      "data_time_duration": [
        {
          "cycle": 0,
          "duration_seconds": 72.3
        },
        ...
      ],
      "data_quality": [
        {
          "energy_idx": 0,
          "azimuthal_idx": 0,
          "incident_idx": 0,
          "cycle": 0,
          "quality": 0
        },
        ...
      ]
    }
  },
  {
    "bitstring_index": 2,
    "data": {
      // Similar structure for another bitstring
    }
  },
  ...
]
```

#### Description of JSON Fields

- **bitstring_index**: Index of the bitstring (starting from 1)
- **data**: Contains all the structured data for this bitstring
  - **epochs**: Time labels for each cycle (45 cycles, ~80s each)
    - **cycle**: Cycle index (0-44)
    - **timestamp_ms**: Unix timestamp in milliseconds
    - **iso_format**: ISO 8601 formatted timestamp
  - **electron_counts**: Electron count data (16×7×6×45 array)
    - **energy_idx**: Energy step index (0-15)
    - **azimuthal_idx**: Azimuthal angle index (0-6)
    - **incident_idx**: Incident angle index (0-5)
    - **cycle**: Cycle index (0-44)
    - **count**: Electron count value (0-1000)
  - **bg_counts**: Background count data (same structure as electron_counts)
  - **measure_energy**: Energy values for each energy step
    - **energy_idx**: Energy step index (0-15)
    - **cycle**: Cycle index (0-44)
    - **energy_value**: Energy value in eV
  - **output_hv**: High voltage output values
    - **electrode**: Electrode name ("upper", "middle", "lower")
    - **electrode_idx**: Electrode index (0-2)
    - **energy_idx**: Energy step index (0-15)
    - **incident_idx**: Incident angle index (0-5)
    - **cycle**: Cycle index (0-44)
    - **voltage**: Voltage value in V
  - **datataking_time_start**: Start time for each data taking cycle
    - **cycle**: Cycle index (0-44)
    - **timestamp_ms**: Unix timestamp in milliseconds
    - **iso_format**: ISO 8601 formatted timestamp
  - **data_time_duration**: Duration of each data taking cycle
    - **cycle**: Cycle index (0-44)
    - **duration_seconds**: Duration in seconds
  - **data_quality**: Quality flags for data
    - **energy_idx**: Energy step index (0-15)
    - **azimuthal_idx**: Azimuthal angle index (0-6)
    - **incident_idx**: Incident angle index (0-5)
    - **cycle**: Cycle index (0-44)
    - **quality**: Quality flag (0=good, others=issues)

### HDF5 Output Structure

If you choose HDF5 as the output format, the data will be saved in a more efficient hierarchical structure:

```
/bitstring_1/
  /epochs/
    /timestamp_ms
    /iso_format
  /electron_counts
  /bg_counts
  /measure_energy
  /output_hv/
    /values
    @electrode_names
  /datataking_time_start/
    /timestamp_ms
    /iso_format
  /data_time_duration
  /data_quality
/bitstring_2/
  ...
```

### Data Dimensions

- **Energy steps**: 16 steps (100eV to 7000eV)
- **Azimuthal angles**: 7 angles
- **Incident angles**: 6 angles (0°, 15°, 30°, 45°, 60°, 75°, 90°)
- **Cycles**: 45 cycles (~80 seconds each)
- **Electrodes**: 3 (upper, middle, lower)

### Output HV Electrode Values

The voltage values for the three electrodes follow this pattern:

| Energy (eV) | Upper Electrode (V) | Middle Electrode (V) | Lower Electrode (V) |
|------------|---------------------|----------------------|---------------------|
| 100        | 0                   | 46                   | 16                  |
| 200        | 0                   | 92                   | 32                  |
| 300        | 0                   | 138                  | 48                  |
| ...        | ...                 | ...                  | ...                 |
| 7000       | 0                   | 3220                 | 1120                |

