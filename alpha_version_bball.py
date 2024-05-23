import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import mediapipe as mp
import time
import numpy as np
import random



#Classe DIficuldade 

class Dificuldade:
    def __init__(self, nome, intervalo, hs, coords):
        self.nome  = nome
        self.intervalo  = intervalo
        self.hs  = hs
        self.coords  = coords

    def select_dif(self,other):
        self.nome = other.nome
        self.intervalo = other.intervalo
        self.hs = other.hs

    def add_point(self):
        self.hs = 1 + self.hs

    def set_hs(self, other):
        other.hs = self.hs



dif1 = Dificuldade('College', 5, 0,(0,0))
dif2 = Dificuldade('Rookie', 3, 0,(0,0))
dif3 = Dificuldade('All Star', 3, 0,(0,0))
dif4 = Dificuldade('M.V.P', 5, 0,(0,0))
dificuldade = Dificuldade(None, 0,0,(0,0))

#Inicia coords
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
cap=cv2.VideoCapture(0)

#inicia hands
hands = mphands.Hands()

#filtro
hsvVals = {'hmin': 179, 'smin': 0, 'vmin': 0, 'hmax': 179, 'smax': 255, 'vmax': 255}

#Inicia timers
current_time = time.time()
firsttimer = time.time()

#Inicia Coordenadas
coordenada_x = np.random.randint(-200, -100)
coordenada_y = np.random.randint(-200, -100)
coordenada_y_2 = np.random.randint(-200, -100)
coordenada_x_2 = np.random.randint(-200, -100)
coordenada_y_3 = np.random.randint(-200, -100)
coordenada_x_3 = np.random.randint(-200, -100)


# vars
nomes = ["College", "Rookie", "All Star", "M.V.P"]
cont = 3
offset = 100



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


# Parametros das Dificuldades/Nomes para caber nos circulos
(text_width, text_height), _ = cv2.getTextSize(nomes[0], fonte, escala, espessura)




#--- Função Menu ---#

