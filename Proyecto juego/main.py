import pygame as pg
import random
from models.constantes import *
from defs_auxiliares import *
from models.player.player import Player
from models.bullet.Bullet import Bullet
from models.enemy.enemy import Enemy
from models.fruit.fruta import Fruta
from models.plataformas.piso import plataforma
from models.trampas.trampas import Trampas



screen = pg.display.set_mode((ANCHO_VENTANA, LARGO_VENTANA))
pg.init()
pg.display.set_caption("Let's destroy Missigno")
back_img = pg.image.load('models\\backgrounds\\fondo.jpeg') 
back_img =  pg.transform.scale(back_img,(ANCHO_VENTANA, LARGO_VENTANA))
shoots_flag = True
clock = pg.time.Clock()
font = pg.font.Font(None, 37)
game = True
puntos = 0

sapardo = Player(50, 525, frame_rate=120, speed_walk=20, speed_run=30)
missigno = Enemy(200, 75, frame_rate=120, speed_walk=20)

surfaces = pg.sprite.Group()
enemy_group = pg.sprite.Group()
enemy_group.add(missigno)
sound_bullet = pg.mixer.Sound('music\sonido disparo.mp3')

##############################################################################
piso = plataforma(0, LARGO_VENTANA - 70, ANCHO_VENTANA, LARGO_VENTANA)
plataform_1 = plataforma(0, 455, 75, 75)
plataform_2 = plataforma(200, 255, 400, 50)
plataform_3 = plataforma(75, 455, 75, 75)
plataform_4 = plataforma(525,455,75,75)
plataform_5 = plataforma(525,380,75,75)
plataform_6 = plataforma(525,305,75,75)
plataformas = [
    piso, plataform_1, plataform_2, 
    plataform_3,plataform_4,plataform_5,
    plataform_6
    ]
###############################################################################
frutas = pg.sprite.Group()
fruta = Fruta(590, 450, 50,50)
frutas.add(fruta)
################################################################################
trampas = pg.sprite.Group()
trampa_uno = Trampas(0,425,30,30)
trampa_dos = Trampas(30,425,30,30)
trampas.add(trampa_uno,trampa_dos)

######################
cooler_disparo = 0
cooler_enemigo = 0
cooler_colision = 0
cooler_muerte_enemigo = 0
cooler_mov_enem = 50
contador_toques = 0
contador_enemigos = 1
######################

##############################
enemigo_vivo = True
personaje_vivo = True
vida_inicial = 100
vida = 100
enemigo_puede_disparar = False
##############################

#############################
clock = pg.time.Clock()
tiempo_transcurrido = 0
points = 0
font = pg.font.Font(None, 37)
texto_uno = 'Game over'
texto_dos = 'Ganaste!!'
##############################

pg.mixer.init()


##############################

