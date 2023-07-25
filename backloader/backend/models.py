from django.db import models

# Create your models here.

class Outlet(models.Model):
    name = models.CharField(max_length=128)
    path = models.TextField()
    video = models.TextField()
    thumbnail = models.TextField(null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    
class Timer(models.Model):
    timer_id = models.TextField()
    interval = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_run = models.DateTimeField()
    
class Flow(models.Model):
    flow_id = models.TextField()
    name = models.CharField(max_length=128)
    url = models.TextField()
    type = models.CharField(max_length=1, choices=(('p','Playlist'), ('c', 'Channel')))
    quality = models.CharField(max_length=4, choices=(('a', 'Audio'), ('720', '720p'), ('1080', '1080p'), ('1440', '1440p'), ('2160', '4k'), ('max', 'Best')))
    outlet = models.ForeignKey(Outlet, on_delete=models.DO_NOTHING)
    timer = models.ForeignKey(Timer, on_delete=models.CASCADE)


