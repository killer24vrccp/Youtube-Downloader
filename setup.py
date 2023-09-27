import sys
from cx_Freeze import setup, Executable

# Répertoire FFmpeg à inclure
ffmpeg_dir = r"C:\Program Files\ffmpeg-6.0"

build_exe_options = {
    "packages": [
        "os",
        "PyQt5",
        "pytube",
        "moviepy",
        "moviepy.video.io.ffmpeg_tools",
    ],
    "include_files": [
        ("youtube_logo.png", "youtube_logo.png"),
        # Inclure le répertoire FFmpeg
        (ffmpeg_dir, "ffmpeg-6.0"),
    ],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Utilisez "Win32GUI" pour une application Windows sans console

executables = [
    Executable("Youtube_Downloader.py", base=base, icon="youtube_logo.png")
]

setup(
    name="YoutubeDownloader",
    version="1.0",
    description="YouTube MP3 Downloader",
    options={"build_exe": build_exe_options},
    executables=executables,
)
