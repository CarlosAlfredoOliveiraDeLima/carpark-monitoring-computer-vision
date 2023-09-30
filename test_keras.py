from keras.models import load_model
import numpy as np
import cv2 as cv

model = load_model('ml-models\keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

#cap = cv2.VideoCapture(0)
img = cv.imread('img_tests\\v-4.jpg')

classes = ['OC','LV']


image_array = np.asarray(img)
normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
data[0] = normalized_image_array
prediction = model.predict(data)
indexVal = np.argmax(prediction)

cv.putText(img, str(classes[indexVal]),(10,60), cv.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 2)
print(classes[indexVal])

cv.imshow('img',img)
cv.waitKey(0)
