# langchain_yt_tools
Custom Langchain tools to search/extract/transcribe Youtube videos

# Installation
pip install -r requirements.txt


# Code
Consists of two custom LangChain tools, _CustomYTSearchTool_ and _CustomYTTranscribeTool_
 * CustomYTSearchTool searches for the youtube videos featuring a *person name* and returns the top *num_results* URLs
 * CustomYTTranscribeTool transcribes the videos and outputs the text transcripts to transcripts.json

# Demo
running *python yt_tools.py* shows you an agent run that transcribes the top 3 video results for Laszlo Bock (Google HR celebrity). you should see the results stored in *transcripts.json* in the current working directory.

# Caveats
you will be required to authenticate with your Youtube credentials the first time around

# To Do
 * clean up the mp4 files that the Transcribe tool creates between runs
 * add threading/async capability to transcribe videos concurrently (may require not outputting transcripts to a single JSON file)
