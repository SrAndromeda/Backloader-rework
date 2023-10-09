from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from asgiref.sync import async_to_sync
from yt_dlp import YoutubeDL
import json
import os
from PIL import Image
import threading
import uuid
import httpx
import requests
import subprocess


from .models import Timer as TimerModel  
from .models import Flow as FlowModel
from .models import Outlet as OutletModel


def timer_function(timer_id, interval, flow_id):

    print(str(timer_id) + " executing with flow id " + str(flow_id))
    
    yt_dl_flow(flow_id)
    
    timer_object = TimerModel.objects.get(timer_id=timer_id)
    timer_object.last_run = timezone.now()
    timer_object.save()
    
    timer_thread = threading.Timer(interval, timer_function, args=(timer_id, interval, flow_id))
    timer_thread.name = f"timer_{timer_id}"
    timer_thread.start()
    

def create_timer(interval, flow_id, timer_id):   
    timer_thread = threading.Timer( interval, timer_function, args=(timer_id, interval, flow_id))
    timer_thread.name = f"timer_{timer_id}"   
    timer_thread.start()
        
    return True 


def stop_timer(timer_id):
    try:
        
        for thread in threading.enumerate():
            if thread.name == f"timer_{timer_id}":
                thread.cancel()
        
        return True
                
    except Timer.DoesNotExist:
        print("Could not find thread:" + f"timer_{timer_id}")
        
        return False
        
        
def find_timer(timer_id):
    try:
        
        for thread in threading.enumerate():
            if thread.name == f"timer_{timer_id}":
                return True
        
        return False
                
    except Timer.DoesNotExist:
        print("Could not find thread:" + f"timer_{timer_id}")
        
        return False
    
    
def initialize():
    
    print("Initializing...")
    
    try:
    
        i = 0
        
        for timer in TimerModel.objects.all():
            
            try:
                
                timer_id = timer.timer_id
                flow_id = timer.flow_set.first().flow_id
                
                if not find_timer(timer_id):
                    print("created timer" + str(i))
                    i += 1
                    create_timer(timer.interval, flow_id, timer_id)
                    
            except Exception as e:
                print("Timer startup failed: " + str(e))
            
    except Exception as e:
            print("Timer startup failed: " + str(e))
    
            







def yt_dl_flow(flow_id):
    
    flow_object = FlowModel.objects.get(flow_id=flow_id)


    format = ''
    
    print(str(flow_object.quality))
    
    match flow_object.quality:
        case 'a':
            format = 'bestaudio[ext=m4a]'
        case 'max':
            format = 'bestaudio[ext=m4a]+bestvideo/best'
        case _:
            format = 'bestaudio[ext=m4a]+bestvideo[height={}]/bestaudio[ext=m4a]+bestvideo[width={}]/bestaudio[ext=m4a]+bestvideo/best'.format(str(flow_object.quality), str(flow_object.quality)) 



    try:
        ydl_args = [
                    '-P', flow_object.outlet.path,
                    '-P', 'temp:tmp',
                    '--ignore-errors',                      # Ignore errors caused by unavailable videos
                    '-o', flow_object.outlet.video,
                    '--quiet',                              # Suppress standard output messages
                    '--format', format,                     # Format code or id
                    '--write-thumbnail',                    # Write thumbnail image to disk
                    '-o', 'thumbnail:' + flow_object.outlet.thumbnail,
                    '--write-info-json',                     # Write video metadata to a .json file
                    '-o', 'infojson:' + flow_object.outlet.info,
                    '--download-archive', f"{flow_object.outlet.path}downloaded_{flow_object.flow_id}.txt",  # File name where the download history is recorded
                    '--embed-subs',                         # Embed subtitles in the output file
                    '--merge-output-format', 'mp4',           # Merge videos in the mp4 format
                    '--embed-metadata',                    # Embed the thumbnail, subtitles, chapters, and other metadata when possible
                    '--write-thumbnail',                    # Write thumbnail image to disk
                    '--write-info-json',                      # Write video metadata to a .json file
                    '--sponsorblock-mark', 'all',               # Sponsorblock marker for ads to be cut
        ]
        
        


        command = ['yt-dlp'] + ydl_args + [flow_object.url]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as error:
            print(f'Download failed with error: error')


   

            
        for root, dirs, files in os.walk(flow_object.outlet.path):
            for file in files:
                # Check if file is a webp image
                if file.endswith('.webp'):
                    # Convert to jpeg
                    filename = os.path.join(root, file)
                    tmp = Image.open(filename).convert("RGB")
                    tmp.save(filename.replace(".webp", ".jpeg"), "jpeg")
                    os.remove(filename) #Removing old thumbnails
        
        
    except Exception as e:
        print(e)










