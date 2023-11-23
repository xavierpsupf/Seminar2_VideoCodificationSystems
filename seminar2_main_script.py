import subprocess

# IMPORTANT! The project folder is "venv". Everything it has to be in that folder in order to be executed correctly.

# Import the "ex4_seminar2_script" python file functions since it's asked in Exercise 5.
# The 2 files need to be in the same project folder:
from ex4_seminar2_script import get_video_subtitles
from ex4_seminar2_script import save_subtitles_to_file
from ex4_seminar2_script import download_youtube_video
from ex4_seminar2_script import add_video_subtitles

# Import the "ex6_seminar2_script" python file functions since it's asked in Exercise 6.
# The 2 files need to be in the same project folder:
from ex6_seminar2_script import extract_yuv_histogram


# EXERCISES 1, 2 AND 3

print("\nEXERCISES 1, 2 and 3: ")


# FIRST WE CUT THE VIDEO IN A SMALL VIDEO OF 9 SECONDS:
def cut_video(input_path, output_path, start_time, duration):
    subprocess.run(['ffmpeg', '-i', input_path, '-ss', start_time, '-t', duration, '-c', 'copy', output_path])


input_video_full_video = 'BigBuckBunny_mp4_video.mp4'
cut_video_path = 'BigBuckBunny_mp4_video_cut.mp4'
initial_time = '00:04:49'
cut_video_duration = '00:00:09'

cut_video(input_video_full_video, cut_video_path, initial_time, cut_video_duration)


# THEN WE CREATE THE CLASS:
class Seminar2MainClass:
    def __init__(self):
        pass

    @staticmethod
    def visualize_motion_vectors(input_file, output_file):
        ffmpeg_cmd = [
            'ffmpeg',
            '-flags2', '+export_mvs',
            '-i',  input_file,
            '-vf', 'codecview=mv=pf+bf+bb',
            output_file
        ]

        try:
            subprocess.run(ffmpeg_cmd, check=True)
            print("Ex1 FFmpeg command executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing Ex1 FFmpeg command: {e}")

    @staticmethod
    def create_bbb_container(input_file, output_file):
        dur = 50  # Duration in seconds
        output_cut_video = "output_cut_video.mp4"
        command1 = [
            "ffmpeg",
            "-i", input_file,
            "-t", str(dur),
            output_cut_video
        ]
        subprocess.run(command1)

        output_mp3_mono_audio = "output_mp3_mono_audio.mp3"
        command2 = [
            "ffmpeg",
            "-i", output_cut_video,
            "-ac", "1",
            "-ar", "44100",
            "-b:a", "192k",
            output_mp3_mono_audio
        ]
        subprocess.run(command2)

        output_mp3_stereo_audio = "output_mp3_stereo_audio.mp3"
        command3 = [
            "ffmpeg",
            "-i", output_cut_video,
            "-ac", "2",  # Set the number of audio channels to 2 for stereo
            "-ar", "44100",
            "-b:a", "128k",  # Set a lower bitrate, adjust as needed
            output_mp3_stereo_audio
        ]
        subprocess.run(command3)

        output_aac_audio = "output_aac_audio.aac"
        command4 = [
            "ffmpeg",
            "-i", output_cut_video,
            "-c:a", "aac",  # Set the audio codec to AAC
            "-strict", "experimental",  # Required for using the experimental AAC encoder
            output_aac_audio
        ]
        subprocess.run(command4)

        command_final = [
            "ffmpeg",
            "-i", output_cut_video,
            "-i", output_mp3_mono_audio,
            "-i", output_mp3_stereo_audio,
            "-i", output_aac_audio,
            "-map", "0:v",
            "-map", "1:a",
            "-map", "2:a",
            "-map", "3:a",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            output_file
        ]
        subprocess.run(command_final)

    @staticmethod
    def container_track_count(input_file):
        # Run ffmpeg to get information about the input file
        ffmpeg_cmd = f'ffmpeg -i {input_file} 2>&1 | grep Stream'
        result = subprocess.run(ffmpeg_cmd, shell=True, capture_output=True, text=True)

        # Extract the audio and video track counts
        audio_count = 0
        video_count = 0

        for line in result.stdout.split('\n'):
            if 'Video' in line:
                video_count += 1
            elif 'Audio' in line:
                audio_count += 1

        return audio_count, video_count


