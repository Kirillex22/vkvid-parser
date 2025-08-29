import json
import os
import uuid
from dataclasses import asdict
from typing import Dict


from src import MAPPING_FILE, DATA_DIR
from src.models import StaticVideoSource


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, "w", encoding="utf-8") as f:
            f.write(json.dumps({}, ensure_ascii=False))


def dump_static_video_source(src: StaticVideoSource) -> None:
    mapping: Dict[str, str] = {}

    _id = str(uuid.uuid4())

    with open(f"{DATA_DIR}/{_id}.json", 'w', encoding='utf-8') as file:
        file.write(json.dumps(asdict(src), ensure_ascii=False))
        mapping[_id] = src.title

    with open(MAPPING_FILE, 'r', encoding='utf-8') as file:
        current_mapping: Dict[str, str] = json.load(file)

    with open(MAPPING_FILE, 'w', encoding='utf-8') as file:
        current_mapping.update(mapping)
        file.write(json.dumps(current_mapping, ensure_ascii=False))


def load_static_video_source(_id: str) -> StaticVideoSource:
    with open(f"{DATA_DIR}/{_id}.json", 'r', encoding='utf-8') as file:
        return StaticVideoSource(**json.load(file))