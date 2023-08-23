"""Transcribe audio file using Google Cloud Speech API."""
import os

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

G_PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


def transcribe_audio(
    audio_file: str,
) -> cloud_speech.RecognizeResponse or bool:
    """Transcribe an audio file."""
    try:
        # Instantiates a client
        client = SpeechClient()

        # Reads a file as bytes
        with open(audio_file, "rb") as file:
            content = file.read()

        config = cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            language_codes=["en-US"],
            model="long",
        )

        request = cloud_speech.RecognizeRequest(
            recognizer=f"projects/{G_PROJECT_ID}/locations/global/recognizers/_",
            config=config,
            content=content,
        )

        # Transcribes the audio into text
        response = client.recognize(request=request)

        for result in response.results:
            print(f"Transcript: {result.alternatives[0].transcript}")

        return response
    except Exception as err:
        print(f"Error: {err}")
        return False
