from flask import Flask, render_template, Response
import cv2 as cv
from time import sleep
import json
from classifier_model import image_classifier

app = Flask(__name__)

video = cv.VideoCapture('videos/carPark.mp4')

if not video.isOpened():
    print('Erro ao carregar o vídeo.')
    exit()

with open('ROIs_definition.json', 'r') as ROIs_json:
    ROIs = json.load(ROIs_json)

def gen_frames():  # generate frame by frame from camera
    frame_pular = 4
    frame_count = 0
    while True:
        red_count = 0
        green_count = 0
        success, image = video.read()
        #Rotina para verificar se o vídeo chegou ao fim e então terminar o loop ou reiniciar o vídeo
        if not success:
            video.set(cv.CAP_PROP_POS_FRAMES, 0)
            # continue
        else:
            y1 = ROIs['y1']
            y2 = ROIs['y2']
                
            if frame_count == 1 or frame_count % frame_pular == 0:
                for i in range(1, 13, 1):  
                    #Coluna A
                    crop_A = cv.resize(image[y1:y2, ROIs["A"]["x1"]:ROIs["A"]["x2"]], (224, 224))
                    classe_predita = image_classifier(crop_A)

                    if classe_predita == 0:
                        cv.rectangle(image, (ROIs["A"]["x1"],y1+1), (ROIs["A"]["x2"],y2-1), (0,0,255), 2)
                        red_count += 1
                    elif classe_predita == 1:
                        cv.rectangle(image, (ROIs["A"]["x1"],y1+1), (ROIs["A"]["x2"],y2-1), (0,255,0), 2)
                        green_count += 1

                    #Coluna B
                    crop_B = cv.resize(image[y1:y2, ROIs["B"]["x1"]:ROIs["B"]["x2"]], (224, 224))
                    classe_predita = image_classifier(crop_B)
                    if classe_predita == 0:
                        cv.rectangle(image, (ROIs["B"]["x1"],y1+1), (ROIs["B"]["x2"],y2-1), (0,0,255), 2)
                        red_count += 1
                    elif classe_predita == 1:
                        cv.rectangle(image, (ROIs["B"]["x1"],y1+1), (ROIs["B"]["x2"],y2-1), (0,255,0), 2)
                        green_count += 1

                    if i != 9: #Posição 9 das colunas C e D não são vagas
                        #Coluna C
                        crop_C = cv.resize(image[y1:y2, ROIs["C"]["x1"]:ROIs["C"]["x2"]], (224, 224))
                        classe_predita = image_classifier(crop_C)
                        if classe_predita == 0:
                            cv.rectangle(image, (ROIs["C"]["x1"],y1+1), (ROIs["C"]["x2"],y2-1), (0,0,255), 2)                
                            red_count += 1
                        elif classe_predita == 1:
                            cv.rectangle(image, (ROIs["C"]["x1"],y1+1), (ROIs["C"]["x2"],y2-1), (0,255,0), 2)                
                            green_count += 1

                        #Coluna D
                        crop_D = cv.resize(image[y1:y2, ROIs["D"]["x1"]:ROIs["D"]["x2"]], (224, 224))
                        classe_predita = image_classifier(crop_D)
                        if classe_predita == 0:
                            cv.rectangle(image, (ROIs["D"]["x1"],y1+1), (ROIs["D"]["x2"],y2-1), (0,0,255), 2)
                            red_count += 1
                        elif classe_predita == 1:
                            cv.rectangle(image, (ROIs["D"]["x1"],y1+1), (ROIs["D"]["x2"],y2-1), (0,255,0), 2)
                            green_count += 1

                    #Coluna E
                    crop_E = cv.resize(image[y1:y2, ROIs["E"]["x1"]:ROIs["E"]["x2"]], (224, 224))
                    classe_predita = image_classifier(crop_E)
                    if classe_predita == 0:
                        cv.rectangle(image, (ROIs["E"]["x1"],y1+1), (ROIs["E"]["x2"],y2-1), (0,0,255), 2)
                        red_count += 1
                    elif classe_predita == 1:
                        cv.rectangle(image, (ROIs["E"]["x1"],y1+1), (ROIs["E"]["x2"],y2-1), (0,255,0), 2)
                        green_count += 1                 
        
                    if i != 1: #Na coluna F, posição, não há uma vaga
                        #Coluna F
                        crop_F = cv.resize(image[y1:y2, ROIs["F"]["x1"]:ROIs["F"]["x2"]], (224, 224))
                        classe_predita = image_classifier(crop_F)
                        if classe_predita == 0:
                            cv.rectangle(image, (ROIs["F"]["x1"],y1+1), (ROIs["F"]["x2"],y2-1), (0,0,255), 2)
                            red_count += 1
                        elif classe_predita == 1:
                            cv.rectangle(image, (ROIs["F"]["x1"],y1+1), (ROIs["F"]["x2"],y2-1), (0,255,0), 2)
                            green_count += 1

                    cv.putText(image, f"a{i}", (ROIs["A"]['put_text_x'],ROIs['put_text_y']+y1), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
                    cv.putText(image, f"b{i}", (ROIs["B"]['put_text_x'],ROIs['put_text_y']+y1), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
                    if i != 9:
                        cv.putText(image, f"c{i}", (ROIs["C"]['put_text_x'],ROIs['put_text_y']+y1), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
                        cv.putText(image, f"d{i}", (ROIs["D"]['put_text_x'],ROIs['put_text_y']+y1), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
                    cv.putText(image, f"e{i}", (ROIs["E"]['put_text_x'],ROIs['put_text_y']+y1), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)
                    if i != 1:
                        cv.putText(image, f"f{i}", (ROIs["F"]['put_text_x'],ROIs['put_text_y']+y1), cv.FONT_HERSHEY_SIMPLEX, 0.5, (51, 255, 255), 1)

                    #Atualização dos valores das ordenadas das vagas
                    y1 += 47
                    y2 += 47
                
                ret, buffer = cv.imencode('.jpg', image)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

            frame_count += 1

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)