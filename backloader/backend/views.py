from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core import serializers
from asgiref.sync import async_to_sync
from yt_dlp import YoutubeDL
import json
import os
import PIL
import threading
import uuid
import httpx
import requests


from .models import Timer as TimerModel  
from .models import Flow as FlowModel
from .models import Outlet as OutletModel


def timer_function(timer_id, interval, flow_id):

    print(str(timer_id) + " executed with flow id " + str(flow_id))
    
    timer_object = TimerModel.objects.get(timer_id=timer_id)
    timer_object.last_run = timezone.now()
    timer_object.save()
    
    timer_thread = threading.Timer(interval, timer_function, args=(timer_id, interval, flow_id))
    timer_thread.name = f"timer_{timer_id}"
    timer_thread.start()
    

def create_timer(interval, flow_id):        
    timer_id = str(uuid.uuid4())
    timer_thread = threading.Timer( interval, timer_function, args=(timer_id, interval, flow_id))
    timer_thread.name = f"timer_{timer_id}"
    timer_thread.start()
        
    return timer_id


def stop_timer(timer_id):
    try:
        #timer = Timer.objects.get(timer_id=timer_id)
        
        for thread in threading.enumerate():
            if thread.name == f"timer_{timer_id}":
                thread.cancel()
        
        return True
                
    except Timer.DoesNotExist:
        print("Could not find thread:" + f"timer_{timer_id}")
        
        return False
        
        


# Create your views here.


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
                outlet_jsons = {}
                

            return HttpResponse(content= outlet_jsons, status=200)
        
    def post(self, request, format=None, *args, **kwargs):

        try:
            payload = json.loads(request.body)
            name = payload['name']
            path = payload['path']
            video = payload['video']
            info = payload['info']
            temp = payload['temp']
            
            # Create the Flow in the databse
            new_outlet = OutletModel(name=name, path=path, video=video, info=info, temp=temp)
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
            
            timer_id = create_timer(interval, flow_id)
            
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


            if response.status_code != httpx.codes.OK or response.text == '':
                return HttpResponse('Failed to create timer', status=500)

            # Get objects from database
            timer_object = TimerModel.objects.get(timer_id = response.json()['timer_id'])
            outlet_object = OutletModel.objects.get(id = outlet)
            
            # Create the Flow in the databse
            new_flow = FlowModel(flow_id=flow_id, name=name, url=url, type=my_type, quality=quality, outlet=outlet_object, timer=timer_object)
            new_flow.save()
                        
            return JsonResponse(data={'flow_id': flow_id}, status=201)

        except KeyError as e:
            return HttpResponse('Invalid request data or database faliure', status=400)

        
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
                flow_jsons = {}

            return HttpResponse(content=flow_jsons, status=200)

                    