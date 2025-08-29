import re
import subprocess
from tqdm import tqdm

from src.models import StaticVideoSource



def download_video_from_static_video_source(src: StaticVideoSource, output_path: str) -> None:
    """
    Скачивает видео с помощью ffmpeg и отображает прогресс через tqdm.
    """
    if src.is_expired():
        raise RuntimeError("Срок действия ссылки истек")

    filename = output_path + f'/{src.title}.{src.file_type}'

    # Узнаём длительность ролика
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", src.link],
        capture_output=True, text=True
    )
    total_duration = float(probe.stdout.strip()) if probe.returncode == 0 else None

    # Запуск ffmpeg
    process = subprocess.Popen(
        ["ffmpeg", "-y", "-i", src.link, "-c", "copy", filename, "-progress", "pipe:2", "-nostats"],
        stderr=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1
    )

    pbar = tqdm(total=total_duration, unit="sec", desc="Downloading", dynamic_ncols=True)
    duration_pattern = re.compile(r"out_time_ms=(\d+)")

    ffmpeg_log = []

    for line in process.stderr:
        ffmpeg_log.append(line.strip())  # сохраняем лог ffmpeg
        match = duration_pattern.search(line)
        if match and total_duration:
            current_time = int(match.group(1)) / 1_000_000
            pbar.n = min(current_time, total_duration)
            pbar.refresh()

    process.wait()
    pbar.close()

    if process.returncode != 0:
        print("\n=== FFmpeg log ===")
        print("\n".join(ffmpeg_log[-20:]))  # последние 20 строк
        raise RuntimeError("Ошибка при скачивании видео через ffmpeg")

    print(f"✅ Видео сохранено в {filename}")