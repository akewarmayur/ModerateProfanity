from difflib import SequenceMatcher
import helperFiles.profaneWords as profaneWords
import argparse
import pysrt


class TextProfanity:

    def get_profanity(self, input_sentence):
        list_of_words = input_sentence.split(" ")
        profanity_words = [u.lower() for u in profaneWords.profanity_words]
        profane_words = {}
        rr = 1
        for index, i in enumerate(list_of_words):
            for we in profanity_words:
                per = SequenceMatcher(None, we, i.lower()).ratio()
                if per >= 0.85:
                    profane_words[i] = index
                    rr += 1
                    break
        return profane_words

    def replace_profanity_with_star(self, input_sentence, profane_dict):
        list_of_words = input_sentence.split(" ")
        result = []
        for index, i in enumerate(list_of_words):
            found = False
            for key, value in profane_dict.items():
                if index == value:
                    result.append("***")
                    found = True
                    break
            if not found:
                result.append(i)
        return " ".join(result)

    def read_srt_file(self, srt_file_path):
        try:
            with open(srt_file_path, 'r', encoding='utf-8', errors='replace') as file:
                content = file.read()
            subs = pysrt.from_string(content)
            return subs
        except FileNotFoundError:
            print(f"File '{srt_file_path}' not found.")
            return None

    def separate_time_and_content(self, subtitles):
        time_and_content = []
        for subtitle in subtitles:
            start_time = subtitle.start
            end_time = subtitle.end
            content = subtitle.text
            time_and_content.append((start_time, end_time, content))
        return time_and_content

    def start_process(self, input):
        what = input.split(".")
        print(what)
        if 'srt' in what:
            name = input.split("/")
            name = name[len(name) - 1].split(".")[0]
            subtitles = self.read_srt_file(input)
            if subtitles:
                time_and_content_list = self.separate_time_and_content(subtitles)
                f = open("outputSRT/" + str(name) + ".srt", "a", encoding="utf-8")
                for idx, (start_time, end_time, content) in enumerate(time_and_content_list, start=1):
                    cont = content.split('\n')
                    f.write(str(idx) + '\n')
                    # 00:00:31,051 --> 00:00:35,151
                    f.write(str(start_time) + '-->' + str(end_time) + '\n')
                    for c in cont:
                        profane_dict = self.get_profanity(c)
                        sent = self.replace_profanity_with_star(c, profane_dict)
                        f.write(sent + "\n")
                    f.write("\n")
                f.close()
            else:
                print("Subtitle reading failed.")

            print("Processes SRT saved Successfully")
        else:
            input_sentence = input
            profane_dict = self.get_profanity(input_sentence)
            sent = self.replace_profanity_with_star(input_sentence, profane_dict)
            print(f"Processed Sentence: {sent} ")


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--input', action='store', type=str, required=True)
    args = my_parser.parse_args()
    input = args.input
    objT = TextProfanity()
    objT.start_process(input)
