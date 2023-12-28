import os
import asyncio
from yt_dl.youtube_dl.extractor import YoutubeIE
from yt_dl.youtube_dl.downloader.http import HttpFD
from yt_dl.youtube_dl import YoutubeDL
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip



class YRLException(Exception):
    pass


class QualityException(Exception):
    pass

class DownloadException(Exception):
    pass

async def download_youtube(url, quality, video_id):
    yt_object = YoutubeIE()
    yt_object.set_downloader(YoutubeDL())
    try:
        all_params = await asyncio.to_thread(yt_object._real_extract(url=url))
    except Exception:
        raise YRLException

    params = [video_quality for video_quality in all_params['formats'] if video_quality['format_note'] == quality
              or video_quality['format_note'] == f"{quality}60"][0]

    sound_params = all_params['formats'][0]

    try:
        await asyncio.to_thread(HttpFD(params=params, ydl=YoutubeDL()).real_download, filename=f'./{video_id}.mp4',
                                info_dict=params)
        await asyncio.to_thread(HttpFD(params=sound_params, ydl=YoutubeDL()).real_download,
                                filename=f'./{video_id}.mp3', info_dict=sound_params)

        video = await asyncio.to_thread(VideoFileClip, f'./{video_id}.mp4')
        audio = await asyncio.to_thread(AudioFileClip, f'./{video_id}.mp3')


        final_clip = video.set_audio(audio)
        await asyncio.to_thread(final_clip.write_videofile(f'./{video_id}_final.mp4'))

        os.remove(f'./{video_id}.mp4')
        os.remove(f'./{video_id}.mp3')

    except Exception:
        raise DownloadException

