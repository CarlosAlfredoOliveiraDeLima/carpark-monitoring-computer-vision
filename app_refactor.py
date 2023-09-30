import cv2 as cv
import numpy as np
import time
from keras.models import load_model
import tensorflow as tf

#Numpy é usado tanto no OpenCV como no Keras, aqui nós configuramos que a impressão de números em arrays sejam exibidos sem notação científica
np.set_printoptions(suppress=True)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

classes = ['vaga_ocupada', 'vaga_livre']

model = load_model("ml-models/keras_model.h5")

video = cv.VideoCapture('videos/carPark.mp4')

if not video.isOpened():
    print('Erro ao carregar o vídeo.')
    exit()


# Configuração do VideoWriter
fourcc = cv.VideoWriter_fourcc(*'MJPG')  # Código do codec MJPEG
fps = 10  # Taxa de quadros por segundo
frameSize = (1100, 720)  # Tamanho dos quadros
isColor = True  # Vídeo colorido
# Crie o objeto VideoWriter
out = cv.VideoWriter('output_video.avi', fourcc, fps, frameSize, isColor)

while True:
    red_count = 0
    green_count = 0
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
    
    preprocessed_images = []

    for i in range(1, 13, 1):
        crops = [
            image[y1:y2, x1:x2],
            image[y1:y2, x2:x2 + length_parking_space],
            image[y1:y2, x1 + distance_column_A_C:x2 + distance_column_A_C],
            image[y1:y2, x2 + distance_column_A_C:x2 + distance_column_A_C + length_parking_space],
            image[y1:y2, x1 + distance_column_A_E:x2 + distance_column_A_E],
            image[y1:y2, x2 + distance_column_A_E + distance_column_E_F:x2 + distance_column_A_E + length_parking_space + distance_column_E_F]
        ]

        for crop in crops:
            crop_resized = cv.resize(crop, (224, 224))
            image_array = np.asarray(crop_resized)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            preprocessed_images.append(normalized_image_array)

    # Faça as previsões em lote
        predictions = model.predict(np.array(preprocessed_images))

        # print(predictions)
        # for x in range(6):
        #     print(np.argmax(predictions[x]))
        
        
        for index_column in range(6):
            #print(index_column)
            # prediction = predictions[index_column]
            result_prediction = np.argmax(predictions[index_column])

            if index_column == 0:
                if result_prediction == 0:
                    cv.rectangle(image, (x1,y1+1), (x2,y2-1), (0,0,255), 2)
                    red_count += 1
                else:
                    cv.rectangle(image, (x1,y1+1), (x2,y2-1), (0,255,0), 2)
                    green_count += 1
            if index_column == 1:
                if result_prediction == 0:
                    cv.rectangle(image, (x2,y1+1), (x2+length_parking_space,y2-1), (0,0,255), 2)
                    red_count += 1
                else:
                    cv.rectangle(image, (x2,y1+1), (x2+length_parking_space,y2-1), (0,255,0), 2)
                    green_count += 1
        
            if i != 9: #Posição 9 das colunas C e D não são vagas
                if index_column == 2:
                    if result_prediction == 0:
                        cv.rectangle(image, (x1+distance_column_A_C,y1+1), (x2+distance_column_A_C,y2-1), (0,0,255), 2)
                        red_count += 1
                    else:
                        cv.rectangle(image, (x1+distance_column_A_C,y1+1), (x2+distance_column_A_C,y2-1), (0,255,0), 2)
                        green_count += 1

                if index_column == 3:
                    if result_prediction == 0:
                        cv.rectangle(image, (x2+distance_column_A_C,y1+1), (x2+distance_column_A_C+length_parking_space,y2-1), (0,0,255), 2)
                        red_count += 1
                    else:
                        cv.rectangle(image, (x2+distance_column_A_C,y1+1), (x2+distance_column_A_C+length_parking_space,y2-1), (0,255,0), 2)
                        green_count += 1

            if index_column == 4:
                if result_prediction == 0:
                    cv.rectangle(image, (x1+distance_column_A_E,y1), (x2+distance_column_A_E,y2), (0,0,255), 2)
                    red_count += 1
                else:
                    cv.rectangle(image, (x1+distance_column_A_E,y1), (x2+distance_column_A_E,y2), (0,255,0), 2)
                    green_count += 1

            if i != 1: #Na coluna F, posição, não há uma vaga
                if index_column == 5:    
                    if result_prediction == 0:
                        cv.rectangle(image, (x2+distance_column_A_E+distance_column_E_F,y1+1), (x2+distance_column_A_E+length_parking_space+distance_column_E_F,y2-1), (0,0,255), 2)
                        red_count += 1
                    else:
                        cv.rectangle(image, (x2+distance_column_A_E+distance_column_E_F,y1+1), (x2+distance_column_A_E+length_parking_space+distance_column_E_F,y2-1), (0,255,0), 2)
                        green_count += 1

        
        #Rotinas de rotulação de cada coluna do estacionamento
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
        
    print(red_count)
    print(green_count)
    cv.putText(image, f"Vagas Ocupadas {red_count}", (100,50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    cv.putText(image, f"Vagas Livres: {green_count}", (550,50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    cv.imshow('Video', image)
    #out.write(image)

    #time.sleep(1)

    #Rotina para parar a execução caso o usuário pressione a tecla ESC
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break

out.release()
video.release()