while game:


    lista_eventos = pg.event.get()
    lista_teclas_presionadas = pg.key.get_pressed()
    for event in lista_eventos:
        match event.type:
            case pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    sapardo.jump()
            case pg.QUIT:
                print('Adios')
                game = False
                
    if lista_teclas_presionadas[pg.K_RIGHT] and not lista_teclas_presionadas[pg.K_LEFT]:
        sapardo.walk('Right')
    if lista_teclas_presionadas[pg.K_LEFT] and not lista_teclas_presionadas[pg.K_RIGHT]:
        sapardo.walk('Left')
    if lista_teclas_presionadas[pg.K_RIGHT] and lista_teclas_presionadas[pg.K_LSHIFT] and not lista_teclas_presionadas[pg.K_LEFT]:
        sapardo.run('Right')
    if lista_teclas_presionadas[pg.K_LEFT] and lista_teclas_presionadas[pg.K_LSHIFT] and not lista_teclas_presionadas[pg.K_RIGHT]:
        sapardo.run('Left')
    if not lista_teclas_presionadas[pg.K_RIGHT] and not lista_teclas_presionadas[pg.K_LEFT]:
        sapardo.stay()
    if lista_teclas_presionadas[pg.K_q] and cooler_disparo == 0 and personaje_vivo:
        sapardo.shoot()
        sound_bullet.play()  
        cooler_disparo += 45

    if cooler_disparo > 0:
        cooler_disparo -= 1
    if cooler_enemigo > 0:
        cooler_enemigo -= 1
    if cooler_muerte_enemigo > 0:
        cooler_muerte_enemigo -= 1

    delta_ms = clock.tick(FPS)
    
    ############################################
    for plataforma in plataformas:
            plataforma.draw(screen)
    
    #############################################
    if cooler_muerte_enemigo == 0:
        for bullet in sapardo.bullet_group:
            hit_enemies = pg.sprite.spritecollide(bullet, enemy_group, True)
            for enemy in hit_enemies:
                enemy.hit_by_bullet()
                missigno.kill()
                enemigo_vivo = False
                cooler_muerte_enemigo = +40
                print('murio')
    ##############################################

    if not enemigo_vivo and contador_enemigos <= 4 :
        missigno = Enemy(200, 0, frame_rate=120, speed_walk=20)
        enemigo_vivo = True  
        contador_enemigos += 1
        enemy_group.add(missigno)
        points += 1000
    if contador_enemigos == 5:
        enemy.hit_by_bullet()
        missigno.kill()
        enemigo_vivo = False
    ##############################################
    
    if pg.sprite.spritecollideany(sapardo, enemy_group) or pg.sprite.spritecollideany(sapardo, trampas):
        if personaje_vivo and cooler_colision == 0:
            contador_toques += 1
            sapardo.hitted()
            cooler_colision += 90
            print('TE TOCO')
            if contador_toques == 4:
                sapardo.kill()
                personaje_vivo = False

            if cooler_colision > 0:
                cooler_colision -= 1

            if contador_toques >= 1 or contador_toques == 0:
                toques = 25 
                sapardo.decrease_life(toques)
                if sapardo.get_vida() > 25 and sapardo.get_vida() < 100:
                    color_vida = amarillo
                elif sapardo.get_vida() == 25 or sapardo.get_vida() == 0:
                    color_vida = rojo
                else:
                    color_vida = verde 
    if pg.sprite.spritecollideany(sapardo, frutas):
        sapardo.gain_vida(100)
        points += 500  # Increment points when collecting frutas
        print("Vida después de ganar:", sapardo.get_vida())
        print("Puntos después de ganar:", points)
    vida = sapardo.get_vida()
    texto_vida = font.render(f'Vida: {vida}',True,color_vida)



    if cooler_colision > 0:
        cooler_colision -= 1
    if cooler_mov_enem >= 1:
        cooler_mov_enem -= 1

    ###############################################

    if personaje_vivo and enemigo_vivo:
        tiempo_segundos = tiempo_transcurrido // 1000
        minutos = tiempo_segundos // 60
        segundos = tiempo_segundos % 60
        
        if segundos < 30 and minutos < 1:
            color = verde
        elif segundos >= 30:
            color = amarillo
            enemigo_puede_disparar = True
        elif minutos >= 1:
            color = rojo 
        elif minutos >= 2:
            color = rojo 
            personaje_vivo = False

    #############################################################

    if enemigo_puede_disparar and enemigo_vivo:
        if random.randint(1,233)%2 == 0 and cooler_enemigo == 0:
            sound_bullet.play()  
            cooler_enemigo += 120
            missigno.shoot()
        
    
    #############################################################

    tiempo_texto = font.render(f'{minutos:02}:{segundos:02}', True, color)
    puntos = font.render(f'{points}', True, (255,155,0))
    texto_perdiste = font.render(f'{texto_uno}',True,(rojo))
    texto_ganaste = font.render(f'{texto_dos}',True,(verde))
    #############################################################
    
    if personaje_vivo:
        sapardo.draw(screen)
        sapardo.update(delta_ms, plataformas)
        sapardo.handle_ground_collision(plataformas)
        sapardo.handle_collisions(plataformas)
        sapardo.bullet_group.update(delta_ms, surfaces)
        sapardo.bullet_group.draw(screen)
        frutas.update(sapardo)
        fruta.animate()
        frutas.draw(screen)  
    elif not personaje_vivo:
        screen.blit(texto_perdiste,(((ANCHO_VENTANA/2)-80),(LARGO_VENTANA/2)))
        
        
    if points == 4000:
        screen.blit(texto_ganaste,(((ANCHO_VENTANA/2)-80),(LARGO_VENTANA/2)))
        
    #############################################################
    if enemigo_vivo:
        missigno.draw(screen)
        if personaje_vivo and cooler_mov_enem == 0:
            missigno.handle_collisions(plataformas)                           
            missigno.handle_ground_collision(plataformas)
            missigno.bullet_group.update(delta_ms, surfaces)
            missigno.bullet_group.draw(screen)
            enemy_group.update(delta_ms,plataformas)
            missigno.update(delta_ms, plataformas)
    trampas.update(sapardo)
    trampas.draw(screen)
    #############################################################
    
    
    pg.display.update()

    
    
    screen.blit(back_img, back_img.get_rect())
    screen.blit(tiempo_texto, (((ANCHO_VENTANA/2)-30) ,5))
    screen.blit(puntos, (5,5))
    screen.blit(texto_vida,(675,5))
    tiempo_transcurrido += delta_ms
pg.quit()