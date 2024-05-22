import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import mediapipe as mp
import time
import numpy as np
import json
import random

with open("data.json", "r") as f:
    data = json.loads(f.read())



cx=0
cy=0
hcx=0
hcy=0

#Lining Landmarks
mp_drawing = mp.solutions.drawing_utils
#Style Line
mp_drawing_styles = mp.solutions.drawing_styles
#var for function
mphands = mp.solutions.hands

#Color Finder
myColorFinder = ColorFinder(False)
intervalo =  5
cont = 3

#Video Capture
cap=cv2.VideoCapture('L1.mp4')

hands = mphands.Hands()
hsvVals = {'hmin': 0, 'smin': 125, 'vmin': 0, 'hmax': 21, 'smax': 255, 'vmax': 255}

current_time = time.time()
firsttimer = time.time()

coordenada_x = np.random.randint(-200, -100)
coordenada_y = np.random.randint(-200, -100)
coordenada_y_2 = np.random.randint(-200, -100)
coordenada_x_2 = np.random.randint(-200, -100)
coordenada_y_3 = np.random.randint(-200, -100)
coordenada_x_3 = np.random.randint(-200, -100)

offset = 70
# Nomes das Dificuldades
nomes = ["College", "Rookie", "All Star", "M.V.P"]


#vars json
nome1 = data['dificuldade'][0]['dif']
nome2 = data['dificuldade'][1]['dif']
nome3 = data['dificuldade'][2]['dif']
nome4 = data['dificuldade'][3]['dif']

intervalo1 = data['dificuldade'][0]['intervalo']
intervalo2 = data['dificuldade'][1]['intervalo']
intervalo3 = data['dificuldade'][2]['intervalo']
intervalo4 = data['dificuldade'][3]['intervalo']

# Parametros Circulo
fonte = cv2.FONT_HERSHEY_SIMPLEX
escala = 1
espessura = 2
espessura_contorno = 2
raio = 50

# Paleta de Cores
cor_texto = (255, 255, 255)
cor_circ = (128, 128, 128)
color = (200, 200, 200)
cor_preta = (0, 0, 0)

# Pontuação
pont = 0

# Parametros das Dificuldades/Nomes para caber nos circulos
(text_width, text_height), _ = cv2.getTextSize(nomes[0], fonte, escala, espessura)

