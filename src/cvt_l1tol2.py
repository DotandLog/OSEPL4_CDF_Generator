import json
import numpy as np
import h5py
from pathlib import Path
from spacepy import pycdf
import datetime
import argparse

def compute_moments(electron_counts, bg_counts=None):
    # 定義效率校正因子
    efficiency_factors = np.array([
        1.010928962,  # CH1
        1.010928962,  # CH2
        1.027322404,  # CH3
        1.147540984,  # CH4
        1.005464481,  # CH5
        1.114754098,  # CH6
        1.043715847,  # CH7
    ])

    # 初始化觀測值和背景值陣列 (6, 7, 16, 45)
    counts_array = np.zeros((6, 7, 16, 45))
    bg_counts_array = np.zeros((6, 7, 16, 45))

    # 填充觀測值陣列
    for entry in electron_counts:
        i, a, e, c = entry["incident_idx"], entry["azimuthal_idx"], entry["energy_idx"], entry["cycle"]
        counts_array[i, a, e, c] = entry["count"]

    # 填充背景值陣列（若提供的話）
    if bg_counts is not None:
        for entry in bg_counts:
            i, a, e, c = entry["incident_idx"], entry["azimuthal_idx"], entry["energy_idx"], entry["cycle"]
            bg_counts_array[i, a, e, c] = entry["count"]

        # 扣除背景值
        corrected_data = counts_array - bg_counts_array
    else:
        corrected_data = counts_array

    # 應用效率校正（使用廣播將校正因子應用到第二個維度）
    corrected_data = corrected_data * efficiency_factors.reshape(1, 7, 1, 1)

    # 此處同時計算總計數與均值（此實作中二者一致，可根據需求分開）
    return corrected_data.tolist(), corrected_data.tolist()

def save_as_cdf(output_file, l2_data):
    output_file = str(output_file)  # 確保路徑為字串

    with pycdf.CDF(output_file, '') as cdf:
        # 提取基本數據
        indices = [d["bitstring_index"] for d in l2_data]
        totals = [d["total_counts_per_energy"] for d in l2_data]
        means = [d["mean_counts_per_energy"] for d in l2_data]
        epochs = [d["epochs"] for d in l2_data]
        durations = [d["durations"] for d in l2_data]
        # 將複雜資料轉換為 JSON 字串
        global_attributes = [json.dumps(d.get("global_attributes", {})) for d in l2_data]
        measure_energy = [json.dumps(d.get("measure_energy", [])) for d in l2_data]
        output_hv = [json.dumps(d.get("output_hv", [])) for d in l2_data]
        data_quality = [json.dumps(d.get("data_quality", [])) for d in l2_data]

        # 儲存各個欄位到 CDF
        cdf["global_attributes"] = global_attributes
        cdf["bitstring_index"] = indices
        cdf["total_counts_per_energy"] = totals
        cdf["mean_counts_per_energy"] = means
        cdf["epoch"] = epochs
        cdf["duration"] = durations
        cdf["measure_energy"] = measure_energy
        cdf["output_hv"] = output_hv
        cdf["data_quality"] = data_quality

        # 添加屬性說明
        cdf["epoch"].attrs["UNITS"] = "ms since 1970-01-01"
        cdf["epoch"].attrs["DESCRIPTION"] = "Start time of each data cycle in milliseconds"
        cdf["duration"].attrs["UNITS"] = "seconds"
        cdf["duration"].attrs["DESCRIPTION"] = "Duration of each data cycle"
        
    print(f"Level-2 CDF saved to {output_file}")

def save_single_bitstring_cdf(output_file, l2_data):
    output_file = str(output_file)

    with pycdf.CDF(output_file, '') as cdf:
        # 儲存單一 bitstring 的資料，將標量資料轉換為列表
        cdf["global_attributes"] = [json.dumps(l2_data["global_attributes"])]
        cdf["bitstring_index"] = [l2_data["bitstring_index"]]
        cdf["total_counts_per_energy"] = [l2_data["total_counts_per_energy"]]
        cdf["mean_counts_per_energy"] = [l2_data["mean_counts_per_energy"]]
        cdf["epoch"] = l2_data["epochs"]
        cdf["duration"] = l2_data["durations"]
        cdf["measure_energy"] = [json.dumps(l2_data["measure_energy"])]
        cdf["output_hv"] = [json.dumps(l2_data["output_hv"])]
        cdf["data_quality"] = [json.dumps(l2_data["data_quality"])]

        # 添加屬性說明
        cdf["epoch"].attrs["UNITS"] = "ms since 1970-01-01"
        cdf["epoch"].attrs["DESCRIPTION"] = "Start time of each data cycle in milliseconds"
        cdf["duration"].attrs["UNITS"] = "seconds"
        cdf["duration"].attrs["DESCRIPTION"] = "Duration of each data cycle"

    print(f"Single bitstring CDF saved to {output_file}")

