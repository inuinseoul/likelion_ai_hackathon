from django.urls import path, include
from streamapp import views


urlpatterns = [
    path("", views.index, name="index"),
    path("camera_feed", views.camera_feed, name="camera_feed"),
]
