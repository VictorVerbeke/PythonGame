#-*- coding: utf-8 -*-

import os
import pygame as pg
from pygame.locals import *
import random
import time
import generation_laby

####### Initialisation PyGame #######
SCREEN_SIZE = (640,640)
SIZE = 640
os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()


#Ouverture de la fenêtre Pygame
screen = pg.display.set_mode((860,640))
pg.display.set_caption("Labyrinthe")
background = pg.image.load("sprites/background.png")
background = pg.transform.scale(background, SCREEN_SIZE)
screen.blit(background,(0,0))

pg.display.flip()
pg.key.set_repeat(1,16) #Pour que tous les déplacements soient fluides (pas de nécessité de réappuyer sur les touches dans le jeu)

# Chargement des musiques et des sons

pg.mixer.music.set_volume(1)				# On met de base le son à 50%
volume = 5									# On définit une variable qui permettra d'effectuer les variations de volume.

pg.mixer.music.load("sounds/track1.ogg") 			# Charge une musique
pg.mixer.music.queue("sounds/track2.ogg")			# Charge une autre musique et la met en file d'attente.
pg.mixer.music.queue("sounds/track3.ogg")
pg.mixer.music.queue("sounds/track4.ogg")
pg.mixer.music.play() 								# Joue les musiques chargées

son_item = pg.mixer.Sound("sounds/itemget.ogg")	# Charge un son jouable plus tard
son_menu_open = pg.mixer.Sound("sounds/menu_open.wav")
son_menu_close = pg.mixer.Sound("sounds/menu_close.wav")
son_menu_hover = pg.mixer.Sound("sounds/menu_hover.wav")

# Chargement de tous les sprites de personnage : on utilise quatre images par direction 
# lors des déplacements et une par direction pour le personnage immobile.

down_0 = pg.transform.scale(pg.image.load("sprites/down_0.png").convert_alpha(),(64,64)) # Load, puis scale sur la taille d'une case
down_1 = pg.transform.scale(pg.image.load("sprites/down_1.png").convert_alpha(),(64,64))
down_2 = pg.transform.scale(pg.image.load("sprites/down_2.png").convert_alpha(),(64,64))
down_3 = pg.transform.scale(pg.image.load("sprites/down_3.png").convert_alpha(),(64,64))
stand_down = pg.transform.scale(pg.image.load("sprites/stand_down.png").convert_alpha(),(64,64))

up_0 = pg.transform.scale(pg.image.load("sprites/up_0.png").convert_alpha(),(64,64))
up_1 = pg.transform.scale(pg.image.load("sprites/up_1.png").convert_alpha(),(64,64))
up_2 = pg.transform.scale(pg.image.load("sprites/up_2.png").convert_alpha(),(64,64))
up_3 = pg.transform.scale(pg.image.load("sprites/up_3.png").convert_alpha(),(64,64))
stand_up = pg.transform.scale(pg.image.load("sprites/stand_up.png").convert_alpha(),(64,64))

left_0 = pg.transform.scale(pg.image.load("sprites/left_0.png").convert_alpha(),(64,64))
left_1 = pg.transform.scale(pg.image.load("sprites/left_1.png").convert_alpha(),(64,64))
left_2 = pg.transform.scale(pg.image.load("sprites/left_2.png").convert_alpha(),(64,64))
left_3 = pg.transform.scale(pg.image.load("sprites/left_3.png").convert_alpha(),(64,64))
stand_left = pg.transform.scale(pg.image.load("sprites/stand_left.png").convert_alpha(),(64,64))

right_0 = pg.transform.scale(pg.image.load("sprites/right_0.png").convert_alpha(),(64,64))
right_1 = pg.transform.scale(pg.image.load("sprites/right_1.png").convert_alpha(),(64,64))
right_2 = pg.transform.scale(pg.image.load("sprites/right_2.png").convert_alpha(),(64,64))
right_3 = pg.transform.scale(pg.image.load("sprites/right_3.png").convert_alpha(),(64,64))
stand_right = pg.transform.scale(pg.image.load("sprites/stand_right.png").convert_alpha(),(64,64))

