from django.urls import path, include
from streamapp import views



urlpatterns = [
    path("", views.index, name="index"),
    path("camera_feed", views.camera_feed, name="camera_feed"),
    path("webcam_feed", views.webcam_feed, name="webcam_feed"),
    path("poker_start", views.poker_start, name="poker_start"),
    path("poker_open", views.poker_open, name="poker_open"),
    path("alcohol_recommend", views.alcohol_recommend, name="alcohol_recommend"),
]
