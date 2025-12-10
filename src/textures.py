import pygame
from OpenGL.GL import *
import os

class GestorTexturas:
    @staticmethod
    def cargar(ruta_relativa, wrap_mode=GL_REPEAT):
        ruta = os.path.join(os.getcwd(), ruta_relativa)
        if not os.path.exists(ruta):
            print(f"[WARN] Textura no encontrada: {ruta}")
            return None
        try:
            image_surface = pygame.image.load(ruta)
            if ruta.lower().endswith(".png"):
                data = pygame.image.tostring(image_surface, "RGBA", 1)
                fmt = GL_RGBA
            else:
                data = pygame.image.tostring(image_surface, "RGB", 1)
                fmt = GL_RGB
            w, h = image_surface.get_width(), image_surface.get_height()
            tex_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, tex_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_mode)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_mode)
            glTexImage2D(GL_TEXTURE_2D, 0, fmt, w, h, 0, fmt, GL_UNSIGNED_BYTE, data)
            return tex_id
        except Exception as e:
            print(f"[ERR] Error cargando textura {ruta}: {e}")
            return None