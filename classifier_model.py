
import numpy as np
import tensorflow as tf

modelo_tflite = 'ml-models/model_unquant.tflite'
interpreter = tf.lite.Interpreter(model_path=modelo_tflite)
interpreter.allocate_tensors()
entrada_details = interpreter.get_input_details()
saida_details = interpreter.get_output_details()
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

def image_classifier(img_crop):
    data[0] = (np.asarray(img_crop).astype(np.float32) / 127.0) - 1
    interpreter.set_tensor(entrada_details[0]['index'], data)
    interpreter.invoke()
    saida = interpreter.get_tensor(saida_details[0]['index'])
    return np.argmax(saida)