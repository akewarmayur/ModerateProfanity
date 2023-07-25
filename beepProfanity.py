from moviepy.editor import *
import moviepy.editor as mp
import whisperx
from difflib import SequenceMatcher
import helperFiles.profaneWords as profaneWords
import argparse

device = "cuda"
compute_type = "float16"
whisper_model = whisperx.load_model("large-v2", device, compute_type=compute_type)


class Profanity:

    def convertvideo2audio(self, input_video):
        sr = 16000
        audio_path = "output.wav"
        query = f'ffmpeg -i "{input_video}" -ac 1 -acodec pcm_s16le -ar {sr} "{audio_path}" -y'
        os.system(query)
        return audio_path

    def check_file_type(self, file_path):
        file_extension = file_path.split('.')[-1].lower()
        if file_extension == 'mp4' or file_extension == 'mkv':
            return 'video'
        else:
            return 'audio'

    def addBeep(self, file_path, beep_path, profane_words, video_name, file_type):
        beep = AudioFileClip(beep_path)
        fadein_duration = 0.5  # in seconds
        fadeout_duration = 0.5  # in seconds
        if file_type == "video":
            video = VideoFileClip(file_path)
            original_audio = video.audio
            for key, value in profane_words.items():
                start_time = value[0]
                end_time = value[1]
                beep_duration = end_time - start_time
                # Cut the beep sound to the desired duration
                beep = beep.subclip(0, beep_duration)
                # Set the beep sound to start at the desired timestamp
                beep = beep.set_start(start_time)
                # Apply fade-in and fade-out to the beep sound
                beep = beep.audio_fadein(fadein_duration).audio_fadeout(fadeout_duration)
                # Set the beep sound at the specified timestamp in the original audio
                original_audio = concatenate_audioclips([original_audio.subclip(0, start_time),
                                                         beep,
                                                         original_audio.subclip(end_time)])
            video_with_beep = video.set_audio(original_audio)
            # Specify the output file path
            output_path = "output/" + video_name + ".mp4"
            # Save the video with the modified audio
            video_with_beep.write_videofile(output_path, codec="libx264")
            return output_path
        else:
            original_audio = AudioFileClip(file_path)
            for key, value in profane_words.items():
                start_time = value[0]
                end_time = value[1]
                beep_duration = end_time - start_time
                # Cut the beep sound to the desired duration
                beep = beep.subclip(0, beep_duration)
                # Set the beep sound to start at the desired timestamp
                beep = beep.set_start(start_time)
                # Apply fade-in and fade-out to the beep sound
                beep = beep.audio_fadein(fadein_duration).audio_fadeout(fadeout_duration)
                # Set the beep sound at the specified timestamp in the original audio
                original_audio = concatenate_audioclips([original_audio.subclip(0, start_time),
                                                         beep,
                                                         original_audio.subclip(end_time)])
            # Specify the output file path
            output_audio_path = "output/" + video_name + ".mp3"
            # Save the audio file to the specified output path
            original_audio.write_audiofile(output_audio_path, codec='pcm_s16le')
            return output_audio_path

    def get_profanity(self, input_video):

        profanity_words = [u.lower() for u in profaneWords.profanity_words]
        audio_path = self.convertvideo2audio(input_video)
        device = "cuda"
        audio_file = audio_path
        batch_size = 16  # reduce if low on GPU mem

        audio = whisperx.load_audio(audio_file)
        result = whisper_model.transcribe(audio, batch_size=batch_size)

        # 2. Align whisper output
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
        result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

        # print(result["segments"]) # after alignment
        data = result["segments"]
        profane_words = {}
        rr = 1
        for i in data:
            words = i['words']
            for qq, ii in enumerate(words):
                for we in profanity_words:
                    per = SequenceMatcher(None, we, ii['word'].lower()).ratio()
                    if per >= 0.8:
                        profane_words[rr] = [ii['start'], ii['end']]
                        rr += 1
                        break
        return profane_words

    def process_file(self, input_file):
        file_type = self.check_file_type(input_file)
        tm = input_file.split("/")
        try:
            name_of_video = tm[len(tm)].split(".")[0]
        except:
            name_of_video = "output_video"

        # Step 4: Extract audio from the input video
        video_clip = mp.VideoFileClip(input_file)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile("tmp/temp_audio.wav")

        profane_words = self.get_profanity(input_file)
        print(profane_words)
        output_path = self.addBeep(input_file, "beepSound/bleep.mp3", profane_words, name_of_video, file_type)
        print(output_path)


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--file_path', action='store', type=str, required=True)
    args = my_parser.parse_args()
    file_path = args.file_path
    objT = Profanity()
    objT.process_file(file_path)



