# Projet Bricks

import pygame
import random
import time

class Jeu:
    def __init__(self, Width, Height):
        self.width = Width
        self.height = Height
        self.balle = Balle(self.width//2, self.height-200)
        self.nb_balles = 3
        self.plateforme = Plateforme(self.width, self.height)
        self.murs = []
        self.game_over = False
        self.victoire = False

        self.init_bricks()

    def init_bricks(self):
        for i in range(4):
            clr = pygame.Color(0, 0, 0)
            clr.hsva = (30*i, 90, 90, 100)
            for j in range(width//10):
                brick = Brique( (width%10)//2 + j*width//10, 50 + 60*i, 59, width//10 - 1, clr)
                self.murs.append(brick)

    def collision(self, brick):
        seuil = 5
        balle = self.balle.rect

        if (abs(brick.right - balle.left) <= seuil) and self.balle.vx > 0:
            self.balle.vx *= -1

        if (abs(brick.left - balle.right) <= seuil) and self.balle.vx < 0:
            self.balle.vx *= -1

        if (abs(brick.bottom - balle.top) <= seuil) and self.balle.vy < 0:
            self.balle.vy *= -1

        if (abs(brick.top - balle.bottom) <= seuil) and self.balle.vy > 0:
            self.balle.vy *= -1

    def rebords(self):
        balle = self.balle.rect

        if (abs(balle.right - self.width) <= 5 and self.balle.vx > 0) or (abs(balle.left) <= 5 and self.balle.vx < 0):
            self.balle.vx *= -1

        if abs(balle.top) <= 5 and self.balle.vy < 0:
            self.balle.vy *= -1

        if abs(balle.bottom - self.height) <= 5:
            self.nb_balles -= 1
            self.balle = Balle(self.width//2, self.height-200)
            self.plateforme = Plateforme(self.width, self.height)
            if self.nb_balles == 0:
                self.game_over = True

    def reborme(self):
        balle = self.balle.rect
        pltf = self.plateforme.rect
        milieu = pltf.midtop[0]
        pos = balle.midbottom[0] - pltf.left

        if pos <= 50 or pos > 200:
            facteur = 4
        elif 51 <= pos <= 100 or 150 <= pos <= 200:
            facteur = 3
        else:
            facteur = 2

        self.collision(pltf)
        if balle.midtop[0] < milieu and self.balle.vx > 0:
            self.balle.vx *= (-1)
        if balle.midtop[0] > milieu and self.balle.vx < 0:
            self.balle.vx *= (-1)

        self.balle.vx = facteur*(abs(self.balle.vx)/self.balle.vx)

    def lancer(self):
        en_cours = True
        while en_cours:
            clock.tick(120)
            pygame.display.update()
            pygame.draw.rect(screen, 0, (0, 0, self.width, self.height))

            if not(self.game_over):
                if not(self.victoire):

                    txtballe = font.render("Balles : "+str(self.nb_balles), True, "white")
                    screen.blit(txtballe, (10, 10))

                    self.plateforme.afficher()
                    self.plateforme.bouger()

                    if len(self.murs) != 0:
                        for brick in list(reversed(self.murs)):
                            brick.afficher()

                            if brick.hp > 0:
                                if brick.rect.colliderect(self.balle.rect):
                                    self.collision(brick.rect)
                                    brick.toucher()
                            else:
                                self.murs.pop(self.murs.index(brick))
                    else:
                        self.victoire = True

                    self.rebords()

                    if self.balle.rect.colliderect(self.plateforme.rect):
                        self.reborme()

                    self.balle.afficher()
                    if time.time() - self.balle.crea_time >= 0.5:
                        self.balle.bouger()
                else:
                    texte = font.render("Vous avez gagné !", True, "white")
                    screen.blit(texte, (self.width//2 - 150, self.height//2))

            else:
                texte = font.render("Game Over", True, "white")
                screen.blit(texte, (self.width//2 - 90, self.height//2))


            for event in pygame.event.get():
                if event.type==pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        en_cours = False


class Balle:
    def __init__(self, X, Y):
        self.x = X
        self.y = Y
        self.radius = 10
        self.vx = [-2, -1, 1, 2][random.randint(0, 3)]
        self.vy = -5
        self.crea_time = time.time()

        self.rect = pygame.Rect(self.x-self.radius, self.y-self.radius, 2*self.radius, 2*self.radius)


    def bouger(self):
        self.x += self.vx
        self.y += self.vy
        self.rect = pygame.Rect(self.x-self.radius, self.y-self.radius, 2*self.radius, 2*self.radius)

    def afficher(self):
        #pygame.draw.rect(screen, (255, 255, 255), self.rect)
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)


class Brique:
    def __init__(self, X, Y, Larg, Lon, Color):
        self.x = X
        self.y = Y
        self.larg = Larg
        self.lon = Lon
        self.hp = 2

        self.color = Color

        self.rect = pygame.Rect(self.x, self.y, self.lon, self.larg)

    def afficher(self):
        teinte = self.hp*(1/2)
        couleur = (self.color[0]*teinte, self.color[1]*teinte, self.color[2]*teinte)
        pygame.draw.rect(screen, couleur, self.rect)

    def toucher(self):
        if self.hp > 0:
            self.hp -= 1

class Plateforme:
    def __init__(self, Width, Height):
        self.width = Width
        self.height = Height
        self.x = self.width//2
        self.y = self.height - 50
        self.taille = 250

        self.rect = pygame.Rect(self.x - self.taille//2, self.y-10, self.taille, 10)

    def afficher(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

    def bouger(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.x - self.taille//2 > 1:
                self.x -= 4
                self.rect = pygame.Rect(self.x - self.taille//2, self.y-10, self.taille, 10)
        elif keys[pygame.K_RIGHT]:
            if self.x + self.taille//2 < self.width:
                self.x += 4
                self.rect = pygame.Rect(self.x - self.taille//2, self.y-10, self.taille, 10)
        else:
            return

pygame.init()
pygame.font.init()

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

screen=pygame.display.set_mode((width, height), pygame.FULLSCREEN)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
pygame.display.set_caption("Bricks")
#screen.set_alpha(None)

jeu = Jeu(width, height)

jeu.lancer()
