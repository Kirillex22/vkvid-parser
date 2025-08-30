import src
from typing import Tuple, Dict

def get_src_videos_from_vkvideo_page(browser, page_url: str) -> Tuple[str, Dict[str, str]]:
    page = browser.new_page()

    responses_data = []

    def handle_response(response):
        if "video.getVideoDiscover" in response.url:
            try:
                data = response.json()
                responses_data.append(data)
            except Exception as e:
                print(e)
                pass

    page.on("response", handle_response)

    page.goto(page_url)
    page.wait_for_timeout(src.PAGE_LOADING_TIMEOUT_MS)

    if responses_data:
        title = page.locator('[class="vkitTextClamp__root--8Ttiw vkitgetColorClass__colorTextPrimary--AX4Wt vkuiTitle__sizeYCompact vkuiTitle__level3 vkuiTypography__host vkuiTypography__normalize vkuiRootComponent__host"]').text_content(timeout=10000)

        result = responses_data[0]["response"]["current_video"]["files"]
        result.pop("failover_host")

        return title, result