def menu(image,hcx, hcy):
    offset = 50
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
    cv2.putText(image, (f'{dif1.nome} {dif1.hs}'), (centro_superior_esquerdo[0] - text_width // 2, centro_superior_esquerdo[1] + text_height // 2), fonte, escala, cor_texto, espessura)
    cv2.putText(image, (f'{dif2.nome} {dif2.hs}'), (centro_superior_direito[0] - text_width // 2, centro_superior_direito[1] + text_height // 2), fonte, escala, cor_texto, espessura)
    cv2.putText(image, (f'{dif3.nome} {dif3.hs}'), (centro_inferior_esquerdo[0] - text_width // 2, centro_inferior_esquerdo[1] + text_height // 2), fonte, escala, cor_texto, espessura)
    cv2.putText(image, (f'{dif4.nome} {dif4.hs}'), (centro_inferior_direito[0] - text_width // 2, centro_inferior_direito[1] + text_height // 2), fonte, escala, cor_texto, espessura)

    if (((image_width // 4) - offset) <= hcx <= ((image_width // 4) + offset)) and (((image_height // 4) - offset) <= hcy <= ((image_height // 4) + offset)):
        dificuldade.select_dif(dif1)
    elif (((3 * image_width // 4) - offset) <= hcx <= ((3 * image_width // 4) + offset)) and (((image_height // 4) - offset) <= hcy <= ((image_height // 4) + offset)):
        dificuldade.select_dif(dif2)

    elif (((image_width // 4) - offset) <= hcx <= ((image_width // 4) + offset)) and (((3 * image_height // 4) - offset) <= hcy <= ((3 * image_height // 4) + offset)):
        dificuldade.select_dif(dif3)

    elif (((3 * image_width // 4) - offset) <= hcx <= ((3 * image_width // 4) + offset)) and (((3 * image_height // 4) - offset) <= hcy <= ((3 * image_height // 4) + offset)):
        dificuldade.select_dif(dif4)
        
    else:
        return None
    return dificuldade



#--- Função Game ---#

def game():
    if(dificuldade.nome != dif4.nome):
        cv2.circle(image, (coordenada_x, coordenada_y), 50, (0,255,0), -1)
        if(dificuldade.nome == dif3.nome):
            cv2.circle(image, (coordenada_x_2, coordenada_y_2), 50, (0 ,0,255), -1)
    else:
        cv2.circle(image, (coordenada_x_3, coordenada_y_3), 50, (0, 127, 255), -1)



#--- Função Timer ---#

def timer(image, cont):
    cv2.putText(image, str(cont), (image_width//2,35), fonte, escala, cor_texto, espessura)



#--- Função refaz coordenada ---#
def coord():
    coordenada_x = np.random.randint(0, image_width - 150)
    coordenada_y = np.random.randint(0, image_height - 150)
    coordenada_x_2 = np.random.randint(0, image_width - 150)
    coordenada_y_2 = np.random.randint(0, image_height - 150)
    coordenada_x_3 = np.random.randint(0, image_width - 150)
    coordenada_y_3 = np.random.randint(image_height // 2, image_height - 150)

    return  coordenada_x, coordenada_y, coordenada_x_2, coordenada_y_2, coordenada_x_3, coordenada_y_3



#--- Função Pegar a bola ---#
def catch_ball(coordenada_x, coordenada_y, coordenada_x_2, coordenada_y_2, coordenada_x_3, coordenada_y_3):
    if(dificuldade.nome != dif4.nome):
        if ((coordenada_x - offset) <= hcx <= (coordenada_x + offset)) and ((coordenada_y - offset) <= hcy <= (coordenada_y + offset)):
            dificuldade.add_point()

        if(dificuldade.nome == dif3.nome):
            if ((coordenada_x_3 - offset) <= cx <= (coordenada_x_3 + offset)) and ((coordenada_y_3 - offset) <= cy <= (coordenada_y_3 + offset)):
                dificuldade.add_point()

    else:
        if ((coordenada_x_2 - offset) <= hcx <= (coordenada_x_2 + offset)) and ((coordenada_y_2 - offset) <= hcy <= (coordenada_y_2 + offset)):
            dificuldade.add_point()



#--- Função Checar dif de volta ---#
def check_dif(dif1,dif2,dif3,dif4,dificuldade):
    if dificuldade.nome == dif1.nome:
        dificuldade.set_hs(dif1)
    elif dificuldade.nome == dif2.nome:
        dificuldade.set_hs(dif2)
    elif dificuldade.nome == dif3.nome:
        dificuldade.set_hs(dif3)
    else:
        dificuldade.set_hs(dif4)



#--- Inicia Telas ---#

is_menu = True
is_game = False
is_timer = False
is_started = False

#Loop CAP
while True:
    data, image = cap.read()
    if data == False:
        print('Sem Frame')
        break
    else:
        image_height, image_width, _ = image.shape
        imgClean = image

    if cv2.waitKey(1) == ord('q'):
        break
   
    #--- Captura de Mão ---#
    #find and draw hand
    #flip image
    image = cv2.cvtColor(cv2.flip(image,1), cv2.COLOR_BGR2RGB)
    #store results
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    #find landmarks in results
    if results.multi_hand_landmarks:
        for idx, hand_handedness in enumerate(results.multi_handedness):
            wich_hand = results.multi_handedness[idx].classification[0].label

        #Line Landmarks as hand connections
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks, mphands.HAND_CONNECTIONS
            )
            #
            hcx = hand_landmarks.landmark[mphands.HandLandmark.MIDDLE_FINGER_MCP].x * image_width
            hcy = hand_landmarks.landmark[mphands.HandLandmark.MIDDLE_FINGER_MCP].y * image_height

             #print(hcx,hcy)


                    

    #--- Captura de Bola ---#    



    #find and draw ball
    imgColor, Mask = myColorFinder.update(image,hsvVals)
    image , contours = cvzone.findContours(image, Mask, minArea=500)
    if contours:
        cx, cy = contours[0]['center']


    #--- Menu & Game ---#
   

    #Inicia Menu
    if is_menu:

        dificuldade_selecionada = menu(image, hcx, hcy)
        #print(f'dificuldade = {str(dificuldade.nome)}')
        if dificuldade_selecionada is not None:
            is_menu = False
            is_timer = True
            is_game = True


    #Inicia Jogo
    if is_game:
        if is_started:
            game()
            if time.time() - current_time > dificuldade.intervalo:
                current_time = time.time()
                #muda coordenada
                coordenada_x, coordenada_y, coordenada_x_2, coordenada_y_2, coordenada_x_3, coordenada_y_3 = coord()

            catch_ball(coordenada_x, coordenada_y, coordenada_x_2, coordenada_y_2, coordenada_x_3, coordenada_y_3)

        if time.time() - firsttimer > 1:
            firsttimer = time.time()
            cont = cont - 1
            #print(f'Segundos: {cont} | Pontução: {dificuldade.hs}')
            if(cont == 0 and not is_started):
                is_started = True
                cont= 10
            elif(cont == 0 and is_started):
                cont= 3
                is_started = False
                is_timer = False
                is_game = False
                check_dif(dif1,dif2,dif3,dif4,dificuldade)
                is_menu = True

    if is_timer:
        timer(image, cont)




    cv2.imshow('Tracking', image)
    cv2.waitKey(1)


cap.release()
cv2.destroyAllWindows()