wall = pg.transform.scale(pg.image.load("sprites/tree.png").convert_alpha(),(86,86))
treasure = pg.transform.scale(pg.image.load("sprites/Triforce.png").convert_alpha(),(128,128))
position_perso = stand_down.get_rect()

win = pg.transform.scale(pg.image.load("sprites/win.png").convert_alpha(),(860,640))
Menu = pg.transform.scale(pg.image.load("sprites/menu.png").convert_alpha(),(860,640))
Panneau = pg.transform.scale(pg.image.load("sprites/panneau.png").convert_alpha(),(220,640))
bar_0 = pg.transform.scale(pg.image.load("sprites/bar.png").convert_alpha(),(250,3))
bar_1 = pg.transform.scale(pg.image.load("sprites/bar.png").convert_alpha(),(290,3))
bar_2 = pg.transform.scale(pg.image.load("sprites/bar.png").convert_alpha(),(180,3))

pg.font.init()
mafont=pg.font.SysFont("Arial", 30)
fontvolume = pg.font.SysFont("Arial",35)
couleur_panneau = (144,107,88)
f = open("maze.txt","r")					# On ouvre le fichier généré par generation_laby.py
x = 0
y = 0


Salles = []									# On va créer deux listes différentes, Salles pour les directions de déplacement à 
State_Salles = []							# l'intérieur de celle-ci, State_Salles pour l'accessibilité (1 si accessible, 0 sinon)
for l in f:
	Ligne_Salle = []
	Ligne_Salle2 = []
	l = l.strip("\n")
	for char in l :
		Ligne_Salle.append(char)
		Ligne_Salle2.append(int(char))
	Salles.append(Ligne_Salle)
	State_Salles.append(Ligne_Salle2)

f.close()

#Structure de la liste de liste : Salles[y][x]==[Ouest,Nord,Est,Sud]
#Structure pour création d'une salle : 
#[Bool*4], représentant si les salles respectivement de gauche, du haut, de droite et du bas sont ouvertes (True) ou fermées (False)

# Génération des listes :

for i in range(len(Salles)):
	for j in range(len(Salles[0])):
		Salles[i][j]=[None,None,None,None]	# On modifie la structure de Salles pour pouvoir indiquer les directions.


for y in range(len(Salles)):
	for x in range(len(Salles[0])):
		#Verification Ouest :
		if x == 0 : Salles[y][x][0]=False
		elif State_Salles[y][x-1] == 1 : Salles[y][x][0]=True
		elif State_Salles[y][x-1] == 0 : Salles[y][x][0]=False

		#Verification Nord :
		if y == 0 : Salles[y][x][1] = False
		elif State_Salles[y-1][x]==1:Salles[y][x][1]=True
		elif State_Salles[y-1][x]== 0:Salles[y][x][1]=False

		#Verification Est :
		if x == len(Salles[0])-1 : Salles[y][x][2] = False
		elif State_Salles[y][x+1]==1 :Salles[y][x][2]=True
		elif State_Salles[y][x+1]==0 : Salles[y][x][2]=False

		#Verification Sud :
		if y == len(Salles)-1: Salles[y][x][3] = False
		elif State_Salles[y+1][x]==1 :Salles[y][x][3]=True
		elif State_Salles[y+1][x]==0 : Salles[y][x][3]=False


minimap = [[0 for x in range(len(Salles[0]))] for y in range(len(Salles))] 
# Salles explorées = 1, Salles non explorées = 0, Salle actuelle = 2, Salle du trésor = 2

