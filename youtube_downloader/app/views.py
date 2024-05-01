from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import JsonResponse
from pytube import *
import io
import base64
from bs4 import BeautifulSoup
import requests
import json

# Create your views here.
def homepage(request):
    is_homepage = True
    return render(request, "homepage.html", {'data':[1,2,3,4],'is_homepage': is_homepage})

def get_video_thumbnail_url(request):
    try:

        if request.method == "POST":
            link = request.POST.get("youtube_link")
            print(f"Link is- {link} ")
            yt_link = YouTube(link)
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find Meta tag containg the thumbnail URL
            thumbnail_tag = soup.find('meta', property='og:image')
            thumbnail_url = thumbnail_tag['content'] if thumbnail_tag else None

            # Find the element containing the video description
            description_tag = soup.find('meta', itemprop='description')
            video_description = description_tag['content'] if description_tag else None
            return JsonResponse({'message':"success", 'status':200, 'url':thumbnail_url, 'title':yt_link.title, 'video_description':video_description, 'video_url': link}, status=200)

    except Exception as e:
        print(f"exception occur {e}")
        return JsonResponse({'error': 'Invalid request method', 'status':405,}, status=405)



def video_download(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            link = data.get("video_link")
            resolution = data.get("video_resolution")
            print("Resolution - ", resolution)

            video = YouTube(link) 
    
            # setting video resolution 
            streams = video.streams
            filtered_streams = streams.filter(res=resolution)
            stream = filtered_streams.first()
            
            # Create a buffer to store the video content
            buffered_stream = io.BytesIO()

            # Download the video content into the buffer
            stream.stream_to_buffer(buffered_stream)

            # Get the content of the buffer
            video_content = buffered_stream.getvalue()

            # Encode the video content using base64
            encoded_video_content = base64.b64encode(video_content).decode('utf-8')

            # Close the buffer
            buffered_stream.close()

            # Return the video content or process it further as needed
            return JsonResponse({'message': 'Video downloaded successfully', 'status':200, 'video_content': encoded_video_content}, status=200)

        else:
            # Handle GET requests or other methods
            return JsonResponse({'error': 'Invalid request method', 'status':405,}, status=405)
        
    except Exception as e:
        print(f"{e}")
        return JsonResponse({'error': 'Invalid request method', 'status':405,}, status=405)