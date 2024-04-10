from threading import Thread
import cv2
import numpy as np
import mss
import mss.tools

class VideoStream:
    def __init__(self, resolution=(640,480), framerate=30):
        self.resolution = resolution
        self.framerate = framerate
        self.stopped = False
        self.screen = mss.mss()
        self.monitor = self.screen.monitors[0]  # Utiliser le premier moniteur

    def start(self):
        # Démarrer le thread pour lire les frames du flux vidéo
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # Garder la boucle indéfiniment jusqu'à ce que le thread soit arrêté
        while True:
            if self.stopped:
                return

            # Capture un screenshot
            screenshot = self.screen.grab(self.monitor)
            # Convertit le screenshot en un numpy array pour pouvoir l'utiliser avec OpenCV
            frame = np.array(screenshot)
            # Convertit de BGR (qui est le format utilisé par mss) à RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # Redimensionne l'image pour correspondre à la résolution souhaitée
            self.frame = cv2.resize(frame, self.resolution)

    def read(self):
        # Retourner la frame la plus récente
        return self.frame

    def stop(self):
        # Indiquer que la capture d'écran et le thread doivent être arrêtés
        self.stopped = True
