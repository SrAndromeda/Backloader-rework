import httpx
import json
import requests
from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse


async def dashboardView(request, **kwargs):

    response = requests.get('http://127.0.0.1:8000/api/ping')
    response = response.text

    return render(request, 'home.html', {'response': response})


async def flowsView(request, **kwargs):

    response = requests.get('http://127.0.0.1:8000/api/flow')
    processed = json.loads(response.text)

    return render(request, 'flows/flows.html', {'flows': processed})


class CreateFlowForm(forms.Form):

    QUALITY_CHOICES = [
        ('a', 'Audio'), 
        ('720', '720p'), 
        ('1080', '1080p'), 
        ('1440', '1440p'), 
        ('2160', '4k'), 
        ('max', 'Best')
    ]

    TYPE_CHOICES = [
        ('p', 'Playlist'), 
        ('c', 'Channel')
    ]

    name = forms.CharField(max_length=100)
    url = forms.URLField()
    type = forms.ChoiceField(choices=TYPE_CHOICES)
    quality = forms.ChoiceField(choices=QUALITY_CHOICES)
    outlet = forms.ChoiceField(choices=[])
    interval = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # make API request to get outlets data
        response = requests.get('http://127.0.0.1:8000/api/outlet')
        try:
            outlets = [(outlet['id'], outlet['name'])
                   for outlet in response.json()]
        except:
            outlets = [(42, 'Nigga')]

        # populate choices for outlet field
        self.fields['outlet'].choices = outlets
    
    def is_valid(self):
        return True
        

    def submit(self):
        api_url = 'http://127.0.0.1:8000/api/flow/'

        # get form data

        name = self.cleaned_data['name']
        url = self.cleaned_data['url']
        type = self.cleaned_data['type']
        quality = self.cleaned_data['quality']
        outlet = self.cleaned_data['outlet']
        interval = self.cleaned_data['interval']

        # prepare post data and make API call
        data = {
            'name': name,
            'url': url,
            'type': type,
            'quality': quality,
            'outlet': outlet,
            'interval': interval,
        }
        
        response = requests.post(api_url, data=data)
        response.raise_for_status()


def createFlowView(request, **kwargs):

    form = CreateFlowForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        form.submit()
        return redirect(reverse('flows'))

    return render(request, 'flows/create.html', {'form': form})


async def outletsView(request, **kwargs):
    async with httpx.AsyncClient() as client:
        response = await client.get('http://127.0.0.1:8000/api/outlet')
        if response.status_code != httpx.codes.OK:
            processed = {}
        else:
            processed = response.json()

        print(processed)

    return render(request, 'outlets/outlets.html', {'outlets': processed})


class CreateOutletForm(forms.Form):
    name = forms.CharField(max_length=255)
    path = forms.CharField(max_length=255)
    video = forms.CharField(max_length=255)
    info = forms.CharField(max_length=255)
    temp = forms.CharField(max_length=255)
    
    def is_valid(self):
        
        return True
    
    def submit(self):
        api_url = 'http://127.0.0.1:8000/api/outlet'

        cleaned_data = self.data

        # get form data
        name = cleaned_data['name']
        path = cleaned_data['path']
        video = cleaned_data['video']
        info = cleaned_data['info']
        temp = cleaned_data['temp']
        
        


        # prepare post data and make API call
        data = {
            'name': name,
            'path': path,
            'video': video,
            'info': info,
            'temp': temp,
        }
        
        print(data) 

        response = requests.post(api_url, json=data)
        response.raise_for_status()
    
    
def createOutletView(request):
    
    form = CreateOutletForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        
        print(form.is_valid())
        
        form.submit()
        return redirect(reverse('outlets'))
    else:
        form = CreateOutletForm()
    return render(request, 'outlets/create.html', {'form': form})


async def settingsView(request, **kwargs):

    response = requests.get('http://127.0.0.1:8000/api/ping')
    response_text = response.text

    return render(request, 'settings.html', {'response': response_text})



