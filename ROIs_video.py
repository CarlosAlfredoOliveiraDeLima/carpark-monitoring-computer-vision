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
    
    x1 = 46 #+4
    x2 = 156 #+6
    y1 = 100
    y2 = 147
    for i in range(1, 13, 1):
        cv.rectangle(image, (x1,y1), (x2,y2), (0,0,255), 2)
        cv.putText(image, f"a{i}", (x1-33,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
        cv.rectangle(image, (x2,y1), (x2+110,y2), (0,0,255), 2)
        cv.putText(image, f"b{i}", (x2+113,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)

        if i != 9:
            cv.rectangle(image, (x1+348,y1), (x2+348,y2), (0,0,255), 2)
            cv.putText(image, f"c{i}", (x1-33,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
            cv.rectangle(image, (x2+348,y1), (x2+458,y2), (0,0,255), 2)
            cv.putText(image, f"d{i}", (x2+113,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)

        cv.rectangle(image, (x1+696,y1), (x2+696,y2), (0,0,255), 2)
        cv.putText(image, f"c{i}", (x1-33,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
        if i != 1:
            cv.rectangle(image, (x2+736,y1), (x2+846,y2), (0,0,255), 2)
            cv.putText(image, f"d{i}", (x2+113,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
        
        y1 += 47
        y2 += 47


    # x1 = 390
    # x2 = 498
    # y1 = 96
    # y2 = 143
    # for i in range(1, 13, 1):
    #     if i == 9:
    #         y1 += 47
    #         y2 += 47
    #         continue
    #     cv.rectangle(image, (x1,y1), (x2,y2), (0,0,255), 2)
    #     cv.putText(image, f"c{i}", (x1-33,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
    #     cv.rectangle(image, (x1+108,y1), (x2+108,y2), (0,0,255), 2)
    #     cv.putText(image, f"d{i}", (x2+113,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
    #     y1 += 47
    #     y2 += 47


    # x1 = 738
    # x2 = 846
    # y1 = 93
    # y2 = 140
    # for i in range(1, 13, 1):

    #     if i == 1:
    #         cv.rectangle(image, (x1,y1), (x2,y2), (0,0,255), 2)
    #         cv.putText(image, f"e{i}", (x1-33,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
    #         y1 += 47
    #         y2 += 47
    #         continue


        # cv.rectangle(image, (x1,y1), (x2,y2), (0,0,255), 2)
        # cv.putText(image, f"e{i}", (x1-33,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
        # cv.rectangle(image, (x1+150,y1), (x2+150,y2), (0,0,255), 2)
        # cv.putText(image, f"f{i}", (x2+154,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
        # y1 += 47
        # y2 += 47


    cv.imshow('Video', image)

    time.sleep(0.03)

    #Rotina para parar a execução caso o usuário pressione a tecla ESC
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break

video.release()
