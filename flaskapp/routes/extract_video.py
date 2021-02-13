import base64
import random
import os

import requests
from flask_restful import Resource, request

from flaskapp.support.frame_extraction import frame_extraction
from flaskapp.support.audio_extraction import audio_extraction

tikaserver = os.getenv('TIKA_SERVER')
if tikaserver is None:
    tikaserver = 'http://localhost:9998'
transcribeserver = os.getenv('TRANSCRIBE_SERVER')
if transcribeserver is None:
    transcribeserver = 'http://localhost:3800'


class ExtractVideo(Resource):

    def post(self):
        args = request.get_json()

        try:
            # Get base64 encoded video data
            b64data = args['data']

            # Transform to binary
            bin_data = base64.b64decode(b64data)

            # Save temp video file
            random_n = str(random.randint(1, 100000))
            video_name = f'video_temp{random_n}.mp4'
            open(video_name, 'wb').write(bin_data)

            fr_file_names = frame_extraction(video_name)

            audiob64 = audio_extraction(video_name)

            # Iterate over frames and sent them to tika for OCR extraction

            full_text_ocr = ''
            last_text_ocr = ''

            # Frames OCR extraction
            for fr_fn in fr_file_names:

                mediadata = open(fr_fn, 'rb')

                # Get text from tika
                response = requests.put(f'{tikaserver}/tika', data=mediadata,
                                        headers={'Content-type': 'image/jpeg', 'X-Tika-OCRLanguage': 'por'})

                text = ' '.join(response.content.decode('utf8').split())

                if last_text_ocr != text:
                    full_text_ocr += text + ' '
                    # To avoid adding the same text over and over
                    last_text_ocr = text

                os.remove(fr_fn)

            # Audio transcription

            response = requests.post(f'{transcribeserver}/transcribe', json={'data': audiob64},
                                     headers={'Content-Type': 'application/json'})

            text_audio = eval(response.content.decode('utf8'))['data']

            os.remove(video_name)

            return {'code': 200, 'data': {
                'video_ocr': full_text_ocr,
                'audio_transcription': text_audio,
                'audiob64': audiob64}}

        except Exception as e:
            print(e)
            return {'code': 500, 'data': ''}
