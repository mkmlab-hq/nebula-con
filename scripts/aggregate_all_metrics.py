import json
import os

def safe_load(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}

if __name__ == "__main__":
    axes = safe_load("metrics/axes_run.json")
    retention = safe_load("metrics/retention_run.json")
    combined = {
        "axes": axes,
        "retention": retention
    }
    os.makedirs("metrics", exist_ok=True)
    with open("metrics/full_report.json", "w") as f:
        json.dump(combined, f, indent=2)
    print("full_report.json written") 