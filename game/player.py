from ast import Global
import pygame
import os

from .config import *

#Crear JUGADOR con clase Player 
class Player (pygame.sprite.Sprite):  #Definir la Clase Player
    
    def __init__(self, left, bottom, dir_images):  
        
        pygame.sprite.Sprite.__init__(self)
        #ATRIBUTOS DE LA CLASE
        self.image = pygame.image.load(os.path.join(dir_images, "pikaaaa.png"))
        self.image = pygame.transform.scale(self.image, (80, 80))

        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.bottom = bottom

        self.pos_y = self.rect.bottom  #velocidad en Y atributos de update_pos
        self.vel_y = 0   #Posicion en Y
        self.can_jump = False
        self.playing = True 
        
    def collide_with(self, sprites):  
        objects = pygame.sprite.spritecollide(self, sprites, False)
        if objects:
            return objects[0]
    def collide_bottom(self, wall):
        return self.rect.colliderect(wall.rect_top)

    def skid(self, wall):
        self.pos_y = wall.rect.top
        self.vel_y = 0
        self.can_jump = True  

    def validate_platform(self, platform):
        result = pygame.sprite.collide_rect(self, platform)
        if result:
            self.vel_y = 0
            self.pos_y = platform.rect.top 
            self.can_jump = True
        


    def jump(self):   #Metodo para saltar 
        if self.can_jump:
            self.vel_y = -23  
            self.can_jump = False



    def update_pos(self):  #Metodo de Aceleración 
         self.vel_y += PLAYER_GRAV    #Velocidad en y (gravedad) 
         self.pos_y += self.vel_y + 0.5 * PLAYER_GRAV
         

    def update(self): #Actualización 
        if self.playing:  # se hara solo sí es verdadero 
            self.update_pos()
            self.rect.bottom = self.pos_y

    def stop(self):
        self.playing = False


        

