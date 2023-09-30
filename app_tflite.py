import cv2 as cv
import numpy as np
import time
import tensorflow as tf
from keras.models import load_model

KCmodel_path = "ml-models/model_unquant.tflite"

# Substitua 'seu_modelo.tflite' pelo caminho para o seu arquivo .tflite
modelo_tflite = 'ml-models/model_unquant.tflite'
interpreter = tf.lite.Interpreter(model_path=modelo_tflite)
interpreter.allocate_tensors()

# Obtenha os detalhes do tensor de entrada e saída
entrada_details = interpreter.get_input_details()
saida_details = interpreter.get_output_details()

video = cv.VideoCapture('videos/carPark.mp4')

if not video.isOpened():
    print('Erro ao carregar o vídeo.')
    exit()

while True:
    ret, image = video.read()
    #Rotina para verificar se o vídeo chegou ao fim e então terminar o loop ou reiniciar o vídeo
    if not ret:
       break
        # video.set(cv.CAP_PROP_POS_FRAMES, 0)
        # continue
    
    x1 = 46
    x2 = 156
    y1 = 100
    y2 = 147
    length_parking_space = 110
    distance_column_A_C = 348
    distance_column_A_E = 696
    distance_column_E_F = 40
    put_text_x1 = -33
    put_text_x2 = 113
    put_text_y = 15
    
    for i in range(1, 13, 1):
        #Coluna A
        cv.rectangle(image, (x1,y1), (x2,y2), (0,0,255), 2)
        crop_A = cv.resize(image[y1:y2, x1:x2], (224, 224))

        #Coluna B
        crop_B = cv.resize(image[y1:y2, x2:x2+length_parking_space], (224, 224))
        crop_B = cv.cvtColor(crop_B, cv.COLOR_BGR2RGB)
        crop_B = np.expand_dims(crop_B, axis=0)
        crop_B = crop_B.astype(entrada_details[0]['dtype'])
        # Alimente a imagem para o modelo
        interpreter.set_tensor(entrada_details[0]['index'], crop_B)
        # Execute a inferência
        interpreter.invoke()
        # Obtenha as saídas do modelo
        saida = interpreter.get_tensor(saida_details[0]['index'])
        # Verifique a classe com maior probabilidade
        classe_predita = np.argmax(saida)
        if classe_predita == 0:
            cv.rectangle(image, (x2,y1), (x2+length_parking_space,y2), (0,0,255), 2)
        elif classe_predita == 1:
            cv.rectangle(image, (x2,y1), (x2+length_parking_space,y2), (0,255,0), 2)


        if i != 9: #Posição 9 das colunas C e D não são vagas
            #Coluna C
            cv.rectangle(image, (x1+distance_column_A_C,y1), (x2+distance_column_A_C,y2), (0,0,255), 2)
            crop_C = cv.resize(image[y1:y2, x1+distance_column_A_C:x2+distance_column_A_C], (224, 224))

            #Coluna D
            cv.rectangle(image, (x2+distance_column_A_C,y1), (x2+distance_column_A_C+length_parking_space,y2), (0,0,255), 2)
            crop_D = cv.resize(image[y1:y2, x2+distance_column_A_C:x2+distance_column_A_C+length_parking_space], (224, 224))

        #Coluna E
        cv.rectangle(image, (x1+distance_column_A_E,y1), (x2+distance_column_A_E,y2), (0,0,255), 2)
        crop_E = cv.resize(image[y1:y2, x1+distance_column_A_E:x2+distance_column_A_E], (224, 224))
        
        if i != 1: #Na coluna F, posição, não há uma vaga
            #Coluna F
            cv.rectangle(image, (x2+distance_column_A_E+distance_column_E_F,y1), (x2+distance_column_A_E+length_parking_space+distance_column_E_F,y2), (0,0,255), 2)
            crop_F = cv.resize(image[y1:y2, x2+distance_column_A_E+distance_column_E_F:x2+distance_column_A_E+length_parking_space+distance_column_E_F], (224, 224))

        
        #Rotinas de rotulação de cada coluna do estacionamento
        cv.putText(image, f"a{i}", (x1+put_text_x1,y1+put_text_y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
        cv.putText(image, f"b{i}", (x2+put_text_x2,y1+put_text_y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
        if i != 9:
            cv.putText(image, f"c{i}", (x1+distance_column_A_C+put_text_x1,y1+put_text_y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
            cv.putText(image, f"d{i}", (x2+distance_column_A_C+put_text_x2,y1+put_text_y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
        cv.putText(image, f"e{i}", (x1+distance_column_A_E+put_text_x1,y1+put_text_y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
        if i != 1:
            cv.putText(image, f"f{i}", (x2+distance_column_A_E+put_text_x2+distance_column_E_F,y1+put_text_y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)

        #Atualização dos valores das ordenadas das vagas
        y1 += 47
        y2 += 47
        

    cv.imshow('Video', image)

    #time.sleep(0.02)

    #Rotina para parar a execução caso o usuário pressione a tecla ESC
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break

video.release()
