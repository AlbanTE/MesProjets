import pygame
import random


class Jeu:
    def __init__(self, Width, Height, Taille_case, Images, Img_fourmi, Activer_Fourmi):
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
        self.activer_fourmi = Activer_Fourmi

    def lancer(self, vitesse):
        self.grille = Grille(self.x, self.y, self.x2-self.x, self.y2-self.y, self.taille_case, self.images)

        if self.activer_fourmi:
            x_moy = self.grille.liste_cel[len(self.grille.liste_cel)//2][len(self.grille.liste_cel[0])//2].x
            y_moy = self.grille.liste_cel[len(self.grille.liste_cel)//2][len(self.grille.liste_cel[0])//2].y
            self.fourmi = Fourmi(x_moy, y_moy, self.taille_case, self.img_fourmi)

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
                        for ligne in self.grille.liste_cel:
                            for cel in ligne:
                                if cel.hitbox.collidepoint(event.pos):
                                    cel.change_etat()
                                    if self.activer_fourmi:
                                        if (cel.x, cel.y) == (self.fourmi.x, self.fourmi.y):
                                            self.fourmi.afficher()

            if phase2:
                for ligne in self.grille.liste_cel:
                    for cel in ligne:
                        self.grille.nb_voisines(cel)
                for ligne in self.grille.liste_cel:
                    for cel in ligne:
                        if cel.etat == 0 and cel.nb_v_vivants == 3:
                            cel.change_etat()
                        elif cel.etat == 1 and not(cel.nb_v_vivants == 2 or cel.nb_v_vivants == 3):
                            cel.change_etat()
                        else:
                            cel.etat == 0
                if self.activer_fourmi and self.fourmi.x >= self.x and self.fourmi.x <= self.x2 and self.fourmi.y >= self.y and self.fourmi.y <= self.y2:
                    for ligne in self.grille.liste_cel:
                        for cel in ligne:
                            if cel.hitbox.collidepoint((self.fourmi.x, self.fourmi.y)):
                                if cel.etat:
                                    self.fourmi.case_blanche(cel)
                                else:
                                    self.fourmi.case_noire(cel)
                for event in pygame.event.get():
                    if event.type==pygame.KEYUP:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            phase2 = False
                            en_cours = False
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        for ligne in self.grille.liste_cel:
                            for cel in ligne:
                                if cel.hitbox.collidepoint(event.pos):
                                    cel.change_etat()
                                    if self.activer_fourmi:
                                        if (cel.x, cel.y) == (self.fourmi.x, self.fourmi.y):
                                            self.fourmi.afficher()
                ctr += 1
                if vitesse <= 1000:
                    pygame.time.wait(int(1000/vitesse))

    def afficher(self):
        screen.fill(0)
        self.grille.afficher()
        if self.activer_fourmi:
            self.fourmi.afficher()


class Grille:
    def __init__(self, X, Y, Width, Height, Taille_case, Images):
        self.x = X
        self.y = Y
        self.width = Width
        self.height = Height
        self.taille_case = Taille_case
        self.longeur = self.width//self.taille_case
        self.largeur = self.height//self.taille_case
        self.images = Images
        self.liste_cel = []

        self.creer_cellules()

    def creer_cellules(self):
        for i in range(self.width//self.taille_case):
            lst = []
            for j in range(self.height//self.taille_case):
                lst.append(Cellule( self.x+i*self.taille_case, self.y+j*self.taille_case, 0, self.taille_case, self.images))
            self.liste_cel.append(lst)

    def afficher(self):
        for ligne in self.liste_cel:
            for cel in ligne:
                cel.afficher()

    def voisines(self, case):
        x = (case.x-self.x) // self.taille_case
        y = (case.y-self.y) // self.taille_case
        autour = []
        i1, i2 = x-1, x+1
        j1, j2 = y-1, y+1
        if i1 < 0:
            i1 += 1
        if j1 < 0:
            j1 += 1
        if i2 > self.longeur-1:
            i2 -= 1
        if j2 > self.largeur-1:
            j2 -= 1
        for i_i in range(i1, i2+1):
            for j_j in range(j1, j2+1):
                autour.append(self.liste_cel[i_i][j_j])
        autour.remove(case)
        return autour

    def nb_voisines(self, case):
        nb = 0
        for voisine in self.voisines(case):
            if voisine.etat == 1:
                nb += 1
        case.nb_v_vivants = nb

class Cellule:
    def __init__(self, X, Y, Etat, taille_case, Images):
        self.x = X
        self.y = Y
        self.etat = Etat
        self.nb_v_vivants = 0
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

taille_case = 20

img_cel_viv = pygame.image.load("case_vivante.png")
img_cel_viv = pygame.transform.scale(img_cel_viv, (taille_case, taille_case))

img_cel_mort = pygame.image.load("case_morte.png")
img_cel_mort = pygame.transform.scale(img_cel_mort, (taille_case, taille_case))

img_fourmi = pygame.image.load("fourmi_pixelart.png")
img_fourmi = pygame.transform.scale(img_fourmi, (taille_case, taille_case))

jeu = Jeu(width, height, taille_case, [img_cel_mort, img_cel_viv], img_fourmi, True)

jeu.lancer(20)