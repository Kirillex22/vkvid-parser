import os
import json
from contextlib import contextmanager
from typing import Union, Dict

from playwright.sync_api import sync_playwright

DATA_DIR = os.path.join(os.getcwd(), "src", "data")
CONFIG_PATH = os.path.join(DATA_DIR, "config")
PROFILE_PATH = os.path.join(os.getcwd(), DATA_DIR, "vk_playwright_profile")
MAPPING_FILE = os.path.join(DATA_DIR, "mapping.json")

PAGE_LOADING_TIMEOUT_MS = None
DOWNLOAD_PATH = None


def load_configuration():
    global DOWNLOAD_PATH, PAGE_LOADING_TIMEOUT_MS

    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config: Dict[str, Union[str, int]] = json.load(f)

        path, timeout = str(config.get("download_path", "")), str(config.get("page_load_timeout", ""))

        if len(path) <= 0 or not os.path.exists(path):
            DOWNLOAD_PATH = os.getcwd()

        else:
            DOWNLOAD_PATH = path

        if timeout.isdigit():
            PAGE_LOADING_TIMEOUT_MS = int(timeout)

        else:
            PAGE_LOADING_TIMEOUT_MS = 4000


@contextmanager
def browser_provider(gui: bool):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_PATH,
            headless= not gui,
            user_agent="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"
        )
        try:
            yield browser
        finally:
            browser.close()


def set_download_path(path: str) -> bool:
    global DOWNLOAD_PATH
    if os.path.exists(path):
        DOWNLOAD_PATH = path

        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
            config["download_path"] = DOWNLOAD_PATH
            config["download_path"] = os.path.normpath(config["download_path"])

        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            f.write(json.dumps(config, indent=2))

        return True

    return False


def set_page_load_timeout(timeout: str) -> bool:
    global PAGE_LOADING_TIMEOUT_MS

    if timeout.isdigit():
        PAGE_LOADING_TIMEOUT_MS = int(timeout)

        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
            config["page_load_timeout"] = PAGE_LOADING_TIMEOUT_MS

        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            f.write(json.dumps(config, indent=2))

        return True

    return False