import math
import numpy as np
import pytesseract
import cv2
import time
import pyautogui
import pygetwindow as gw
from random import randint


class ClashBot:

    def __init__(self):
        self.pytesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pytesseract.pytesseract.tesseract_cmd = self.pytesseract_path
        self.psm = 7
        self.alphanumeric = "axMsO0123456789"
        self.options = "-c tessedit_char_whitelist={}".format(
            self.alphanumeric)
        self.options += " --oem 3 --psm {}".format(self.psm)
        self.init_dimensions()
        self.coc_window = self.get_coc_window()
        self.time_init = 0
        self.time_end = 0

    def init_dimensions(self):
        self.pAncho = 100 / 1339
        self.pAltura = 100 / 783
        self.init_positions()

    def init_positions(self):
        self.positions = {
            "atacar": (self.pAncho * 79, self.pAltura * 695),
            "buscar": (self.pAncho * 994, self.pAltura * 517),
            "tiempo": (self.pAncho * 589, self.pAltura * 60, self.pAncho * 190, self.pAltura * 64),
            "tropa": (self.pAncho * 331, self.pAltura * 712),
            "destruccion": (self.pAncho * 1142, self.pAltura * 601, self.pAncho * 161, self.pAltura * 32),
            "heroe": (self.pAncho * 234, self.pAltura * 716),
            "heroe_cap": (self.pAncho * 191, self.pAltura * 663, self.pAncho * 74, self.pAltura * 100),
            "volver": (self.pAncho * 666, self.pAltura * 658),
            "nombre": (self.pAncho * 93, self.pAltura * 43, self.pAncho * 52, self.pAltura * 16),
            "volver_cap": (self.pAncho * 617, self.pAltura * 642, self.pAncho * 100, self.pAltura * 30),
            "recurso": (self.pAncho * 874, self.pAltura * 38),
            "tomar": (self.pAncho * 973, self.pAltura * 654),
            "margen": {
                "x": (self.pAncho * 175, self.pAncho * 1163, self.pAncho * 568),
                "y": (self.pAltura * 624, self.pAltura * 112, self.pAltura * 542)
            },
            "contador": (self.pAncho * 291, self.pAltura * 662, self.pAncho * 72,
                         self.pAltura * 20, self.pAltura * 80, self.pAncho * 87)
        }

    def get_coc_window(self):
        windows = gw.getAllTitles()
        for window in windows:
            if "Clash of Clans" in window:
                return gw.getWindowsWithTitle(window)[0]
        return None
    
    def setTrast(self,slap):
        self.time_end = time.time()
        if (self.time_end - self.time_init) >= 182:
            self.volver
            return  False
        else:
            low = time.time()
            if (low - self.slap) >= 3:
                self.slap = time.time()
                if self.text(self.positions["volver_cap"][0], self.positions["volver_cap"][1], self.positions["volver_cap"][2], self.positions["volver_cap"][3], literal=True, min=184) == 'Volver':
                    self.volver()
                    return False
        return True

    def secondBatle(self):
        time.sleep(0.1)
        return self.text(self.positions["destruccion"][0], self.positions["destruccion"][1],
                  self.positions["destruccion"][2], self.positions["destruccion"][3]).find('100') != -1 and self.text(self.positions["tiempo"][0], self.positions["tiempo"][1],
                                                                                     self.positions["tiempo"][2], self.positions["tiempo"][3]) != '0s' and self.text(self.positions["tiempo"][0], self.positions["tiempo"][1],
                                                                                                                                    self.positions["tiempo"][2], self.positions["tiempo"][3]) != 'Os'
    def volver(self):
        time.sleep(2.3)
        pyautogui.click(self.getX(self.positions["volver"][0]), 
                        self.getY(self.positions["volver"][1]), _pause=False)
        time.sleep(1)
        while True:
            if len(self.text(self.positions["nombre"][0], self.positions["nombre"][1], self.positions["nombre"][2], self.positions["nombre"][3],180, literal=True)) >= 4:
                return True
            else:
                time.sleep(1) 


    def final(self):
        return self.text(self.positions["tiempo"][0], self.positions["tiempo"][1],
                  self.positions["tiempo"][2], self.positions["tiempo"][3]) == '0s' or self.text(self.positions["tiempo"][0], self.positions["tiempo"][1],
                                                                self.positions["tiempo"][2], self.positions["tiempo"][3]) == 'Os'

    
    def cord(self,radius, points, x, y):
        circle_points = [
            (int(x + radius * math.cos(2 * math.pi * i / points)),
            int(y + radius * math.sin(2 * math.pi * i / points)))
            for i in range(points)
        ]
        return circle_points

    def liberarTropa(self,radio,puntos,iterador):
        cords = self.cord(radio,puntos, self.coc_window.width/2, self.coc_window.height/2)
        contador = 0
        origin = self.getX(self.positions["contador"][0])
        pos = self.getW(self.positions["contador"][5]) * iterador
        for (x,y) in cords:
            x, y = self.ajustar_valores(x,y) 
            pyautogui.click(x,y, _pause = False)
            contador += 1
            if contador == 24:
                return self.text(origin + pos, self.positions["contador"][1],
                                 self.positions["contador"][2], self.positions["contador"][3],222,True) == 'ox'
            
        
        return False
            

    def soltarTropa(self,x,y,trop):
        pyautogui.click(x,y, _pause = False)
        radio = 180
        puntos = 10
        run = 1
        while True:
            if self.liberarTropa(radio,puntos,trop):
                break
            else:
                puntos += 2
                run += 1
                if run == 2:
                    run = 0
                    radio += 50
    
    def cart(self):
        x = self.getX(self.positions["contador"][0])
        while True:
            if self.is_gray(x, self.positions["contador"][1], self.positions["contador"][2], self.positions["contador"][3], True):
                x += self.getW(self.positions["contador"][5])
            else:
                return x + (self.getW(self.positions["contador"][2]) / 2), self.getY(self.positions["contador"][1]) + \
                (self.getH(self.positions["contador"][4]) / 2)
    
    def trops(self):
        contador = 0
        conf = 253
        x = self.getX(self.positions["contador"][0])
        while True:
            if len(self.text(x, self.positions["contador"][1], self.positions["contador"][2], self.positions["contador"][3], conf, crud=True)) == 0:
                contador -= 1
                if contador != -1:
                    return contador
                conf = randint(235, 252)
            else:
                contador += 1
                x += self.getW(self.positions["contador"][5])

    
    def tropa(self):
        trop = self.trops()
        x, y = self.cart()
        self.soltarTropa(x,y,trop)

    
    def compare_images(self, image1, image2):
        image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
        image2 = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)
        gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        hist_image1 = cv2.calcHist([gray_image1], [0], None, [256], [0, 256])
        hist_image2 = cv2.calcHist([gray_image2], [0], None, [256], [0, 256])
        hist_image1 = cv2.normalize(hist_image1, hist_image1).flatten()
        hist_image2 = cv2.normalize(hist_image2, hist_image2).flatten()
        similarity = cv2.compareHist(hist_image1, hist_image2, cv2.HISTCMP_CORREL)
        return similarity * 100
    
    def ajustar_valores(self, x, y):
        if y < self.getY(self.positions["margen"]["y"][0]):
            if x < self.getX(self.positions["margen"]["x"][0]):
                x = self.getX(self.positions["margen"]["x"][0])
            elif x > self.getX(self.positions["margen"]["x"][1]):
                x = self.getX(self.positions["margen"]["x"][1])
        else:
            if x < self.getX(self.positions["margen"]["x"][2]):
                x = self.getX(self.positions["margen"]["x"][2])
            elif x > self.getX(self.positions["margen"]["x"][1]):
                x = self.getX(self.positions["margen"]["x"][1])

        if x < self.getX(self.positions["margen"]["x"][2]):
            if y < self.getY(self.positions["margen"]["y"][1]):
                y = self.getY(self.positions["margen"]["y"][1])
            elif y > self.getY(self.positions["margen"]["y"][2]):
                y = self.getY(self.positions["margen"]["y"][2])
        else:
            if y < self.getY(self.positions["margen"]["y"][1]):
                y = self.getY(self.positions["margen"]["y"][1])
            elif y > self.getY(self.positions["margen"]["y"][0]):
                y = self.getY(self.positions["margen"]["y"][0])

        return x, y

    def soltarHeroe(self, radio, puntos):
        cords = self.cord(radio, puntos, self.coc_window.width / 2, self.coc_window.height / 2)
        pyautogui.click(self.getX(self.positions["heroe"][0]), self.getY(self.positions["heroe"][1]), _pause=False)
        time.sleep(0.3)
        for (x, y) in cords:
            x, y = self.ajustar_valores(x, y)
            punto0 = pyautogui.screenshot(region=[self.getX(self.positions["heroe_cap"][0]),
                                                  self.getY(self.positions["heroe_cap"][1]),
                                                  self.getW(self.positions["heroe_cap"][2]),
                                                  self.getH(self.positions["heroe_cap"][3])])
            pyautogui.click(x, y)
            time.sleep(0.2)
            punto1 = pyautogui.screenshot(region=[self.getX(self.positions["heroe_cap"][0]),
                                                  self.getY(self.positions["heroe_cap"][1]),
                                                  self.getW(self.positions["heroe_cap"][2]),
                                                  self.getH(self.positions["heroe_cap"][3])])
            if self.compare_images(punto0, punto1) <= 88:
                return True
        return False

    def is_gray(self, x, y, w, h, crud=False, umbral=10):
        x = self.getX(x) if not crud else x
        img = pyautogui.screenshot(region=[x, self.getY(y), self.getW(w), self.getH(h)])
        imagen_np = np.array(img)
        if imagen_np.shape[-1] == 4:
            imagen_np = imagen_np[:, :, :3]
        std_dev = np.std(imagen_np, axis=-1)
        mean_std_dev = np.mean(std_dev)
        return mean_std_dev < umbral

    def heroe(self):
        self.time_init = time.time()
        pyautogui.moveTo(self.coc_window.width / 2, self.coc_window.height / 2)
        time.sleep(0.2)
        for _ in range(3): pyautogui.scroll(-200)
        print('aqui scroll')
        time.sleep(0.1)
        if not self.is_gray(self.positions["heroe_cap"][0], self.positions["heroe_cap"][1],
                            self.positions["heroe_cap"][2], self.positions["heroe_cap"][3]):
            radio = 300
            puntos = 4
            run = 1
            while True:
                if self.soltarHeroe(radio, puntos):
                    self.time_init = time.time()
                    break
                else:
                    puntos += 2
                    run += 1
                    if run == 3:
                        run = 0
                        radio += 50
        time.sleep(1)

    def text(self, x, y, w, h, min=200, crud=False, literal=False):
        x = self.getX(x) if not crud else x
        img = pyautogui.screenshot(region=[x, self.getY(y), self.getW(w), self.getH(h)])
        img = np.array(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, th = cv2.threshold(gray, min, 255, cv2.THRESH_BINARY)
        th = cv2.bitwise_not(th)
        config = None if (crud or literal) else self.options
        text = pytesseract.image_to_string(th, config=config)
        return text.strip()


    def getX(self, x):
        return int((x) / (100 / self.coc_window.width) + self.coc_window.left)

    def getY(self, y):
        return int((y) / (100 / self.coc_window.height) + self.coc_window.top)

    def getW(self, width):
        return int(width / (100 / self.coc_window.width))

    def getH(self, height):
        return int(height / (100 / self.coc_window.height))

    def start(self):
        for i in range(10):
            if self.coc_window:
                self.coc_window.activate()
                self.coc_window.moveTo(0, 0)
                pyautogui.click(self.getX(self.positions["atacar"][0]),
                                self.getY(self.positions["atacar"][1]))
                time.sleep(0.1)
                pyautogui.click(self.getX(self.positions["buscar"][0]),
                                self.getY(self.positions["buscar"][1]))
                trast = True
                time.sleep(3)
                while trast:
                    time.sleep(1)
                    if len(self.text(self.positions["tiempo"][0],
                                     self.positions["tiempo"][1],
                                     self.positions["tiempo"][2],
                                     self.positions["tiempo"][3])) >= 2:
                        self.heroe()
                        self.tropa()
                        self.slap = time.time()
                        while trast:
                            if self.final():
                                self.volver()
                                trast = False
                            elif self.secondBatle():
                                time.sleep(10)
                                if self.text(self.positions["volver_cap"][0], self.positions["volver_cap"][1], self.positions["volver_cap"][2], self.positions["volver_cap"][3], literal=True, min=184) != 'Volver':
                                    self.heroe()
                                    self.tropa()
                                    while trast:
                                        if self.final():
                                            self.volver()
                                            trast = False
                                        else:
                                            trast = self.setTrast(self.slap)
                                else:
                                    self.volver()
                                    trast = False
                            else:
                                time.sleep(0.2)
                                trast = self.setTrast(self.slap)
                                
                        
                    else: 
                        print('Esperando la Batalla')

            else:
                print('No se encontro la ventana de clash of Clans')

            print(f'Partida numero {i + 1}')
            if ((i + 1) % 10) == 0:
                time.sleep(0.2)
                time.sleep(0.2)
                pyautogui.click(self.getX(self.positions["recurso"][0]),
                                self.getY(self.positions["recurso"][1]), _pause=False)
                time.sleep(0.3)
                pyautogui.click(self.getX(self.positions["tomar"][0]),
                                self.getY(self.positions["tomar"][1]), _pause=False)
                time.sleep(0.1)
                pyautogui.click(self.getX(self.positions["atacar"][0]),
                                self.getY(self.positions["atacar"][1]))



if __name__ == "__main__":
    bot = ClashBot()
    bot.start()