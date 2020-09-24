from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import imutils
import cv2, os
import numpy as np
from .models import Test
import random

modelPath = os.path.join(os.getcwd(), "models", "keras_model.h5")
myNet = load_model(modelPath)


class ClassifyMove(object):
    def __init__(self):
        self.vs = VideoStream(src=0).start()

    def __del__(self):
        cv2.destroyAllWindows()

    def classify_image(self, frame, myNet):
        images = []

        # 주어진 이미지(프레임) 전처리
        image = frame
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))
        image = img_to_array(image)
        image = preprocess_input(image)

        # 전처리한 이미지(프레임) images에 추가, 전처리
        images.append(image)
        images = np.array(images, dtype="float32")

        # 최종 예측
        preds = myNet.predict(images, batch_size=32)

        # 결과 리턴
        return preds[0]

    def get_frame(self):
        # 카메라로부터 프레임 불러와서 전처리
        frame = self.vs.read()
        frame = cv2.resize(frame, (800, 600))
        frame = cv2.flip(frame, 1)

        # classify_image 함수를 통해 preds 불러오고 각 값 반환
        preds = self.classify_image(frame, myNet)
        (basic, cheers, drink, heart) = preds
        preds = list(preds)
        labels = ["basic", "cheers", "drink", "heart"]

        # 결과에 따라 label, color 설정
        max_index = np.argmax(np.array(preds))
        label = labels[max_index]
        if preds[max_index] < 0.9:
            label = "basic"
        color = (0, 255, 0)

        if label == "basic":
            Test.objects.filter(pk=1).update(
                state=0,
            )
        elif label == "cheers":
            state = Test.objects.get(pk=2).state
            Test.objects.filter(pk=2).update(
                state=((int(state) + 1) % 70),
            )
            imgPath = f"C:/img/heart ({(int(state)+1) % 70}).png"
            imgMustache = cv2.imread(imgPath)
            img2_resized = cv2.resize(imgMustache, (800, 600))
            frame = cv2.bitwise_and(img2_resized, frame)
        elif label == "drink":
            state = Test.objects.get(pk=3).state
            Test.objects.filter(pk=3).update(
                state=((int(state) + 1) % 70),
            )
            imgPath = f"C:/img/heart ({(int(state)+1) % 70}).png"
            imgMustache = cv2.imread(imgPath)
            img2_resized = cv2.resize(imgMustache, (800, 600))
            frame = cv2.bitwise_and(img2_resized, frame)
        elif label == "heart":
            state = Test.objects.get(pk=4).state
            Test.objects.filter(pk=4).update(
                state=((int(state) + 1) % 70),
            )
            imgPath = f"C:/img/heart ({(int(state)+1) % 70}).png"
            imgMustache = cv2.imread(imgPath)
            img2_resized = cv2.resize(imgMustache, (800, 600))
            frame = cv2.bitwise_and(img2_resized, frame)

        # 최종 라벨 결정
        label = "{}: {:.2f}%".format(label, max(basic, cheers, drink, heart) * 100)

        # 웹캠 위에 텍스트(label) 출력되도록 설정
        cv2.putText(frame, label, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # 결과 반환
        ret, jpeg = cv2.imencode(".jpg", frame)

        # 최종 리턴
        return jpeg.tobytes()