# Create your views here.

class Initialize(APIView):
    
    def post(self, request, format=None, *args, **kwargs):
        
        initialize()
        
        return Response("Initialization function called", status=status.HTTP_200_OK)

class Ping(APIView):
    
    def get(self, request, format=None, *args, **kwargs):
        return Response("Pong", status=status.HTTP_200_OK)


class BasicDownload(APIView):  # https://youtu.be/C0DPdy98e4c
    
    def post(self, request, format=None, *args, **kwargs):
        
        print(request.body)
        
        payload = json.loads(request.body)
        
        with YoutubeDL() as ydl:
            ydl.download([payload['url']])
            
        return Response("Downloading", status=status.HTTP_200_OK)
    
class FlowDownload(APIView):  # https://youtu.be/C0DPdy98e4c

    def post(self, request, format=None, *args, **kwargs):
        
        try:
            payload = json.loads(request.body)
            flow_id = payload['flow_id']
            
            download_thread = threading.Thread(target=yt_dl_flow, args=(flow_id,))
            download_thread.start()

            return HttpResponse('Downloading', status=200)

        except KeyError as e:
            return HttpResponse('Invalid request data', status=400)


class Outlet(APIView):
    
    def get(self, request, format=None, *args, **kwargs):

        if len(request.body) != 0:
            parsed_json = json.loads(request.body)

            try:
                outlet_id = parsed_json['outlet_id']
            except KeyError as e:
                return HttpResponse('Invalid request data', status=400)

            # So we return the information about a particular Outlet

            outlet_object = get_object_or_404(OutletModel, id=outlet_id)

            outlet_json = serializers.serialize('json', [outlet_object])

            return JsonResponse(data=outlet_json, status=200)
        else:
            # JSON is empty, so we return the list of all Outlet objects

            outlet_objects = list(OutletModel.objects.all().values())
            

            if len(outlet_objects) > 0:
                outlet_jsons = json.dumps(outlet_objects)
                
            else:
                outlet_jsons = json.dumps([])
                

            return HttpResponse(content= outlet_jsons, status=200)
        
    def post(self, request, format=None, *args, **kwargs):

        try:
            payload = json.loads(request.body)
            name = payload['name']
            path = payload['path']
            video = payload['video']
            thumbnail = payload['thumbnail']
            info = payload['info']
            
            # Create the Flow in the databse
            new_outlet = OutletModel(name=name, path=path, video=video, thumbnail=thumbnail, info=info)
            new_outlet.save()

            return HttpResponse(status=201)

        except KeyError as e:
            return HttpResponse('Invalid request data or database faliure', status=400)
        
    def delete(self, request, format=None, *args, **kwargs):

        try:
            payload = json.loads(request.body)
            outlet_id = payload['outlet_id']

            # Find requested object
            outlet_object = get_object_or_404(OutletModel, id=outlet_id)
            outlet_object.delete()
            return HttpResponse(status=204)

        except KeyError as e:
            return HttpResponse('Invalid request data', status=400)


