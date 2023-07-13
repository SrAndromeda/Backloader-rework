from . import views
from django.urls import path


urlpatterns = [
    path('', views.dashboardView,  name="dashboard"),
    path('flows/', views.flowsView,  name="flows"),
    path('flows/create/', views.createFlowView,  name="flows-create"),
    path('outlets/', views.outletsView,  name="outlets"),
    path('outlets/create', views.createOutletView,  name="outlets-create"),
    path('settings/', views.settingsView,  name="settings"),
]