# Salles éligibles pour contenir la Triforce : Celles en bout de chemin : Seulement un True dans le bool.
Eligibles = []
for y in range(len(Salles)):
	for x in range(len(Salles[0])):
		compteur = 0
		for i in range(4):
			if Salles[y][x][i]==True : compteur = compteur + 1
		if compteur == 1 : Eligibles.append((x,y))

div = len(Eligibles)		 # Nombre de salles éligibles pour contenir la Triforce
random.seed(div)			 # La seed du choix random de salle dépend de la longueur => vraiment random
a = random.random()*div		 # Choix du numéro dans la liste [0,1[ => 0, [1,2[ => 1, etc...
e,f = Eligibles[int(a)]		 # Transformation en entier du nombre aléatoire (réduit à l'entier inférieur, tel que 4,6345625 passe à 4)
State_Salles[f][e]=2		 # On définit la salle à chercher
minimap[f][e]=3
Eligibles.pop(int(a))		 # On retire la salle des salles éligibles.
c,b = Eligibles[int(random.random()*len(Eligibles))] # Same thing mais plus rapidement.
State_Salles[b][c]=3		 # On définit la salle de départ, pas besoin de la supprimer car on n'utilise plus Eligibles.
miniX = b
miniY = c 					 # Les coordonnées sur la minimap


def Generation_Salle(Room):
	cases = [[1,1,1,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1,1,1]]
	# Liste de liste : cases[x][y] = 1 si mur, 0 si terrain libre, 2 si objet à trouver présent,3 si chemin vers autre salle.
	
	if Room[0]==True :		# Structure de base (sans les chemins rajoutés) :
		cases[4][0]=3		# 1111111111
		cases[5][0]=3		# 1000000001
	if Room[1]==True :		# 1000000001
		cases[0][4]=3		# 1000000001	Puis on rajoute des passages à gauche, en haut, à droite, et finalement en bas.
		cases[0][5]=3		# 1000000001
	if Room[2]==True :		# 1000000001
		cases[4][9]=3		# 1000000001
		cases[5][9]=3		# 1000000001
	if Room[3]==True :		# 1000000001
		cases[9][4]=3		# 1111111111
		cases[9][5]=3
	return cases

position_perso = (320,320) #Le personnage démarre au milieu de la salle.
direction = 'down'

cases = Generation_Salle(Salles[miniX][miniY])
for i in range(len(cases)):
	for j in range(len(cases[i])):
		if cases[i][j]==1:
			screen.blit(wall, ((64*i)-10,(64*j)-10))
		if cases[i][j]==2:
			screen.blit(treasure, (64*i,64*j))
screen.blit(stand_down,position_perso)

#BOUCLE INFINIE
continuer = 1
mouvement_possible = 1
item_found = 0				# Si on trouve l'objet, passe à 1.
has_changed = 0 			# Passe à 1 pour marquer le changement de salle et la génération de carte.
menu_ouvert = 0 			# 0 pour fermé, 1 pour ouvert.
menu_selection = 0 			# Curseur du menu : 0 pour Reprendre, 1 pour Volume, 2 pour Quitter.
jouer_cinematique = 0 		# 1 si on joue la cinématique à la fin du jeu (utilisé ligne 249 et 338)
precedente_animation = stand_down
clock = pg.time.Clock()
clock.tick()
timer_duree_init = 7 #Utilisée plus tard pour les animations
Temps = 0
a = 1

