from src.models import StaticVideoSource


def map_vk_video_link_to_static_video_source(title: str, file_type: str, link: str) -> StaticVideoSource:
    if "mp4_" in file_type:
        quality = file_type.split("_")[1]
        file_type = file_type.split("_")[0]

    else:
        quality = None
        file_type = file_type

    expires = int(link.split('&')[2].replace("expires=", ""))/1000

    return StaticVideoSource(
        title = title,
        file_type=file_type,
        quality=quality,
        link=link,
        link_expires=expires,
    )