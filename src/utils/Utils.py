from pathlib import Path
import json

def write_data_to_file(path_of_file, data):
    path: Path = Path(path_of_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")