while (continuer == 1):
	minimap[miniX][miniY] = 2 #On fixe la salle actuelle comme celle présente
	if menu_ouvert == 1 or mouvement_possible == 0 :
		clock.tick()
	else :
		Temps = Temps + clock.tick()
		Minutes = Temps / 60000 # Il s'agit de milisecondes.
		Secondes = (Temps - 60000 * Minutes)/1000 

	deplacement = 0 		# Si touche de déplacement appuyée, passe à 1
	if has_changed !=0 :	# S'il y a eu un changement de salle.

		cases = Generation_Salle(Salles[miniX][miniY])			# On génère la liste des cases.
		
		if State_Salles[miniX][miniY]==2 : cases[4][4]=2		# Vérification si la salle possède la Triforce => On la met dedans.
		if has_changed == 1 : position_perso = (320-32,70) 		# Le personnage apparait en haut
		if has_changed == 2 : position_perso = (320-32,640-70)	#...en bas
		if has_changed == 3 : position_perso = (70,320-32)		#...à gauche
		if has_changed == 4 : position_perso = (640-70,320-32) 	#...à droite
		if has_changed == 5 : position_perso = (320,320)		# A servi pour du débuggage : PAS ACTIF EN JEU
		has_changed = 0 										#Le personnage a changé de salle => Plus besoin de le redéplacer à la position de départ.
																
		screen.blit(background, (0,0))							#On fait apparaitre la nouvelle salle.
		for i in range(len(cases)):
			for j in range(len(cases[i])):
				if cases[i][j]==1:
					screen.blit(wall, ((64*i)-10,(64*j)-10))
		if cases[4][4]==2:
			screen.blit(treasure, (64*4,64*4))
		

	for event in pg.event.get():   				#Attente des evenements
		if event.type == QUIT:
			continuer = 0
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE: 		# Si on appuie sur la touche echap
				if menu_ouvert == 0 and mouvement_possible == 1 : # Si le menu est fermé,
					menu_ouvert = 1 							# On ouvre le menu,
					pg.key.set_repeat(50000,16) 				# Et on met un chiffre abominablement grand (50s) pour empêcher la répétition des inputs.
					menu_selection = 0 							# On veut mettre le curseur de base sur "Reprendre"
					son_menu_open.play()						# On joue le son d'ouverture de menu.

				elif menu_ouvert == 1 :			# Si le menu est ouvert,
					menu_ouvert = 0				# On ferme le menu
					pg.key.set_repeat(1,16)		# Et on remet la répétition des inputs comme avant.
					son_menu_close.play()		# On joue le son de fermeture de menu.

				elif mouvement_possible == 0 :
					continuer = 0
					jouer_cinematique = 0

																				# Mouvement du personnage:
			if event.key == K_DOWN: 												# Si "fleche bas"
				if menu_ouvert == 0 and mouvement_possible == 1 : 					# Menu fermé => Personnage libre de se déplacer
					if direction != 'down' : direction_change = True 				# Si on change de direction, on l'enregistre pour les animations.
					direction = 'down'												# On change de direction.
					if cases[((position_perso[0]+32)/64)][((position_perso[1]+69)/64)]!=1 : # Si il n'y a pas de mur en bas,
						position_perso = (position_perso[0],position_perso[1]+5)			# On peut faire descendre le personnage.
						deplacement = 1														# Et on indique qu'il se déplace pour les animations.
						if position_perso[1]>640-70 : 	# Si il est sur une case sortie
							has_changed = 1 			# On indique qu'on a changé de carte, et où il doit apparaitre
							minimap[miniX][miniY]=1		# On rajoute cet endroit comme exploré sur la minimap	
							miniY = miniY + 1 			# On change l'endroit dans la mini-map.

				if menu_ouvert == 1 :
					menu_selection = (menu_selection + 1)%3 # Si le curseur est en bas, il revient en haut. Sinon il descend au menu suivant.
					son_menu_hover.play()					# On joue le petit son qui indique qu'on change de sélection.


			if event.key == K_UP: # Si "fleche haut"
				if menu_ouvert == 0 and mouvement_possible == 1 :
					if direction != 'up' : direction_change = True
					direction = "up"
					if cases[((position_perso[0]+32)/64)][((position_perso[1]-5)/64)]!=1 :
						position_perso = (position_perso[0],position_perso[1]-5)
						deplacement = 1
						if position_perso[1]<5 :
							has_changed = 2 
							minimap[miniX][miniY]=1		# On rajoute cet endroit comme exploré sur la minimap	
							miniY = miniY -1 

				if menu_ouvert == 1 :
					menu_selection = (menu_selection - 1)%3 # Si le curseur est en haut, il va en bas. Sinon il remonte au menu précédent.
					son_menu_hover.play()					# On joue le petit son qui indique qu'on change de sélection.

			if event.key == K_RIGHT: # Si "fleche droite"

				if menu_ouvert == 0 and mouvement_possible == 1 :
					if direction != 'right' : direction_change = True
					direction = 'right'
					if cases[((position_perso[0]+69)/64)][((position_perso[1]+32)/64)]!=1 :
						deplacement = 1
						position_perso = (position_perso[0]+5,position_perso[1])
						if position_perso[0]>640-71 :
							has_changed = 3 
							minimap[miniX][miniY]=1		# On rajoute cet endroit comme exploré sur la minimap	
							miniX = miniX + 1

				if menu_ouvert == 1 :
					if menu_selection == 1 : 									# Si on est sur le bouton "Volume : X0 %"
						if volume < 10 :
							volume = volume + 1
							pg.mixer.music.set_volume(float(volume)/10) 					# On augmente le volume de 10%
						son_menu_hover.play()									# On joue le petit son pour avoir un feedback sonore.

			if event.key == K_LEFT: # Si "fleche gauche"

				if menu_ouvert == 0 and mouvement_possible == 1 :
					if direction != 'left' : direction_change = True
					direction = 'left'
					if cases[((position_perso[0]-5)/64)][((position_perso[1]+32)/64)]!=1 :
						deplacement = 1
						position_perso = (position_perso[0]-5,position_perso[1])
						if position_perso[0]< 5 :
							has_changed = 4 
							minimap[miniX][miniY]=1		# On rajoute cet endroit comme exploré sur la minimap	
							miniX = miniX - 1

				if menu_ouvert == 1 :
					if menu_selection == 1 : 											# Si on est sur le bouton "Volume : X0 %"
						if volume > 0 :													# Si le volume n'est pas à 0.
							volume = volume - 1	
							pg.mixer.music.set_volume(float(volume)/10) 							# On baisse le son de 10%
						son_menu_hover.play()											# On joue le petit son pour avoir un feedback sonore.

			if event.key == K_RETURN :
				if menu_ouvert == 1 :
					if menu_selection == 0 :	# Si Reprendre...
						menu_ouvert = 0		 	# On reprend le jeu.
						son_menu_close.play()
					if menu_selection == 1 :	# Si Volume,
						son_menu_hover.play() 	# On donne juste un feedback sonore.
					if menu_selection == 2 :	# Si Quitter,
						continuer = 0			# On quitte le jeu.

				elif mouvement_possible == 0 :
					continuer = 0
					jouer_cinematique = 1


		#Verification : Est-ce qu'on a trouvé l'objet ?
		if State_Salles[miniX][miniY] == 2 : # Grande ligne : Si le personnage est dans l'une des quatres cases du milieu.
			if cases[(position_perso[0]+32)/64][(position_perso[1]+32)/64]==2 or cases[(position_perso[0]-32)/64][(position_perso[1]+32)/64]==2 or cases[(position_perso[0]+32)/64][(position_perso[1]-32)/64]==2 or cases[(position_perso[0]-32)/64][(position_perso[1]-32)/64]==2:
				if item_found == 0 : 
					son_item.play() # Youhou, on a trouvé l'objet. Fin du jeu.
					item_found = 1  # On évite de répéter le son en boucle.
					mouvement_possible = 0 # On modifie toutes les options.

				
	# Animations.
	if menu_ouvert == 0 : #Ne pas affecter les animations si le menu est ouvert (le menu étant transparant)
		if deplacement == 0 : 
			timer_duree = timer_duree_init # Bloque le timer sur la valeur de départ
			numero_sprite = 0 	# Bloque les sprites sur leur image de départ (on s'en moque un peu ici vu que on aura l'animation 
								# stand_direction, mais sert pour réinitialiser les animations pour la mise en déplacement)
		if deplacement == 1 : # Si mouvement, condition vérifiée
			timer_duree = timer_duree - 1 # On enlève 1 au timer
			if timer_duree == 0 : # Si le temps de l'image est écoulée,
				timer_duree = timer_duree_init # on réinitialise le timer,
				numero_sprite = numero_sprite + 1 # On passe à l'image suivante.
		if numero_sprite == 4 : numero_sprite = 0 # Si on dépasse le nombre d'images (4), on revient à l'image de départ.


	screen.blit(background,(0,0))
	
	for i in range(len(cases)):
		for j in range(len(cases[i])):
			if cases[i][j]==1:
				screen.blit(wall, ((64*i)-10,(64*j)-10))
			if cases[i][j]==2:
				screen.blit(treasure, (64*i,64*j))

	if direction == 'down' :
		if menu_ouvert == 1 :
			screen.blit(precedente_animation,position_perso)
		elif deplacement == 0 :
			screen.blit(stand_down,position_perso)
			precedente_animation = stand_down
		elif numero_sprite == 0 :
			screen.blit(down_0,position_perso)
			precedente_animation = down_0
		elif numero_sprite == 1 :
			screen.blit(down_1,position_perso)
			precedente_animation = down_1
		elif numero_sprite == 2 :
			screen.blit(down_2,position_perso)
			precedente_animation = down_2
		elif numero_sprite == 3 :
			screen.blit(down_3,position_perso)
			precedente_animation = down_3

	if direction == 'up' :
		if menu_ouvert == 1 :
			screen.blit(precedente_animation,position_perso)
		elif deplacement == 0 :
			screen.blit(stand_up,position_perso)
			precedente_animation = stand_up
		elif numero_sprite == 0 :
			screen.blit(up_0,position_perso)
			precedente_animation = up_0
		elif numero_sprite == 1 :
			screen.blit(up_1,position_perso)
			precedente_animation = up_1
		elif numero_sprite == 2 :
			screen.blit(up_2,position_perso)
			precedente_animation = up_2
		elif numero_sprite == 3 :
			screen.blit(up_3,position_perso)
			precedente_animation = up_3

	if direction == 'right' :
		if menu_ouvert == 1 :
			screen.blit(precedente_animation,position_perso)
		elif deplacement == 0 :
			screen.blit(stand_right,position_perso)
			precedente_animation = stand_right
		elif numero_sprite == 0 :
			screen.blit(right_0,position_perso)
			precedente_animation = right_0
		elif numero_sprite == 1 :
			screen.blit(right_1,position_perso)
			precedente_animation = right_1
		elif numero_sprite == 2 :
			screen.blit(right_2,position_perso)
			precedente_animation = right_2
		elif numero_sprite == 3 :
			screen.blit(right_3,position_perso)
			precedente_animation = right_3

	if direction == 'left' :
		if menu_ouvert == 1 :
			screen.blit(precedente_animation,position_perso)
		elif deplacement == 0 :
			screen.blit(stand_left,position_perso)
			precedente_animation = stand_left
		elif numero_sprite == 0 :
			screen.blit(left_0,position_perso)
			precedente_animation = left_0
		elif numero_sprite == 1 :
			screen.blit(left_1,position_perso)
			precedente_animation = left_1
		elif numero_sprite == 2 :
			screen.blit(left_2,position_perso)
			precedente_animation = left_2
		elif numero_sprite == 3 :
			screen.blit(left_3,position_perso)
			precedente_animation = left_3

	screen.blit(Panneau,(640,0))

	# On affiche la minimap :

	for x in range(len(minimap)):
		for y in range(len(minimap[x])):
			if minimap[x][y]== 1 :
				pg.draw.rect(screen,(200,200,200),(650+20*x,42+20*y,20,20))
			if minimap[x][y]== 2 :
				pg.draw.rect(screen,(50,50,200),(650+20*x,42+20*y,20,20))
			if minimap[x][y]== 3 :
				pg.draw.rect(screen,(200,50,50),(650+20*x,42+20*y,20,20))


	# On affiche le timer :
	if Minutes < 10 :
		screen.blit(mafont.render(str(0),1,couleur_panneau),(666,417))
		screen.blit(mafont.render(str(Minutes),1,couleur_panneau),(684,417))
	else :
		screen.blit(mafont.render(str(Minutes),1,couleur_panneau),(666,417))
	if Secondes < 10 :
		screen.blit(mafont.render(str(0),1,couleur_panneau),(765,417))
		screen.blit(mafont.render(str(Secondes),1,couleur_panneau),(783,417))
	else :
		screen.blit(mafont.render(str(Secondes),1,couleur_panneau),(765,417))
	screen.blit(mafont.render("[ " + str(miniX) +" ; " + str(miniY) + " ]",1,couleur_panneau),(706,520))
	screen.blit(mafont.render("[ X ; Y ]",1,couleur_panneau),(704,560))

	if menu_ouvert == 1:
		screen.blit(Menu,(0,0))
		screen.blit(fontvolume.render(str(int(volume*10))+"%",1,(255,255,255)),(400,380)) # On affiche le % de volume.
		if menu_selection == 0 :
			screen.blit(bar_0,(194,350))
		if menu_selection == 1 :
			screen.blit(bar_1,(180,420))
		if menu_selection == 2 :
			screen.blit(bar_2,(233,495))

	if item_found == 1 :
		screen.blit(win,(0,0))
		pg.mixer.music.stop() # On coupe la musique pour la cinématique.

	pg.display.update()

		
