import pygame, sys, time
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_UP
import random

screen_width = 700
screen_height = 700
white = (105,105,105)
green = (23,255,0)
grey = (0,0,0)
box = 30  # définir la taille des carrés


S = [['.....',
      '.....',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

objets = [S, Z, I, O, J, L, T]
objet_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
alea = random.randint(0,6)
pos_piece = 0

def getTetrimo(i):
    global objets
    return objets[i]

def getColor(i):
    global objet_colors
    return objet_colors[i]

def run_game():
    global alea
    global pos_piece

    pygame.init() #charge module pygame
    window_size = (screen_width,screen_height)  # la taille de la fenetre
    screen = pygame.display.set_mode(window_size) # Créer la fenetre ici c'est (screen)
    pygame.display.set_caption("Le jeu Tetris") # Le titre de la fenetre
    
    ######## Associer les fonctions ####################
    
    play_map = create_map()
    piece = create_piece()
    moving = time.time()
    Score = 0

    #####################################################

    running = True
    while running: 
        ''' Donné couleur noir a notre écran'''
        screen.fill((0,0,0))   # Ecran noir

        '''  Faire tomber la piece avec fonction time (pas de lag, si utiliser fontion time.sleep , beaucoup lag dans la fenetre) '''
        if time.time() - moving > 0.5:  
            piece[0] = piece[0] + 1
            moving = time.time()

        ''' Créer la map avec les carrés de 30 pixels , total 200 carrés . (100,50) point départ , 10 colones * box size , 20 ligne * box size. fontion Rect(Point départ, largueur , hauteur )'''
        pygame.draw.rect(screen, green, [100,50,10*box,20*box],1)
        
        ''' Ajouter la piece complete dans la map'''
        draw_piece_complet(screen, piece)

        '''Afficher zone de score dans la fenetre'''
        draw_score(screen, Score)
         
        print(pos_piece) # !!! bug si je print pas , les piece bouge pas , ne comprend pas pour quoi

        # Fonction pour bouger les pieces gauche et droite et rotation la piece
        touch(play_map, piece)

        ''' Vérifier si la ligne suivant est vide ou c'est la derniere ligne pour stopper la piece et recréer nouvelle piece . Pour vérifier la ligne just après la piece complete on utilise la parametre adRow 1. la piece complete est "piece[0] + row, piece[1] + col
        adRow = 1 (on regarde la ligne + 1 de notre piece complete)
        '''

        if(not isValid(play_map,piece,adRow=1)):
            play_map = update_map_play(play_map,piece)  
            line_removed = clear_line(play_map,piece)  # Compter la ligne surprimé
            Score += line_removed   # Ajouter les score par rapport de la ligne surprimé
            piece = create_piece()  # Recréér une nouvelle piece en haut

        # ajouter la meme piece une fois la stoppé
        blocked(screen, play_map)

        pygame.display.flip() # Mise a jour de la fenetre 

        for event in pygame.event.get(): # Ce boucle empeche de fermer la fenetre
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()


####################  Création de map  ##################################

''' Ici on va créer notre map matrice avec 10 colones et 20 ligne . ici "0" est la case occupé et "." est la case vide '''
def create_map():
    map_row = 20        # Nombre de ligne
    map_column = 10  # Nombre de colone
    play_map = []    # Créer un liste vide
    for row in range(map_row):    # le boucle for va créer un tableau avec 20 ligne , chaque ligne on ajoute 10 points
        new_row = []
        for column in range(map_column):
            new_row.append(".")
        play_map.append(new_row)
    return play_map

''' Position de la piece dans la map , La position de la piece est avec une liste [0,2] , la piece commence dans la ligne 0 et la colone 2 '''
def create_piece():  
    global alea
    global pos_piece
    piece = [0,2]
    alea = random.randint(0,6)
    pos_piece = 0
    return piece

''' Cette fonction va créer 1 simple carré dans notre map '''
def draw_piece(screen, row, col, color,shadow_color):
    y = 50 + (row * 30) # Coord x de la piece ( 50 c'est le point départ quand crée la case , ici 20 ligne avec les carrés de 30 pixels)
    x = 100  + (col * 30)     # Coord y de la piece  ( 100 c'est le point départ quand crée la case, ici 10 colones avec les carrés de 30 pixels )
    pygame.draw.rect(screen,shadow_color,[x,y,30,30])
    pygame.draw.rect(screen,color,[x,y,28,28])

''' Ici on va créer la zone pour afficher les score '''

def draw_score(screen, score):
    font = pygame.font.Font('freesansbold.ttf', 18) # Import font de text
    show_score = font.render('Score: %s' % score, True, (255,255,255)) # Affichage de score
    screen.blit(show_score, (screen_width - 200 , 50))  # Position de text dans la fenetre , utiliser fonction blit de pygame

############ Création de la piece ##############

''' Cette fonction regarde dans la piece matrice (5,5), il dessine la forme  avec les "0" qu'il trouve dans piece matrice '''

def draw_piece_complet(screen, piece):
    objet_to_draw = getTetrimo(alea)[pos_piece]
    for row in range(5):
        for col in range(5):
            if objet_to_draw[row][col] == '0':
                draw_piece(screen,piece[0]+row,piece[1]+col, getColor(alea), grey)


'''cette fonction va coppier les "0" de la piece matrice dans les case vide "." dans la map'''
def update_map_play(play_map, piece):
    random_objet = getTetrimo(alea)[pos_piece]
    for row in range(5):
        for col in range(5):
            if(random_objet[row][col] != "."):
                play_map[piece[0]+row][piece[1]+col] = "0"
    return play_map  
    
'''Cette fonction va regarder tous les case dans la map s'il y a des "0" que la fonction en haut "update_map_play" a fait, en suite elle va draw la forme'''   
def blocked(screen, play_map):  
    for row in range(len(play_map)):
        for col in range(len(play_map[row])):
            if play_map[row][col] != ".":
                draw_piece(screen,row, col, white, grey)


##############  Surprimer les lignes completes ##############################

''' Ici on va regarder quelle ligne est complete '''
def check_line(play_map, row):  # Check si une ligne est complete
    for col in range(10):
        if play_map[row][col] == ".":   # si dans une ligne il y a "." , retourn false
            return False
    return True  # si non cette ligne est complete


''' Ici on va surprimer les lignes completes et faire descendre les lignes pas completes '''
def clear_line(play_map, piece):   # La fonction va surprimer la ligne complete
    line_removed = 0  # Pour ajouter les score apres
    for row in range(20):
        if check_line(play_map, row):    # on récupère la fonction check ligne
            for col in range(10):
                # Ici on va surprimer la ligne est plein , replace le "0" avec le "."
                play_map[piece[0]][piece[1]] = '.'
                line_removed += 1    # Pour ajouter les Score apres
            for row_to_down in range(row, 0, -1):  
                # ici on va chercher la ligne just au dessus de la ligne qui est complete
                for col in range(10):
                    # on va faire descendre cette ligne en bas pour replacer la ligne qui est complete et surprimé
                    play_map[row_to_down][col] = play_map[row_to_down-1][col]
    return line_removed




################ Verification les bords ########################

''' Ici on donne la limit de notre map de jeu avec 20 ligne et 10 colone '''
def limit(row, column):
    return column >= 0 and column < 10 and row < 20

'''On va regarder si tous les carrés de la piece complete ne depassent pas les bords , on va utiliser les 2 parametres adCol et adRow pour vérifier les ligne et colone autour de notre piece complete . la piece complete est "piece[0] + row, piece[1] + col '''

def isValid(play_map, piece, adCol=0, adRow=0):
    random_objet = getTetrimo(alea)[pos_piece]
    for row in range(5):
        for col in range(5):
            # si dans l'objet il y a "." on continue , on fait rien
            if random_objet[row][col] == '.':  
                continue
            ''' Ici on récupère la fonction "limit" just en haut, si la piece complete n'est pas dans la limit , on passe False '''    
            if not limit(piece[0]+ row + adRow, piece[1]+ col + adCol):
                return False
            ''' Ici on va vérifier la collision entre les piece , si la case n'est pas vide , on passe False'''
            if play_map[piece[0]+ row + adRow][piece[1] +col + adCol] != '.':
                return False
    return True


#############  Les movements avec clavier ###################


def touch(play_map, piece):   # Utiliser fonction pygame pour les claviers
    global pos_piece
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            ''' Piece va a gauche si on touche sur le touch '<',  et si notre piece complete ne sort pas de la case . la piece complete est "piece[0] + row, piece[1] + col . On passe la parametre adCol = -1 pour verifier la colone a gauche de la piece complete '''

            if (event.key == K_LEFT ) and isValid(play_map,piece,adCol=-1):
               piece[1] -= 1  #  enlève 1 colone a chaque touche

               ''' Piece va a droite si on touche sur le touch '>' et si elle ne sort pas la case , et si notre piece complete ne sort pas de la case . la piece complete est "piece[0] + row, piece[1] + col . On passe la parametre adCol = 1 pour verifier la colone a droite de la piece complete '''
               
            elif (event.key == K_RIGHT ) and isValid(play_map,piece,adCol=1):
                piece[1] += 1  #  Ajoute 1 colone a chaque touche

                ''' Rotation de la piece '''
            elif (event.key == K_UP ):
                pos_piece = (pos_piece + 1) % len(getTetrimo(alea))
                if not isValid(play_map,piece):
                    pos_piece = (pos_piece - 1) % len(getTetrimo(alea))

run_game()