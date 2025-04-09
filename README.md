# OSEPL4 CDF Generator

## Installation

- **Python Version:** 3.12.9 or higher

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
      "global_attributes": {
        "Project": "A-ESA science payload",
        "Discipline": "lunar surface plasma environment",
        "Data_type": "L1 > Level 1 calibrated count data",
        "Descriptor": "A-ESA",
        "File_naming_convention": "source_datatype_descriptor",
        "Data_version": "V01",
        "PI_name": "Lin, Hsin-Fa / Chang, Tzu-Fang",
        "PI_affiliation": "TASA / NCKU",
        "TEXT": "All-Sky Electrostatic Analyze (10eV ~ 10KeV)",
        "Instrument_type": "Particles (space)",
        "Logical_source": "Aesa_L1",
        "Logical_file_id": "Aesa_L1_20250409_v01",
        "Logical_source_description": "Level 1 data for 10eV ~ 10KeV electron distribution on the lunar surface",
        "Time_resolution": "Cycle period ~ 80 s",
        "Rules_of_use": "TBD",
        "Generated_by": "TASA / NCKU",
        "Generation_date": "2025-04-09",
        "Acknowledgement": "TBD",
        "LINK_TEXT": "TBD",
        "LINK_TITLE": "TBD"
      },
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
  - global_attributes: L1 CDF global attributes
    - Contains all the metadata for the CDF file as specified in the OSEPL4 specification
    - Includes project details, data descriptions, PI information, etc.
  - **epochs**: Time labels for each cycle (45 cycles, ~80s each)
    - **cycle**: Cycle index (0-44)
    - **timestamp_ms**: Unix timestamp in milliseconds
    - **iso_format**: ISO 8601 formatted timestamp
  - **electron_counts**: Electron count data (6×7×16×45 array)
    - **incident_idx**: Incident angle index (0-5)
    - **azimuthal_idx**: Azimuthal angle index (0-6)
    - **energy_idx**: Energy step index (0-15)
    - **cycle**: Cycle index (0-44)
    - **count**: Electron count value (100-1000)
  - **bg_counts**: Background count data (same structure as electron_counts)
    - **incident_idx**: Incident angle index (0-5)
    - **azimuthal_idx**: Azimuthal angle index (0-6)
    - **energy_idx**: Energy step index (0-15)
    - **cycle**: Cycle index (0-44)
    - **count**: Background count value (0-100)
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
/
  /global_attributes/  # CDF global attributes stored as HDF5 attributes
/bitstring_1/
  @Project  # Global attributes stored as HDF5 attributes
  @Discipline
  @Data_type
  # ... other global attributes
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

The data is organized in the following order:

- **Incident angles**: 6 angles (0°, 15°, 30°, 45°, 60°, 75°, 90°)
- **Azimuthal angles**: 7 angles
- **Energy steps**: 16 steps (100eV to 7000eV)
- **Cycles**: 45 cycles (~80 seconds each)
  Additional dimensions:
- **Electrodes**: 3 (upper, middle, lower)

### Value Ranges

- **Electron counts**: 100-1000 counts
- **Background counts**: 0-100 counts

### Output HV Electrode Values

The voltage values for the three electrodes follow this pattern:

| Energy (eV) | Upper Electrode (V) | Middle Electrode (V) | Lower Electrode (V) |
| ----------- | ------------------- | -------------------- | ------------------- |
| 100         | 0                   | 46                   | 16                  |
| 200         | 0                   | 92                   | 32                  |
| 300         | 0                   | 138                  | 48                  |
| ...         | ...                 | ...                  | ...                 |
| 7000        | 0                   | 3220                 | 1120                |

## Convert L1 to L2 - CDF Generator

This Python script processes Level-1 scientific telemetry data (in `.json` or `.h5` format) and converts it into Level-2 Common Data Format (`.cdf`) files. The output includes total and mean electron counts per energy channel, as well as time-related metadata per data cycle.

---

### Input File Formats

The script supports:

- **JSON** files generated by the `parser.py` script
- **HDF5** files containing decoded electron count arrays

The JSON input must include at least:

