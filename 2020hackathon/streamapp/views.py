from django.http import request
from django.shortcuts import render
from django.http import JsonResponse
from django.http.response import StreamingHttpResponse
from streamapp.camera import ClassifyMove, IPWebCam
from .models import Test
import random

# Create your views here.


def poker_start(request):
    if Test.objects.get(pk=5).state:
        Test.objects.filter(pk=5).update(
            state=0,
        )
    else:
        Test.objects.filter(pk=5).update(
            state=random.randrange(1, 14),
        )
    if Test.objects.get(pk=6).state:
        Test.objects.filter(pk=6).update(
            state=0,
        )
    else:
        Test.objects.filter(pk=6).update(
            state=random.randrange(1, 14),
        )
    return JsonResponse({}, status=204)


def poker_open(request):
    if Test.objects.get(pk=7).state:
        Test.objects.filter(pk=7).update(
            state=0,
        )
    else:
        Test.objects.filter(pk=7).update(
            state=1,
        )
    return JsonResponse({}, status=204)


def index(request):
    if not (Test.objects.filter(pk=1)):
        Test.objects.create(
            state=0,
        )
        # 기본
        Test.objects.create(
            state=0,
        )
        # 짠
        Test.objects.create(
            state=0,
        )
        # 마신다
        Test.objects.create(
            state=0,
        )
        # 내카드번호
        Test.objects.create(
            state=0,
        )
        # 상대카드번호
        Test.objects.create(
            state=0,
        )
        # 내카드번호
    if not (Test.objects.filter(pk=7)):
        Test.objects.create(
            state=0,
        )
        # 내 카드 공개여부
    return render(request, "streamapp/home.html")


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")


def webcam_feed(request):
    return StreamingHttpResponse(
        gen(IPWebCam()), content_type="multipart/x-mixed-replace; boundary=frame"
    )


def camera_feed(request):
    return StreamingHttpResponse(
        gen(ClassifyMove()), content_type="multipart/x-mixed-replace; boundary=frame"
    )
