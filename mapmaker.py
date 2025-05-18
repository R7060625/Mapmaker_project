import os
import fltk
import random
from typing import List, Dict, Tuple, Optional
################################# GESTION DES FICHIERS ###########################################
def cree_dico() -> Dict[str, str] : 
    """
    Récupère l'ensemble des titres de chaque fichier image, stockés respectivement
    dans le dossier "tuiles" du dossier "fichiers fournis".
    Le programme et le dossier "fichiers fournis" doivent être stockés au même endroit de
    l'arborescence et chaque dossier contenant des images doit être stocké dans le dossier
    "fichiers fournis".
    
    Args :
        None
        
    Retours :
        dict : dictionnaire dont les clés sont les noms des tuiles et leurs valeurs
            des string représentant le chemin de la tuile à partir du dossier parent.
    """
    
    # fichiers_images = ("megatuile", "tuiles") #dossier contenant des tuiles

    dico_path = {}

    path = os.getcwd() # chemin actuel de l'arborescence

    path_fichier = path + "\\fichiers fournis\\tuiles"
    
    for tuile in os.listdir(path_fichier) :
        dico_path[tuile[:4]] = f"tuiles\\{tuile}"

    return dico_path

# def cree_dico() -> Dict[str, str]:
#     """
#     Ajoute les megatuiles dans le dictionnaire créé par cree_dico_intermediaire().
#     Les clés des megatuiles sont leurs noms (composés de 4 lettres
#     majuscules représentant les biomes) et leurs valeurs les chemins
#     depuis leur dossier parent. 
#     Les megatuiles doivent être codés d'une manière particulière. Par exemple,
#     si l'on a une megatuile de montagne, on doit avoir un nom "MegaMMM.png".
#     Il faut précéder le code de la tuile du nom Mega.

#     Args :

#     Retours :
#         dict : même dictionnaire contenant en plus les megatuiles selon le même système de noms.
#     """

#     dico = {}

#     path = os.getcwd()
#     path_fichier = path + "\\fichiers fournis\\megatuile"

#     for megatuile in os.listdir(path_fichier) :
#         dico[megatuile[4:8]] = f"megatuile\\{megatuile}" # extrait le code de la tuile et lui donne en clé la chaîne de caractères 

#     return dico

def renvoie_chemin(code_tuile : str, dico: Dict[str, str]) -> str :
    """
    renvoie le chemin d'accès à l'image

    Args :
        code_tuile (str) : nom de la tuile

        dico (dict) : dictionnaire contenant les chemins d'accès des tuiles
    Retours : 
        str : chemin dans l'arborescence de la tuile 
    """

    return f"{os.getcwd()}\\fichiers fournis\\{dico[code_tuile]}"

###################################################################################################

################################# PLACEMENT DES TUILES  ###########################################
def emplacement_valide(grille : List[List[Optional[str]]] , i:int, j:int, nom_tuile: str) -> bool :
    """
    Vérifie si la tuile nom_tuile se connecte
    correctement aux tuiles déjà posées dans les cases voisines de la case (i, j).
    Renvoie True si c'est le cas et False sinon.
    
    Args:
        grille (list) : liste de listes représentant le tableau 10x10 de base
        
        i, j (int) : coordonnées de la tuile
        
        nom_tuile (str) : string représentant la tuile
        
    Retours:
        bool : Vrai si la tuile se racolle aux voisines, False sinon
    """
    voisins = [(i-1, j), (i, j+1), (i+1, j), (i, j-1)] # liste des coordonnées des tuiles voisines
    
    for indice, voisin in enumerate(voisins) :
        indice_voisin = (indice+2) % 4 #l'indice des voisins fait une boucle de 0 à 4 avec un incrément de 2
        if 0 <= voisin[0] < len(grille) and 0 <= voisin[1] < len(grille) : # checke if les voisins oont des indices valables dans la liste
            if grille[voisin[0]][voisin[1]] is not None and grille[voisin[0]][voisin[1]][indice_voisin] != nom_tuile[indice] : # vérifie si les indices sont correctes puis vérifie les lettres 
                return False
    return True

