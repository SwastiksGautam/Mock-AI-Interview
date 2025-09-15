from pydub.utils import which

if __name__ == "__main__":
    ffmpeg_path = which("ffmpeg")
    if ffmpeg_path:
        print(f"✅ FFmpeg is available at: {ffmpeg_path}")
    else:
        print("❌ FFmpeg is not found in your system PATH.")
