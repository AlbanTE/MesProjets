# Projet Snake

import pygame
import random
import time

class Snake:
    def __init__(self, X_max, Y_max):
        self.x = 5
        self.y = 5
        self.x_max = X_max
        self.y_max = Y_max
        self.taille = 3
        self.dir = (0, 1)
        self.pos = [(5, 5), (4, 5), (3, 5)]
        self.etat = True
        
    def avancer(self):
        x, y = self.dir
        self.x += x
        self.y += y
        self.pos.insert(0, (self.x, self.y))
        if len(self.pos) > self.taille:
            self.pos.pop()
        
    def tourner(self, key):
        if key == pygame.K_UP:
            dir = (0, -1)
        elif key == pygame.K_DOWN:
            dir = (0, 1)
        elif key == pygame.K_LEFT:
            dir = (-1, 0)
        elif key == pygame.K_RIGHT:
            dir = (1, 0)
        else:
            return
            
        x = self.pos[0][0] - self.pos[1][0]
        y = self.pos[0][1] - self.pos[1][1]
        
        if dir[0] != (-1)*x or dir[1] != (-1)*y:
            self.dir = dir
        
    def check(self):
        x, y = self.x+self.dir[0], self.y+self.dir[1]
        if x >= self.x_max or x < 0 or y >= self.y_max or y < 0 or (x, y) in self.pos[:-1]:
            self.etat = False
        return self.etat
        
class Jeu:
    def __init__(self, Width, Height, Taille_case):
        self.width = Width
        self.height = Height
        self.taille_case = Taille_case
        self.cases = []
        self.nbc_lar = Width//Taille_case
        self.nbc_haut = Height//Taille_case
        self.snake = Snake(Width//Taille_case, Height//Taille_case)
        
        self.pomx = 0
        self.pomy = 0
        
        self.cases_init()
        self.creer_pomme()
        
    def cases_init(self):
        for i in range(self.width//self.taille_case):
            lst = []
            for j in range(self.height//self.taille_case):
                lst.append((i, j))
            self.cases.append(lst)
            
    def lancer(self, vitesse):
        en_cours = True
        while en_cours:
                
            #print(self.snake.x, self.snake.y)
            
            if self.snake.check():
                self.check_pomme()
                self.afficher()
                pygame.display.flip()
                self.snake.avancer()
                    
            else:
                self.afficher((255, 0, 0))
                pygame.display.flip()
                            
                            
            for event in pygame.event.get():
                if event.type==pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        en_cours = False
                    else:
                        self.snake.tourner(event.key)
                        
            if vitesse <= 1000:
                if not(self.attendre(0.1)):
                    en_cours = False
                        
    def afficher(self, color=(0, 255, 0)):
        for ligne in self.cases:
            for case in ligne:
                if case in self.snake.pos:
                    pygame.draw.rect(screen, color, (case[0]*self.taille_case, case[1]*self.taille_case, self.taille_case-1, self.taille_case-1))
                else:
                    pygame.draw.rect(screen, (20, 20, 20), (case[0]*self.taille_case, case[1]*self.taille_case, self.taille_case-1, self.taille_case-1))
                    if case == (self.pomx, self.pomy):
                        pygame.draw.circle(screen, (255, 0, 0), ((1/2+case[0])*self.taille_case, (1/2+case[1])*self.taille_case), self.taille_case*(1/3))
                    
    def creer_pomme(self):
        x, y = self.snake.x, self.snake.y
        while (x, y) in self.snake.pos:
            x = random.randint(0, self.nbc_lar-1) 
            y = random.randint(0, self.nbc_haut-1) 
        self.pomx = x
        self.pomy = y
        
    def check_pomme(self):
        if self.snake.x == self.pomx and self.snake.y == self.pomy:
            self.snake.taille += 1
            self.creer_pomme()
            
    def attendre(self, temps):
        boucle = True
        t1 = time.time()
        t2 = 0
        retour = True
        while boucle:
            if t2 - t1 > temps:
                boucle = False
            else:
                t2 = time.time()
            for event in pygame.event.get():
                if event.type==pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        boucle = False
                        retour = False
                    else:
                        self.snake.tourner(event.key)
        return retour
            

pygame.init()
pygame.font.init()

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

screen=pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Snake")
screen.set_alpha(None)

taille_case = 33

jeu = Jeu(width, height, taille_case)

jeu.lancer(10)
