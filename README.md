# Moderate Profanity
Identification of profanity in the spoken words and beep that words.

Identification of profanity in the input text, or the input srt file.

## Moderate Profanity (Video)
* First the ASR will be done using [whisperx](https://github.com/m-bain/whisperX) model.
* Detect profane words from detected ASR.
*Superimpose beep sound on the timestamp given by the whisperx model
  
```
python beepProfanity.py --file_path "video_path"
```

### Output

https://github.com/akewarmayur/ModerateProfanity/assets/31464781/1347d494-e94a-4c1c-8897-c05d56474256

## Gradio APP
```
python beepProfanityGradioApp.py
```
### Output
![img](https://github.com/akewarmayur/ModerateProfanity/assets/31464781/6f8eff46-29e9-407b-95a9-0bde881b58cd)

## Moderate Profanity (Text)
* The input sentence or srt file will be moderated by comparing it with list of profane words.
![image](https://github.com/akewarmayur/ModerateProfanity/assets/31464781/cd9c10d1-3e74-49b9-891b-bab99995b617)


```
python textProfanity.py --input "sentence/srt_file"
```
* input : Can be a srt file, or a sentence

### Output
