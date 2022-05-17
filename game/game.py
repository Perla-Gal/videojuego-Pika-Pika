import pygame #Primero importamos pygame
import sys
import random 
import os

from .config import *
from .platform import Platform
from .player import Player
from .wall import Wall    #importamos la clase
from .coin import Coin   


class Game:  #Realizamos la clase Game con sus respectivos metodos 
    def __init__(self):
        pygame.init()  
        
        self.surface = pygame.display.set_mode( (WIDTH,HEIGHT) ) #generamos la panatalla
        pygame.display.set_caption(TITLE)

        
        self.running = True #Sirve ver si se ejecuta 
        

        self.clock = pygame.time.Clock()
        self.font = pygame.font.match_font(FONT)

        self.dir = os.path.dirname(__file__)
        self.dir_sounds = os.path.join(self.dir, "sources/sonidos")
        self.dir_imgs = os.path.join(self.dir, "sources/imagenes")
        self.play_music()
		
                       
   
    def start(self): #sirve para INICIAR ejecutar el videojuego
        self.menu()
       
        self.new()


    def new(self): #empezar un nuevo juego nueva partida 
        self.score = 0
        self.level = 0
        self.playing = True
        self.background = pygame.image.load(os.path.join(self.dir_imgs, "FONDO.png"))
        self.background = pygame.transform.scale(self.background, (900, 500))
        self.generate_elements()
        self.run()

    def play_music(self):
        pygame.mixer.music.load(os.path.join(self.dir_sounds, "final-fantasy.mp3"))  #sirve para cargar musica desde su ruta 
        pygame.mixer.music.set_volume(0.3) # Volumen de la musica 0.0 min 1.0 max
        pygame.mixer.music.play(-1, 0.0)
        

    def generate_elements(self):  #Sirve para generar Los elementos, aquí iran todos (personaje, plataforma, paredes, monedas, etc)
        self.platform = Platform()      #Generamos la plataforma 
        self.player = Player(100, self.platform.rect.top - 200, self.dir_imgs )
        
        self.sprites = pygame.sprite.Group() #Un grupo de sprite para agrupar sprites (personaje, plataforma, paredes, monedas, etc)
        self.walls = pygame.sprite.Group() #Un grupo de obstaculos para agrupar
        self.coins = pygame.sprite.Group()
        
        self.sprites.add(self.platform)
        self.sprites.add(self.player)

        self.generate_walls() 
       

    def generate_walls(self):  #Sirve para generar Los obstaculos
        last_position = WIDTH + 100 #Posicion entre un obstáculo y otro
        if not len(self.walls) > 0:
            for w in range(0, MAX_WALLS): #numeros de obstaculos 
                left = random.randrange(last_position + 200, last_position + 400)  #generar obstaculos en posiciones aleatorias 
                wall = Wall(left, self.platform.rect.top)
                last_position= wall.rect.right

                self.sprites.add(wall)
                self.walls.add(wall)

            self.level += 1
            self.generate_coins()

    def generate_coins(self):
        last_position = WIDTH + 100 #Posicion entre un obstáculo y otro
        
        for c in range(0, MAX_COINS): #numeros de monedas 
            pos_x = random.randrange(last_position + 180, last_position + 300)  
            coin = Coin(pos_x, 250, self.dir_imgs)
            last_position = coin.rect.right

            self.sprites.add(coin)
            self.coins.add(coin)



    def run(self): #ejecuta el juego 
        while self.running:
            self.clock.tick(FPS)
            self.events()            
            self.update()
            self.draw()
            

    def events(self): #sirve para diferentes eventos que puedan crear
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.player.jump()   
        if key[pygame.K_r] and not self.playing:
            self.new()   
            

                      
        
        

    def draw(self): #pintar los elementos del videojuego 
        self.surface.blit(self.background, (0, 0))  #color de la superficie
        self.draw_text()
        self.sprites.draw(self.surface)
        pygame.display.flip()  #en vez de utilzar .update se cambia para por .flip para mas rapido 
            

    def update(self): #encargada de actualizar la pantalla
        if not self.playing: 
            return
           
        wall = self.player.collide_with(self.walls)
        if wall:
            if self.player.collide_bottom(wall):
                self.player.skid(wall)
            else:
                self.stop()
        
        coin = self.player.collide_with(self.coins)
        if coin:
            self.score += 1
            coin.kill()

            sound = pygame.mixer.Sound(os.path.join(self.dir_sounds, "coin.wav"))              
            sound.play()
            
        self.sprites.update()

        self.player.validate_platform(self.platform) #Mandamos ejecutar con argumento la plataforma 
        self.update_elements(self.walls)
        self.update_elements(self.coins)
        self.generate_walls()



    def update_elements(self, elements):
        for element in elements:
           if not element.rect.right > 0:
               element.kill()


                      
    def stop(self): #Detendra el videojuego 
        sound = pygame.mixer.Sound(os.path.join(self.dir_sounds, "plop.wav"))              
        sound.play()

        self.player.stop()
        self.stop_elements(self.walls) #Detener los elemnetos en caso de colisión como elemntos los obstaculos
        self.playing = False 

    def stop_elements(self, elements): #Detener los elementos en caso de colisionar 
        for element in elements:
            element.stop()

    def score_format(self):
        return "Score : {}".format(self.score)
    

    def level_format(self):
        return "Level : {}".format(self.level)
    
    def draw_text(self):
        self.display_text(self.score_format(), 36, WHITE, WIDTH//2, 30)
        self.display_text(self.level_format(), 36, WHITE, 60, 30)

        if not self.playing: 
            self.display_text("Perdiste", 60, WHITE, WIDTH // 2, (HEIGHT// 2) - 80)
            self.display_text("Presiona r para comenzar", 38, WHITE, WIDTH // 2, (HEIGHT// 2) + 80)
      
          
    def display_text(self, text, size, color, pos_x, pos_y): #Permite pintar todo texto 
        font = pygame.font.Font(self.font, size,)

        text = font.render(text, True, color)
        rect = text.get_rect()
        rect.midtop = (pos_x, pos_y)

        self.surface.blit(text, rect)

    def menu(self):
        self.background_menu = pygame.image.load(os.path.join(self.dir_imgs, "pokemon-MENU.png"))
        self.background_menu = pygame.transform.scale(self.background_menu, (900, 500))
        self.surface.blit(self.background_menu, (0,0))

        self.display_text("Presiona una tecla para comenzar", 36, BLACK, WIDTH // 2, 10)


        pygame.display.flip()
        self.wait()

    def wait(self):
        wait = True

        while wait:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
                    self.running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYUP:
                    wait = False