def process_json_to_l2(input_path, output_path, separate_files=False):
    with open(input_path, 'r') as f:
        data = json.load(f)

    l2_results = []
    for bitstring in data:
        # 擷取新增的 metadata
        global_attrs = bitstring["data"].get("global_attributes", {})
        measure_energy = bitstring["data"].get("measure_energy", [])
        output_hv = bitstring["data"].get("output_hv", [])
        data_quality = bitstring["data"].get("data_quality", [])

        # 原始計數資料
        electron_counts = bitstring["data"]["electron_counts"]
        bg_counts = bitstring["data"].get("bg_counts", None)

        # 計算校正後的數據（總計數與均值，這裡回傳兩個相同的結果）
        total, mean = compute_moments(electron_counts, bg_counts)

        # 從 datataking_time_start 提取 timestamp_ms 當作 epoch
        epoch_list = [entry["timestamp_ms"] for entry in bitstring["data"].get("datataking_time_start", [])]
        # 從 data_time_duration 提取 duration_seconds 當作持續時間
        duration_list = [entry["duration_seconds"] for entry in bitstring["data"].get("data_time_duration", [])]

        l2_result = {
            "global_attributes": global_attrs,
            "bitstring_index": bitstring["bitstring_index"],
            "total_counts_per_energy": total,
            "mean_counts_per_energy": mean,
            "epochs": epoch_list,
            "durations": duration_list,
            # 儲存其他 metadata
            "measure_energy": measure_energy,
            "output_hv": output_hv,
            "data_quality": data_quality
        }
        
        if separate_files:
            # 為每個 bitstring 創建獨立的 CDF 檔案
            output_file = Path(output_path).parent / f"{Path(output_path).stem}_bitstring_{bitstring['bitstring_index']}.cdf"
            save_single_bitstring_cdf(output_file, l2_result)
        else:
            l2_results.append(l2_result)

    if not separate_files:
        save_as_cdf(output_path, l2_results)

def process_hdf5_to_l2(input_path, output_path, separate_files=False):
    l2_results = []
    with h5py.File(input_path, 'r') as f:
        for bitstring_key in f.keys():
            electron_counts = f[bitstring_key]["electron_counts"][:]
            index = int(bitstring_key.split('_')[-1])

            l2_result = {
                "global_attributes": {},
                "bitstring_index": index,
                "total_counts_per_energy": electron_counts.tolist(),
                "mean_counts_per_energy": electron_counts.tolist(),
                "epochs": [0] * 45,
                "durations": [0.0] * 45,
                "measure_energy": [],
                "output_hv": [],
                "data_quality": []
            }

            if separate_files:
                output_file = Path(output_path).parent / f"{Path(output_path).stem}_bitstring_{index}.cdf"
                save_single_bitstring_cdf(output_file, l2_result)
            else:
                l2_results.append(l2_result)

    if not separate_files:
        save_as_cdf(output_path, l2_results)

def convert_l1_to_l2(input_file, output_dir=None, separate_files=False):
    input_path = Path(input_file)
    
    # 如果沒有指定輸出目錄，則使用輸入檔案的目錄下的 output 資料夾
    if output_dir is None:
        output_dir = input_path.parent / "output"
    else:
        output_dir = Path(output_dir)
    
    # 確保輸出目錄存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 在指定目錄下建立輸出檔案路徑
    output_file = output_dir / f"{input_path.stem}_l2.cdf"

    if input_file.endswith(".json"):
        process_json_to_l2(input_path, output_file, separate_files)
    elif input_file.endswith(".h5"):
        process_hdf5_to_l2(input_path, output_file, separate_files)
    else:
        raise ValueError("不支援的檔案格式：必須是 .json 或 .h5")

def main():
    parser = argparse.ArgumentParser(description='將 Level-1 資料轉換為 Level-2 CDF 格式')
    parser.add_argument('--input_file', type=str, help='輸入檔案路徑 (.json 或 .h5)')
    parser.add_argument('--output_dir', type=str, help='輸出目錄路徑 (選填)')
    parser.add_argument('--separate_files', action='store_true', help='是否為每個 bitstring 建立獨立檔案')
    
    args = parser.parse_args()
    
    convert_l1_to_l2(
        input_file=args.input_file,
        output_dir=args.output_dir,
        separate_files=args.separate_files
    )

if __name__ == "__main__":
    main()

# 使用範例：
# 預設輸出到 input 目錄下的 output 資料夾
# convert_l1_to_l2("../input/l1_cdf_data.json", separate_files=True)
# 指定輸出目錄
# convert_l1_to_l2("../input/l1_cdf_data.json", output_dir="../output", separate_files=False)    