def place_megatuiles(grille: List[List[Optional[str]]], i_ancrage: int, j_ancrage: int, hauteur: int, largeur: int, code_megatuile: str) -> List[Tuple[int, int]] :
    """
    Place la megatuile dans la fenêtre et 
    ajoute le code de la megatuile à chaque 
    case utilisée dans la matrice. 

    Args :
        grille (list) : matrice représentative

        code_megatuile (str) : nom de la tuile

        hauteur, largeur (int) : taille de la megatuile

        i_ancrage, j_ancrage (int) : coordonnées de la case "de départ"
                                    cliquée pour placer la tuile
    Retours :
        list : liste des couples de coordonnées prises par la megatuile
    """
    dico = cree_dico()

    if verifie_megatuiles(grille, code_megatuile, hauteur, largeur, i_ancrage, j_ancrage) : # la megatuile est compatible dans son emplacement

        liste_cases_prises = []

        fltk.image(j_ancrage*75, i_ancrage*75, renvoie_chemin(code_megatuile, dico), largeur=75*largeur, hauteur=75*hauteur, tag=...)  # image globale

        # on ajoute l'image une fois dans la fenêtre puis on ajoute le code dans la matrice -> évite les répétitions
        for i in range(i_ancrage, i_ancrage+hauteur):
            for j in range(j_ancrage, j_ancrage+largeur):
                grille[i][j] = code_megatuile

                liste_cases_prises.append((i, j))

    return liste_cases_prises


def tuiles_possibles(grille: List[List[Optional[str]]], i: int, j:int) -> List[str] :
    """
    Renvoie la liste de toutes les tuilles qui peuvent être
    positionnées à la case (i, j) dans la grille en respectant les règles d’adjacence.
    
    Args :
        grille (list) : liste de listes représentant le tableau 10x10 de base
        
        i, j (int) : coordonnées de la tuile
        
    Retours :
        list : liste représentant toutes les tuiles qui peuvent être placées en respectant les racollements.
    """
    
    dico = cree_dico()
    liste_tuiles = []
    for tuile in dico : # checke les 160 tuiles
        if emplacement_valide(grille, i, j, tuile) : # vérifie que la tuile se racolle aux autres
            liste_tuiles.append(tuile)
    
    return liste_tuiles

def verifie_megatuiles(grille: List[List[Optional[str]]], code_megatuile: str, hauteur: int, largeur: int, i_ancrage: int, j_ancrage: int) -> bool :
    """
    Permet de vérifier si en cliquant sur la case d'ancrage
    de la megatuile, elle est dans la grille, elle se racolle 
    et elle n'empiète pas sur une tuile pré-existante. 

    Args : 
        grille (list) : matrice représentative

        code_megatuile (str) : nom de la tuile

        hauteur, largeur (int) : taille de la megatuile

        i_ancrage, j_ancrage (int) : coordonnées de la case "de départ"
                                    cliquée pour placer la tuile

    Retours : 
        None
    """
    
    for i in range(i_ancrage, (i_ancrage+hauteur)) : # on vérifie la place que prend la megatuile avec les boucles
        for j in range(j_ancrage, (j_ancrage+largeur)):

            if 0 <= i < len(grille) and 0 <= j < len(grille[0]) :  # vérifie si megatuile peut être placée dans la fenêtre
                if grille[i][j] is None and not(emplacement_valide(grille, i, j, code_megatuile)) : # on vérifie si la case se racolle bien
                    return False
            else : # la megatuile sort de la fenêtre
                return False
    return True 


#######################################################################################################  

################################# FONCTIONNALITES GRAPHIQUES ###########################################

def cree_UI() -> None :
    """
    Crée la fenêtre par défaut dans FLTK de 1000x1000 pixels.

    Args :
        None
    Returns :
        None
    """
    fltk.cree_fenetre(750, 750, affiche_repere = True, redimension=True)

def clear_fenetre() -> None :
    """
    Permet d'effacer toute la fenêtre.

    Args :
        None

    Retours : 
        None
    """
    for i in range(10) :
        for j in range(10) :
            fltk.efface(f"case_{i}_{j}")

    fltk.mise_a_jour()
            


