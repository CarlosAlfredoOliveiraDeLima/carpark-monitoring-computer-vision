import cv2 as cv

image = cv.imread('separated_images/frame_0.jpg')

# Verificar se a imagem foi corretamente carregada
if image is None:
    print('Erro ao carregar a imagem.')
    exit()

# cv.rectangle(image, (42,100), (147,147), (0,0,255), 2)
# cv.putText(image, "01", (22,115), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# cv.rectangle(image, (42,147), (147,194), (0,0,255), 2)
# cv.putText(image, "02", (22,162), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# cv.rectangle(image, (42,194), (147,241), (0,0,255), 2)
# cv.putText(image, "03", (22,209), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# x1 = 42
# x2 = 150
# y1 = 100
# y2 = 147
x1 = 42
x2 = 157
y1 = 100
y2 = 147
for i in range(1, 13, 1):
    cv.rectangle(image, (x1,y1), (x2,y2), (0,0,255), 2)
    cv.putText(image, f"a{i}", (x1-33,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
    cv.rectangle(image, (x1+108,y1), (x2+108,y2), (0,0,255), 2)
    cv.putText(image, f"b{i}", (x2+113,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
    y1 += 47
    y2 += 47


x1 = 390
x2 = 498
y1 = 96
y2 = 143
for i in range(1, 13, 1):
    if i == 9:
        y1 += 47
        y2 += 47
        continue
    cv.rectangle(image, (x1,y1), (x2,y2), (0,0,255), 2)
    cv.putText(image, f"c{i}", (x1-33,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
    cv.rectangle(image, (x1+108,y1), (x2+108,y2), (0,0,255), 2)
    cv.putText(image, f"d{i}", (x2+113,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
    y1 += 47
    y2 += 47


x1 = 738
x2 = 846
y1 = 93
y2 = 140
for i in range(1, 13, 1):

    if i == 1:
        cv.rectangle(image, (x1,y1), (x2,y2), (0,0,255), 2)
        cv.putText(image, f"e{i}", (x1-33,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
        y1 += 47
        y2 += 47
        continue


    cv.rectangle(image, (x1,y1), (x2,y2), (0,0,255), 2)
    cv.putText(image, f"e{i}", (x1-33,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
    cv.rectangle(image, (x1+150,y1), (x2+150,y2), (0,0,255), 2)
    cv.putText(image, f"f{i}", (x2+154,y1+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
    y1 += 47
    y2 += 47



cv.imshow('Imagem estatica', image)

# Rotina que aguarda o usuário pressionar a tecla Q para fechar a janela da imagem
cv.waitKey(0)

cv.destroyAllWindows()