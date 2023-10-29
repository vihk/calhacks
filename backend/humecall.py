#!/venv/bin/python
from hume import HumeBatchClient
from hume.models.config import FaceConfig
from hume.models.config import ProsodyConfig
import pandas as pd
import numpy as np
import json 
from flask import Flask, request, jsonify
from flask_cors import CORS


def dick(url):
    client = HumeBatchClient("GB5GR8utyBkDmLHy5Kh7mtAGGebtMK5R9nDVhn7p5u7FMcT2")
    urls = [url]
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
        group = group[group["Emotion_Score"].apply(float) > .10].sort_values(by="Emotion_Score",ascending=False).head(3)
        groups.append(group)
        texts.append(name)

    newdict = {}
    while texts != []:
        if len(texts) == 1:
            newdict[texts[0]] = groups[0]
            texts = []
        else:
            newdict[texts[0]] = groups[0]
            groups = groups[1:]
            texts = texts[1:]
    scoredict = {}
    for key in newdict.keys():
        appendscore = {}
        newdicts = newdict[key].set_index("Emotion_Name")
        scoredict[key] = newdicts['Emotion_Score'].to_dict()
    return scoredict

app = Flask(__name__)
CORS(app)
@app.route('/', methods=['POST'])

def predict():
    text = request.json['text']
    print('recieved.')
    result = dick(text)
    print(result)
    return {'result':result}
if __name__ == '__main__':
    app.run(host='localhost',port=3000)

