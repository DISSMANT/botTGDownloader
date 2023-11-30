import os

from yt_dl.youtube_dl.extractor import YoutubeIE

from yt_dl.youtube_dl.downloader.http import HttpFD
from yt_dl.youtube_dl import YoutubeDL
import requests
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


class YRLException(Exception):
    pass


class QualityException(Exception):
    pass


def download_youtube(url, quality):
    yt_object = YoutubeIE()
    yt_object.set_downloader(YoutubeDL())
    try:
        all_params = yt_object._real_extract(url=url)
    except Exception:
        raise YRLException

    try:
        params = [video_quality for video_quality in all_params['formats'] if video_quality['format_note'] == "240p"
                  or video_quality['format_note'] == "240p60"][0]
    except Exception:
        raise QualityException

    sound_params = all_params['formats'][0]

    video = HttpFD(params=params, ydl=YoutubeDL()).real_download(filename='C:/Users/Ghost/OneDrive/Рабочий стол/1.mp4',
                                                                info_dict=params)

    sound = HttpFD(params=sound_params, ydl=YoutubeDL()).real_download(
        filename='C:/Users/Ghost/OneDrive/Рабочий стол/2.mp3',
        info_dict=sound_params)

    video = VideoFileClip('C:/Users/Ghost/OneDrive/Рабочий стол/1.mp4')
    audio = AudioFileClip('C:/Users/Ghost/OneDrive/Рабочий стол/2.mp3')

    final_clip = video.set_audio(audio)
    final_clip.write_videofile('final.mp4')


print(os.getcwd())
