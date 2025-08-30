from typing import List

from src.models import StaticVideoSource


def map_vk_video_link_to_static_video_source(title: str, file_type: str, link: str) -> StaticVideoSource:
    if "mp4_" in file_type:
        quality = file_type.split("_")[1]
        file_type = file_type.split("_")[0]

    else:
        quality = None
        file_type = file_type

    args_splitted: List[str] = link.split('&')

    expires = None

    for arg in args_splitted:
        if "expires=" in arg:
            expires = int(arg.replace("expires=", ""))/1000
            break

    return StaticVideoSource(
        title = title,
        file_type=file_type,
        quality=quality,
        link=link,
        link_expires=expires,
    )