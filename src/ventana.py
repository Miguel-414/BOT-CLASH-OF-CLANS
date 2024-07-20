
# ! Con
# ? gh
# TODO:
# * percase
import math
import numpy as np
import pytesseract
import cv2
import time
import pyautogui
import pygetwindow as gw
import matplotlib.pyplot as plt
# // hola como estas

# ! Configuracion del Modelo
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
psm = 7
alphanumeric = "axMsO0123456789"
options = "-c tessedit_char_whitelist={}".format(alphanumeric)
options += "--oem 3 --psm {}".format(psm)
# * Declaracion de variables
# Dimensiones
pAncho = 100/1339
pAltura = 100/783
# atacar
porcentaje_X_Atacar = pAncho * 79
porcentaje_Y_Atacar = pAltura * 695
# Buscar
porcentaje_X_Buscar = pAncho * 994
porcentaje_Y_Buscar = pAltura * 517
# Tiempo
porcentaje_X_Tiempo = pAncho * 589
porcentaje_Y_Tiempo = pAltura * 60
ancho_Tiempo = pAncho * 190  # 163
alto_Tiempo = pAltura * 64
# Tropa
porcentaje_X_Tropa = pAncho * 331
porcentaje_Y_Tropa = pAltura * 712
# Porcentaje destruccion
porcentaje_X_Destruccion = pAncho * 1142
porcentaje_Y_Destruccion = pAltura * 601
ancho_Destruccion = pAncho * 161
alto_Destruccion = pAltura * 32
# Rango de ataque
ataque = {
    'punto_X_1': pAncho * 331,
    'punto_Y_1': pAltura * 375,
    'punto_X_2': pAncho * 708,
    'punto_Y_2': pAltura * 99,
    'punto_X_3': pAncho * 1043,
    'punto_Y_3': pAltura * 366,
    'punto_X_4': pAncho * 695,
    'punto_Y_4': pAltura * 623
}

# Heroe
porcentaje_X_Heroe = pAncho * 234
porcentaje_Y_Heroe = pAltura * 716
# Captura Heroe
porcentaje_X_Heroe_cap = pAncho * 191
porcentaje_Y_Heroe_cap = pAltura * 663
ancho_X_Heroe_cap = pAncho * 74
alto_Y_Heroe_cap = pAltura * 100
# Valores equivalentes con respecto  margen

porcentaje_X_Uno = pAncho * 175
porcentaje_X_Dos = pAncho * 1163
porcentaje_X_Tres = pAncho * 568
porcentaje_Y_Uno = pAltura * 624
porcentaje_Y_Dos = pAltura * 112
porcentaje_Y_Tres = pAltura * 542

# Captura Porcentaje
porcentaje_X_Contador = pAncho * 291
porcentaje_Y_Contador = pAltura * 662
cont_ancho = pAncho * 72
cont_alto = pAltura * 20
trop_alto = pAltura * 80
cont_movimiento = pAncho * 87

# Volver
porcentaje_X_Volver = pAncho * 666
porcentaje_Y_Volver = pAltura * 658

# Captura nombre cuenta
porcentaje_X_Nombre = pAncho * 93
porcentaje_Y_Nombre = pAltura * 43
cap_Ancho_Nombre = pAncho * 52
cap_Alto_Nombre = pAltura * 16

# Captura volver
porcentaje_X_Volver_Cap = pAncho * 617
porcentaje_Y_Volver_Cap = pAltura * 642
cap_Ancho_Volver = pAncho * 100
cap_Alto_Volver = pAltura * 30

# Tiempo Heroe

time_init = 0
time_end = 0

# Recolectar Recursos
recurso_X = pAncho * 874
recurso_Y = pAltura * 38
tomar_X = pAncho * 973
tomar_Y = pAltura * 654


