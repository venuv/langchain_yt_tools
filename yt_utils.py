'''
Transcription utilities that generate textual summaries of Youtube videos, given their URL(s)
- yt_get uses pytube to download the video URLs into a local file
- yt_transcribe used the Whisper ASR model to convert the audio into text

'''

import whisper
import datetime
import subprocess
from pathlib import Path
import pandas as pd
import re
import time
import os 
import numpy as np

from pytube import YouTube
import torch
import time


def load_model():
    return whisper.load_model("base")

model = load_model()


def yt_get(yt_url):
    yt = YouTube("https://youtube.com"+ yt_url,use_oauth=True, allow_oauth_cache=True)
    print(f"youtube to be downloadd - {yt}")
    vpath = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
    print(f"Downloaded video {vpath}")
    return vpath


def yt_transcribe(video_url):
    print(f"transcribing {video_url}")
    result = model.transcribe(video_url)
    return (result['text'])

    
