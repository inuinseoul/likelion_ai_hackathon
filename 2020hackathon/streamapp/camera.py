from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import imutils
import cv2, os, urllib.request
import numpy as np
from django.conf import settings
import numpy as np
import cv2

face_detection_videocam = cv2.CascadeClassifier(
    os.path.join(
        settings.BASE_DIR, "opencv_haarcascade_data/haarcascade_frontalface_default.xml"
    )
)
face_detection_webcam = cv2.CascadeClassifier(
    os.path.join(
        settings.BASE_DIR, "opencv_haarcascade_data/haarcascade_frontalface_default.xml"
    )
)
# load our serialized face detector model from disk
prototxtPath = os.path.sep.join([settings.BASE_DIR, "face_detector/deploy.prototxt"])
weightsPath = os.path.sep.join(
    [settings.BASE_DIR, "face_detector/res10_300x300_ssd_iter_140000.caffemodel"]
)
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
maskNet = load_model(
    os.path.join(settings.BASE_DIR, "face_detector/mask_detector.model")
)
modelPath = os.path.join(os.getcwd(), "models", "keras_model.h5")
myNet = load_model(modelPath)


class MaskDetect(object):
    def __init__(self):
        self.vs = VideoStream(src=0).start()

    def __del__(self):
        cv2.destroyAllWindows()

    def detect_and_predict_mask(self, frame, myNet):
        # grab the dimensions of the frame and then construct a blob
        # from it
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

        # pass the blob through the network and obtain the face detections
        faceNet.setInput(blob)
        detections = faceNet.forward()
        # initialize our list of faces, their corresponding locations,
        # and the list of predictions from our face mask network
        faces = []
        preds = []

        # extract the face ROI, convert it from BGR to RGB channel
        # ordering, resize it to 224x224, and preprocess it
        face = frame
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        face = cv2.resize(face, (224, 224))
        face = img_to_array(face)
        face = preprocess_input(face)

        # add the face and bounding boxes to their respective
        # lists
        faces.append(face)
        # for faster inference we'll make batch predictions on *all*
        # faces at the same time rather than one-by-one predictions
        # in the above `for` loop
        faces = np.array(faces, dtype="float32")
        preds = myNet.predict(faces, batch_size=32)

        # return a 2-tuple of the face locations and their corresponding
        # locations
        return preds

    def get_frame(self):
        frame = self.vs.read()
        frame = imutils.resize(frame, width=650)
        frame = cv2.flip(frame, 1)
        # detect faces in the frame and determine if they are wearing a
        # face mask or not
        pred = self.detect_and_predict_mask(frame, myNet)

        # loop over the detected face locations and their corresponding
        # locations
        # unpack the bounding box and predictions
        (basic, thumbsup) = pred[0]

        # determine the class label and color we'll use to draw
        # the bounding box and text
        label = "basic" if basic > thumbsup else "thumbsup"
        color = (0, 255, 0) if label == "basic" else (0, 0, 255)

        # include the probability in the label
        label = "{}: {:.2f}%".format(label, max(basic, thumbsup) * 100)

        # display the label and bounding box rectangle on the output
        # frame
        cv2.putText(frame, label, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        ret, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes()
