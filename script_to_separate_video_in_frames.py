import cv2 as cv
import numpy as np

video = cv.VideoCapture('videos/carPark.mp4')

if not video.isOpened():
    print('Erro ao carregar o vídeo.')
    exit()

#Rotina para obter o número de frames existentes no vídeo
num_frames = int(video.get(cv.CAP_PROP_FRAME_COUNT))

for i in range(num_frames):

    #ret é um identificador de término de execução de vídeo
    ret, frame = video.read()

    cv.imwrite(f'images/frame_{i}.jpg', frame)

video.release()