def menu(image,hcx, hcy, intervalo):
    offset = 10
    image_height, image_width, _ = image.shape
        # Coordenadas dos quartos
    centro_superior_esquerdo = (image_width // 4, image_height // 4)
    centro_superior_direito = (3 * image_width // 4, image_height // 4)
    centro_inferior_esquerdo = (image_width // 4, 3 * image_height // 4)
    centro_inferior_direito = (3 * image_width // 4, 3 * image_height // 4)

    # Circulos em cada quarto
    cv2.circle(image, centro_superior_esquerdo, raio, cor_circ, -1)
    cv2.circle(image, centro_superior_direito, raio, cor_circ, -1)
    cv2.circle(image, centro_inferior_esquerdo, raio, cor_circ, -1)
    cv2.circle(image, centro_inferior_direito, raio, cor_circ, -1)

    # Desenhar contornos pretos ao redor dos círculos
    cv2.circle(image, centro_superior_esquerdo, raio, cor_preta, espessura_contorno)
    cv2.circle(image, centro_superior_direito, raio, cor_preta, espessura_contorno)
    cv2.circle(image, centro_inferior_esquerdo, raio, cor_preta, espessura_contorno)
    cv2.circle(image, centro_inferior_direito, raio, cor_preta, espessura_contorno)

    # Inserindo as Dificuldades/Nomes nos circulos
    cv2.putText(image, nomes[0], (centro_superior_esquerdo[0] - text_width // 2, centro_superior_esquerdo[1] + text_height // 2), fonte, escala, cor_texto, espessura)
    cv2.putText(image, nomes[1], (centro_superior_direito[0] - text_width // 2, centro_superior_direito[1] + text_height // 2), fonte, escala, cor_texto, espessura)
    cv2.putText(image, nomes[2], (centro_inferior_esquerdo[0] - text_width // 2, centro_inferior_esquerdo[1] + text_height // 2), fonte, escala, cor_texto, espessura)
    cv2.putText(image, nomes[3], (centro_inferior_direito[0] - text_width // 2, centro_inferior_direito[1] + text_height // 2), fonte, escala, cor_texto, espessura)

    if (((image_width // 4) - offset) <= hcx <= ((image_width // 4) + offset)) and (((image_height // 4) - offset) <= hcy <= ((image_height // 4) + offset)):
        dificuldade = nome1
    elif (((3 * image_width // 4) - offset) <= hcx <= ((3 * image_width // 4) + offset)) and (((image_height // 4) - offset) <= hcy <= ((image_height // 4) + offset)):
        dificuldade = nome2

    elif (((image_width // 4) - offset) <= hcx <= ((image_width // 4) + offset)) and (((3 * image_height // 4) - offset) <= hcy <= ((3 * image_height // 4) + offset)):
        dificuldade = nome3

    elif (((3 * image_width // 4) - offset) <= hcx <= ((3 * image_width // 4) + offset)) and (((3 * image_height // 4) - offset) <= hcy <= ((3 * image_height // 4) + offset)):
        dificuldade = nome4
        
    else:
        return None
    return dificuldade

def game():
    if(dificuldade == 'College' or dificuldade == 'Rookie' or dificuldade == 'All Star'):
        cv2.circle(image, (coordenada_x, coordenada_y), 50, (0,255,0), -1)
        if(dificuldade == 'All Star'):
            cv2.circle(image, (coordenada_x_2, coordenada_y_2), 50, (0 ,0,255), -1)
    else:
        cv2.circle(image, (coordenada_x_3, coordenada_y_3), 50, (0, 127, 255), -1)

def timer(image, cont):
    cv2.putText(image, str(cont), (image_width//2,35), fonte, escala, cor_texto, espessura)


is_menu = True
is_game = False
is_timer = False
# Dificuldade
dif = ''

while True:

    data, image = cap.read()
    image_height, image_width, _ = image.shape
    imgClean = image
   
    #--- Captura de Mão ---#
    #find and draw hand
    #flip image
    image = cv2.cvtColor(cv2.flip(image,1), cv2.COLOR_BGR2RGB)
    #store results
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    #find landmarks in results
    if results.multi_hand_landmarks:
        #Line Landmarks as hand connections
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks, mphands.HAND_CONNECTIONS
            )
            for ids, landmrk in enumerate(hand_landmarks.landmark):
                if ids == 9:
                    hcx, hcy = landmrk.x * image_width, landmrk.y*image_height


    #--- Captura de Bola ---#    
    #find and draw ball
    imgColor, Mask = myColorFinder.update(image,hsvVals)
    image , contours = cvzone.findContours(image, Mask, minArea=500)
    if contours:
        cx, cy = contours[0]['center']


    #--- Menu & Game ---#
    if is_game:
        game()
        if time.time() - current_time > intervalo:
            current_time = time.time()
            coordenada_x = np.random.randint(0, image_width - 150)
            coordenada_y = np.random.randint(0, image_height - 150)
            coordenada_x_2 = np.random.randint(0, image_width - 150)
            coordenada_y_2 = np.random.randint(0, image_height - 150)
            coordenada_x_3 = np.random.randint(0, image_width - 150)
            coordenada_y_3 = np.random.randint(image_height // 2, image_height - 150)
            print(current_time)
            print('deu tempo')
            
    if is_menu:
        dificuldade = menu(image, hcx, hcy, data)
        if(dificuldade == 'College'):
            intervalo = 5
        elif(dificuldade == 'Rookie' or dificuldade == 'All Star' or dificuldade == 'M.V.P'):
            intervalo = 3
        print(dificuldade)
        #print(f'dificuldade = {dificuldade}')
        if dificuldade is not None:
            is_menu = False
            is_timer = True

    if is_timer:
        timer(image, cont)

    if not is_menu:
        if time.time() - firsttimer > 1:
            firsttimer = time.time()
            cont = cont - 1
            print(f'Segundos: {cont} | Pontução: {pont}')
            if(cont == 0):
                cont = 60
                is_game = True
            with open("pont.json", "w") as f:
                json.dump(data, f, indent=4)
                print('SAVED')

    if ((coordenada_x - offset) <= hcx <= (coordenada_x + offset)) and ((coordenada_y - offset) <= hcy <= (coordenada_y + offset)):
        # highscore = highscore + 1
        coordenada_x = np.random.randint(0, image_width - 150)
        coordenada_y = np.random.randint(0, image_height - 150)
        pont = pont+1
        print(pont)

    if ((coordenada_x_3 - offset) <= cx <= (coordenada_x_3 + offset)) and ((coordenada_y_3 - offset) <= cy <= (coordenada_y_3 + offset)):
        # highscore = highscore + 1
        pont = pont + 1
        coordenada_x_3 = np.random.randint(0, image_width - 150)
        coordenada_y_3 = np.random.randint(0, image_height - 150)
        print(pont)

    if ((coordenada_x_2 - offset) <= hcx <= (coordenada_x_2 + offset)) and ((coordenada_y_2 - offset) <= hcy <= (coordenada_y_2 + offset)):
        # highscore = highscore - 1
        pont = pont - 1
        coordenada_x_2 = np.random.randint(0, image_width - 150)
        coordenada_y_2 = np.random.randint(0, image_height - 150)
        print(pont)

    #print(results.multi_handedness)
    # print(hcx, hcy, cx,cy)


    print(f'hcx = {cx}, coord_X = {coordenada_x_3},hcy = {cy}, coord_Y = {coordenada_y_3}')
    cv2.imshow('Tracking', image)
    cv2.waitKey(1)