def gere_clic_v1(grille: List[List[Optional[str]]], dico_etat_visuel: Dict[str, bool]) -> None :
    """
    Gère un clic gauche de la souris sur la grille :
     Convertit les coordonnées en indices de case.
    Tente de placer une tuile aléatoire compatible.
     Affiche un message si aucune tuile n'est compatible.
     
     Args :
        grille (list) : tableau
         
        dico_etat_visuel (dict) : permet de garder l'état du visuel, qui est un booléen selon s'il est activé ou non
    Returns :
        None
    """
    ev = fltk.attend_ev()
    tev = fltk.type_ev(ev)
    
    fltk.efface("aucune_tuile") # efface les potentiels messages d'erreur précédents

    if tev == "ClicGauche": # gère le placement manuel des tuiles sur le tableau
        x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
        i, j = y // 75, x // 75 # renvoie une position dans le tableau 
        
        
        tag_case = f"case_{i}_{j}" # création du tag à l'emplacement (i, j)
        
        assistant_conception(grille) # affiche en rouge l'emplacement le plus contraint

        if grille[i][j] is None: # process ajouter une case au tableau : vérifier si la case est vide, vérifier si bien placé -> place l'image
            if 0 <= i < len(grille) and 0 <= j < len(grille[0]) :  
                dico = cree_dico()
                compatibles = tuiles_possibles(grille, i, j)
    
                if compatibles:
                    tuile = affiche_sous_menu_tuiles(compatibles, dico)
                    
                    grille[i][j] = tuile # ajoute notre tuile à la matrice de représentation
                    
                    chemin = renvoie_chemin(tuile, dico) # récudpération du chemin dans l'arborescence
                    
                    fltk.image(j * 75, i * 75, chemin, ancrage = "nw", largeur=75, hauteur=75, tag=tag_case)
                    # place_megatuiles(grille, i, j, 2, 2, "MMMM")

                    
                else: # message d'erreur si aucune tuile n'est posable
                    fltk.rectangle(15, 15, 375, 80, remplissage="white", tag = "aucune_tuile")
                    fltk.texte(195, 45, "Aucune tuile compatible", ancrage="center", couleur="red", tag="aucune_tuile")

            
        else : # la case n'est pas vide donc il faut supprimer l'image à cet emplacement
            grille[i][j] = None # enlève la case de la matrice de représentation
            fltk.efface(tag_case) # efface la case avec les coordonnées (i, j)

        assistant_conception(grille) # dessine la nouvelle case la plus contrainte


    elif tev == "Touche":
        gere_clavier(grille, ev, dico_etat_visuel)
            
        fltk.mise_a_jour() # rafraîchit la page pour supprimer tout ce qui est nécessaire







def gere_clavier(grille: List[List[Optional[str]]], ev: tuple, dico_etat_visuel: Dict[str, bool]) -> None :
    """
    Gère les évènements clavier :
        l'utilisateur doit appuyer sur :
            - espace pour déclencher le solveur
            - les flèches clavier (haut, droite, bas, gauche pour activer le défilement infini)
            - v pour activer ou désactiver le solveur. Par défaut, il est activé
            - c pour effacer complétement la fenêtre et recommencer la carte
     
     Args :
         grille(list) : tableau
         
         ev (tuple) : événement ( en l'occurence, forcément une touche) qui a activé la fonction
         
         dico_etat_visuel : dictionnaire gardant en mémoire l'état du visuel
    Returns :
        None       
    """

    touche = fltk.touche(ev)
    dico = cree_dico()
    
    if touche == "v" :
        dico_etat_visuel["visuel_actif"] = not(dico_etat_visuel["visuel_actif"])  # on affiche quand l'utilisateur appuie sur v
        print(dico_etat_visuel["visuel_actif"])
        affiche_etat_visuel(dico_etat_visuel)

    elif touche == "space": # gère le placement manuel des tuiles sur le tableau

        fltk.efface("rectangle_contraint") # efface le rectangle rouge lié à l'assistant de conception, s'il existe

        solveur_n3_visuel(grille, dico, visuel= dico_etat_visuel["visuel_actif"]) # complète (si possible) la matrice
        # solveur_n1_visuel(grille, dico)

    elif touche in ["Up", "Left", "Down", "Right"] :
        fltk.efface('rectangle_contraint') # efface le rectangle rémanent de l'assistant de conception

        decale_grille(grille, touche)
        clear_fenetre()
        affiche_nv_fenetre(grille, dico)
        fltk.mise_a_jour()
        solveur_n1_visuel(grille, dico)


    elif touche == "c" :
        for i in range(len(grille)) :
            for j in range(len(grille[0])) :

                fltk.efface(f"case_{i}_{j}") # efface l'image
                grille[i][j] = None # efface la place dans la matrice

        fltk.efface("rectangle_contraint") # efface la case de l'assistant de conception

        fltk.mise_a_jour()
        

    fltk.mise_a_jour()

