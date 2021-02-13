# Video Transcription and OCR

This service tries to retrieve all text content from a video. The image part of the video is retrieved by splitting it in several image frames and then making an OCR (using Tika). The audio transcription part is obtained by using another service (like AudioTranscriberAPI) that receives an audio and returns the text transcription.

## How to run
You will need to set the environment variables described below. After that, follow the steps:

### Development env

Install packages
```commandline
pip install -r requirements
```

Go to Flask API folder
```commandline
cd ./flaskapp
```

Start Flask server (e.g. http://localhost:3860)
```commandline
flask run -h localhost -p 3680
```

## How to use
For testing, it's  recommended to use an API tool like [Postman](https://www.postman.com/downloads/).

On Headers: Include the key Content-Type with value application/json as we will send the base64 audio data using a JSON format.

In Body: Create a JSON where the data key has the base64 mp4 data, for example:

```json
{
  "data": "BASE64DATA"
}
```

Finally on URL field, select the POST method and send the JSON to the following address: `http://localhost:3860/extract_video`

If successful, it will return a JSON with code 200 and the following data:

```json
{
  "code": 200,
  "data": {
    "video_ocr": "OCR_TEXT_EXTRACTED_FROM_VIDEO",
    "audio_transcription": "TRANSCRIPTED_TEXT_FROM_VIDEO_AUDIO",
    "audiob64": "BASE64_AUDIO_DATA"
  } 
}
```

## Environment Variables

* TIKA_SERVER: Tika text extractor host (example: https://hub.docker.com/r/apache/tika)
* TRANSCRIBE_SERVER: Transcriber service host (example: https://github.com/rmazzine/AudioTranscriberAPI)