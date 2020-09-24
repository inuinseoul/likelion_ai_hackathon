from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from streamapp.camera import ClassifyMove
from .models import Test

# Create your views here.


def index(request):
    if not (Test.objects.filter(pk=1)):
        Test.objects.create(
            state=0,
        )
        Test.objects.create(
            state=0,
        )
        Test.objects.create(
            state=0,
        )
        Test.objects.create(
            state=0,
        )
    return render(request, "streamapp/home.html")


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")


def camera_feed(request):
    return StreamingHttpResponse(
        gen(ClassifyMove()), content_type="multipart/x-mixed-replace; boundary=frame"
    )
