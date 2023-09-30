import cv2 as cv
import numpy as np
import time
import tensorflow as tf
from keras.models import load_model


# Substitua 'seu_modelo.tflite' pelo caminho para o seu arquivo .tflite
modelo_tflite = 'ml-models/model_unquant.tflite'
interpreter = tf.lite.Interpreter(model_path=modelo_tflite)
interpreter.allocate_tensors()

# Obtenha os detalhes do tensor de entrada e saída
entrada_details = interpreter.get_input_details()
saida_details = interpreter.get_output_details()
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

video = cv.VideoCapture('videos/carPark.mp4')

if not video.isOpened():
    print('Erro ao carregar o vídeo.')
    exit()

# Configuração do VideoWriter
fourcc = cv.VideoWriter_fourcc(*'MJPG')  # Código do codec MJPEG
fps = 2  # Taxa de quadros por segundo
frameSize = (1100, 720)  # Tamanho dos quadros
isColor = True  # Vídeo colorido
# Crie o objeto VideoWriter
out = cv.VideoWriter('output_video.avi', fourcc, fps, frameSize, isColor)

frame_pular = 4
frame_count = 0
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
    
    if frame_count == 1 or frame_count % frame_pular == 0:
        for i in range(1, 13, 1):  
            #Coluna A
            cv.rectangle(image, (x1,y1), (x2,y2), (0,0,255), 2)
            crop_A = cv.resize(image[y1:y2, x1:x2], (224, 224))
            image_array = np.asarray(crop_A)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            data[0] = normalized_image_array
            interpreter.set_tensor(entrada_details[0]['index'], data)
            interpreter.invoke()
            saida = interpreter.get_tensor(saida_details[0]['index'])
            classe_predita = np.argmax(saida)
            if classe_predita == 0:
                cv.rectangle(image, (x1,y1+1), (x2,y2-1), (0,0,255), 2)
                red_count += 1
            elif classe_predita == 1:
                cv.rectangle(image, (x1,y1+1), (x2,y2-1), (0,255,0), 2)
                green_count += 1


            #Coluna B
            crop_B = cv.resize(image[y1:y2, x2:x2+length_parking_space], (224, 224))
            image_array = np.asarray(crop_B)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            data[0] = normalized_image_array
            interpreter.set_tensor(entrada_details[0]['index'], data)
            interpreter.invoke()
            saida = interpreter.get_tensor(saida_details[0]['index'])
            classe_predita = np.argmax(saida)
            if classe_predita == 0:
                cv.rectangle(image, (x2,y1), (x2+length_parking_space,y2), (0,0,255), 2)
                red_count += 1
            elif classe_predita == 1:
                cv.rectangle(image, (x2,y1), (x2+length_parking_space,y2), (0,255,0), 2)
                green_count += 1




            if i != 9: #Posição 9 das colunas C e D não são vagas
                #Coluna C
                crop_C = cv.resize(image[y1:y2, x1+distance_column_A_C:x2+distance_column_A_C], (224, 224))
                image_array = np.asarray(crop_C)
                normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
                data[0] = normalized_image_array
                interpreter.set_tensor(entrada_details[0]['index'], data)
                interpreter.invoke()
                saida = interpreter.get_tensor(saida_details[0]['index'])
                classe_predita = np.argmax(saida)
                if classe_predita == 0:
                    cv.rectangle(image, (x1+distance_column_A_C,y1), (x2+distance_column_A_C,y2), (0,0,255), 2)                
                    red_count += 1
                elif classe_predita == 1:
                    cv.rectangle(image, (x1+distance_column_A_C,y1), (x2+distance_column_A_C,y2), (0,255,0), 2)                
                    green_count += 1
                

                #Coluna D
                crop_D = cv.resize(image[y1:y2, x2+distance_column_A_C:x2+distance_column_A_C+length_parking_space], (224, 224))
                image_array = np.asarray(crop_D)
                normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
                data[0] = normalized_image_array
                interpreter.set_tensor(entrada_details[0]['index'], data)
                interpreter.invoke()
                saida = interpreter.get_tensor(saida_details[0]['index'])
                classe_predita = np.argmax(saida)
                if classe_predita == 0:
                    cv.rectangle(image, (x2+distance_column_A_C,y1), (x2+distance_column_A_C+length_parking_space,y2), (0,0,255), 2)
                    red_count += 1
                elif classe_predita == 1:
                    cv.rectangle(image, (x2+distance_column_A_C,y1), (x2+distance_column_A_C+length_parking_space,y2), (0,255,0), 2)
                    green_count += 1
                
                

            #Coluna E
            crop_E = cv.resize(image[y1:y2, x1+distance_column_A_E:x2+distance_column_A_E], (224, 224))
            image_array = np.asarray(crop_E)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            data[0] = normalized_image_array
            interpreter.set_tensor(entrada_details[0]['index'], data)
            interpreter.invoke()
            saida = interpreter.get_tensor(saida_details[0]['index'])
            classe_predita = np.argmax(saida)
            if classe_predita == 0:
                cv.rectangle(image, (x1+distance_column_A_E,y1), (x2+distance_column_A_E,y2), (0,0,255), 2)
                red_count += 1
            elif classe_predita == 1:
                cv.rectangle(image, (x1+distance_column_A_E,y1), (x2+distance_column_A_E,y2), (0,255,0), 2)
                green_count += 1
                    
            
            if i != 1: #Na coluna F, posição, não há uma vaga
                #Coluna F
                crop_F = cv.resize(image[y1:y2, x2+distance_column_A_E+distance_column_E_F:x2+distance_column_A_E+length_parking_space+distance_column_E_F], (224, 224))
                image_array = np.asarray(crop_F)
                normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
                data[0] = normalized_image_array
                interpreter.set_tensor(entrada_details[0]['index'], data)
                interpreter.invoke()
                saida = interpreter.get_tensor(saida_details[0]['index'])
                classe_predita = np.argmax(saida)
                if classe_predita == 0:
                    cv.rectangle(image, (x2+distance_column_A_E+distance_column_E_F,y1), (x2+distance_column_A_E+length_parking_space+distance_column_E_F,y2), (0,0,255), 2)
                    red_count += 1
                elif classe_predita == 1:
                    cv.rectangle(image, (x2+distance_column_A_E+distance_column_E_F,y1), (x2+distance_column_A_E+length_parking_space+distance_column_E_F,y2), (0,255,0), 2)
                    green_count += 1


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
        out.write(image)
    #time.sleep(0.02)
    frame_count += 1


    #Rotina para parar a execução caso o usuário pressione a tecla ESC
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break

video.release()
