import pandas as pd
import json
from pathlib import Path


INPUT_XLSX = fr"public\data\benchmark.xlsx"
OUTPUT_JSON = fr"public\data\leaderboards.json"

TASK_INFO = {
    "id": "cod",
    "name": "Camouflaged Object Detection"
}

# 数据集名称映射（Excel 列名 -> 标准名）
DATASET_NAME_MAP = {
    "CAMO": "CAMO",
    "CASIA": "CASIA",
    "CHAMELEON": "CHAMELEON",
    "COD10K": "COD10K",
    "COVERAGE": "COVERAGE",
    "GSD": "GSD",
    "ISTD": "ISTD",
    "MSD": "MSD",
    "NC4K": "NC4K",
    "PMD": "PMD",
    "SBU": "SBU",
    "Trans10K": "Trans10K"
}

# 当前表格只有一个指标
METRICS = ["Cmeasure"]

HIGHER_IS_BETTER = {
    "Cmeasure": True
}

# 模型额外信息（可选，不写就为 null）
MODEL_META = {
    "SINet": {
        "paper": "https://arxiv.org/abs/2004.09030",
        "code": "https://github.com/DengPingFan/SINet",
        "year": 2020
    },
    "SINet-V2": {
        "paper": "https://arxiv.org/abs/2108.00128",
        "code": "https://github.com/GewelsJI/SINet-V2",
        "year": 2021
    }
    # 其他模型可以继续补
}

# ======================
# 2. 读取 Excel
# ======================

df = pd.read_excel(INPUT_XLSX)

# 第一列是方法名
method_col = df.columns[0]
dataset_cols = df.columns[1:]

# ======================
# 3. 构建 JSON 结构
# ======================

datasets_json = []

for col in dataset_cols:
    dataset_id = col.lower()
    dataset_name = DATASET_NAME_MAP.get(col, col)

    models = []
    for _, row in df.iterrows():
        method_name = row[method_col]
        score = row[col]

        if pd.isna(score):
            continue

        meta = MODEL_META.get(method_name, {})

        models.append({
            "name": method_name,
            "paper": meta.get("paper"),
            "code": meta.get("code"),
            "year": meta.get("year"),
            "results": {
                "Cmeasure": round(float(score), 3)
            }
        })

    datasets_json.append({
        "id": dataset_id,
        "name": dataset_name,
        "metrics": METRICS,
        "higherIsBetter": HIGHER_IS_BETTER,
        "models": models
    })

final_json = {
    "tasks": [
        {
            "id": TASK_INFO["id"],
            "name": TASK_INFO["name"],
            "datasets": datasets_json
        }
    ]
}

# ======================
# 4. 保存 JSON
# ======================

Path(OUTPUT_JSON).write_text(
    json.dumps(final_json, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"Saved to {OUTPUT_JSON}")
