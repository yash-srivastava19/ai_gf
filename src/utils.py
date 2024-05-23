import requests
import replicate
import os
import re
import simplejson as json
import ast
from dotenv import load_dotenv

load_dotenv()

avatar_image = open("static\margot_robbie.jpeg", "rb")
margot_voice_id = "eWnjaCUKWIIhtSplMdIh"
audio_path = "outputs\generated_audio.mp3"
video_path = "gf.mp4"
voice_url = f"https://api.elevenlabs.io/v1/text-to-speech/{margot_voice_id}"
video_url = "devxpy/cog-wav2lip:8d65e3f4f4298520e079198b493c25adfc43c058ffec924f2aefc8010ed25eef"
#pipeline: record voice -> text -> audio -> video 
def get_text_from_chat(message):
    prompt = f"you are an margot robbie, a girlfriend who is loving and caring and willing to please all her boyfriends request. Respond in a flirtatious way, but do not use emotions within asterisks(like *blinks*/ *giggles* / *smiles* ) and any variant of it. Do not use emoticons as well. Reply like a normal companion. the following is a chat message from your boyfriend:\n{message}\nyour response:"

    output = replicate.run(
        "meta/llama-2-7b-chat",
        input={
        "top_k": 0,
        "top_p": 1,
        "temperature": 0.75,
        "system_prompt": prompt,
        "prompt": message,
        "length_penalty": 1,
        "max_new_tokens": 800,
        "prompt_template": "<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{prompt} [/INST]",
        "presence_penalty": 0
    },)

    clean_str  = [re.sub(r'\*\w+\*', '', ''.join(output))]
    # print(clean_str)

    json_output = json.dumps(clean_str, iterable_as_array=True)
    print(json_output)
    print(type(json_output))
    lst = ast.literal_eval(json_output)
    str_output = ''.join(lst)
    print(str_output)
    return str_output

def get_audio_from_text(text):
    payload = {
        "language_id": "en-us",
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.50,
            "similarity_boost": 0.75
        },
        "text": text
    }

    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": os.environ["XI_API_KEY"],
        "Content-Type": "application/json"
    }

    response = requests.post(voice_url, json=payload, headers=headers)
    print('generated audio')
    with open(audio_path, "wb") as f:
        f.write(response.content)

    return open(audio_path, "rb")

def get_lipsync_video(image, audio):
    output_url = replicate.run(
        video_url,
        input={"face": image, "audio": audio, "smooth:": True}
    )
    print(output_url)
    return output_url

def get_video_from_chat(message):
    text = get_text_from_chat(message)
    avatar_audio = get_audio_from_text(text)
    video_url = get_lipsync_video(avatar_image, avatar_audio)
    return video_url