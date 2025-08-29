import os
from contextlib import contextmanager

from playwright.sync_api import sync_playwright

DATA_DIR = os.path.join(os.getcwd(), "src", "data")
PROFILE_PATH = os.path.join(os.getcwd(), DATA_DIR, "vk_playwright_profile")
MAPPING_FILE = os.path.join(DATA_DIR, "mapping.json")
DOWNLOAD_PATH = None

with open(os.path.join(DATA_DIR, "download_path"), 'r', encoding='utf-8') as f:
    path = f.read()
    if len(path) <= 0 or not os.path.exists(path):
        DOWNLOAD_PATH = os.getcwd()

    else:
        DOWNLOAD_PATH = path


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
        with open("data/download_path", 'w', encoding='utf-8') as f:
            f.write(path)

        return True

    return False