# On importe ici les modules nécessaire pour faire fonctionner le jeu
import pygame, sys
from pygame.locals import *
from random import randint
import math
import time

# On prépare ensuite tout ce qui sera utile afin de lancer le jeu comme la taille de la fenêtre,
# la carte sur laquelle on joue ...
pygame.display.set_caption("Monster Attack")
pygame.init()
pygame.key.set_repeat(50)

horloge = pygame.time.Clock()            

LARGEUR = 2400
HAUTEUR = 1300

fenetre = pygame.display.set_mode((LARGEUR,HAUTEUR))

carte = pygame.image.load('map.png').convert_alpha()
position_carte = carte.get_rect()
position_carte.topleft = (-1100, -1300)

# On créer d'abord la classe de notre personnage
class Player:
    def __init__(self, position_x, position_y):
        self.deplacement_gauche = False
        self.deplacement_droite = False
        self.deplacement_bas = False
        self.deplacement_haut = False
        
        # On initialise la position du joueur
        self.x = position_x
        self.y = position_y
        
        # On initialise d'autres variables telles que les points de vie
        # ou encore la position par rapport à la carte
        self.image = pygame.image.load('Sprites_NSI/player.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x,self.y]
        self.vie = 50
        self.max_vie = 50
        
        # On créer ensuite des listes qui contiendront unes à unes les sprites,
        # permettant de donner l'illusion d'un mouvement "fluide"
        self.sprites_haut = []
        self.sprites_haut.append(pygame.image.load('Sprites_NSI/up_0.png'))
        self.sprites_haut.append(pygame.image.load('Sprites_NSI/up_1.png'))
        self.sprites_haut.append(pygame.image.load('Sprites_NSI/up_2.png'))
        self.sprites_haut.append(pygame.image.load('Sprites_NSI/up_3.png'))
        self.sprites_bas = []
        self.sprites_bas.append(pygame.image.load('Sprites_NSI/down_0.png'))
        self.sprites_bas.append(pygame.image.load('Sprites_NSI/down_1.png'))
        self.sprites_bas.append(pygame.image.load('Sprites_NSI/down_2.png'))
        self.sprites_bas.append(pygame.image.load('Sprites_NSI/down_3.png'))
        self.sprites_droite = []
        self.sprites_droite.append(pygame.image.load('Sprites_NSI/right_0.png'))
        self.sprites_droite.append(pygame.image.load('Sprites_NSI/right_1.png'))
        self.sprites_droite.append(pygame.image.load('Sprites_NSI/right_2.png'))
        self.sprites_droite.append(pygame.image.load('Sprites_NSI/right_3.png'))
        self.sprites_gauche = []
        self.sprites_gauche.append(pygame.image.load('Sprites_NSI/left_0.png'))
        self.sprites_gauche.append(pygame.image.load('Sprites_NSI/left_1.png'))
        self.sprites_gauche.append(pygame.image.load('Sprites_NSI/left_2.png'))
        self.sprites_gauche.append(pygame.image.load('Sprites_NSI/left_3.png'))
        self.sprite_actuel = 0
        
       
    # On créer des méthodes afin d'autoriser ou d'interdire
    # le déplacement du joueur
    def mouvement_haut(self):
        self.deplacement_haut = True

        
    def mouvement_bas(self):
        self.deplacement_bas = True

        
    def mouvement_droite(self):
        self.deplacement_droite = True

        
    def mouvement_gauche(self):
        self.deplacement_gauche = True
    
    def draw(self):
        fenetre.blit(self.image, self.rect)
              
    # Cette méthode sert à afficher la barre de vie du joueur en temps réel
    # ainsi qu'à la modifier si nécessaire (changement de couleur, baisse de points de vie...)
    def barre_vie(self):
        couleur_barre_vie = (111, 210, 46)
        couleur_fond_barre = (0, 0, 0)
        if self.vie <= 25 and self.vie > 10:
            couleur_barre_vie = (252, 126, 0)
        elif self.vie <= 10:
            couleur_barre_vie = (255, 0, 0)
        
        # Ici on positionne la barre de vie au-dessus de la tête du joueur
        barre_position = [self.rect[0] + 10, self.rect[1] - 10, self.vie, 6]
        barre_position_fond = [self.rect[0] + 10, self.rect[1] - 10, self.max_vie, 6]
        
        pygame.draw.rect(fenetre, couleur_fond_barre, barre_position_fond)
        pygame.draw.rect(fenetre, couleur_barre_vie, barre_position)
        
        # Lorsque le joueur n'a plus de points de vie, c'est perdu ! Il faut réessayer
        if self.vie <= 0:
            defaite()
            time.sleep(2)
            sys.exit()
            pygame.quit()
    
    # Cette méthode sert à actualiser les enchainements de sprites lors des déplacements
    def update(self, vitesse):
        if self.deplacement_haut == True:
            self.sprite_actuel += vitesse
            if int(self.sprite_actuel) >= len(self.sprites_haut):
                self.sprite_actuel = 0
                self.deplacement_haut = False
            self.image = self.sprites_haut[int(self.sprite_actuel)]
            
        if self.deplacement_bas == True:
            self.sprite_actuel += vitesse
            if int(self.sprite_actuel) >= len(self.sprites_bas):
                self.sprite_actuel = 0
                self.deplacement_bas = False
            self.image = self.sprites_bas[int(self.sprite_actuel)]
            
            
        if self.deplacement_gauche == True:
            self.sprite_actuel += vitesse
            if int(self.sprite_actuel) >= len(self.sprites_gauche):
                self.sprite_actuel = 0
                self.deplacement_gauche = False
            self.image = self.sprites_gauche[int(self.sprite_actuel)]
            
            
        if self.deplacement_droite == True:
            self.sprite_actuel += vitesse
            if int(self.sprite_actuel) >= len(self.sprites_droite):
                self.sprite_actuel = 0
                self.deplacement_droite = False
            self.image = self.sprites_droite[int(self.sprite_actuel)]
            
            

# Ici il s'agit de la classe visant à créer les enemies que nous affronterons
class Monstre(pygame.sprite.Sprite):
    def __init__(self, sprite_1, sprite_2, sprite_3, sprite_4, vie, dommage, vitesse, barre):
        # super().__init__() est fait pour manipuler plus aisément les sprites (supprimer, ajouter ...)
        super().__init__()
        # On initalise les valeurs de bases telles que la taille, le lieu d'apparition (aléatoire dans une fenêtre donnée),
        # la vitesse, les points de vie mais aussi les dommages qu'ils pourront infliger au joueur
        self.image = pygame.image.load(sprite_1)
        self.rect = self.image.get_rect()
        self.taille = 10
        self.x = randint(10,1500)
        self.y = randint(10,900)
        self.rect.topleft = [self.x,self.y]
        self.vitesse = vitesse
        self.vie = vie
        self.max_vie = vie
        self.dommage = dommage
        self.barre = barre
        
        # On charge les 4 images (sprites) qui ferons le déplacement de nos enemies 
        self.deplacement = []
        self.deplacement.append(pygame.image.load(sprite_1))
        self.deplacement.append(pygame.image.load(sprite_2))
        self.deplacement.append(pygame.image.load(sprite_3))
        self.deplacement.append(pygame.image.load(sprite_4))
        self.sprite_actuelle = 0
        self.mouvement = False
           
    def mouvements(self):
        self.mouvement = True
    
    # On actualise afin de changer le sprite et donc de donner cette illusion de mouvement
    def update(self, vitesse):
        if self.mouvement == True:
            self.sprite_actuelle += vitesse
            if int(self.sprite_actuelle) >= len(self.deplacement):
                self.sprite_actuelle = 0
                self.mouvement = False
            self.image = self.deplacement[int(self.sprite_actuelle)]
    
    # Dans cette méthode, nous calculons la distance entre les monstres et le joueur
    def distance_joueur(self, cible_x, cible_y):
        distance_x = cible_x  - self.rect[0] 
        distance_y = cible_y  - self.rect[1] 
        distance = (distance_x**2 + distance_y**2)**0.5
        
        # Si le joueur est trop proche du monstre, alors il reçoit des dégâts
        if distance <= 40:
            player.vie -= self.dommage
        
        # Cette condition fait en sorte que si le monstre voit le joueur, alors celui-ci est
        # 'attiré', il se déplace vers le joueur
        if distance < 900:
            if self.rect[0] < player.rect[0]:
                self.rect[0] += self.vitesse
            if self.rect[0] > player.rect[0]:
                self.rect[0] -= self.vitesse
            if self.rect[1] < player.rect[1]:
                self.rect[1] += self.vitesse
            if self.rect[1] > player.rect[1]:
                self.rect[1] -= self.vitesse
                
    def barre_vie(self):
        couleur_barre_vie = (255, 0, 0)
        couleur_fond_barre = (0, 0, 0)
        
        # On place leur barre de vie au-dessus d'eux  
        barre_position = [self.rect[0] - self.barre, self.rect[1] - 10, self.vie, 6]
        barre_position_fond = [self.rect[0] - self.barre, self.rect[1] - 10, self.max_vie, 6]
        
        pygame.draw.rect(fenetre, couleur_fond_barre, barre_position_fond)
        pygame.draw.rect(fenetre, couleur_barre_vie, barre_position)
        
        # Lorsque l'enemie n'a plus de vie, il disparaît
        if self.vie <= 0:
            self.kill()
    
    # Cette méthode elle, calcule la distance entre le monstre et le projectile envoyé par le joueur
    def distance_balle(self, cible_x, cible_y):
        distance_x = cible_x - self.rect[0]
        distance_y = cible_y - self.rect[1]
        distance = (distance_x**2 + distance_y**2)**0.5
        
        # Si ils sont en contact, alors le monstres perd de la vie
        if distance <= 70:
            self.vie -= 0.8
            
            
# On créer une autre classe pour les projectiles que le joueur utilise pour se défendre           
class Playerbullet:
    def __init__(self, x, y, souris_x, souris_y):
        self.x = x
        self.y = y
        # On vise l'enemie avec la souris de bureau, et on calcule l'angle pour que le projectile
        # parte vers le lieux appuyer
        self.souris_x = souris_x
        self.souris_y = souris_y
        self.vitesse = 4
        self.angle = math.atan2(souris_y - self.y, souris_x - self.x)
        '''
        Keske vel ????????????????????????????????????????
        '''
        self.x_vel = math.cos(self.angle) * self.vitesse
        self.y_vel = math.sin(self.angle) * self.vitesse
        self.taille = 5
    
    # Cette méthode gère le déplacement linéaire du projectile
    def main(self, fenetre):
        self.x += self.x_vel
        self.y += self.y_vel
        pygame.draw.circle(fenetre, (0,0,0),(self.x, self.y), self.taille)
        
        # Si le projectile sors de la surface visible il est supprimé
        if self.x > LARGEUR or self.x < 0:
            self.taille = 0
        if self.y > HAUTEUR or self.y < 0:
            self.taille = 0
        
        

# La fonction défaite qui permet, d'afficher le 'Game Over' et le retour au menu
def defaite():
    police = pygame.font.SysFont('John Hubbard',120)
    image_texte = police.render("Game Over", 1, (255,0,50))
    fenetre.blit(image_texte,(700 ,500))
    pygame.display.flip()

# On créer notre personnage, une liste contenant les projectiles ainsi qu'un groupe de sprite qui
# contiendra tous nos enemies
player = Player(LARGEUR/2, HAUTEUR/2)
player_bullets = []
lst_monstres = pygame.sprite.Group()

# On place notre premier enemie à éliminer dans la liste pour le faire apparaître dans le jeu
lst_monstres.add(Monstre('Sprites_NSI/0.png', 'Sprites_NSI/1.png', 'Sprites_NSI/2.png', 'Sprites_NSI/3.png', 50, 0.5, 1, -10))

# On a ici un système de 'vague' c'est-à-dire que les monstres arriveront de plus en plus nombreux
def vague(nombre_enemie):
    for i in range(nombre_enemie):
        lst_monstres.add(Monstre('Sprites_NSI/0.png', 'Sprites_NSI/1.png', 'Sprites_NSI/2.png', 'Sprites_NSI/3.png', 50, 0.5, 1, -10))            

# C'est ici que le jeu va tourner en boucle, permettre tous les déplacements, les interactions ...
def main_jeux():
    # Queleques variables que l'on pourra modifier pour faire évoluer le jeu
    nombre_enemie = 2
    attente = 400
    dernier_tir = 0
    apparition = True
    apparition_2 = True
    
    while True:
        fenetre.fill('blue')
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Si le joueur s'aventure trop loin (dans les eaux profondes) alors il perdra des points de vie 
        if (player.rect.left - 250) < position_carte.left:
            player.vie -= 0.3
        if (player.rect.right + 450) > position_carte.right:
            player.vie -= 0.3  
        if (player.rect.top - 20) < position_carte.top:
            player.vie -= 0.3
        if (player.rect.bottom + 400) > position_carte.bottom:
            player.vie -= 0.3
            
        # Si tous les monstres sur la carte sont morts, alors de nouveaux apparaissent, plus nombreux
        if len(lst_monstres) == 0:
            vague(nombre_enemie)
            nombre_enemie += 1
        
        # Nous avons un système de 'Mini-Boss', ils apparaitront à partir d'un certain palier (un certains nombre de vagues survécues)
        if nombre_enemie == 11  and apparition == True:
            lst_monstres.add(Monstre('Sprites_NSI/00.png', 'Sprites_NSI/11.png', 'Sprites_NSI/22.png', 'Sprites_NSI/33.png', 150, 1, 2, -10))
            apparition = False
                
        if nombre_enemie == 21 and apparition_2 == True:
            lst_monstres.add(Monstre('Sprites_NSI/g1.png', 'Sprites_NSI/g2.png', 'Sprites_NSI/g3.png', 'Sprites_NSI/g4.png', 250, 1.5, 4, 70))
            apparition_2 = False
            
            

        # Cette partie gère les interractions clavier/souris, c'est-à-dire que le joueur et déplaçable et peut 'tirer'
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and pygame.time.get_ticks() - dernier_tir > attente:
                    player_bullets.append(Playerbullet(player.rect[0], player.rect[1] + 10, mouse_x, mouse_y))
                    dernier_tir = pygame.time.get_ticks()
                    
                    
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_d:
                    player.mouvement_droite()
                    position_carte[0] -= 25
                    for bullet in  player_bullets:
                        bullet.x -= 25
                    for esprit in lst_monstres:
                        esprit.rect[0] -= 25
                        
                if event.key == pygame.K_z:
                    position_carte[1] += 25
                    for bullet in  player_bullets:
                        bullet.y += 25
                    for esprit in lst_monstres:
                        esprit.rect[1] += 25
                    player.mouvement_haut()
                    
                if event.key == pygame.K_s:
                    for bullet in  player_bullets:
                        bullet.y -= 25
                    for esprit in lst_monstres:
                        esprit.rect[1] -= 25
                    position_carte[1] -= 25
                    player.mouvement_bas()
                    
                if event.key == pygame.K_q:
                    player.mouvement_gauche()
                    position_carte[0] += 25
                    for bullet in  player_bullets:
                        bullet.x += 25
                    for esprit in lst_monstres:
                        esprit.rect[0] += 25
            
            # Fermer le jeu proprement
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()

        # Ici on fait appraître les monstres et les projectiles, on fait ensuite appelle à leurs méthodes
        # pour qu'ils fonctionnent correctement
        fenetre.blit(carte, position_carte)
        lst_monstres.draw(fenetre)
        lst_monstres.update(0.25)
        
        for esprit in lst_monstres:
            esprit.mouvements()
            esprit.distance_joueur(player.rect[0], player.rect[1])
            esprit.barre_vie()
            
            for bullet in player_bullets:
                esprit.distance_balle(bullet.x, bullet.y)
           
        for bullet in player_bullets:
            bullet.main(fenetre)
          
        player.barre_vie()
        player.draw()
        player.update(0.25)
        
        # Pour gérer les FPS
        pygame.display.flip()
        horloge.tick(60)
                
                
main_jeux()
