import base64
import os

from moviepy.editor import AudioFileClip


def audio_extraction(video_name):
    """ Receive a video filepath and returns a base64 bytes string of the ogg/vorbis video's audio

    :param video_name: The video file path
    :return: (bytes) base64 bytes string of the video's ogg/vorbis audio.
    """

    audioclip = AudioFileClip(video_name)

    audio_fn = f"{video_name}_audio.ogg"

    audioclip.write_audiofile(audio_fn, codec='vorbis')

    b64audio = base64.b64encode(open(audio_fn, 'rb').read()).decode('utf-8')

    os.remove(audio_fn)

    return b64audio