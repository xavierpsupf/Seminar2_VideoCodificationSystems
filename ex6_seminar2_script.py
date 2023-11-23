import subprocess


def extract_yuv_histogram(input_file, output):
    command = [
        'ffmpeg',
        '-i', input_file,
        '-vf',
        'split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay',
        output
    ]
    subprocess.run(command)
