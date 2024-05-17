import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import mediapipe as mp
import time
import numpy as np
import random


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

#Video Capture
cap=cv2.VideoCapture('bball.mp4')

hands = mphands.Hands()
hsvVals = {'hmin': 0, 'smin': 164, 'vmin': 120, 'hmax': 9, 'smax': 213, 'vmax': 155}

current_time = time.time()
intervalo = 1

coordenada_x = np.random.randint(0, 300 - 150)
coordenada_y = np.random.randint(0, 300 - 150)

offset = 50
# Nomes das Dificuldades
nomes = ["College", "Rookie", "All Star", " M.V.P"]

# Parametros Circulo
fonte = cv2.FONT_HERSHEY_SIMPLEX
escala = 1
espessura = 2
espessura_contorno = 2
raio = 100

# Paleta de Cores
cor_texto = (255, 255, 255)
cor_circ = (128, 128, 128)
color = (200, 200, 200)
cor_preta = (0, 0, 0)

# Parametros das Dificuldades/Nomes para caber nos circulos
(text_width, text_height), _ = cv2.getTextSize(nomes[0], fonte, escala, espessura)

def menu(image,hcx, hcy ):
    offset = 300
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
        print(nomes[0])
        dificuldade= nomes[0]
    elif (((3 * image_width // 4) - offset) <= hcx <= ((3 * image_width // 4) + offset)) and (((image_height // 4) - offset) <= hcy <= ((image_height // 4) + offset)):
        print(nomes[1])
        dificuldade = nomes[1]
    elif (((image_width // 4) - offset) <= hcx <= ((image_width // 4) + offset)) and (((3 * image_height // 4) - offset) <= hcy <= ((3 * image_height // 4) + offset)):
        print(nomes[2])
        dificuldade = nomes[2]
    elif (((3 * image_width // 4) - offset) <= hcx <= ((3 * image_width // 4) + offset)) and (((3 * image_height // 4) - offset) <= hcy <= ((3 * image_height // 4) + offset)):
        print(nomes[3])
        dificuldade = nomes[3]
    else:
        return None
    return dificuldade

    pass

is_menu = True
# Dificuldade
dif = ''
while True:
    data, image = cap.read()
    image_height, image_width, _ = image.shape
    imgClean = image
   
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
    if is_menu:
        dificuldade = menu(image, hcx, hcy)
        print(f'dificuldade = {dificuldade}')
        if dificuldade is not None:
            is_menu = False
    


    #find and draw ball
    imgColor, Mask = myColorFinder.update(image,hsvVals)
    image , contours = cvzone.findContours(image, Mask, minArea=500)
    if contours:
        cx, cy = contours[0]['center']


    if time.time() - current_time > intervalo:
        current_time = time.time()
        coordenada_x = np.random.randint(0, image_width - 150)
        coordenada_y = np.random.randint(0, image_height - 150)
        # print('deu tempo')


    cv2.circle(image, (coordenada_x, coordenada_y), 50, (0,255,0), -1)




    print(f'hcx = {hcx}, coord_X = {coordenada_x},hcy = {hcy}, coord_Y = {coordenada_y}')


    if ((coordenada_x - offset) <= hcx <= (coordenada_x + offset)) and ((coordenada_y - offset) <= hcy <= (coordenada_y + offset)):
        print('peguei a bola!!!')
    
    #print(results.multi_handedness)
    # print(hcx, hcy, cx,cy)

    cv2.imshow('Tracking', image)

    cv2.waitKey(1)

    
