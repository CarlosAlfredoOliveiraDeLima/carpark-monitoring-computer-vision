import cv2 as cv

video = cv.VideoCapture('videos/video_park_lot.mp4')

if not video.isOpened():
    print('Erro ao carregar o vídeo.')
    exit()

while True:
    ret, frame = video.read()

    #Rotina para verificar se o vídeo chegou ao fim e então terminar o loop
    if not ret:
        break

    cv.imshow('Video', frame)

    #Rotina para parar a execução caso o usuário pressione a tecla ESC
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break

video.release()
