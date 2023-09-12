# YouTube Video Clipper

## Description

The YouTube Video Clipper is a GUI tool that allows users to swiftly download specific segments from YouTube videos. Input the video URL, set start and end times, and obtain your desired clip. Additionally, it offers video transcription, ensuring you capture both video and spoken content in one go.

## Features
- User-friendly GUI for clipping videos.
- Option to transcribe the entire audio of the video.
- Set custom start and end times for the clip.
- Sanitized filenames for compatibility.
- Transcriptions saved in a readable `.txt` format.

## Limitations
- Clipped video segments are limited to a maximum duration of 90 seconds.
- The transcription feature relies on the `youtube_transcript_api`, which may not have transcriptions available for all videos.
- Video downloading is dependent on the availability of video streams from YouTube. Some videos may not be downloadable due to restrictions.
- The GUI is optimized for standard displays and may not display correctly on all screen resolutions.

## Installation
1. Clone the repository: git clone https://github.com/amadeuszbartosz/YoutubeVideoClipper.git
2. Navigate to the directory: cd YoutubeVideoClipper****
3. Install the required libraries: pip install -r requirements.txt


## Usage
Run the script using Python: python youtube_video_clipper.py

Follow the on-screen prompts to download and clip your desired video segment.

## Contributions
Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
