import pygame
import random
# import ctypes
# import os

class Jeu:
    def __init__(self, Width, Height, Taille_case, Images, Img_fourmi):
        self.x = 100
        self.y = 0
        self.width = Width
        self.height = Height
        self.x2 = Width-100
        self.y2 = Height
        self.taille_case = Taille_case
        self.images = Images
        self.img_fourmi = Img_fourmi
        self.grille = None
        self.fourmi = None

    def lancer(self, vitesse):
        self.grille = Grille(self.x, self.y, self.x2-self.x, self.y2-self.y, self.taille_case, self.images)
        x_moy = 0
        y_moy = 0
        for cel in self.grille.liste_cel:
            x_moy += cel.x
            y_moy += cel.y
        x_moy = x_moy/len(self.grille.liste_cel)
        y_moy = y_moy//len(self.grille.liste_cel)
        if (self.grille.width//self.taille_case)%2 == 0:

            x_moy = x_moy-self.taille_case/2
        if (self.grille.height//self.taille_case)%2 == 0:
            y_moy = y_moy-self.taille_case/2
        self.fourmi = Fourmi(int(x_moy), int(y_moy), self.taille_case, self.img_fourmi)

        myFont = pygame.font.SysFont("Times New Roman", 20)

        en_cours = True
        phase1 = True
        phase2 = False
        ctr = 0
        self.afficher()
        while en_cours:
            compteur = myFont.render(str(ctr), False, (255,255,255))
            pygame.draw.rect(screen, 0, (0, 0, 100, 20))
            screen.blit(compteur, (15,0))
            pygame.display.flip()

            if phase1:
                for event in pygame.event.get():
                    if event.type==pygame.KEYUP:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            en_cours = False
                        elif event.key == pygame.K_RETURN:
                            phase1 = False
                            phase2 = True
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        for cel in jeu.grille.liste_cel:
                            if cel.hitbox.collidepoint(event.pos):
                                cel.change_etat()
                                if (cel.x, cel.y) == (self.fourmi.x, self.fourmi.y):
                                    self.fourmi.afficher()
            if phase2:
                for event in pygame.event.get():
                    if event.type==pygame.KEYUP:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            phase2 = False
                            en_cours = False
                if self.fourmi.x >= self.x and self.fourmi.x <= self.x2 and self.fourmi.y >= self.y and self.fourmi.y <= self.y2 and en_cours:
                    for cel in self.grille.liste_cel:
                        if cel.hitbox.collidepoint((self.fourmi.x, self.fourmi.y)):
                            if cel.etat:
                                self.fourmi.case_blanche(cel)
                            else:
                                self.fourmi.case_noire(cel)

                            ctr += 1
                            if vitesse <= 1000:
                                pygame.time.wait(int(1000/vitesse))

    def afficher(self):
        screen.fill(0)
        self.grille.afficher()
        self.fourmi.afficher()


class Grille:
    def __init__(self, X, Y, Width, Height, Taille_case, Images):
        self.x = X
        self.y = Y
        self.width = Width
        self.height = Height
        self.taille_case = Taille_case
        self.images = Images
        self.liste_cel = []

        self.creer_cellules()

    def creer_cellules(self):
        for i in range(self.width//self.taille_case):
            for j in range(self.height//self.taille_case):
                self.liste_cel.append(Cellule( self.x+i*self.taille_case, self.y+j*self.taille_case, 0, self.taille_case, self.images))

    def afficher(self):
        for cel in self.liste_cel:
            cel.afficher()

class Cellule:
    def __init__(self, X, Y, Etat, taille_case, Images):
        self.x = X
        self.y = Y
        self.etat = Etat
        self.taille = taille_case
        self.images = Images
        self.hitbox = pygame.Rect(self.x, self.y, self.taille, self.taille)

    def afficher(self):
        screen.blit(self.images[self.etat], (self.x, self.y))

    def change_etat(self):
        self.etat = not(self.etat)
        self.afficher()

class Fourmi:
    def __init__(self, X, Y, Taille_case, Img):
        self.x = X
        self.y = Y
        self.taille_case = Taille_case
        self.directions = [(0, -1), (1, 0), (0, 1), (-1, 0)] # = ["N", "E", "S", "W"]
        self.orientation = (0, -1)
        self.img = Img

    def case_blanche(self, case):
        self.orientation = self.directions[(self.directions.index(self.orientation)+1)%4]
        case.afficher()
        case.change_etat()
        self.avancer()
        self.afficher()



    def case_noire(self, case):
        self.orientation = self.directions[(self.directions.index(self.orientation)-1)%4]
        case.afficher()
        case.change_etat()
        self.avancer()
        self.afficher()


    def avancer(self):
        self.x = self.x + self.orientation[0]*self.taille_case
        self.y = self.y + self.orientation[1]*self.taille_case

    def afficher(self):
        img2 = pygame.transform.rotate(self.img, 90*self.directions.index(self.orientation))
        screen.blit(img2, (self.x, self.y))

pygame.init()
pygame.font.init()

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

screen=pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("La Fourmi de Langton")
screen.set_alpha(None)

taille_case = 15

img_cel_viv = pygame.image.load("case_vivante.png")
img_cel_viv = pygame.transform.scale(img_cel_viv, (taille_case, taille_case))

img_cel_mort = pygame.image.load("case_morte.png")
img_cel_mort = pygame.transform.scale(img_cel_mort, (taille_case, taille_case))

img_fourmi = pygame.image.load("fourmi_pixelart.png")
img_fourmi = pygame.transform.scale(img_fourmi, (taille_case, taille_case))

jeu = Jeu(width, height, taille_case, [img_cel_mort, img_cel_viv], img_fourmi)

jeu.lancer(1000)