from django.http import request
from django.shortcuts import render
from django.http import JsonResponse
from django.http.response import StreamingHttpResponse
from streamapp.camera import ClassifyMove, IPWebCam, han_ClassifyMove
from .models import Test
import random
import numpy as np
import re
import pandas as pd
import csv
from .models import Alcohol, Cook
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django_pandas.io import read_frame

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


def han_onoff(request):
    if Test.objects.get(pk=13).state:
        Test.objects.filter(pk=13).update(
            state=0,
        )
    else:
        Test.objects.filter(pk=13).update(
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
    if not (Test.objects.filter(pk=8)):
        Test.objects.create(
            state=0,
        )
        # 한가인기본
    if not (Test.objects.filter(pk=9)):
        Test.objects.create(
            state=0,
        )
        # 한가인 짠
    if not (Test.objects.filter(pk=10)):
        Test.objects.create(
            state=0,
        )
        # 한가인 마신다
    if not (Test.objects.filter(pk=11)):
        Test.objects.create(
            state=0,
        )
        # 한가인 하트
    if not (Test.objects.filter(pk=12)):
        Test.objects.create(
            state=0,
        )
        # 사용자 상태
    if not (Test.objects.filter(pk=13)):
        Test.objects.create(
            state=0,
        )
        # 한가인켜기끄기
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


def han_camera_feed(request):
    return StreamingHttpResponse(
        gen(han_ClassifyMove()),
        content_type="multipart/x-mixed-replace; boundary=frame",
    )

#안주부분입니다.
def cook(request):
    
    if request.method == "POST": 
        cook_list = Cook.objects.all()
        data = read_frame(cook_list)

        tfidf_vec = TfidfVectorizer()
        tfidf_matrix = tfidf_vec.fit_transform(data['tag'])

        genres_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
        similar_index = np.argsort(-genres_similarity)

        input_cook = request.POST['input_cook']

        cook_index = data[data['food'] == input_cook].index.values
        similar_cook = similar_index[cook_index, :10]

        similar_cook_index = similar_cook.reshape(-1)
        lst = []
        links = data.iloc[similar_cook_index,1].values.tolist()
        foods = data.iloc[similar_cook_index,2].values.tolist()
        imgs = data.iloc[similar_cook_index,3].values.tolist()
        for i in range(5):
            lst.append(
                {
                    "link": links[i],
                    "food": foods[i],
                    "img": imgs[i],
                }
            )

        context = {
            "lst" : lst
        }

        return render(request,'streamapp/cook.html',context)

    return render(request, 'streamapp/cook.html')

def alcohol_recommend(request):
    if request.method == "POST": 
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

        input_beer = request.POST['input_beer']

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

        return render(request, "streamapp/cook.html", context)  
    return render(request, 'streamapp/cook.html')