input_video_full_video = 'BigBuckBunny_mp4_video.mp4'
input_video_cut_video = 'BigBuckBunny_mp4_video_cut.mp4'
output_motion_vectors_video = 'BigBuckBunny_mp4_video_motion_vectors.mp4'
output_container_video = 'BigBuckBunny_mp4_video_container.mp4'

# For Exercise 1 (visualize the motion vectors in the previous 9 seconds cut BBB video):
Seminar2MainClass.visualize_motion_vectors(input_video_cut_video, output_motion_vectors_video)

print("\nCODE OF EXERCISE 1 EXECUTED WITH SUCCESS! THE OUTPUT VIDEOS ARE IN THE PROJECT FOLDER.")

# For Exercise 2 (create the container of 50 seconds BBB video):
Seminar2MainClass.create_bbb_container(input_video_full_video, output_container_video)

print("\nCODE OF EXERCISE 2 EXECUTED WITH SUCCESS! THE OUTPUT VIDEO IS IN THE PROJECT FOLDER.")

# FOR Exercise 3 (count the number of tracks of a container):
input_video_container = 'BigBuckBunny_mp4_video_container.mp4'
audio_tracks, video_tracks = Seminar2MainClass.container_track_count(input_video_container)

print(f'\nThe MP4 container at {input_video_container} contains:')
print(f'{audio_tracks} audio track(s)')
print(f'{video_tracks} video track(s)')

print("\nCODE OF EXERCISE 3 EXECUTED WITH SUCCESS!")


# EXERCISES 4 AND 5

print("\nEXERCISES 4 and 5: ")

# 1) First, we obtain the YouTube video subtitles:

youtube_video_link = "https://www.youtube.com/watch?v=G2nL0Lfi8vI&t=12s"
# video_id = "G2nL0Lfi8vI"
youtube_video_subtitles_path = "youtube_video_subtitles.txt"

youtube_video_subtitles = get_video_subtitles(youtube_video_link)

if youtube_video_subtitles:
    save_subtitles_to_file(youtube_video_subtitles, youtube_video_subtitles_path)

# 2) Second, we download the YouTube video:
youtube_video_link = "https://www.youtube.com/watch?v=G2nL0Lfi8vI&t=12s"
download_youtube_video(youtube_video_link)  # We call the function to download a YouTube video.

# 3) Third, we add the download subtitles to the download YouTube video:

input_video_file = 'The Historical Journey of AI From Origins to Modern Tools  Founderz.mp4'
subtitles_file = 'download_youtube_video_subtitles.srt' # We use the Internet download subtitles file.
output_video_file = 'output_video_with_subtitles.mp4'

add_video_subtitles(input_video_file, output_video_file, subtitles_file)

print("\n3) Subtitles added successfully.")

print("\nCODE OF EXERCISES 4 AND 5 EXECUTED WITH SUCCESS! THE OUTPUT FILES AND VIDEOS ARE IN THE PROJECT FOLDER.")


# EXERCISE 6

print("\nEXERCISE 6: ")

# First we will cut the video in order to have a faster execution:
input_video_full_video = 'BigBuckBunny_mp4_video.mp4'
cut_video_path_ex6 = 'BigBuckBunny_mp4_video_cut_ex6.mp4'
initial_time_ex6 = '00:00:00'
cut_video_duration_ex6 = '00:01:00'

cut_video(input_video_full_video, cut_video_path_ex6, initial_time_ex6, cut_video_duration_ex6)

# Then we will call the "extract_yuv_histogram" function from the "ex6_seminar2_script.py":
input_video_ex6 = 'BigBuckBunny_mp4_video_cut_ex6.mp4'
output_video_ex6 = 'BigBuckBunny_mp4_YUV_histogram.mp4'

extract_yuv_histogram(input_video_ex6, output_video_ex6)

print("\nCODE OF EXERCISE 6 EXECUTED WITH SUCCESS! THE OUTPUT VIDEO IS IN THE PROJECT FOLDER.")
