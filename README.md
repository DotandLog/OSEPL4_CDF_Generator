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

#### 基本用法

```bash
# 解析 bitstrings 並輸出為 JSON（預設格式）
python src/parser.py input/l1_cdf_data.txt

# 解析 bitstrings 並輸出為 HDF5 格式
python src/parser.py input/l1_cdf_data.txt --output-format hdf5

# 指定自訂輸出檔案名稱
python src/parser.py input/l1_cdf_data.txt --output-file my_parsed_data.json

# 直接生成 CDF 檔案
python src/direct_cdf_generator.py input/l1_cdf_data.txt --output-cdf-dir input/l1/cdf_files

# 同時生成 JSON 與 CDF 檔案
python src/direct_cdf_generator.py input/l1_cdf_data.txt --output-json input/l1_data.json --output-cdf-dir input/l1/cdf_files

# 只生成 CDF 檔案，跳過 JSON
python src/direct_cdf_generator.py input/l1_cdf_data.txt --cdf-only
```

#### 參數說明

- `input_file`: 輸入檔案路徑（必要參數）
  - 包含 hex bitstrings 的文字檔案
- `--output-format`: 輸出格式（選填）
  - 可選值：`json`（預設）或 `hdf5`
- `--output-file`: 輸出檔案名稱（選填）
  - 若未指定，將使用輸入檔案名稱並更改副檔名
- `--output-json`: JSON 輸出檔案路徑
- `--output-cdf-dir`: CDF 輸出目錄
- `--json-only`: 只生成 JSON 檔案
- `--cdf-only`: 只生成 CDF 檔案

#### 輸入檔案格式

輸入檔案應為純文字檔案，包含多個 bitstring 區塊，格式如下：

```
Bitstring 1:
0123456789ABCDEF...

Bitstring 2:
FEDCBA9876543210...
```

每個 bitstring 區塊應以 "Bitstring X:" 開頭，後面跟著十六進制字串。

#### 輸出檔案格式

1. **JSON 格式**：

   - 預設輸出格式
   - 適合人類閱讀和除錯
   - 檔案較大，讀寫速度較慢

2. **HDF5 格式**：

   - 二進制格式，檔案較小
   - 讀寫速度快
   - 適合處理大量數據
   - 需要安裝 `h5py` 套件

3. **CDF 格式**：
   - 直接生成 CDF 檔案
   - 符合 OSEPL4 規格
   - 支援 SPEDAS 和 NASA CDF Viewer 等工具
   - 需要安裝 `spacepy` 套件

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

### Features

- Parses OSEPL4 hex bitstrings to extract payload data
- Saves parsed data in JSON or HDF5 format for further analysis
- Generates CDF files directly with the exact structure defined in the OSEPL4 specification
- Cross-platform file path support (Windows, macOS, Linux)
- Handles multiple bitstrings in a single input file

### Requirements

- Python 3.6+
- NumPy
- SpacePy (for CDF generation)

#### Installing SpacePy

SpacePy requires the NASA CDF library to be installed on your system:

```bash
# Install SpacePy using pip
pip install spacepy

# For detailed installation instructions for the NASA CDF library, visit:
# https://spacepy.github.io/install.html
```

### Usage

#### 基本用法

```bash
# 解析 bitstrings 並輸出為 JSON（預設格式）
python src/parser.py input/l1_cdf_data.txt

# 解析 bitstrings 並輸出為 HDF5 格式
python src/parser.py input/l1_cdf_data.txt --output-format hdf5

# 指定自訂輸出檔案名稱
python src/parser.py input/l1_cdf_data.txt --output-file my_parsed_data.json

# 直接生成 CDF 檔案
python src/direct_cdf_generator.py input/l1_cdf_data.txt --output-cdf-dir output/cdf_files

# 同時生成 JSON 與 CDF 檔案
python src/direct_cdf_generator.py input/l1_cdf_data.txt --output-json output/parsed_data.json --output-cdf-dir output/cdf_files

# 只生成 CDF 檔案，跳過 JSON
python src/direct_cdf_generator.py input/l1_cdf_data.txt --cdf-only
```

#### 參數說明

- `input_file`: 輸入檔案路徑（必要參數）
  - 包含 hex bitstrings 的文字檔案
- `--output-format`: 輸出格式（選填）
  - 可選值：`json`（預設）或 `hdf5`
- `--output-file`: 輸出檔案名稱（選填）
  - 若未指定，將使用輸入檔案名稱並更改副檔名
- `--output-json`: JSON 輸出檔案路徑（適用於 direct_cdf_generator.py）
- `--output-cdf-dir`: CDF 輸出目錄（適用於 direct_cdf_generator.py）
- `--json-only`: 只生成 JSON 檔案（適用於 direct_cdf_generator.py）
- `--cdf-only`: 只生成 CDF 檔案（適用於 direct_cdf_generator.py）

#### 輸入檔案格式

