import pygame as pg
from models.auxiliar import SurfaceManager as sf
from models.constantes import ANCHO_VENTANA
from random import choice

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction):
        super().__init__()
        self.direction = direction
        self.__bullet_uno = sf.get_surface_from_spritesheet('models\\bullet\\bullet_1.png', 1, 1)
        self.__bullet_dos = sf.get_surface_from_spritesheet('models\\bullet\\bullet_2.png', 1, 1)
        self.images = choice([self.__bullet_uno, self.__bullet_dos])
        self.image = self.images[0].copy()
        self.rect = self.image.get_rect(midtop=(pos_x, pos_y))
        self.speed = 10  

    def do_shoot(self, surfaces):
        if self.direction:
            self.rect.x += self.speed
            if self.rect.x >= ANCHO_VENTANA or self.check_collision(surfaces):
                self.kill()
        else:
            self.rect.x -= self.speed
            if self.rect.x <= 0 or self.check_collision(surfaces):
                self.kill()

    def check_collision(self, surfaces):
        return pg.sprite.spritecollideany(self, surfaces)

    def update(self, delta_ms, surfaces):
        self.do_shoot(surfaces)