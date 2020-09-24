from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import imutils
import cv2, os, urllib
import numpy as np
from .models import Test

modelPath = os.path.join(os.getcwd(), "models", "keras_model.h5")
myNet = load_model(modelPath)


class han_ClassifyMove(object):
    def __init__(self):
        pass

    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        label = Test.objects.get(pk=12).state
        imgPath = f"./img/han/wait.png"
        frame = cv2.imread(imgPath)
        frame = cv2.resize(frame, (800, 600))
        if Test.objects.get(pk=13).state:
            if label == 1:
                state = Test.objects.get(pk=8).state
                Test.objects.filter(pk=8).update(
                    state=((int(state) + 1) % 450),
                )
                number = int((int(state) + 1) / 3) % 150
                imgPath = f"./img/han/han_basic ({number}).png"
                imgMustache = cv2.imread(imgPath)
                frame = cv2.resize(imgMustache, (800, 600))
            elif label == 2:
                state = Test.objects.get(pk=9).state
                Test.objects.filter(pk=9).update(
                    state=((int(state) + 1) % 66),
                )
                number = int((int(state) + 1) / 3) % 22
                imgPath = f"./img/han/han_cheers ({number}).png"
                imgMustache = cv2.imread(imgPath)
                frame = cv2.resize(imgMustache, (800, 600))
            elif label == 3:
                state = Test.objects.get(pk=10).state
                Test.objects.filter(pk=10).update(
                    state=((int(state) + 1) % 84),
                )
                number = int((int(state) + 1) / 3) % 28
                imgPath = f"./img/han/han_drink ({number}).png"
                imgMustache = cv2.imread(imgPath)
                frame = cv2.resize(imgMustache, (800, 600))
            elif label == 4:
                state = Test.objects.get(pk=11).state
                Test.objects.filter(pk=11).update(
                    state=((int(state) + 1) % 51),
                )
                number = int((int(state) + 1) / 3) % 17
                imgPath = f"./img/han/han_heart ({number}).png"
                imgMustache = cv2.imread(imgPath)
                frame = cv2.resize(imgMustache, (800, 600))

        # 결과 반환
        ret, jpeg = cv2.imencode(".jpg", frame)

        # 최종 리턴
        return jpeg.tobytes()


class IPWebCam(object):
    def __init__(self):
        self.url = "http://192.168.35.193:8080/shot.jpg"

    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        imgResp = urllib.request.urlopen(self.url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)

        resize = cv2.resize(img, (800, 600), interpolation=cv2.INTER_LINEAR)
        frame_flip = cv2.flip(resize, 1)

        if Test.objects.get(pk=5).state:
            imgPath = f"./img/cards/card ({Test.objects.get(pk=5).state}).png"
            imgMustache = cv2.imread(imgPath)
            img2_resized = cv2.resize(imgMustache, (800, 600))
            frame_flip = cv2.bitwise_and(img2_resized, frame_flip)

        ret, jpeg = cv2.imencode(".jpg", frame_flip)
        return jpeg.tobytes()


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

        if Test.objects.get(pk=6).state:
            if Test.objects.get(pk=7).state:
                imgPath = f"./img/cards/card ({Test.objects.get(pk=6).state}).png"
                imgMustache = cv2.imread(imgPath)
                img2_resized = cv2.resize(imgMustache, (800, 600))
                frame = cv2.bitwise_and(img2_resized, frame)
            else:
                imgPath = f"./img/cards/card (14).png"
                imgMustache = cv2.imread(imgPath)
                img2_resized = cv2.resize(imgMustache, (800, 600))
                frame = cv2.bitwise_and(img2_resized, frame)
        if label == "basic":
            Test.objects.filter(pk=1).update(
                state=0,
            )
            Test.objects.filter(pk=12).update(
                state=1,
            )
        elif label == "cheers":
            state = Test.objects.get(pk=2).state
            Test.objects.filter(pk=2).update(
                state=((int(state) + 1) % 70),
            )
            imgPath = f"./img/cheers/cheers ({(int(state)+1) % 11}).png"
            imgMustache = cv2.imread(imgPath)
            img2_resized = cv2.resize(imgMustache, (800, 600))
            frame = cv2.bitwise_and(img2_resized, frame)
            Test.objects.filter(pk=12).update(
                state=2,
            )
        elif label == "drink":
            state = Test.objects.get(pk=3).state
            Test.objects.filter(pk=3).update(
                state=((int(state) + 1) % 70),
            )
            imgPath = f"./img/drink/drink ({(int(state)+1) % 125}).png"
            imgMustache = cv2.imread(imgPath)
            img2_resized = cv2.resize(imgMustache, (800, 600))
            frame = cv2.bitwise_and(img2_resized, frame)
            Test.objects.filter(pk=12).update(
                state=3,
            )
        elif label == "heart":
            state = Test.objects.get(pk=4).state
            Test.objects.filter(pk=4).update(
                state=((int(state) + 1) % 70),
            )
            imgPath = f"./img/heart/heart ({(int(state)+1) % 68}).png"
            imgMustache = cv2.imread(imgPath)
            img2_resized = cv2.resize(imgMustache, (800, 600))
            frame = cv2.bitwise_and(img2_resized, frame)
            Test.objects.filter(pk=12).update(
                state=4,
            )

        # 최종 라벨 결정
        label = "{}: {:.2f}%".format(label, max(basic, cheers, drink, heart) * 100)

        # 웹캠 위에 텍스트(label) 출력되도록 설정
        cv2.putText(frame, label, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # 결과 반환
        ret, jpeg = cv2.imencode(".jpg", frame)

        # 최종 리턴
        return jpeg.tobytes()
