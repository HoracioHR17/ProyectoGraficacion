import numpy as np
import math
from OpenGL.GLU import gluLookAt
from pygame.locals import *
from src.config import Config

class Camara:
    def __init__(self):
        self.pos = np.array([0.0, 2.0, 5.0], dtype=np.float32)
        self.yaw = -90.0 
        self.pitch = -5.0
        self.front = np.array([0.0, 0.0, -1.0])
        self.right = np.array([1.0, 0.0, 0.0])
        self.up = np.array([0.0, 1.0, 0.0])

    def actualizar_vectores(self):
        rad_yaw = math.radians(self.yaw)
        rad_pitch = math.radians(self.pitch)
        x = math.cos(rad_yaw) * math.cos(rad_pitch)
        y = math.sin(rad_pitch)
        z = math.sin(rad_yaw) * math.cos(rad_pitch)
        self.front = np.array([x, y, z])
        norm = np.linalg.norm(self.front)
        if norm > 0: self.front /= norm
        self.right = np.cross(self.front, np.array([0.0, 1.0, 0.0]))
        self.right /= np.linalg.norm(self.right)
        self.up = np.cross(self.right, self.front)

    def procesar_input(self, teclas):
        front_xz = np.array([self.front[0], 0.0, self.front[2]])
        norm = np.linalg.norm(front_xz)
        if norm > 0: front_xz /= norm
        
        vel = Config.VELOCIDAD_CAMARA
        if teclas[K_w]: self.pos += front_xz * vel
        if teclas[K_s]: self.pos -= front_xz * vel
        if teclas[K_a]: self.pos -= self.right * vel
        if teclas[K_d]: self.pos += self.right * vel
        
        sens = Config.SENSIBILIDAD_CAMARA * 5
        if teclas[K_LEFT]: self.yaw -= sens
        if teclas[K_RIGHT]: self.yaw += sens
        if teclas[K_UP]: self.pitch += sens 
        if teclas[K_DOWN]: self.pitch -= sens 
        
        self.pitch = np.clip(self.pitch, -89, 89)
        self.pos[1] = 2.0 
        
        if self.pos[2] < -Config.LARGO_CALZADA + 2: self.pos[2] = -Config.LARGO_CALZADA + 2
        if self.pos[2] > 10: self.pos[2] = 10

    def aplicar_vista(self):
        target = self.pos + self.front
        gluLookAt(self.pos[0], self.pos[1], self.pos[2],
                  target[0], target[1], target[2],
                  0.0, 1.0, 0.0)