from flask import Flask, request,jsonify
from video_indexer import VideoIndexer
import json as json
from flask_cors import CORS,cross_origin


app = Flask(__name__)
CORS(app,support_credentials=True)
CONFIG = {
    'SUBSCRIPTION_KEY': 'ffaf53b4d9434ed59d43937bbd857357',
    'LOCATION': 'trial',
    'ACCOUNT_ID': '164b80dc-17e1-45d3-a186-1d84d6eb7b6d'
}

vi = VideoIndexer(
    vi_subscription_key=CONFIG['SUBSCRIPTION_KEY'],
    vi_location=CONFIG['LOCATION'],
    vi_account_id=CONFIG['ACCOUNT_ID']
)



def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        name=f.filename
        return name


def createinstance(name,language):
    video_id = vi.upload_to_video_indexer(
        input_filename=f'{name}',
        video_name=f'{name}',  # identifier for video in Video Indexer platform, must be unique during indexing time
        video_language=language
    )
    return video_id


def indexvideo(video_id,language):
    info = vi.get_video_info(
        video_id,
        video_language=language
    )
    return info




@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    language=request.form.get('lang')
    name=upload_file()
    video_id=createinstance(name,language)

    while(True):
        info = indexvideo(video_id,language)
        if info['state']=='Processed':
            info1=json.dumps(info)
            return info1




if __name__ == '__main__':
    app.run(debug=True)