class Timer(APIView):
    
    def get(self, request, format=None, *args, **kwargs):

        if len(request.body) != 0:
            parsed_json = json.loads(request.body)

            try:
                timer_id = parsed_json['timer_id']
            except KeyError as e:
                return HttpResponse('Invalid request data', status=400)

            # So we return the information about a particular Timer

            timer_object = get_object_or_404(TimerModel, id=timer_id)

            timer_json = serializers.serialize('json', [timer_object])

            return JsonResponse(data=timer_json, status=200)
        else:
            # JSON is empty, so we return the list of all Timer objects

            timer_objects = list(TimerModel.objects.all().values())
        
            if len(timer_objects) > 0:
                outlet_jsons = json.dumps(timer_objects)
                
            else:
                timer_jsons = {}

            return HttpResponse(content=timer_jsons, status=200)

    def post(self, request, format=None, *args, **kwargs):
        
        try:
            payload = json.loads(request.body)
            flow_id = payload['flow_id']
            interval = int(payload['interval'])
            
            timer_id = str(uuid.uuid4())
            
            create_timer(interval, flow_id, timer_id)
            
            new_timer = TimerModel(timer_id=timer_id, interval=interval, last_run=timezone.now())
            new_timer.save()
            
            return JsonResponse(data={'timer_id': timer_id}, status=201)
        except KeyError as e:
            return HttpResponse('Invalid request data', status=400)
        
    def delete(self, request, format=None, *args, **kwargs):
        

        try:
            payload = json.loads(request.body)
            timer_id = payload['timer_id']

            is_deleted = stop_timer(timer_id)

            if is_deleted:

                try:
                    timer_object = TimerModel.objects.get(timer_id=timer_id)
                    timer_object.delete()
                except:
                    return HttpResponse('Could not find requested timer process', status=400)

                return JsonResponse(data={'success': True}, status=200)
            else:
                return HttpResponse('Could not find requested timer process', status=400)

        except KeyError as e:
            return HttpResponse('Invalid request data', status=400)


class Flow(APIView):
    
    @csrf_exempt
    def post(self, request, format=None, *args, **kwargs):

        
        try:
            payload = json.loads(request.body)
            name = payload['name']
            url = payload['url']
            my_type = payload['type']
            quality = payload['quality']
            outlet = int(payload['outlet'])
            interval = int(payload['interval'])
            
            flow_id = str(uuid.uuid4())
            
            
            # Make the timer post API call using async_to_sync()
            async_client = httpx.AsyncClient()
            response = async_to_sync(async_client.post)('http://127.0.0.1:8000/api/timer', json={'interval': interval, 'flow_id': flow_id})


            if response.status_code != 201:
                return HttpResponse('Failed to create timer', status=500)

            # Get objects from database
            timer_object = TimerModel.objects.get(timer_id = response.json()['timer_id'])
            outlet_object = OutletModel.objects.get(id = outlet)
            
            # Create the Flow in the databse
            new_flow = FlowModel(flow_id=flow_id, name=name, url=url, type=my_type, quality=quality, outlet=outlet_object, timer=timer_object)
            new_flow.save()
            
            requests.post('http://127.0.0.1:8000/api/flow_download', json={'flow_id': flow_id})
                        
            return JsonResponse(data={'flow_id': flow_id}, status=201)

        except KeyError as e:
            return HttpResponse('Invalid request data or database faliure', status=400)

    @csrf_exempt
    def delete(self, request, format=None, *args, **kwargs):

        try:
            payload = json.loads(request.body)
            flow_id = payload['id']
            
            # Find requested object
            flow_object = get_object_or_404(FlowModel, id=flow_id)
            
            # Make the timer delete API call
            response = requests.delete(
                'http://127.0.0.1:8000/api/timer', json={'timer_id': flow_object.timer.timer_id})

            # Check the response status code and raise ValidationError if not successful
            if not response.status_code // 100 == 2:  # check for 2XX status codes
                return HttpResponse('Failed to delete Timer', status=500)
            
            flow_object.delete()
            
            return HttpResponse('Deleted Flow and Timer', status=200)

        except KeyError as e:
            return HttpResponse('Invalid request data', status=400)

    def get(self, request, format=None, *args, **kwargs):
        
        if len(request.body) != 0:
            parsed_json = json.loads(request.body)

            try:
                flow_id = parsed_json['flow_id']
            except KeyError as e:
                return HttpResponse('Invalid request data', status=400)

            # So we return the information about a particular Flow

            flow_object = get_object_or_404(FlowModel, id=flow_id)

            flow_json = serializers.serialize('json', [flow_object])

            return JsonResponse(data=flow_json, status=200)
        else:
            # JSON is empty, so we return the list of all Flow objects

            flow_objects = list(FlowModel.objects.all().values())
        
            if len(flow_objects) > 0:
                flow_jsons = json.dumps(flow_objects)
                
            else:
                flow_jsons = json.dumps([])

            return HttpResponse(content=flow_jsons, status=200)

                    