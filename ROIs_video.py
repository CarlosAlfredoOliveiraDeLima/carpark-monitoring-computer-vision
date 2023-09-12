import cv2 as cv
import time

video = cv.VideoCapture('videos/carPark.mp4')

if not video.isOpened():
    print('Erro ao carregar o vídeo.')
    exit()

while True:
    ret, image = video.read()
    #Rotina para verificar se o vídeo chegou ao fim e então terminar o loop ou reiniciar o vídeo
    if not ret:
    #   break
        video.set(cv.CAP_PROP_POS_FRAMES, 0)
        continue
    
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
        #Colunas A e B
        cv.rectangle(image, (x1,y1), (x2,y2), (0,0,255), 2)
        cv.rectangle(image, (x2,y1), (x2+length_parking_space,y2), (0,0,255), 2)
        #Colunas C e D
        if i != 9:
            cv.rectangle(image, (x1+distance_column_A_C,y1), (x2+distance_column_A_C,y2), (0,0,255), 2)
            cv.rectangle(image, (x2+distance_column_A_C,y1), (x2+distance_column_A_C+length_parking_space,y2), (0,0,255), 2)
        #Colunas E e F
        cv.rectangle(image, (x1+distance_column_A_E,y1), (x2+distance_column_A_E,y2), (0,0,255), 2)
        if i != 1:
            cv.rectangle(image, (x2+distance_column_A_E+distance_column_E_F,y1), (x2+distance_column_A_E+length_parking_space+distance_column_E_F,y2), (0,0,255), 2)
            
        
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

    time.sleep(0.03)

    #Rotina para parar a execução caso o usuário pressione a tecla ESC
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break

video.release()
