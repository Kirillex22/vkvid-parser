import os
from contextlib import contextmanager

from playwright.sync_api import sync_playwright

PROFILE_PATH = f"{os.getcwd()}\\data\\vk_playwright_profile"
DATA_DIR = "data"
MAPPING_FILE = os.path.join(DATA_DIR, "mapping.json")

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
