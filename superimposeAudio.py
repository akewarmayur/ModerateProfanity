from moviepy.editor import *
import argparse


def superimposeAudio(video_path, audio_path, start_time, end_time):
    # Load the video
    video = VideoFileClip(video_path)

    # Load the beep sound
    beep = AudioFileClip(audio_path)

    # Set the duration of the beep sound
    beep_duration = end_time - start_time

    # Cut the beep sound to the desired duration
    beep = beep.subclip(0, beep_duration)

    # Set the beep sound to start at the desired timestamp
    beep = beep.set_start(start_time)

    # Add the beep sound to the video
    video_with_beep = video.set_audio(beep)

    # Specify the output file path
    output_path = "output.mp4"

    # Save the video with the beep sound
    video_with_beep.write_videofile(output_path, codec="libx264")


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--video_path', action='store', type=str, required=True)
    my_parser.add_argument('--audio_path', action='store', type=str, required=True)
    my_parser.add_argument('--start_time', action='store', type=str, required=True)
    my_parser.add_argument('--end_time', action='store', type=str, required=True)
    args = my_parser.parse_args()
    video_path = args.video_path
    audio_path = args.audio_path
    start_time = args.start_time
    end_time = args.end_time
    superimposeAudio(video_path, audio_path, start_time, end_time)