def decale_grille(grille: List[List[Optional[str]]], touche: str) -> None: # pas besoin de toucher
    """
    Décale toutes les cases de la matrice dans la direction
     appropriée. La direction opposée au scroll (les nouvelles
     cases que l'on veut voir) sont remplacées par None.

     Args :
        grille (list) : matrice représentative

        touche : valeur de la touche (ici, flèche directionnelle) sur laquelle on a appuyé

    Retours :
        None
    """
    if touche == "Down":
        grille.pop(0)  # supprime la première ligne
        grille.append([None]*len(grille[0]))  # ajoute une ligne en bas

    elif touche == "Up" :
        grille.pop(-1)
        grille.insert(0, [None]*len(grille[0]))


    elif touche == "Right":
        for ligne in grille:
            ligne.pop(0)
            ligne.append(None)

        
    elif touche == "Left" :
        for index_ligne, ligne in enumerate(grille) :
            ligne.pop(-1)
            ligne.insert(0, None)



def affiche_nv_fenetre(grille: List[List[Optional[str]]], dico_tuiles: Dict[str, str]) -> None :
    """
    après avoir décalé la grille dans la direction appropriée,
    et rendu la fenêtre vierge, 
    on peut replace chaque image dans la bonne nouvelle case.
    On supprimera les images qui sortent du champ dans une autre
    fonction.

    Args :
        dico_tuiles (dict) : dictionnaire contenant tous les chemins
    Retours : 
        None
    """


    for i in range(len(grille)):
        for j in range(len(grille[0])):

            tuile = grille[i][j] 

            if tuile:  # si la tuile est None, on ne l'affiche pas -> évite de faire des disjonctions de cas

                chemin = renvoie_chemin(tuile, dico_tuiles)
                fltk.image(j*75, i*75, chemin, ancrage="nw", hauteur=75, largeur=75, tag=f"case_{i}_{j}")


def supprime_megatuile(grille: List[List[Optional[str]]], i: int , j: int, liste_cases_prises: List[Tuple[int, int]]) -> None :
    """
    efface de la grille et de la fenêtre la megatuile si l'on 
    clique dessus. 

    Args : 
        grille (list) : matrice représentative
        i, j (int) : coordonnées de la case cliquée 
        liste_cases_prises (list) : liste des coordonnées 
                des cases prises par la megatuile

    Retours : 
        None
    """
    

    liste_cases_prises.remove((i, j))

    fltk.efface(f"case_{i}_{j}")

    grille[i][j] = None 

    for i_restant, j_restant in liste_cases_prises : 
        grille[i_restant][j_restant] = None

        fltk.efface(f"case_{i_restant}_{j_restant}")    

