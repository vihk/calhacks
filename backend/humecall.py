#!/venv/bin/python
from hume import HumeBatchClient
from hume.models.config import FaceConfig
from hume.models.config import ProsodyConfig
import pandas as pd
import numpy as np
import json 
from flask import Flask, request, jsonify
from flask_cors import CORS



client = HumeBatchClient("GB5GR8utyBkDmLHy5Kh7mtAGGebtMK5R9nDVhn7p5u7FMcT2")
urls = ["https://tmpfiles.org/dl/2979437/untitled.mp3"]
configs = [ProsodyConfig(identify_speakers = True)]
job = client.submit_job(urls, configs)

print(job)
print("Running...")

job.await_complete()
job.download_predictions("predictions.json")
print("Predictions downloaded to predictions.json")

job.download_artifacts("artifacts.zip")
print("Artifacts downloaded to artifacts.zip")

with open('/Users/gill/Documents/GitHub/calhacks/backend/predictions.json', 'r') as f:

    data = json.load(f)


print(data)

predictions = data[0]['results']['predictions'][0]['models']['prosody']['grouped_predictions'][0]['predictions']

texts = []
for pred in predictions:
    texts.append(pred['text'])

df = pd.DataFrame({'text': texts})

print(df)

flattened_data = []
for item in data:
    for prediction in item['results']['predictions'][0]['models']['prosody']['grouped_predictions']:
        for text_prediction in prediction['predictions']:
            for emotion in text_prediction['emotions']:
                flattened_data.append({
                    'Text': text_prediction['text'],
                    'Time_Begin': text_prediction['time']['begin'],
                    'Time_End': text_prediction['time']['end'],
                    'Emotion_Name': emotion['name'],
                    'Emotion_Score': emotion['score']
                })


df = pd.DataFrame(flattened_data)


print(df)

grouped_df = df.groupby('Text')


groups = []
texts = []
for name, group in grouped_df:
    print(f"Text: {name}")
    group = group.sort_values(by="Emotion_Score",ascending=False) 
    group = group[group["Emotion_Score"].apply(float) > .10]
    groups.append(group)
    texts.append(name)

send_data = {}
for i,text in enumerate(texts):
    df_json = groups[i].to_json()
    send_data[text] = json.loads(df_json)
json_data = json.dumps(send_data)

# app = Flask(__name__)
# CORS(app)

# @app.route('/', methods=['POST'])

# def predict():
#     text = request.json['text']
#     print('recieved.')
#     result = json_data
#     return result
# if __name__ == '__main__':
#     app.run(host='localhost',port=3000)