"""Audio format conversion functions."""
from pydub import AudioSegment

BITRATE = "22k"
CODEC = "pcm_s16le"


def convert_mp3_to_wav(
    audio_file: str,
) -> str or bool:
    """Convert an audio file to WAV format."""
    print("Converting to WAV format...")

    try:
        out_file = audio_file.replace("input", "output").replace(".mp3", ".wav")

        audio = AudioSegment.from_mp3(audio_file)
        audio.export(out_file, format="wav", codec=CODEC, bitrate=BITRATE)
        print(f"Converted {audio_file} to {out_file}.")

        return out_file
    except Exception as err:
        print(f"Error: {err}")
        return False
