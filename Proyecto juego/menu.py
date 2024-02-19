import pygame as pg
from models.botones.botones import Botones
from models.constantes import *
from name import set_name


def menu():
    screen = pg.display.set_mode((ANCHO_VENTANA, LARGO_VENTANA))
    pg.init()
    pg.display.set_caption("Let's destroy Missigno")
    back_img = pg.image.load('models\\backgrounds\\fondo_menu.jpeg') 
    back_img =  pg.transform.scale(back_img,(ANCHO_VENTANA, LARGO_VENTANA))
    font = pg.font.Font(None, 37)

    menu = True

    pg.mixer.music.load('music\\ambiente.wav')
    pg.mixer.music.set_volume(0.5)
    pg.mixer.music.play(-1)

    boton_start = Botones((ANCHO_VENTANA * 0.1),(LARGO_VENTANA // 2),'models\\botones\Text_Play_Button.png',2)
    boton_exit = Botones((ANCHO_VENTANA * 0.65),(LARGO_VENTANA // 2),'models\\botones\Text_Exit_Button.png',2)
    boton_mute = Botones((ANCHO_VENTANA * 0.47),(((LARGO_VENTANA * 0.6) + 130)),'models\\botones\Sound_Off_Button.png',1.5)

    volumen = 0.3

    while menu:


        lista_eventos = pg.event.get()
        for event in lista_eventos:
            match event.type:
                case pg.QUIT:

                    print('Adios')
                    menu = False

        screen.blit(back_img, back_img.get_rect())  
        if boton_start.update():
            set_name(volumen)
            pg.mixer.music.stop()
            menu = False

        if boton_exit.update():
            menu = False

        if boton_mute.update():
            if volumen == 0.3:
                pg.mixer.music.stop()
                volumen = 0
            else:
                pg.mixer.music.play()
                volumen = 0.3

        
        text = font.render("Let's destroy Missigno!",True,BLANCO)
        rectangulo_texto = text.get_rect(center=(ANCHO_VENTANA // 2, ((LARGO_VENTANA // 2) - 170)))
        screen.blit(text,rectangulo_texto)
        boton_start.draw(screen)       
        boton_exit.draw(screen)        
        boton_mute.draw(screen)
        pg.display.update()

    pg.quit()

menu()