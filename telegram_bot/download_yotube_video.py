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

class DownloadException(Exception):
    pass

def download_youtube(url, quality, video_id):
    yt_object = YoutubeIE()
    yt_object.set_downloader(YoutubeDL())
    try:
        all_params = yt_object._real_extract(url=url)
    except Exception:
        raise YRLException

    params = [video_quality for video_quality in all_params['formats'] if video_quality['format_note'] == quality
              or video_quality['format_note'] == f"{quality}60"][0]

    sound_params = all_params['formats'][0]

    try:
        video = HttpFD(params=params, ydl=YoutubeDL()).real_download(filename=f'./{video_id}.mp4',
                                                                     info_dict=params)

        sound = HttpFD(params=sound_params, ydl=YoutubeDL()).real_download(
            filename=f'./{video_id}.mp3',
            info_dict=sound_params)

        video = VideoFileClip(f'./{video_id}.mp4')
        audio = AudioFileClip(f'./{video_id}.mp3')

        final_clip = video.set_audio(audio)
        final_clip.write_videofile(f'./{video_id}_final.mp4')

        os.remove(f'./{video_id}.mp4')
        os.remove(f'./{video_id}.mp3')

    except Exception:
        raise DownloadException

