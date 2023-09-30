import cv2 as cv
import numpy as np
import tensorflow as tf
from keras.models import load_model


#TFLite
modelo_tflite = 'ml-models/model_unquant.tflite'
interpreter = tf.lite.Interpreter(model_path=modelo_tflite)
interpreter.allocate_tensors()
# Obtenha os detalhes do tensor de entrada e saída
entrada_details = interpreter.get_input_details()
saida_details = interpreter.get_output_details()
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


image = cv.imread('teste_imagens\o7.jpg')


crop_B = image
image_array = np.asarray(crop_B)
normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
data[0] = normalized_image_array
interpreter.set_tensor(entrada_details[0]['index'], data)
interpreter.invoke()
saida = interpreter.get_tensor(saida_details[0]['index'])
print(saida)
classe_predita = np.argmax(saida)

if classe_predita == 0:
    print('ocupada')
elif classe_predita == 1:
    print('livre')

cv.imshow('Vaga', image)

cv.waitKey()