def affiche_sous_menu_tuiles(compatibles: List[str], dico: Dict[str, str]) -> None:
    """
    Affiche un menu carré avec les tuiles compatibles et un message.
    Si plus de 8 tuiles, permet de défiler avec les flèches gauche/droite.
    Appuyer sur 'i' masque/affiche le menu.

    Args : 
        compatibles (list) : liste des tuiles compatibles 

        dico : dico contenant les codes et les chemins des tuiles 

    Retours :
        None
    """

    TAILLE = 75
    MARGE = 10
    NB_COL = 4
    NB_LIG = 2
    NB_PAR_PAGE = NB_COL * NB_LIG
    X_MENU = 200
    Y_MENU = 250

    HAUTEUR_MESSAGE = 40
    LARGEUR_MENU = NB_COL * (TAILLE + MARGE) - MARGE + 60
    Y_MENU_FOND = Y_MENU - 50
    HAUTEUR_FOND = NB_LIG * (TAILLE + MARGE) - MARGE + 5 + HAUTEUR_MESSAGE + 20

    PAGE = 0
    nb_pages = (len(compatibles) + NB_PAR_PAGE - 1) // NB_PAR_PAGE

    def affiche_page(PAGE):
        fltk.efface("menu_carre")
        fltk.efface("menu_carre_border")
        fltk.efface("menu_message")
        for idx in range(NB_PAR_PAGE):
            fltk.efface(f"sousmenu_{idx}")
        # Fond et bordure
        fltk.rectangle(
            X_MENU-30, Y_MENU_FOND,
            X_MENU-30 + LARGEUR_MENU,
            Y_MENU_FOND + HAUTEUR_FOND,
            couleur="white", remplissage="white", epaisseur=3, tag="menu_carre"
        )
        fltk.rectangle(
            X_MENU-30, Y_MENU_FOND,
            X_MENU-30 + LARGEUR_MENU,
            Y_MENU_FOND + HAUTEUR_FOND,
            couleur="black", epaisseur=3, tag="menu_carre_border"
        )
        # Message
        fltk.texte(
            X_MENU-30 + LARGEUR_MENU//2, Y_MENU_FOND + 22,
            "Choisissez la tuile que vous voulez placer !",
            ancrage="center", taille=13, tag="menu_message"
        )
        # Affichage des tuiles de la page courante
        positions.clear()
        start = PAGE * NB_PAR_PAGE
        end = min(start + NB_PAR_PAGE, len(compatibles))
        tuiles_affichees = compatibles[start:end]
        for idx, tuile in enumerate(tuiles_affichees):
            col = idx % NB_COL
            lig = idx // NB_COL
            x = X_MENU + col * (TAILLE + MARGE)
            y = Y_MENU + lig * (TAILLE + MARGE)
            chemin = f"{os.getcwd()}\\fichiers fournis\\{dico[tuile]}"
            fltk.image(x, y, chemin, ancrage="nw", largeur=TAILLE, hauteur=TAILLE, tag=f"sousmenu_{idx}")
            positions.append((x, y, x + TAILLE, y + TAILLE, tuile))
        # Flèches de navigation si besoin
        if nb_pages > 1:
            if PAGE > 0:
                fltk.texte(X_MENU-40, Y_MENU+TAILLE, "<", ancrage="center", taille=30, tag="menu_carre")
            if PAGE < nb_pages-1:
                fltk.texte(X_MENU-30 + LARGEUR_MENU+10, Y_MENU+TAILLE, ">", ancrage="center", taille=30, tag="menu_carre")
        fltk.mise_a_jour()

    positions = []
    menu_visible = True

    affiche_page(PAGE)

    while True:
        ev = fltk.attend_ev()
        tev = fltk.type_ev(ev)
        if tev == "ClicGauche" and menu_visible:
            x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
            # Navigation gauche
            if nb_pages > 1 and PAGE > 0 and X_MENU-60 < x < X_MENU-10 and Y_MENU+TAILLE < y < Y_MENU+TAILLE+40:
                PAGE -= 1
                affiche_page(PAGE)
                continue
            # Navigation droite
            if nb_pages > 1 and PAGE < nb_pages-1 and X_MENU-10 + LARGEUR_MENU < x < X_MENU+40 + LARGEUR_MENU and Y_MENU+TAILLE < y < Y_MENU+TAILLE+40:
                PAGE += 1
                affiche_page(PAGE)
                continue
            # Sélection tuile
            for idx, (x1, y1, x2, y2, tuile) in enumerate(positions):
                if x1 <= x <= x2 and y1 <= y <= y2:
                    # Efface le menu
                    for idx2 in range(NB_PAR_PAGE):
                        fltk.efface(f"sousmenu_{idx2}")
                    fltk.efface("menu_carre")
                    fltk.efface("menu_carre_border")
                    fltk.efface("menu_message")
                    return tuile
        elif tev == "Touche":
            touche = fltk.touche(ev)
            if touche == "Escape":
                for idx in range(NB_PAR_PAGE):
                    fltk.efface(f"sousmenu_{idx}")
                fltk.efface("menu_carre")
                fltk.efface("menu_carre_border")
                fltk.efface("menu_message")
                return None
            elif touche == "i":
                if menu_visible:
                    for idx in range(NB_PAR_PAGE):
                        fltk.efface(f"sousmenu_{idx}")
                    fltk.efface("menu_carre")
                    fltk.efface("menu_carre_border")
                    fltk.efface("menu_message")
                    menu_visible = False
                else:
                    affiche_page(PAGE)
                    menu_visible = True
            elif touche == "Right" and PAGE < nb_pages-1:
                PAGE += 1
                affiche_page(PAGE)
            elif touche == "Left" and PAGE > 0:
                PAGE -= 1
                affiche_page(PAGE)


def affiche_etat_visuel(etat_visuel: Dict[str, bool]) -> None:
    """
    Affiche un rond vert (ON) ou rouge (OFF) en haut à droite selon l'état du solveur visuel.
    """
    fltk.efface("etat_visuel")
    x, y, r = 720, 30, 15  # position et rayon du rond
    couleur = "green" if etat_visuel["visuel_actif"] else "red"
    fltk.cercle(x, y, r, couleur=couleur, remplissage=couleur, epaisseur=2, tag="etat_visuel")
    fltk.texte(x, y + 25, "Anim.", ancrage="center", taille=12, couleur="black", tag="etat_visuel") 
#####################################################################################   

################################# SOLVEUR ###########################################

