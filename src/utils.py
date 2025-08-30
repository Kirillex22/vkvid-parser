import json
import os
import uuid
from dataclasses import asdict
from typing import Dict, Any, List, Tuple
from xml.etree.ElementTree import indent

from src import MAPPING_FILE, DATA_DIR
from src.models import StaticVideoSource


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, "w", encoding="utf-8") as f:
            f.write(json.dumps({}, ensure_ascii=False))


def dump_static_video_source(src: StaticVideoSource) -> None:
    _id = str(uuid.uuid4())

    with open(MAPPING_FILE, 'r', encoding='utf-8') as file:
        current_mapping: Dict[str, Any] = json.load(file)

    with open(MAPPING_FILE, 'w', encoding='utf-8') as file:
        current_mapping[_id] = (asdict(src))
        file.write(json.dumps(current_mapping, ensure_ascii=False, indent=4))


def load_static_video_source(_id: str = None) -> StaticVideoSource | List[Tuple[str | StaticVideoSource]]:
    with open(MAPPING_FILE, 'r', encoding='utf-8') as file:
        current_mapping: Dict[str, Any] = json.load(file)

        if _id is None:
            return [(__id, StaticVideoSource(**current_mapping[__id])) for __id in current_mapping]

        return StaticVideoSource(**current_mapping[_id])