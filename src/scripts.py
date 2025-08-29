import os

from src import PROFILE_PATH


def vk_login(browser):
    os.makedirs(PROFILE_PATH, exist_ok=True)
    url = "https://vk.com/"
    page = browser.new_page()
    page.goto(url)
    print("Залогиньтесь вручную в открывшемся браузере.")
    input("Нажмите Enter после того, как залогинились и закрыли браузер...")
    browser.close()