def choisit_case_vide_slv1(grille):
    """
    Prend la première case vide selon le sens de lecture
    occidental (gauche à droite et haut en bas) afin de 
    faire l'algorithme de backtracking dessus.
    
    Args :
        grille (list) : liste de listes représentant le tableau 10x10 de base
    
    Retours :
        indice_ligne, indice_case (int) : coordonnées de la case choisie
    """
    
    emplacement = None
    for indice_ligne, ligne in enumerate(grille) :
        for indice_case, case in enumerate(ligne) :
            if case is None :
                return indice_ligne, indice_case # retourne la première case vide lors d'un parcours itératif

def solveur_n1_visuel(grille, dico) -> None :
    """
    # TODO : niveau 2 = prendre le dernier indice parcouru et lancer la recherche qu'à
                        partir de là
    Algorithme de backtracking, basé sur un parcours itératif
    pour trouver la première case vide sur laquelle baser l'algorithme.
    On choisit la case en parcourant la liste dans le sens de lecture occidental
    (i.e. de gauche à droite puis de haut en bas). La différence avec la fonction
    "solveur_n1" est que celle-ci affiche le processus de recherche fait pour chaque case.
    
    Args :
        grille (list) : liste de listes représentant le tableau 10x10 de base

        dico (dict) : dictionnaire contenant les chemins d'accès aux images
    
    Retours :
        None
    """
    if grille_remplie(grille) :
        fltk.mise_a_jour()
        return True
    else :
        i, j = choisit_case_vide_slv1(grille) # coordonnées de la première case vide
        liste_tuiles = tuiles_possibles(grille, i, j)
        random.shuffle(liste_tuiles)
        
        fltk.efface(f"case_{i}_{j}")

        for index, tuile in enumerate(liste_tuiles) :
            grille[i][j] = tuile # on ajoute une tuile dans la case vide
            
            chemin = renvoie_chemin(tuile, dico) # récupération du chemin dans l'arborescence
                    
            fltk.image(j * 75, i * 75, chemin, ancrage = "nw", largeur=75, hauteur=75, tag = f"case_{i}_{j}")
            

            if solveur_n1_visuel(grille, dico): #on lance la recherche récursive pour compléter la grilles
                return True
            else :
                grille[i][j] = None
        return 
    


def grille_remplie(grille : List[List[Optional[str]]]) -> bool :
    """
    Vérifie s'il reste au moins un None dans la matrice.
    
    
    Args :
        grille (list) : liste de listes représentant le tableau 10x10 de base
    
    Retours :
        bool : False si au moins un None est présent dans la matrice.
        
    """
    for ligne in grille :
        if not(all(ligne)) : # renvoie True si et seulement si chaque case est évaluée à True (donc non-vide)
            return False
    return True


def plus_contrainte(grille: List[List[Optional[str]]]) -> Tuple[int, int] :
    """
    Cherche dans la matrice la case vide avec le moins de 
    tuiles que l'on peut placer dessus. Ce système est basé sur la recherche 
    du Minimum Remaining Value, solution utilisée en Constraint
    Satisfaction Problems. 
    
    Args :
        grille (list) : matrice des tuiles
        
    Retours :
        i, j (int) : coordonnées de la case la plus contrainte

    """
    # on considère que la case la plus contrainte est la première
    plus_contrainte = float('inf') # toutes les cases ont un nombre fini de contraintes (donc inférieur à inf); pratique de fixer la limite haute à cette valeur

    coordonnees_plus_contrainte = (-1, -1) # pour l'instant, la case avec le plus de contraintes n'existe pas donc on la met hors-grille

    for i, ligne in enumerate(grille) :
        
        for j, case in enumerate(ligne) :
            
            nb_tuiles = len(tuiles_possibles(grille, i, j)) # on compte le nombre de tuiles dispo pour la case (i, j)
            
            if nb_tuiles < plus_contrainte and grille[i][j] is None: # on tombe sur une case vide plus contrainte que notre plus contrainte

                # on assigne donc la nouvelle MRV 
                plus_contrainte = nb_tuiles
                coordonnees_plus_contrainte = (i, j)
    return coordonnees_plus_contrainte



