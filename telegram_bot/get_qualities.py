import asyncio
from yt_dl.youtube_dl import YoutubeDL
from yt_dl.youtube_dl.extractor import YoutubeIE
from telegram_bot.download_yotube_video import YRLException

async def get_qualities(url):
    yt_object = YoutubeIE()
    yt_object.set_downloader(YoutubeDL())
    try:
        all_params = yt_object._real_extract(url=url)
    except Exception as e:
        print(e)
        raise YRLException

    params = set([video_quality['format_note'] for video_quality in all_params['formats']])
    if "tiny" in params:
        params.remove("tiny")
    params = sorted(params, key=lambda x: int(x[:-3]) if 'p60' in x else int(x[:-2]))
    return params
