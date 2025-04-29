from django.shortcuts import render
import yt_dlp


def download_song(url) -> None:
    ydl_opts = {
        'format':'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract audio
            'preferredcodec': 'mp3',      # Convert audio to MP3 format
            'preferredquality': '192',    # Set audio quality (192 kbps)
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except:
        pass
def download_video(url):
    ydl_opts = {
        'format':'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except:
        pass


def song_download_view(request):
    context = {}
    video_url =  request.POST.get('video_url')
    format = request.POST.get('format')

    if video_url:
        if format == 'video':
            download_video(url=video_url)
        elif format == 'audio':
            download_song(video_url)

    context['video_url'] = video_url
    return render(request, 'song_download.html', context=context)