def solveur_n3_visuel(grille : List[List[Optional[str]]], dico : Dict[str, str], visuel=False) -> None :

    # NIVEAU 4 : PARAMETRE SUPPLEMENTAIRE POUR COMPTER LES CONTRAINTES ET NE REGARDER
        # QUE LES CONTRAINTES QUI SONT MODIFIEES 
    """
    On parcourt l'entièreté de la liste afin de trouver 
    la case la plus contrainte et on base notre 
    algorithme de backtracking dessus, à chaque itération
    du solveur. Ce système est basé sur la recherche 
    de la Minimum Remaining Value (RMV), solution utilisée en Constraint
    Satisfaction Problems.
    
    Args :
        grille (list) : matrice des tuiles

        dico (dict) : dictionnaire qui contient les noms des tuiles en clés et leurs chemins en valeurs

    Keyword Args :
        visuel (bool) : indique si le solveur doit afficher chaque étape ou non
        
    Retours :
        None    
    """
    if grille_remplie(grille) :
        if visuel is False :
            fltk.mise_a_jour()
        return True 

    else :
        i, j = plus_contrainte(grille) # on séléctionne la case la plus contrainte (étape 2)

        lst_tuiles = tuiles_possibles(grille, i, j) 

        fltk.efface(f"case_{i}_{j}")

        random.shuffle(lst_tuiles)
        
        for tuile in lst_tuiles :
            grille[i][j] = tuile

            chemin = renvoie_chemin(tuile, dico) # récupération du chemin dans l'arborescence
                    
            fltk.image(j * 75, i * 75, chemin, ancrage = "nw", largeur=75, hauteur=75, tag = f"case_{i}_{j}")
            
            if visuel :
                fltk.mise_a_jour()
            
            if solveur_n3_visuel(grille, dico, visuel= visuel): #on lance la recherche récursive pour compléter la grille
                return True
            else :
                grille[i][j] = None
        return False

def cases_voisins_changes(grille:List[List[Optional[str]]], i: int, j:int) -> List[Tuple[int, int]] :
    """
    Renvoie la liste des cases valides dont au moins un des quatres voisins a été modifié.

    Args :
        grille (list) : matrice représentative
        i, j (int) : coordonnées de la dernière case placée 

    Returns :
        list : liste des couples de coordonnées
    """
    voisins = [(i-1, j), (i, j+1), (i+1, j), (i, j-1)] # liste des coordonnées des tuiles voisines à la case modifiée

    nv_liste = []

    for voisin in voisins :
        i_voisin, j_voisin = voisin
        if voisin is not None and 0 <= i_voisin <= len(grille) and 0 <= j_voisin <= len(grille[0]) : # on vérifie que le voisin soit valide
            nv_liste.append(voisin)
    
    return nv_liste 


def plus_contrainte_v2(grille: List[List[Optional[str]]], liste_voisins : List[Tuple[int, int]]) -> Tuple[int, int] :
    """
    Cherche dans la matrice la case vide avec le moins de 
    tuiles que l'on peut placer dessus. Ce système est basé sur la recherche 
    du Minimum Remaining Value, solution utilisée en Constraint
    Satisfaction Problems. 
    
    Args :
        grille (list) : matrice des tuiles
        
    Retours :
        i, j (int) : coordonnées de la case la plus contrainte

    """
    # on considère que la case la plus contrainte est la première
    plus_contrainte = float('inf') # toutes les cases ont un nombre fini de contraintes (donc inférieur à inf); pratique de fixer la limite haute à cette valeur

    coordonnees_plus_contrainte = (-1, -1) # pour l'instant, la case avec le plus de contraintes n'existe pas donc on la met hors-grille


    for i, j in liste_voisins :
            
            nb_tuiles = len(tuiles_possibles(grille, i, j)) # on compte le nombre de tuiles dispo pour la case (i, j)
            
            if nb_tuiles < plus_contrainte and grille[i][j] is None: # on tombe sur une case vide plus contrainte que notre plus contrainte

                # on assigne donc la nouvelle MRV 
                plus_contrainte = nb_tuiles
                coordonnees_plus_contrainte = (i, j)
    return coordonnees_plus_contrainte

def show_case_contrainte(grille: List[List[Optional[str]]]) -> Tuple[str, str] :
    """
    L'assistant de conception affiche en direct quelle est la case vide
    la plus contrainte, qui sera en l'occurence entourée d'un cadre rouge.

    Args :
        grille (list) : matrice représentative

    Retours : 
        renvoie les coordonnées de la case la plus contrainte (pourrait 
        renvoyer None mais faire ceci économise un appel à 
        plus_contrainte() étant donné que la fonction est appelée
        dans assitant_conception(). )
    """

    fltk.efface("rectangle_contraint")

    i, j = plus_contrainte(grille)

    fltk.rectangle(j*75, i*75, (j+1)*75, (i+1)*75, couleur="red", epaisseur=2, tag="rectangle_contraint")

    return i, j


