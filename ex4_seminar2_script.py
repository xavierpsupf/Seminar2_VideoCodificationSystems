# First, we import all the  necessary dependencies to this part of the seminar (exercise 4):
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import ffmpeg

# Install the "youtube_transcript_api" package through the PyCharm Terminal (and also it's recommended to install it
# in the computer Terminal too):

# For this part of the seminar (exercise 4), I have used a YouTube video
# called "The Historical Journey of AI From Origins to Modern Tools  Founderz".
#   -> 1) First, I will download its subtitles.
#   -> 2) Second, I will download the video itself (with the "download_youtube_video" function).
#   -> 3) Third, I will put the download subtitles in the download YouTube video (with
#         the "add_video_subtitles" function).


# 1) First, we obtain the YouTube video subtitles:

# IMPORTANT: The following function get the subtitles from a YouTube video and save
# them in a .txt file named "youtube_video_subtitles.txt". However, for the part 3) we
# won't use this .txt file and we will use an equivalent file download from the Internet
# named "download_youtube_video_subtitles.srt".

def get_video_subtitles(video_url):
    try:
        video_id = video_url.split("v=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        subtitles = ""
        for entry in transcript:
            subtitles += entry['start'] + ' --> ' + entry['start'] + '\n'
            subtitles += entry['text'] + '\n\n'
        return subtitles

    except Exception as e:
        return f"\nAn error occurred in getting the video subtitles: {str(e)}"


def save_subtitles_to_file(subtitles, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(subtitles)
        print(f"\n1) Subtitles saved to {file_path}.")
    except Exception as e:
        print(f"\n1) Error saving subtitles: {str(e)}.")


# 2) Second, we download the YouTube video:
def download_youtube_video(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("\n2) An error has occurred in downloading the video.")

    print("\n2) Download is completed successfully.")


# 3) Third, we add the download subtitles to the download YouTube video:
def add_video_subtitles(input_file, output_file, subtitle_file):
    try:
        ffmpeg.input(input_file).output(output_file, vf=f'subtitles={subtitle_file}').run(overwrite_output=True)
    except ffmpeg._run.Error as e:
        print(e.stderr.decode())