pg.mixer.stop()				# On coupe tous les sons pour la cinématique.

if jouer_cinematique == 1 :

	pg.draw.rect(screen,(0,0,0),(0,0,860,640))
	pg.mixer.music.load("sounds/cinematic_music.ogg")

	slide_1 = pg.image.load("cinematique/part_1.png")
	slide_2 = pg.image.load("cinematique/part_2.png")
	slide_3 = pg.image.load("cinematique/part_3.png")
	slide_4 = pg.image.load("cinematique/part_4.png")
	slide_5 = pg.image.load("cinematique/part_5.png")
	slide_6 = pg.image.load("cinematique/part_6.png")

	texte_1 = pg.image.load("cinematique/t_1.png")
	texte_2 = pg.image.load("cinematique/t_2.png")
	texte_3 = pg.image.load("cinematique/t_3.png")
	texte_4 = pg.image.load("cinematique/t_4.png")
	texte_5 = pg.image.load("cinematique/t_5.png")
	texte_6 = pg.image.load("cinematique/t_6.png")
	texte_7 = pg.image.load("cinematique/t_7.png")
	texte_8 = pg.image.load("cinematique/t_8.png")
	texte_9 = pg.image.load("cinematique/t_9.png")
	texte_10 = pg.image.load("cinematique/t_10.png")
	texte_11 = pg.image.load("cinematique/t_11.png")
	texte_12 = pg.image.load("cinematique/t_12.png")
	texte_13 = pg.image.load("cinematique/t_13.png")
	texte_14 = pg.image.load("cinematique/t_14.png")
	texte_15 = pg.image.load("cinematique/t_15.png")
	texte_16 = pg.image.load("cinematique/t_16.png")
	texte_17 = pg.image.load("cinematique/t_17.png")
	texte_18 = pg.image.load("cinematique/t_18.png")
	texte_19 = pg.image.load("cinematique/t_19.png")
	texte_20 = pg.image.load("cinematique/t_20.png")
	texte_21 = pg.image.load("cinematique/t_21.png")
	texte_22 = pg.image.load("cinematique/t_22.png")

	pg.display.update()
	
	Temps = 0
	Minutes = 0
	Secondes = 0
	pg.mixer.music.play()

