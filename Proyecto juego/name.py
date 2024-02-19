import pygame as pg
from models.botones.botones import Botones
from models.constantes import *
from stage_1 import *

def set_name(volumen):

    screen = pg.display.set_mode((ANCHO_VENTANA, LARGO_VENTANA))
    pg.init()
    pg.display.set_caption("Menu Principal")
    back_img = pg.image.load('models\\backgrounds\\fondo_nombre.jpg') 
    back_img = pg.transform.scale(back_img,(ANCHO_VENTANA, LARGO_VENTANA))
    img = pg.image.load('models\player\\fall\Fall.png') 
    img = pg.transform.scale(img,(130,130))
    font = pg.font.Font(None, 37)
    nombre = ""

    pg.mixer.music.load('music\\ambiente.wav')
    pg.mixer.music.set_volume(volumen)
    pg.mixer.music.play(-1)

    menu = True

    while menu:
        
        screen.blit(back_img, back_img.get_rect())
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                menu = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if len(nombre) > 2:
                        print("Nombre ingresado:", nombre)
                        stage_uno(volumen,nombre)
                        menu = False

                elif event.key == pg.K_BACKSPACE:
                    nombre = nombre[:-1] 
                elif len(nombre) < 6:
                    nombre += event.unicode 

        texto_nombre = font.render("" + nombre, True, NEGRO)
        texto = font.render("¿Cómo te gustaría ser llamado?", True, NEGRO)
        rectangulo_texto_2 = texto.get_rect(center=((ANCHO_VENTANA // 2), ((LARGO_VENTANA // 2) - 120)))
        rectangulo_texto = texto_nombre.get_rect(center=(ANCHO_VENTANA // 2, LARGO_VENTANA // 2))
        screen.blit(texto_nombre, rectangulo_texto)
        screen.blit(texto,rectangulo_texto_2)
        screen.blit(img, img.get_rect(center=(((ANCHO_VENTANA // 2)-5), ((LARGO_VENTANA // 2) + 60))))
        
        pg.display.update()

    pg.quit()