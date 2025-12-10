========================================================================
PROYECTO DE GRAFICACIÓN: CALZADA DE LA ESTUDIANTINA 3D
AUTOR: HERNÁNDEZ RAMÍREZ ANGEL HORACIO
========================================================================

DESCRIPCIÓN
-----------
Este proyecto consiste en una simulación 3D de la calzada de la estudiantina del ITVER
utilizando Python y OpenGL. Incluye renderizado de árboles, arbustos, bancas, edificios, 
iluminación dinámica, sombras proyectadas y texturizado.

ESTRUCTURA DEL PROYECTO
-----------------------
/proyecto_raiz
  |-- main.py             # Punto de entrada de la aplicación
  |-- README.txt          # Este archivo
  |-- /src                # Código fuente
      |-- __init__.py
      |-- camera.py       # Lógica de la cámara
      |-- config.py       # Configuraciones globales
      |-- renderer.py     # Lógica de renderizado con OpenGL
      |-- textures.py     # Gestor de carga de texturas
  |-- /assets             # Recursos gráficos
      |-- pasto.png
      |-- letrero.png
      |-- edificio.png

REQUERIMIENTOS TÉCNICOS
-----------------------
Para ejecutar este proyecto necesitas tener instalado:

1. Python 3.8 o superior.
2. Las librerías necesarias especificadas abajo.

INSTALACIÓN DE DEPENDENCIAS
---------------------------
Abre tu terminal o línea de comandos y ejecuta el siguiente comando para 
instalar las librerías requeridas:

pip install pygame PyOpenGL PyOpenGL_accelerate numpy

Siendo PyOpenGL_accelerate opcional, para un mejor rendimiento.
CONTROLES
---------
- W, A, S, D: Mover la cámara (Adelante, Izquierda, Atrás, Derecha).
- Flechas (Arr, Aba, Izq, Der): Rotar la vista de la cámara.
- ESC: Cerrar la aplicación.

