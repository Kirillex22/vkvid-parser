import os
import json
import src as config
from typing import Dict

from src import MAPPING_FILE, browser_provider, PROFILE_PATH, set_download_path
from src.mappers import map_vk_video_link_to_static_video_source
from src.parsers import get_src_videos_from_vkvideo_page
from src.scripts import vk_login
from src.utils import dump_static_video_source, load_static_video_source, ensure_data_dir
from src.video_loaders import download_video_from_static_video_source


def main():
    config.load_configuration()
    ensure_data_dir()

    if not os.path.exists(PROFILE_PATH):
        with browser_provider(True) as browser:
            vk_login(browser)

    with browser_provider(False) as browser:
        while True:
            input('Нажмите ENTER, чтобы продолжить...')
            os.system('cls' if os.name == 'nt' else 'clear')

            print(f"\n=== VK Video Parser ===")
            print("1. Вставить ссылку и скачать видео")
            print("2. Посмотреть все дампнутые ролики в формате ID: Название")
            print("3. Скачать ролик по ID")
            print(f"4. Указать папку для скачивания (текущая: {config.DOWNLOAD_PATH})")
            print(f"5. Указать таймаут загрузки страницы с роликом (текущий: {config.PAGE_LOADING_TIMEOUT_MS} мс)")
            print("0. Выход")
            choice = input("👉 Выберите действие: ")

            if choice == "1":
                url = input("Введите ссылку на видео: ").strip()
                try:
                    title, files = get_src_videos_from_vkvideo_page(browser, url)
                    print(f"\nНайдено видео: {title}")
                    print("Доступные качества:")
                    for i, (ftype, link) in enumerate(files.items(), start=1):
                        print(f"{i}. {ftype}")

                    sel = int(input("Выберите качество: "))
                    ftype, link = list(files.items())[sel - 1]

                    src = map_vk_video_link_to_static_video_source(title, ftype, link)
                    dump_static_video_source(src)
                    print(f"\nВидео дампнуто! ID: сохранено в mapping.json")

                    if input("Скачать сейчас? (y/n): ").lower() == "y":
                        download_video_from_static_video_source(src)

                except Exception as e:
                    print(f"❌ Ошибка: {e}")


            elif choice == "2":
                with open(MAPPING_FILE, "r", encoding="utf-8") as f:
                    mapping: Dict[str, str] = json.load(f)
                if not mapping:
                    print("Пока ничего не дампнуто.")
                else:
                    print("\nДампнутые ролики:")
                    for _id, title in mapping.items():
                        print(f"{_id} → {title}")

            elif choice == "3":
                vid = input("Введите ID ролика: ").strip()
                try:
                    src = load_static_video_source(vid)
                    print(f"Выбран ролик: {src.title}")
                    download_video_from_static_video_source(src)
                except Exception as e:
                    print(f"❌ Ошибка: {e}")

            elif choice == "4":
                path = input("Введите адрес папки: ")
                try:
                    if set_download_path(path):
                        print("Успешно установлена новая папка.")
                    else:
                        print("Папка не найдена.")
                except Exception as e:
                    print(f"❌ Ошибка: {e}")

            elif choice == "5":
                try:
                    timeout = input("Введите время в миллисекундах: ")
                    if config.set_page_load_timeout(timeout):
                        print("Успешно установлен новый таймаут.")

                    else:
                        print("Неверный формат числа.")

                except Exception as e:
                    print(f"❌ Ошибка: {e}")

            elif choice == "0":
                print("👋 Выход")
                break
            else:
                print("Неверный выбор!")


if __name__ == "__main__":
    main()