def plot_image(img, grayscale=True):
    plt.axis('off')
    if grayscale:
        plt.imshow(img, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()


# todo: Interaccion con las ventanas abiertas de windows
# Encuentra todas las ventanas abiertas
windows = gw.getAllTitles()

# Filtra la ventana de "Clash of Clans"
coc_window = None
for window in windows:
    if "Clash of Clans" in window:
        coc_window = gw.getWindowsWithTitle(window)[0]
        break


def is_gray(x, y, ancho, alto, crud=False, umbral=10):
    if crud:
        img = pyautogui.screenshot(
            region=[x, getY(y), getW(ancho), getH(alto)])
    else:
        img = pyautogui.screenshot(
            region=[getX(x), getY(y), getW(ancho), getH(alto)])

    imagen_np = np.array(img)

    # Si la imagen tiene un canal alfa, eliminarlo
    if imagen_np.shape[-1] == 4:
        imagen_np = imagen_np[:, :, :3]

    # Calcular la desviación estándar a lo largo del eje de los canales de color
    std_dev = np.std(imagen_np, axis=-1)

    # Calcular la media de las desviaciones estándar
    mean_std_dev = np.mean(std_dev)

    # Comparar con el umbral
    if mean_std_dev < umbral:
        return True  # La imagen es mayormente gris
    else:
        return False  # La imagen es a color


def compare_images(image1, image2):
    # Verificar si las imágenes están en formato correcto
    image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
    image2 = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    hist_image1 = cv2.calcHist([gray_image1], [0], None, [256], [0, 256])
    hist_image2 = cv2.calcHist([gray_image2], [0], None, [256], [0, 256])
    hist_image1 = cv2.normalize(hist_image1, hist_image1).flatten()
    hist_image2 = cv2.normalize(hist_image2, hist_image2).flatten()
    similarity = cv2.compareHist(hist_image1, hist_image2, cv2.HISTCMP_CORREL)
    similarity_score = similarity * 100

    return similarity_score


# pyautogui.locate
# pyautogui.locateAll
# !pyautogui.locateAllOnScreen Devuelve una especie de lista que solo se puede iterar a traves de un loop
# pyautogui.locateCenterOnScreen
# pyautogui.locateOnScreen
# pyautogui.locateOnWindow

#! ajustar a porcentajes
def ajustar_valores(x, y):
    # Ajustar x basado en el valor de y
    if y < getY(porcentaje_Y_Uno):
        if x < getX(porcentaje_X_Uno):
            x = getX(porcentaje_X_Uno)
        elif x > getX(porcentaje_X_Dos):
            x = getX(porcentaje_X_Dos)
    else:
        if x < getX(porcentaje_X_Tres):
            x = getX(porcentaje_X_Tres)
        elif x > getX(porcentaje_X_Dos):
            x = getX(porcentaje_X_Dos)

    # Ajustar y basado en el valor de x
    if x < getX(porcentaje_X_Tres):
        if y < getY(porcentaje_Y_Dos):
            y = getY(porcentaje_Y_Dos)
        elif y > getY(porcentaje_Y_Tres):
            y = getY(porcentaje_Y_Tres)
    else:
        if y < getY(porcentaje_Y_Dos):
            y = getY(porcentaje_Y_Dos)
        elif y > getY(porcentaje_Y_Uno):
            y = getY(porcentaje_Y_Uno)

    return x, y


def cord(radius, points, x, y):

    circle_points = [
        (int(x + radius * math.cos(2 * math.pi * i / points)),
         int(y + radius * math.sin(2 * math.pi * i / points)))
        for i in range(points)
    ]

    return circle_points


def soltarHeroe(radio, puntos):
    cords = cord(radio, puntos, coc_window.width/2, coc_window.height/2)
    pyautogui.click(getX(porcentaje_X_Heroe), getY(
        porcentaje_Y_Heroe), _pause=False)
    time.sleep(0.3)
    for (x, y) in cords:
        x, y = ajustar_valores(x, y)
        punto0 = pyautogui.screenshot(region=[getX(porcentaje_X_Heroe_cap), getY(
            porcentaje_Y_Heroe_cap), getW(ancho_X_Heroe_cap), getH(alto_Y_Heroe_cap)])
        # ! problema heroe no se suelta por exceso de velocidad
        pyautogui.click(x, y)
        time.sleep(0.2)
        punto1 = pyautogui.screenshot(region=[getX(porcentaje_X_Heroe_cap), getY(
            porcentaje_Y_Heroe_cap), getW(ancho_X_Heroe_cap), getH(alto_Y_Heroe_cap)])
        print(compare_images(punto0, punto1))
        if compare_images(punto0, punto1) <= 88:
            return True

    return False


def heroe():
    global time_init
    pyautogui.moveTo(coc_window.width/2, coc_window.height/2)
    pyautogui.scroll(-200)
    pyautogui.scroll(-200)
    pyautogui.scroll(-200)
    time.sleep(0.1)  # !
    if not (is_gray(porcentaje_X_Heroe_cap, porcentaje_Y_Heroe_cap, ancho_X_Heroe_cap, alto_Y_Heroe_cap)):
        disaint = True
        radio = 300
        puntos = 4
        run = 1
        while disaint:
            if soltarHeroe(radio, puntos):
                disaint = False
                time_init = time.time()
            else:
                puntos += 2
                run += 1
                if run == 3:
                    run = 0
                    radio += 50

        # ! Desplegar tropa en uno de los puntos dados por el circulo
        # ? Revisar si la imagen dio señas de haberse desplegado

    time.sleep(1)


def trops():
    virat = True
    contador = 0
    x = getX(porcentaje_X_Contador)
    while virat:
        if len(getText(x, porcentaje_Y_Contador, cont_ancho, cont_alto, min=250, crud=True)) == 0:
            virat = False
            contador -= 1
            return contador
        else:
            contador += 1
            x += getW(cont_movimiento)


def cart():
    sent = True
    x = getX(porcentaje_X_Contador)
    while sent:
        if is_gray(x, porcentaje_Y_Contador, cont_ancho, trop_alto, crud=True):
            x += getW(cont_movimiento)
        else:
            a, b = x + (getW(cont_ancho) / 2), getY(porcentaje_Y_Contador) + \
                (getH(trop_alto) / 2)
            sent = False
            return a, b


def soltarTr(x, y, trop):
    pyautogui.click(x, y, _pause=False)
    tesar = True
    radio = 250
    puntos = 10
    run = 1
    while tesar:
        if soltarTropa(radio, puntos, trop):
            tesar = False
            # print('se solto la tropa')
        else:
            puntos += 2
            run += 1
            if run == 2:
                run = 0
                radio += 50


def soltarTropa(radio, puntos, iterador):
    cords = cord(radio, puntos, coc_window.width/2, coc_window.height/2)
    contador = 0
    origin = getX(porcentaje_X_Contador)
    pos = getW(cont_movimiento) * iterador
    for (x, y) in cords:
        x, y = ajustar_valores(x, y)
        pyautogui.click(x, y, _pause=False)
        contador += 1
        if contador == 24:
            #! problema no identifica si solto todas las tropas
            if getText(origin + pos, porcentaje_Y_Contador,
                       cont_ancho, cont_alto, min=222, crud=True) != 'ox':
                return False
            else:
                return True

    return False


def tropa():
    trop = trops()
    print(f'Cantidad de Tropas: {trop}')
    x, y = cart()
    soltarTr(x, y, trop)


def atacar():
    heroe()
    tropa()


def getW(x):
    x = int((x)/(100/coc_window.width))
    return x


def getH(x):
    x = int((x)/(100/coc_window.height))
    return x


def getX(x):
    x = int((x)/(100/coc_window.width) + coc_window.left)
    return x


def getY(y):
    y = int((y)/(100/coc_window.height) + coc_window.top)
    return y


def final():
    val = getText(porcentaje_X_Tiempo, porcentaje_Y_Tiempo,
                  ancho_Tiempo, alto_Tiempo) == '0s' or getText(porcentaje_X_Tiempo, porcentaje_Y_Tiempo,
                                                                ancho_Tiempo, alto_Tiempo) == 'Os'
    return val


def secondBattle():
    time.sleep(0.1)
    val = getText(porcentaje_X_Destruccion, porcentaje_Y_Destruccion,
                  ancho_Destruccion, alto_Destruccion).find('100') != -1 and getText(porcentaje_X_Tiempo, porcentaje_Y_Tiempo,
                                                                                     ancho_Tiempo, alto_Tiempo) != '0s' and getText(porcentaje_X_Tiempo, porcentaje_Y_Tiempo,
                                                                                                                                    ancho_Tiempo, alto_Tiempo) != 'Os'
    return val


def volver():
    time.sleep(2.3)
    pyautogui.click(getX(porcentaje_X_Volver), getY(
        porcentaje_Y_Volver), _pause=False)
    time.sleep(1)
    while True:
        if len(getText(porcentaje_X_Nombre, porcentaje_Y_Nombre, cap_Ancho_Nombre, cap_Alto_Nombre, min=180, literal=True)) >= 4:
            return True
        else:
            time.sleep(1)

def getText(x, y, ancho, alto, min=200, crud=False, literal=False):
    if crud:
        img = pyautogui.screenshot(region=[x, getY(
            y), getW(ancho), getH(alto)])
    else:
        img = pyautogui.screenshot(region=[getX(x), getY(
            y), getW(ancho), getH(alto)])
    img = np.array(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, min, 255, cv2.THRESH_BINARY)
    th = cv2.bitwise_not(th)
    if crud or literal:
        text = pytesseract.image_to_string(th)
    else:
        text = pytesseract.image_to_string(th, config=options)
    text = text.strip()
    return text


contador = 1
# * Ejecucion del Bot
for i in range(200):
    print('-'*30)
    if coc_window:
        # Obtener dimensiones y posición de la ventana
        # print(f"Posición: {coc_window.left}, {coc_window.top}")
        # print(f"Dimensiones: {coc_window.width}x{coc_window.height}")

        # Activar la ventana (equivalente a Alt+Tab directo)
        coc_window.activate()

        # (Opcional) Mover el mouse a una posición dentro de la ventana
        # pyautogui.moveTo(coc_window.left + 10, coc_window.top + 10)
        # ! Notable reutilizacion de codigo a la vista
        coc_window.moveTo(0, 0)
        # Atacar
        pyautogui.click(getX(porcentaje_X_Atacar), getY(
            porcentaje_Y_Atacar))  # mover a boton atacar

        # Buscar
        time.sleep(0.1)
        pyautogui.click(getX(porcentaje_X_Buscar), getY(
            porcentaje_Y_Buscar))  # mover a boton atacar

        # Leer Tiempo
        trast = True
        # Porcentaje
        time.sleep(3)
        while trast:
            # ! ¿Inicio una partida?
            time.sleep(1)
            if len(getText(porcentaje_X_Tiempo, porcentaje_Y_Tiempo,
                           ancho_Tiempo, alto_Tiempo)) >= 2:
                atacar()
                slap = time.time()
                while trast:
                    if final():
                        volver()
                        trast = False
                    elif secondBattle():
                        print('Segunda batalla')
                        time.sleep(10)
                        if getText(porcentaje_X_Volver_Cap, porcentaje_Y_Volver_Cap, cap_Ancho_Volver, cap_Alto_Volver, literal=True, min=184) != 'Volver':
                            atacar()
                            while trast:
                                if final():
                                    volver()
                                    trast = False
                                else:
                                    time_end = time.time()
                                    endi = time_end - time_init
                                    if endi >= 182:
                                        print(f'Tiempo pasado : {endi}')
                                        trast = False
                                        volver()
                                    else:
                                        low = time.time()
                                        if (low - slap) >= 3:
                                            slap = time.time()
                                            if getText(porcentaje_X_Volver_Cap, porcentaje_Y_Volver_Cap, cap_Ancho_Volver, cap_Alto_Volver, literal=True, min=184) == 'Volver':
                                                volver()
                                                trast = False
                        else:
                            print('Se encontro volver')
                            volver()
                            trast = False
                    else:
                        time.sleep(0.2)
                        time_end = time.time()
                        endi = time_end - time_init
                        if endi >= 182:
                            print(f'Tiempo pasado : {endi}')
                            trast = False
                            volver()
                        else:
                            low = time.time()
                            if (low - slap) >= 3:
                                slap = time.time()
                                if getText(porcentaje_X_Volver_Cap, porcentaje_Y_Volver_Cap, cap_Ancho_Volver, cap_Alto_Volver, literal=True, min=184) == 'Volver':
                                    volver()
                                    trast = False

            else:
                print('Esperando a la batalla')

    else:
        print("No se encontró la ventana de 'Clash of Clans'.")

    print(f'Partida numero {contador}')
    if (contador % 10) == 0:
        time.sleep(0.2)
        pyautogui.click(getX(recurso_X), getY(recurso_Y), _pause=False)
        time.sleep(0.3)
        pyautogui.click(getX(tomar_X), getY(tomar_Y), _pause=False)
        time.sleep(0.1)
        pyautogui.click(getX(porcentaje_X_Atacar), getY(porcentaje_Y_Atacar))

    contador += 1
