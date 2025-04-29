from django.shortcuts import render
import yt_dlp
import os
from django.conf import settings
from django.http import HttpResponse
from wsgiref.util import FileWrapper


def download(url, format) -> None:
    download_path = 'tmp/%(title)s.%(ext)s'
    
    ydl_opts = {
        'format':'bestaudio/best',
        'outtmpl': download_path,
    }
    if format == 'audio':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract audio
            'preferredcodec': 'mp3',      # Convert audio to MP3 format
            'preferredquality': '192',    # Set audio quality (192 kbps)
        }]


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info)  # Retrieve the actual file name
    
    # Prepare the file for download
    file_path = file_name  # Path to the downloaded file
    wrapper = FileWrapper(open(file_path, 'rb'))
    response = HttpResponse(wrapper, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    return  response



def song_download_view(request):
    context = {}
    video_url =  request.POST.get('video_url')
    format = request.POST.get('format')

    if video_url:
        return download(video_url, format)

    context['video_url'] = video_url
    return render(request, 'song_download.html', context=context)