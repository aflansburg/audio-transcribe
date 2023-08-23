"""Main script for running the transcription process."""
import sys

from lib.convert import convert_mp3_to_wav
from lib.compress import downsample_compress
from lib.transcribe import transcribe_audio


if __name__ == "__main__":
    print("Let's transcribe some audio.")

    # Convert, compress, & transcribe sample session mp3

    wav = convert_mp3_to_wav(
        audio_file="resources/input/sample_therapy_audio.mp3"
    )

    if not wav:
        print("Error converting file to WAV format.")
        sys.exit(1)

    compressed_wav = downsample_compress(wav)

    if not compressed_wav:
        print("Error compressing WAV file.")
        sys.exit(1)

    transcription = transcribe_audio(
        audio_file=compressed_wav
    )

    if not transcription:
        print("Error transcribing WAV file.")
        sys.exit(1)

    print(f"Transcription:\n{transcription}")
