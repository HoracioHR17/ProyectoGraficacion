from OpenGL.GL import *
from OpenGL.GLU import *
from src.config import Config
import math

class EscenaRenderer:
    
    LUZ_POS = [-60.0, 60.0, 20.0, 1.0]
    
    @staticmethod
    def configurar_iluminacion():
        glEnable(GL_LIGHTING)      
        glEnable(GL_LIGHT0)        
        glEnable(GL_COLOR_MATERIAL) 
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE) 
        glEnable(GL_NORMALIZE)
        
        ambient = [0.3, 0.3, 0.3, 1.0] 
        diffuse = [0.9, 0.9, 0.9, 1.0] 
        specular = [0.5, 0.5, 0.5, 1.0]
        
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
        glLightfv(GL_LIGHT0, GL_POSITION, EscenaRenderer.LUZ_POS)

    @staticmethod
    def configurar_niebla():
        glEnable(GL_FOG)
        glFogfv(GL_FOG_COLOR, (*Config.AZUL_CIELO, 1.0)) 
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogf(GL_FOG_START, 60.0)    
        glFogf(GL_FOG_END, Config.LARGO_CALZADA + 150.0)

    @staticmethod
    def dibujar_sol():
        glPushMatrix()
        glTranslatef(EscenaRenderer.LUZ_POS[0], EscenaRenderer.LUZ_POS[1], EscenaRenderer.LUZ_POS[2])
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 0.9, 0.0) 
        quad = gluNewQuadric()
        gluSphere(quad, 6.0, 16, 16)
        glEnable(GL_LIGHTING)
        glPopMatrix()

    @staticmethod
    def dibujar_suelo(tex_pasto_id=None):
        largo = Config.LARGO_CALZADA
        ancho_calzada = 12.0
        guarnicion_ancho = 0.5
        ancho_pasto = 53.5 
        
        glDisable(GL_TEXTURE_2D)
        
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.2, 0.2, 0.2, 1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [50.0])
        glColor3f(*Config.GRIS_CALZADA)
        
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glVertex3f(-ancho_calzada/2, 0, 10); glVertex3f(ancho_calzada/2, 0, 10)
        glVertex3f(ancho_calzada/2, 0, -largo); glVertex3f(-ancho_calzada/2, 0, -largo)
        glEnd()
        
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0, 1])
        glColor3f(*Config.GRIS_GUARNICION)
        
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glVertex3f(-ancho_calzada/2 - guarnicion_ancho, 0.1, 10); glVertex3f(-ancho_calzada/2, 0.1, 10)
        glVertex3f(-ancho_calzada/2, 0.1, -largo); glVertex3f(-ancho_calzada/2 - guarnicion_ancho, 0.1, -largo)
        glVertex3f(ancho_calzada/2, 0.1, 10); glVertex3f(ancho_calzada/2 + guarnicion_ancho, 0.1, 10)
        glVertex3f(ancho_calzada/2 + guarnicion_ancho, 0.1, -largo); glVertex3f(ancho_calzada/2, 0.1, -largo)
        glEnd()
        
        if tex_pasto_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, tex_pasto_id)
            glColor3f(1, 1, 1)
        else:
            glColor3f(*Config.VERDE_PASTO)

        rep = 15.0 
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glTexCoord2f(0, 0); glVertex3f(-ancho_calzada/2 - guarnicion_ancho - ancho_pasto, 0, 10)
        glTexCoord2f(rep, 0); glVertex3f(-ancho_calzada/2 - guarnicion_ancho, 0, 10)
        glTexCoord2f(rep, rep); glVertex3f(-ancho_calzada/2 - guarnicion_ancho, 0, -largo)
        glTexCoord2f(0, rep); glVertex3f(-ancho_calzada/2 - guarnicion_ancho - ancho_pasto, 0, -largo)
        
        glTexCoord2f(0, 0); glVertex3f(ancho_calzada/2 + guarnicion_ancho, 0, 10)
        glTexCoord2f(rep, 0); glVertex3f(ancho_calzada/2 + guarnicion_ancho + ancho_pasto, 0, 10)
        glTexCoord2f(rep, rep); glVertex3f(ancho_calzada/2 + guarnicion_ancho + ancho_pasto, 0, -largo)
        glTexCoord2f(0, rep); glVertex3f(ancho_calzada/2 + guarnicion_ancho, 0, -largo)
        glEnd()
        glDisable(GL_TEXTURE_2D)

        glDisable(GL_LIGHTING)
        glColor3f(1.0, 1.0, 1.0) 
        glLineWidth(2.0)
        glBegin(GL_LINES)
        for z in range(10, -int(largo), -5):
            glVertex3f(0, 0.03, z); glVertex3f(0, 0.03, z - 3)
        glEnd()
        glLineWidth(1.0)
        glEnable(GL_LIGHTING)

    @staticmethod
    def dibujar_cartel(x, z, tex_id):
        glPushMatrix()
        glTranslatef(x, 0, z)
        glRotatef(-90, 0, 1, 0)
        
        glColor3f(0.3, 0.15, 0.05)
        for px in [-1.8, 1.8]:
            glPushMatrix(); glTranslatef(px, 1.2, 0); glScalef(0.2, 2.4, 0.2); EscenaRenderer.cubo_simple(); glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0, 2.5, 0)
        
        glPushMatrix()
        glScalef(4.4, 1.6, 0.15)
        EscenaRenderer.cubo_simple()
        glPopMatrix()
        
        if tex_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, tex_id)
            glColor3f(1, 1, 1)
            w, h = 4.2, 1.4
            
            glBegin(GL_QUADS)
            glNormal3f(0, 0, 1)
            glTexCoord2f(0, 0); glVertex3f(-w/2, -h/2, 0.08)
            glTexCoord2f(1, 0); glVertex3f(w/2, -h/2, 0.08)
            glTexCoord2f(1, 1); glVertex3f(w/2, h/2, 0.08)
            glTexCoord2f(0, 1); glVertex3f(-w/2, h/2, 0.08)
            glEnd()
            glDisable(GL_TEXTURE_2D)
            
        glPopMatrix()
        glPopMatrix()

    @staticmethod
    def dibujar_caseta(x, z):
        glPushMatrix()
        glTranslatef(x, 1.5, z)
        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix(); glScalef(3.0, 3.0, 3.0); EscenaRenderer.cubo_simple(); glPopMatrix()
        glColor3f(0.2, 0.2, 0.3)
        glPushMatrix(); glTranslatef(-1.51, 0.2, 0); glScalef(0.1, 1.5, 2.0); EscenaRenderer.cubo_simple(); glPopMatrix()
        glColor3f(0.4, 0.4, 0.4)
        glPushMatrix(); glTranslatef(0, 1.6, 0); glScalef(3.4, 0.2, 3.4); EscenaRenderer.cubo_simple(); glPopMatrix()
        glPopMatrix()

    @staticmethod
    def dibujar_kiosko(x, z):
        glPushMatrix()
        glTranslatef(x, 0, z)
        glColor3f(0.1, 0.1, 0.3)
        for px in [-1.5, 1.5]:
            for pz in [-1.5, 1.5]:
                glPushMatrix(); glTranslatef(px, 1.5, pz); glScalef(0.15, 3.0, 0.15); EscenaRenderer.cubo_simple(); glPopMatrix()
        glColor3f(0.8, 0.8, 0.8)
        glPushMatrix(); glTranslatef(0, 3.0, 0); glScalef(3.8, 0.1, 3.8); EscenaRenderer.cubo_simple(); glPopMatrix()
        glColor3f(0.4, 0.2, 0.1)
        glPushMatrix(); glTranslatef(0, 0.8, 0); glScalef(1.5, 0.1, 2.5); EscenaRenderer.cubo_simple(); glPopMatrix()
        glPushMatrix(); glTranslatef(0, 0.4, 0); glScalef(0.5, 0.8, 0.5); EscenaRenderer.cubo_simple(); glPopMatrix()
        for sx in [-1.2, 1.2]:
            glPushMatrix(); glTranslatef(sx, 0.5, 0); glScalef(0.6, 0.1, 2.5); EscenaRenderer.cubo_simple(); glPopMatrix()
            for sz in [-1.0, 1.0]:
                glPushMatrix(); glTranslatef(sx, 0.25, sz); glScalef(0.1, 0.5, 0.1); EscenaRenderer.cubo_simple(); glPopMatrix()
        glPopMatrix()

    @staticmethod
    def _geometria_venus():
        quad = gluNewQuadric()
        base_y = 1.0
        glPushMatrix(); glTranslatef(0, 0.5, 0); glScalef(1.2, 1.0, 1.2); EscenaRenderer.cubo_simple(); glPopMatrix()
        glPushMatrix(); glTranslatef(0, base_y, 0); glRotatef(-90, 1, 0, 0); gluCylinder(quad, 0.4, 0.3, 1.5, 12, 1); glPopMatrix()
        glPushMatrix(); glTranslatef(0, base_y + 1.5, 0); glRotatef(-90, 1, 0, 0); gluCylinder(quad, 0.3, 0.25, 0.8, 12, 1); glPopMatrix()
        glPushMatrix(); glTranslatef(0, base_y + 2.5, 0); gluSphere(quad, 0.25, 12, 12); glPopMatrix()
        glPushMatrix(); glTranslatef(0.3, base_y + 2.0, 0); glRotatef(-45, 0, 0, 1); glRotatef(-90, 1, 0, 0); gluCylinder(quad, 0.08, 0.06, 0.8, 8, 1); glPopMatrix()
        glPushMatrix(); glTranslatef(-0.3, base_y + 2.0, 0); glRotatef(20, 0, 0, 1); glRotatef(-90, 1, 0, 0); gluCylinder(quad, 0.08, 0.06, 0.8, 8, 1); glPopMatrix()

    @staticmethod
    def _geometria_arbol():
        quad = gluNewQuadric()
        glPushMatrix(); glRotatef(-90, 1, 0, 0); gluCylinder(quad, 0.6, 0.6, 4.0, 12, 1); glPopMatrix()
        glPushMatrix(); glTranslatef(0, 5.0, 0); gluSphere(quad, 2.8, 16, 16); glPopMatrix()

    @staticmethod
    def dibujar_venus(x, z, tex_id=None):
        glPushMatrix()
        glTranslatef(x, 0, z)
        glScalef(1.2, 1.2, 1.2)
        glColor3f(0.5, 0.5, 0.5)
        glPushMatrix(); glTranslatef(0, 0.5, 0); glScalef(1.2, 1.0, 1.2); EscenaRenderer.cubo_simple(); glPopMatrix()
        glColor3f(0.9, 0.9, 0.85)
        quad = gluNewQuadric(); base_y = 1.0
        glPushMatrix(); glTranslatef(0, base_y, 0); glRotatef(-90, 1, 0, 0); gluCylinder(quad, 0.4, 0.3, 1.5, 12, 1); glPopMatrix()
        glPushMatrix(); glTranslatef(0, base_y + 1.5, 0); glRotatef(-90, 1, 0, 0); gluCylinder(quad, 0.3, 0.25, 0.8, 12, 1); glPopMatrix()
        glPushMatrix(); glTranslatef(0, base_y + 2.5, 0); gluSphere(quad, 0.25, 12, 12); glPopMatrix()
        glPushMatrix(); glTranslatef(0.3, base_y + 2.0, 0); glRotatef(-45, 0, 0, 1); glRotatef(-90, 1, 0, 0); gluCylinder(quad, 0.08, 0.06, 0.8, 8, 1); glPopMatrix()
        glPushMatrix(); glTranslatef(-0.3, base_y + 2.0, 0); glRotatef(20, 0, 0, 1); glRotatef(-90, 1, 0, 0); gluCylinder(quad, 0.08, 0.06, 0.8, 8, 1); glPopMatrix()
        glPopMatrix()

    @staticmethod
    def dibujar_arbol(x, z):
        glPushMatrix()
        glTranslatef(x, 0, z)
        glColor3f(*Config.CAFE_TRONCO)
        quad = gluNewQuadric()
        glPushMatrix(); glRotatef(-90, 1, 0, 0); gluCylinder(quad, 0.6, 0.6, 4.0, 12, 1); glPopMatrix()
        glColor3f(*Config.VERDE_HOJAS)
        glPushMatrix(); glTranslatef(0, 5.0, 0); gluSphere(quad, 2.8, 16, 16); glPopMatrix()
        glPopMatrix()

    @staticmethod
    def dibujar_arbusto(x, z):
        glPushMatrix()
        glTranslatef(x, 0, z)
        glColor3f(0.1, 0.45, 0.1) 
        glScalef(1.8, 0.8, 1.8)
        quad = gluNewQuadric()
        gluSphere(quad, 1.0, 12, 12)
        glPopMatrix()

    @staticmethod
    def dibujar_banca(x, z, rotacion):
        glPushMatrix()
        glTranslatef(x, 0.6, z); glRotatef(rotacion, 0, 1, 0); glColor3f(1.0, 1.0, 1.0) 
        glPushMatrix(); glScalef(3.6, 0.3, 1.5); EscenaRenderer.cubo_simple(); glPopMatrix()
        for px in [-1.5, 1.5]: 
            glPushMatrix(); glTranslatef(px, -0.3, 0); glScalef(0.5, 0.7, 1.2); EscenaRenderer.cubo_simple(); glPopMatrix()
        glPopMatrix()

    @staticmethod
    def dibujar_edificio(z_pos, tex_id):
        ancho, alto, profundidad = 120.0, 40.0, 25.0
        glPushMatrix()
        glTranslatef(0, alto/2, z_pos)
        if tex_id:
            glEnable(GL_TEXTURE_2D); glBindTexture(GL_TEXTURE_2D, tex_id); glColor3f(1, 1, 1) 
            glBegin(GL_QUADS); glNormal3f(0, 0, 1)
            glTexCoord2f(0, 1); glVertex3f(-ancho/2, alto/2, 0); glTexCoord2f(0, 0); glVertex3f(-ancho/2, -alto/2, 0)
            glTexCoord2f(1, 0); glVertex3f(ancho/2, -alto/2, 0); glTexCoord2f(1, 1); glVertex3f(ancho/2, alto/2, 0)
            glEnd(); glDisable(GL_TEXTURE_2D)
        
        glColor3f(0.2, 0.25, 0.35) 
        glBegin(GL_QUADS)
        glVertex3f(-ancho/2, alto/2, 0); glVertex3f(ancho/2, alto/2, 0); glVertex3f(ancho/2, alto/2, -profundidad); glVertex3f(-ancho/2, alto/2, -profundidad)
        glVertex3f(-ancho/2, alto/2, 0); glVertex3f(-ancho/2, alto/2, -profundidad); glVertex3f(-ancho/2, -alto/2, -profundidad); glVertex3f(-ancho/2, -alto/2, 0)
        glVertex3f(ancho/2, alto/2, 0); glVertex3f(ancho/2, alto/2, -profundidad); glVertex3f(ancho/2, -alto/2, -profundidad); glVertex3f(ancho/2, -alto/2, 0)
        glEnd()
        glPopMatrix()

    @staticmethod
    def _dibujar_sombra_generica(geometria_func):
        lx, ly, lz = EscenaRenderer.LUZ_POS[0], EscenaRenderer.LUZ_POS[1], EscenaRenderer.LUZ_POS[2]
        matrix = [1.0, 0.0, 0.0, 0.0, -lx/ly, 0.0, -lz/ly, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.1, 0.0, 1.0]
        glMultMatrixf(matrix)
        glDisable(GL_LIGHTING); glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.0, 0.0, 0.0, 0.5) 
        geometria_func()
        glDisable(GL_BLEND); glEnable(GL_LIGHTING)

    @staticmethod
    def dibujar_sombra_arbol(x, z):
        glPushMatrix()
        glTranslatef(x, 0.02, z)
        EscenaRenderer._dibujar_sombra_generica(EscenaRenderer._geometria_arbol)
        glPopMatrix()

    @staticmethod
    def dibujar_sombra_venus(x, z):
        glPushMatrix()
        glTranslatef(x, 0.02, z)
        glScalef(1.2, 1.2, 1.2)
        EscenaRenderer._dibujar_sombra_generica(EscenaRenderer._geometria_venus)
        glPopMatrix()

    @staticmethod
    def cubo_simple():
        glBegin(GL_QUADS)
        glNormal3f(0,0,1); glVertex3f(-0.5,-0.5,0.5); glVertex3f(0.5,-0.5,0.5); glVertex3f(0.5,0.5,0.5); glVertex3f(-0.5,0.5,0.5)
        glNormal3f(0,0,-1); glVertex3f(-0.5,-0.5,-0.5); glVertex3f(-0.5,0.5,-0.5); glVertex3f(0.5,0.5,-0.5); glVertex3f(0.5,-0.5,-0.5)
        glNormal3f(-1,0,0); glVertex3f(-0.5,-0.5,-0.5); glVertex3f(-0.5,-0.5,0.5); glVertex3f(-0.5,0.5,0.5); glVertex3f(-0.5,0.5,-0.5)
        glNormal3f(1,0,0); glVertex3f(0.5,-0.5,-0.5); glVertex3f(0.5,0.5,-0.5); glVertex3f(0.5,0.5,0.5); glVertex3f(0.5,-0.5,0.5)
        glNormal3f(0,1,0); glVertex3f(-0.5,0.5,-0.5); glVertex3f(-0.5,0.5,0.5); glVertex3f(0.5,0.5,0.5); glVertex3f(0.5,0.5,-0.5)
        glNormal3f(0,-1,0); glVertex3f(-0.5,-0.5,-0.5); glVertex3f(0.5,-0.5,-0.5); glVertex3f(0.5,-0.5,0.5); glVertex3f(-0.5,-0.5,0.5)
        glEnd()