from django.urls import path
from . import views

urlpatterns = [
    path('ping', views.Ping.as_view()),
    path('initialize', views.Initialize.as_view()),
    path('download', views.BasicDownload.as_view()),
    path('timer', views.Timer.as_view()),
    path('flow', views.Flow.as_view()),
    path('flow_download', views.FlowDownload.as_view()),
    path('outlet', views.Outlet.as_view()),
]

# views.initialize()