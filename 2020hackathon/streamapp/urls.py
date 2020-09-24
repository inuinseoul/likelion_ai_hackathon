from django.urls import path, include
from streamapp import views


urlpatterns = [
    path("", views.index, name="index"),
    path("camera_feed", views.camera_feed, name="camera_feed"),
    path("webcam_feed", views.webcam_feed, name="webcam_feed"),
    path("han_camera_feed", views.han_camera_feed, name="han_camera_feed"),
    path("poker_start", views.poker_start, name="poker_start"),
    path("poker_open", views.poker_open, name="poker_open"),
    path("han_onoff", views.han_onoff, name="han_onoff"),
]