輸入檔案應為純文字檔案，包含多個 bitstring 區塊，格式如下：

```text
Bitstring 1:
0123456789ABCDEF...

Bitstring 2:
FEDCBA9876543210...
```

每個 bitstring 區塊應以 "Bitstring X:" 開頭，後面跟著十六進制字串。

#### 輸出檔案格式

1. **JSON 格式**：

   - 預設輸出格式
   - 適合人類閱讀和除錯
   - 檔案較大，讀寫速度較慢

2. **HDF5 格式**：

   - 二進制格式，檔案較小
   - 讀寫速度快
   - 適合處理大量數據
   - 需要安裝 `h5py` 套件

3. **CDF 格式**：
   - 專為科學數據設計的格式
   - 符合 OSEPL4 規格
   - 可直接用於科學分析軟體
   - 需要安裝 `spacepy` 套件

### CDF File Structure

The CDF files are generated according to the exact specification from the OSEPL4 definition:

#### Global Attributes

| Name                       | Value                                                                                       |
| -------------------------- | ------------------------------------------------------------------------------------------- |
| Project                    | A-ESA science payload                                                                       |
| Discipline                 | lunar surface plasma environment                                                            |
| Data_type                  | L1 > Level 1 uncalibrated count data                                                        |
| Descriptor                 | A-ESA                                                                                       |
| File_naming_convention     | source_datatype_descriptor                                                                  |
| Data_version               | V01                                                                                         |
| PI_name                    | Lin, Shin-Fa / Chang, Tzu-Fang                                                              |
| PI_affiliation             | TASA / NCKU                                                                                 |
| TEXT                       | All-Sky Electrostatic Analyze (10eV ~ 10KeV)                                                |
| Instrument_type            | Particles (space)                                                                           |
| Logical_source             | AESA_L1                                                                                     |
| Logical_file_id            | AESA_L1_yyyymmdd_v01                                                                        |
| Logical_source_description | Level 1 uncalibrated count data for 10eV ~ 10KeV electron distribution on the lunar surface |
| Time_resolution            | Cycle period ~ 80 s                                                                         |
| Rules_of_use               | TBD                                                                                         |
| Generated_by               | TASA / NCKU                                                                                 |
| Generation_date            | yyyy-mm-dd                                                                                  |
| Acknowledgement            | TBD                                                                                         |
| LINK_TEXT                  | TBD                                                                                         |
| LINK_TITLE                 | TBD                                                                                         |

#### Variables

The CDF variable definitions match the specification exactly:

| Data Variable name    | Description                              | Array Size                                               | Remarks       |
| --------------------- | ---------------------------------------- | -------------------------------------------------------- | ------------- |
| EPOCH                 | Time Label for each cycle                | 1 X 45 (cycle period ~ 80 s)                             | TT2000 format |
| Electron_Count        | Electron counts, uncalibrated            | 16(energy) X 7(azimuthal) X 6(incident) X 45(cycle)      | integer       |
| BG_Count              | Count Data for background                | 16(energy) X 7(times) X 6(incident) X 45(cycle)          | integer       |
| Measure_Energy        | Sweeping Energy Value                    | 16(energy step) X 45(cycle)                              | float         |
| Output_HV             | HV output of 3 electrode                 | 3(electrode) X 16(energy step) X 6(incident) X 45(cycle) | float         |
| Datataking_Time_Start | Time start of each data                  | 1(record) X 45(cycle)                                    | TT2000 format |
| Data_Time_Duration    | Time duration of each data taking states | 1(record) X 45(cycle)                                    | float         |
| Data_Quality          | Data Quality flag                        | 16(energy) X 7(azimuthal) X 6(incident) X 45(cycle)      | unsigned byte |

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

```bash
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

### Cross-Platform Compatibility

This tool is designed to work across all major operating systems:

- Windows
- macOS
- Linux

The code uses Python's `pathlib` module to handle file paths in a platform-independent manner. This means:

1. File paths are automatically handled correctly regardless of the operating system
2. Forward slashes (`/`) or backslashes (`\`) in paths are automatically converted to the appropriate format
3. Directory separators and path manipulations work consistently

Additionally, the tool automatically creates any necessary parent directories when saving output files, making it easier to use across different environments.

```bash
# Example paths that will work on any platform:
python src/parser.py data/input.txt --output-file results/output.json
python src/direct_cdf_generator.py data/input.txt --output-cdf-dir cdf_output
```

## Convert L1 to L2 - CDF Generator

This Python script processes Level-1 scientific telemetry data (in `.json` or `.h5` format) and converts it into Level-2 Common Data Format (`.cdf`) files. The output includes total and mean electron counts per energy channel, as well as time-related metadata per data cycle.

---

### Usage

```bash
python cvt_l1tol2.py  --input_file "../input/l1_cdf_data.json" --output_dir "../output"
python cvt_l1tol2.py  --input_file "../input/l1_cdf_data.json" --output_dir "../output" --separate_files
```

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