<pre class="overflow-visible!" data-start="627" data-end="780"><div class="contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative bg-token-sidebar-surface-primary"><div class="flex items-center text-token-text-secondary px-4 py-2 text-xs font-sans justify-between h-9 bg-token-sidebar-surface-primary dark:bg-token-main-surface-secondary select-none rounded-t-[5px]">json</div><div class="sticky top-9"><div class="absolute right-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-sidebar-surface-primary text-token-text-secondary dark:bg-token-main-surface-secondary flex items-center rounded-sm px-2 font-sans text-xs"><span class="" data-state="closed"><button class="flex gap-1 items-center select-none px-4 py-1" aria-label="複製"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-xs"><path fill-rule="evenodd" clip-rule="evenodd" d="M7 5C7 3.34315 8.34315 2 10 2H19C20.6569 2 22 3.34315 22 5V14C22 15.6569 20.6569 17 19 17H17V19C17 20.6569 15.6569 22 14 22H5C3.34315 22 2 20.6569 2 19V10C2 8.34315 3.34315 7 5 7H7V5ZM9 7H14C15.6569 7 17 8.34315 17 10V15H19C19.5523 15 20 14.5523 20 14V5C20 4.44772 19.5523 4 19 4H10C9.44772 4 9 4.44772 9 5V7ZM5 9C4.44772 9 4 9.44772 4 10V19C4 19.5523 4.44772 20 5 20H14C14.5523 20 15 19.5523 15 19V10C15 9.44772 14.5523 9 14 9H5Z" fill="currentColor"></path></svg>複製</button></span><span class="" data-state="closed"><button class="flex items-center gap-1 px-4 py-1 select-none"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-xs"><path d="M2.5 5.5C4.3 5.2 5.2 4 5.5 2.5C5.8 4 6.7 5.2 8.5 5.5C6.7 5.8 5.8 7 5.5 8.5C5.2 7 4.3 5.8 2.5 5.5Z" fill="currentColor" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"></path><path d="M5.66282 16.5231L5.18413 19.3952C5.12203 19.7678 5.09098 19.9541 5.14876 20.0888C5.19933 20.2067 5.29328 20.3007 5.41118 20.3512C5.54589 20.409 5.73218 20.378 6.10476 20.3159L8.97693 19.8372C9.72813 19.712 10.1037 19.6494 10.4542 19.521C10.7652 19.407 11.0608 19.2549 11.3343 19.068C11.6425 18.8575 11.9118 18.5882 12.4503 18.0497L20 10.5C21.3807 9.11929 21.3807 6.88071 20 5.5C18.6193 4.11929 16.3807 4.11929 15 5.5L7.45026 13.0497C6.91175 13.5882 6.6425 13.8575 6.43197 14.1657C6.24513 14.4392 6.09299 14.7348 5.97903 15.0458C5.85062 15.3963 5.78802 15.7719 5.66282 16.5231Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path><path d="M14.5 7L18.5 11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>編輯</button></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-json"><span><span>{</span><span>
  </span><span>"bitstring_index"</span><span>:</span><span> </span><span>1</span><span>,</span><span>
  </span><span>"data"</span><span>:</span><span> </span><span>{</span><span>
    </span><span>"electron_counts"</span><span>:</span><span> </span><span>[</span><span>...</span><span>]</span><span>,</span><span>
    </span><span>"datataking_time_start"</span><span>:</span><span> </span><span>[</span><span>...</span><span>]</span><span>,</span><span>
    </span><span>"data_time_duration"</span><span>:</span><span> </span><span>[</span><span>...</span><span>]</span><span>
  </span><span>}</span><span>
</span><span>}</span><span>
</span></span></code></div></div></pre>

---

### 📤 Output: CDF Variables

Each `.cdf` output contains the following variables:

| Variable Name             | Shape         | Description                                               |
| ------------------------- | ------------- | --------------------------------------------------------- |
| `bitstring_index`         | `(N,)`        | Index of each bitstring block                             |
| `total_counts_per_energy` | `(N, 16, 45)` | Total electron counts per energy channel and cycle        |
| `mean_counts_per_energy`  | `(N, 16, 45)` | Mean electron counts per energy channel and cycle         |
| `epoch`                   | `(N, 45)`     | Start time of each cycle in milliseconds since 1970-01-01 |
| `duration`                | `(N, 45)`     | Duration of each cycle in seconds                         |

Each variable includes descriptive attributes (`UNITS`, `DESCRIPTION`) for compatibility with SPEDAS, NASA CDF Viewer, or other tools.

---

### 🛠️ Customization

- The `compute_moments()` function can be extended to compute advanced physical moments (e.g., density, flux).
- Timestamps can be converted to TT2000 or ISO format if needed.
- Additional metadata can be added to the `.cdf` file for better documentation and integration with visualization tools.