def DrawCadre():
	pg.draw.rect(screen,(0,0,0),(0,0,100,640))
	pg.draw.rect(screen,(0,0,0),(760,0,100,640))
	pg.draw.rect(screen,(0,0,0),(0,0,860,100))
	pg.draw.rect(screen,(0,0,0),(0,406,860,254))
time.sleep(3)
clock.tick(60)

while jouer_cinematique == 1 :

	Temps = Temps + clock.tick()
	# Il s'agit de milisecondes.
	Secondes = float(Temps) / 1000

	# Liste des animations à faire selon le timer :
	pg.draw.rect(screen,(0,0,0),(0,0,860,640)) # Fond noir
	if 1==1 : #Juste pour rabattre la liste des animations sur Sublime Text
		if Secondes < 8  :
			screen.blit(texte_1,(0,242))
		if Secondes < 27 :
			if Secondes > 10 :
				screen.blit(slide_1,(100,280-(18*Secondes)))
				DrawCadre()
			if Secondes > 10 and Secondes < 18 :
				screen.blit(texte_2,(0,436))
			if Secondes > 20 :
				screen.blit(texte_3,(0,436))
		if Secondes < 53 :
			if Secondes > 27 :
				screen.blit(slide_2,(100,100))
				DrawCadre()
			if Secondes > 28 and Secondes < 36 :
				screen.blit(texte_4,(0,436))
			if Secondes > 37 and Secondes < 45 :
				screen.blit(texte_5,(0,436))
			if Secondes > 46 :
				screen.blit(texte_6,(0,436))
		if Secondes < 77 :
			if Secondes > 53 :
				screen.blit(slide_3,(100,100))
				DrawCadre()
			if Secondes > 54 and Secondes < 66 :
				screen.blit(texte_7,(0,436))
			if Secondes > 67 and Secondes < 76 :
				screen.blit(texte_8,(0,436))
		if Secondes < 120 :
			if Secondes > 77 :
				screen.blit(slide_4,(947-(11*Secondes),100))
				DrawCadre()
			if Secondes > 77 and Secondes < 85 :
				screen.blit(texte_9,(0,436))
			if Secondes > 85 and Secondes < 93 :
				screen.blit(texte_10,(0,436))
			if Secondes > 94 and Secondes < 102 :
				screen.blit(texte_11,(0,436))
			if Secondes > 103 and Secondes < 111 :
				screen.blit(texte_12,(0,436))
			if Secondes > 112 and Secondes < 120 :
				screen.blit(texte_13,(0,436))
		if Secondes < 158 :
			if Secondes > 120 :
				screen.blit(slide_5,(100,100))
				DrawCadre()
			if Secondes > 120 and Secondes < 129 :
				screen.blit(texte_14,(0,436))
			if Secondes > 130 and Secondes < 138 :
				screen.blit(texte_15,(0,436))
			if Secondes > 139 and Secondes < 147 :
				screen.blit(texte_16,(0,436))
			if Secondes > 148 and Secondes < 157 :
				screen.blit(texte_17,(0,436))

		if Secondes > 162 and Secondes < 169 :
			screen.blit(texte_18,(0,242))

		if Secondes < 207 :
			if Secondes > 171 :
				screen.blit(slide_6,(100,100))
			if Secondes > 171 and Secondes < 179 :
				screen.blit(texte_19,(0,436))
			if Secondes > 180 and Secondes < 188 :
				screen.blit(texte_20,(0,436))
			if Secondes > 189 and Secondes < 197 :
				screen.blit(texte_21,(0,436))
			if Secondes > 198 and Secondes < 206 :
				screen.blit(texte_22,(0,436))

	if Secondes > 213 :
		jouer_cinematique = 0


	pg.display.update()
