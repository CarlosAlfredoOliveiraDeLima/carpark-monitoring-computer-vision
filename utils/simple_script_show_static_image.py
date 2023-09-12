import cv2 as cv
import numpy as np

image = cv.imread('separated_images/frame_0.jpg')

# Verificar se a imagem foi corretamente carregada
if image is None:
    print('Erro ao carregar a imagem.')
    exit()

cv.imshow('Imagem estatica', image)

# Rotina que aguarda o usuário pressionar a tecla Q para fechar a janela da imagem
cv.waitKey(0)

cv.destroyAllWindows()