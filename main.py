import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from src.config import Config
from src.camera import Camara
from src.textures import GestorTexturas
from src.renderer import EscenaRenderer
import random
import os

class Aplicacion:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((Config.ANCHO, Config.ALTO), DOUBLEBUF | OPENGL)
        pygame.display.set_caption(Config.TITULO)
        
        self.inicializar_opengl()
        self.camara = Camara()
        self.reloj = pygame.time.Clock()
        self.running = True
        
        self.tex_edificio = GestorTexturas.cargar("assets/edificio.png")
        self.tex_pasto = GestorTexturas.cargar("assets/pasto.png")
        self.tex_letrero = GestorTexturas.cargar("assets/letrero.png")

        self.caseta_pos = (18, 10)

        self.arboles_pos = []
        for z in range(5, -int(Config.LARGO_CALZADA)-20, -15):
            self.arboles_pos.append((-20, z))
            self.arboles_pos.append((25, z))

        for z in range(-20, -60, -8):
            self.arboles_pos.append((35, z))
        self.arboles_pos.append((22, -15))

        self.arbustos_pos = []
        for z in range(5, -int(Config.LARGO_CALZADA), -6):
            bx_izq = -17 + random.uniform(-2, 2)
            if random.random() > 0.4: self.arbustos_pos.append((bx_izq, z))
            bx_der = 28 + random.uniform(-2, 2)
            if random.random() > 0.4: self.arbustos_pos.append((bx_der, z))

        self.bancas_pos = [
            (-9, -8, 90), 
            (-9, -30, 90), 
        ]
        
        self.kioskos_pos = [
            (16, -25), (24, -25),
            (16, -40), (24, -40)
        ]

        self.venus_pos = (-13, -Config.LARGO_CALZADA / 2 - 10)

    def inicializar_opengl(self):
        glViewport(0, 0, Config.ANCHO, Config.ALTO)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(Config.FOV, (Config.ANCHO/Config.ALTO), Config.CERCA, Config.LEJOS)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_DEPTH_TEST)
        EscenaRenderer.configurar_niebla()
        EscenaRenderer.configurar_iluminacion()

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.running = False
        self.camara.procesar_input(pygame.key.get_pressed())

    def renderizar(self):
        glClearColor(*Config.AZUL_CIELO, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        self.camara.actualizar_vectores()
        self.camara.aplicar_vista()
        
        EscenaRenderer.dibujar_sol()
        EscenaRenderer.dibujar_suelo(self.tex_pasto)
        
        glDepthMask(GL_FALSE) 
        for pos in self.arboles_pos: 
            EscenaRenderer.dibujar_sombra_arbol(pos[0], pos[1])
        EscenaRenderer.dibujar_sombra_venus(self.venus_pos[0], self.venus_pos[1])
        glDepthMask(GL_TRUE)

        EscenaRenderer.dibujar_cartel(9.0, -5.0, self.tex_letrero)
        EscenaRenderer.dibujar_caseta(self.caseta_pos[0], self.caseta_pos[1])

        for k_pos in self.kioskos_pos:
            EscenaRenderer.dibujar_kiosko(k_pos[0], k_pos[1])
        
        for (x, z, rot) in self.bancas_pos: 
            EscenaRenderer.dibujar_banca(x, z, rot)
        
        for pos in self.arboles_pos: 
            EscenaRenderer.dibujar_arbol(pos[0], pos[1])
            
        for pos in self.arbustos_pos: 
            EscenaRenderer.dibujar_arbusto(pos[0], pos[1])
            
        EscenaRenderer.dibujar_venus(self.venus_pos[0], self.venus_pos[1], None)
        EscenaRenderer.dibujar_edificio(-Config.LARGO_CALZADA - 20, self.tex_edificio)

        pygame.display.flip()

    def correr(self):
        while self.running:
            self.reloj.tick(Config.FPS)
            self.manejar_eventos()
            self.renderizar()
        pygame.quit()

if __name__ == "__main__":
    app = Aplicacion()
    app.correr()