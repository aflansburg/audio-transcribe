"""Compress audio files."""
import numpy as np
import soundfile as sf


def downsample_compress(
    audio_file: str,
) -> str or bool:
    """Downsample and compress an audio file."""
    print("Downsampling and compressing...")

    output_file = audio_file.replace(
        ".wav", "_compressed.wav"
    )

    try:
        data, samplerate = sf.read(audio_file)

        print(f'Sample rate : {samplerate} Hz')

        # Fourier analysis
        # Title: Simple Audio Compression With Python
        # Author: Jean Meunier-Pion
        # Date: Dec 19, 2021
        # URL: https://medium.com/@jmpion/simple-audio-compression-with-python-70bdd7535b0a

        n = len(data)
        Fs = samplerate

        # not sure we need to separate the channels?
        ch1 = np.array([data[i][0] for i in range(n)])
        # ch2 = np.array([data[i][1] for i in range(n)])

        ch1_fourier = np.fft.fft(ch1)
        abs_ch1_fourier = np.absolute(ch1_fourier[:n // 2])

        eps = 1e-5
        # Boolean array where each value indicates whether we keep the corresponding freq
        frequencies_to_remove = (1 - eps) * \
            np.sum(abs_ch1_fourier) < np.cumsum(abs_ch1_fourier)
        # The frequency for which we cut the spectrum
        f0 = (
            len(frequencies_to_remove) - np.sum(frequencies_to_remove)
        ) * (Fs / 2) / (n / 2)

        print(f'f0 : {f0} Hz')

        # Then we define the downsampling factor
        D = int(Fs / f0)
        print(f'Downsampling factor : {D}')
        new_data = data[::D, :]  # getting the downsampled data
        sf.write(output_file, new_data, int(Fs / D), 'PCM_16')

        return output_file
    except Exception as err:
        print(f'Error: {err}')
        return False