def assistant_conception(grille: List[List[Optional[str]]]) -> None :
    """
    Associé à la fonction show_case_contrainte(). 
    Si la case contrainte affichée en rouge n'a pas 
    de solutions, alors on considère que la carte ne peut plus être
    remplie et le solveur affiche un message d'alerte, qui se retirera
    une fois que la case pourra à nouveau être complétée.

    Args : 
        grille (list) : matrice représentative

    Retours :
        None
    """
    fltk.efface("aucune_tuile")
    i, j = show_case_contrainte(grille)

    nb_tuiles = len(tuiles_possibles(grille, i, j))

    if nb_tuiles == 0 :

        # AMELIORER L'APPARENCE DU MESSAGE D'ERREUR 

        fltk.rectangle(100, 100, 500, 300, couleur= "red", tag="aucune_tuile")


def solve_rivieres(grille: List[List[Optional[str]]]) -> None:
    """
    Algorithme similaire à la coloration de zone afin de
    créer des rivières réalistes. 
    Chaque rivière doit :
        - ne pas faire de boucles;
        - démarrer d'une montagne (ou hors de la carte);
        - Toute rivière doit terminer dans la mer (ou hors de la carte).
        - Une rivière peut rejoindre une autre rivière, mais 
            ne peut pas se séparer en deux.

    Args : 
        grille (list) : matrice représentative du tableau

    Retours :
        None
    """
    #     def chemins_profondeur(plateau, directions, deque):
    # fltk.attente(5)
    # while len(deque) != 0:
    #     i,j,old_i,old_j = deque.pop()

    #     if plateau[i][j] != "white":
    #         continue

    #     plateau[i][j] = "yellow"
    #     directions[i][j] = old_i,old_j
    #     affiche_plateau(plateau, maj = False)
    #     affiche_arbre(directions)
        
    #     for new_i,new_j in [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]:
    #         deque.append((new_i,new_j,i,j))

    







####################################################################################
    
def mapmaker() -> None :
    """
    Fonction principale qui gère tout le programme.

    Args :
        None
    Retours :
        None
    """
    grille = [[None for x in range(10)] for x in range(10)] # création d'une grille représentant les 10 par 10 cases de base 
    
# [['RBDP', 'PBSB', 'PRGB', 'DSDR', 'SHGS', 'GRRH', 'RRPR', 'MPPR', 'DHRP', 'GBDH'], ['DHPR', 'SSDH', 'GPGS', 'DSDP', 'GMGS', 'RPMM', 'PRMP', 'PBDR', 'RPGB', 'DHPP'], ['PRRR', 'DHRR', 'GRRH', 'DHPR', 'GRPH', 'MMMR', 'MRMM', 'DSDR', 'GRGS', 'PBDR'], ['RRGB', 'RPPR', 'RRRP', 'PMPR', 'PPMM', 'MMPP', 'MRMM', 'DHPR', 'GPRH', 'DHRP'], ['GMGS', 'PPMM', 'RBDP', 'PPGB', 'MFPP', 'PMPF', 'MMMM', 'PMMM', 'RPMM', 'RRPP'], ['GPPH', 'MPFP', 'DSDP', 'GPGS', 'PRRP', 'PBDR', 'MBSB', 'MBSB', 'MBSB', 'PRGB'], ['PMPP', 'FPMM', 'DSDP', 'GPGS', 'RRPP', 'DSDR', 'SHGS', 'SHFH', 'SSDH', 'GRGS'], ['PBDR', 'MBSB', 'DSSB', 'GBSS', 'PBSB', 'DSSB', 'GFGS', 'FPFF', 'DHRP', 'GRRH'], ['DSDR', 'SHGS', 'SHRH', 'SHPH', 'SHPH', 'SHPH', 'GPPH', 'FPPP', 'RPMP', 'RMPP'], ['DSSB', 'GMGS', 'RPPM', 'PFFP', 'PMMF', 'PRMM', 'PPMR', 'PMMP', 'MPMM', 'PFPP']]
    cree_UI()

    etat_visuel = {"visuel_actif" : False} # désactive par défaut l'affichage dynamique 
    affiche_etat_visuel(etat_visuel)
    while True :
        gere_clic_v1(grille, etat_visuel)


if __name__ == "__main__" :
    mapmaker()

    
