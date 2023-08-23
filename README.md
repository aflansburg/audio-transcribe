# Simple Audio File Conversion, Compression & Speech Transcription

## What this does

- Converts audio files to WAV w/ PCM codec
- Uses maths to downsample for smaller audio file size
- Feeds the file to Google Cloud Speech-to-text (STT) for transcribing
- Returns the transcribed text

## Plans

This is a basic PoC that could be used as a jump point for transcribing conversations between two people. Such as a patient and a physician.
The Cloud STT API can process these asynchronously up to 480 minutes in length. However, if needed we could also split audio files into chunks.

## Sample Data
Included in the `resources/input` directory is a 60 second sample from a publicly available Youtube video where a volunteer (host) sits through a therapy session with a therapist.

### Audio transcription
We could implement the audio transcription part in Cloud Run / Cloud Functions and then feed the transcription to a Dataflow job.

### Transformation
Then we could transform & redact any information with DLP.

### Big Query
Finally we store the data in Big Query

## Notes
Cloud Run is for stateless applications so any filesystem ops consume memory.
In this PoC files are read and written to the filesystem.
We would need to leverage Cloud Storage or another NFS type solution.


## How to set this up locally

Assuming you have IAM permissions for using Cloud Speech-to-text, follow the gcloud setup:
[Cloud Speech-To-Text](https://cloud.google.com/speech-to-text/v2/docs/transcribe-client-libraries)

Example:
```
gcloud auth application-default login
gcloud config set project <PROJECT_ID>
```

### Install ffmpeg & ffprobe
Download [ffmpeg](https://ffmpeg.org/download.html) or just run this in the directory:
(example)

```
# ffmpeg
curl -O https://evermeet.cx/ffmpeg/ffmpeg-111795-g95433eb3aa.zip
unzip ffmpeg-111795-g95433eb3aa.zip -d ./ffmpeg

# ffprobe
curl -O https://evermeet.cx/ffmpeg/ffprobe-111795-g95433eb3aa.zip
unzip ffmpeg-111795-g95433eb3aa.zip -d ./ffprobe

# export to PATH
export PATH="$PATH:$(pwd)/ffmpeg"
export PATH="$PATH:$(pwd)/ffprobe"
```

Setup env & deps (assuming`poetry` installed):
```
poetry env use 3.11.4
poetry install
```

Run
```
# you may wish to tweak the BITRATE & CODEC constants in lib/convert.py
GOOGLE_CLOUD_PROJECT=$(gcloud config get project) python main.py
```

## Output
If everything is setup correctly and inputs are good, you should see something similar to this:
```
Let's transcribe some audio.
Converting to WAV format...
Converted resources/input/sample_therapy_audio.mp3 to resources/output/sample_therapy_audio.wav.
Downsampling and compressing...
Sample rate : 44100 Hz
f0 : 21579.757922444307 Hz
Downsampling factor : 2
Transcript: so Kyle you know as we think about
Transcript:  the pattern of narcissism in you the place I'm going to start is your relationships okay can you tell me are you dating anyone right now no you're not okay so we don't have that if you think about your last relationship
Transcript:  how was that emotionally was that an emotionally fulfilling relationship
Transcript:  it was but I am not a very emotional person what do you mean by that it doesn't take a lot for me to feel like I'm emotionally filled up
Transcript:  so you almost get overwhelmed by emotions yes like if somebody is just like oh I love you you're so I'm like oh my gosh like have it your own deal okay yeah that kind of pushed back
Transcript:  has anyone ever experienced it as something hurtful oh yeah oh really like everybody I've ever dated is like I wish you would just like show me you care I'm like I'm trying you're trying yeah so you actually do try oh I try as best as I can and I remember one conversation with an ex
Transcription:
results {
  alternatives {
    transcript: "so Kyle you know as we think about"
    confidence: 0.972195506
  }
  result_end_offset {
    seconds: 2
    nanos: 940000000
  }
  language_code: "en-US"
}
results {
  alternatives {
    transcript: " the pattern of narcissism in you the place I\'m going to start is your relationships okay can you tell me are you dating anyone right now no you\'re not okay so we don\'t have that if you think about your last relationship"
    confidence: 0.958517551
  }
  result_end_offset {
    seconds: 14
    nanos: 840000000
  }
  language_code: "en-US"
}
results {
  alternatives {
    transcript: " how was that emotionally was that an emotionally fulfilling relationship"
    confidence: 0.945113301
  }
  result_end_offset {
    seconds: 20
    nanos: 60000000
  }
  language_code: "en-US"
}
results {
  alternatives {
    transcript: " it was but I am not a very emotional person what do you mean by that it doesn\'t take a lot for me to feel like I\'m emotionally filled up"
    confidence: 0.932192743
  }
  result_end_offset {
    seconds: 30
    nanos: 560000000
  }
  language_code: "en-US"
}
results {
  alternatives {
    transcript: " so you almost get overwhelmed by emotions yes like if somebody is just like oh I love you you\'re so I\'m like oh my gosh like have it your own deal okay yeah that kind of pushed back"
    confidence: 0.966319144
  }
  result_end_offset {
    seconds: 42
    nanos: 680000000
  }
  language_code: "en-US"
}
results {
  alternatives {
    transcript: " has anyone ever experienced it as something hurtful oh yeah oh really like everybody I\'ve ever dated is like I wish you would just like show me you care I\'m like I\'m trying you\'re trying yeah so you actually do try oh I try as best as I can and I remember one conversation with an ex"
    confidence: 0.959738374
  }
  result_end_offset {
    seconds: 59
    nanos: 260000000
  }
  language_code: "en-US"
}
metadata {
  total_billed_duration {
    seconds: 60
  }
}
```
