from django.http import request
from django.shortcuts import render
from django.http import JsonResponse
from django.http.response import StreamingHttpResponse
from streamapp.camera import ClassifyMove, IPWebCam
from streamapp.models import Test, Alcohol
import random
from django_pandas.io import read_frame



from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

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

def camera_feed(request):
    return StreamingHttpResponse(
        gen(ClassifyMove()), content_type="multipart/x-mixed-replace; boundary=frame"
    )


def alcohol_recommend(request):
    beer = Alcohol.objects.all()
    df0 = read_frame(beer)

    beer = df0.loc[
        :,
            ["nation",
            "name",
            "alcohol_type",
            "tag",
            "alcohol",
        ],
    ]

    beer['tag'] = beer['tag'].str.replace(',',' ')

    tfidf_vec = TfidfVectorizer(ngram_range=(1, 3))
    tfidf_matrix = tfidf_vec.fit_transform(beer['tag'])

    genres_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)

    similar_index = np.argsort(-genres_similarity)

    input_beer = '이슬톡톡'

    beer_index = beer[beer['name']==input_beer].index.values
    similar_beer = similar_index[beer_index, :5]

    similar_beer_index = similar_beer.reshape(-1)
    top5 = pd.DataFrame(beer.iloc[similar_beer_index])
    top5.reset_index(drop=True, inplace=True)
    result_list = [] 

    for i in range(5):
            result_list.append(
                {
                    "nation": top5["nation"][i],
                    "name": top5["name"][i],
                    "alcohol_type": top5["alcohol_type"][i],
                    "tag": top5["tag"][i],
                    "alcohol": top5["alcohol"][i],
                }
            )
    

    context = {"result_list":result_list}

    return render(request, "recommend.html", context)