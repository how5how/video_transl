import os
import speech_recognition as sr
from tqdm import tqdm
from multiprocessing.dummy import Pool
from google.cloud import translate_v2
import pandas as pd

pool = Pool(8) # Number of concurrent threads

with open("api-key.json") as f:
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

r = sr.Recognizer()
files = sorted(os.listdir('parts/'))

def transcribe(data):
    idx, file = data
    name = "parts/" + file
    print(name + " started")
    # Load audio file
    with sr.AudioFile(name) as source:
        audio = r.record(source)
    # Transcribe audio file
    text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
    print(name + " done")
    return {
        "idx": idx,
        "text": text
    }

all_text = pool.map(transcribe, enumerate(files))
pool.close()
pool.join()

transcript = ""
for t in sorted(all_text, key=lambda x: x['idx']):
    total_seconds = t['idx'] * 30
    # Cool shortcut from:
    # https://stackoverflow.com/questions/775049/python-time-seconds-to-hms
    # to get hours, minutes and seconds
    m, s = divmod(total_seconds, 60)
    h, m = divmod(m, 60)

    # Format time as h:m:s - 30 seconds of text
    transcript = transcript + "{:0>2d}:{:0>2d}:{:0>2d} {}\n".format(h, m, s, t['text'])

print(transcript)

with open("transcript.txt", "w") as f:
    f.write(transcript)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = \
r'/Users/haozheng/Documents/Learning/google_cloud/translation/translation_env/API_key/GoogleCloudAPIKey_MyServiceAcct.json'

translate_client = translate_v2.Client()

lan_code = [['zh'],['ko'],['ja'],['gu'],['hu'],['af']]

f = open('/Users/haozheng/Desktop/results.txt','w') 

read_text = open('transcript.txt','r').read()

f.write(read_text)
f.write('\n')

test_text = read_text


for lan in lan_code:
    lan_str = str(lan[0])
    result2 = translate_client.translate(test_text, target_language = lan_str)
    # print(result2)
    f.write(str(result2['translatedText']))
    f.write('\n\n')

f.close()
