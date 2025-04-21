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
    
    fichiers_images = ("megatuile", "tuiles") #dossier contenant des tuiles

    dico_path = {}

    path = os.getcwd() # chemin actuel de l'arborescence

    # for dossier in fichiers_images :
    #     path_fichier = path + f"\\fichiers fournis\\{dossier}" # crée le bon path pour chaque dossier d'images
        
    #     for image in os.listdir(path_fichier) :
    #         dico_path[image[:4]] = f"{dossier}\\{image}" # ajoute dans le dictionnaire la clé et la valeur correspondante

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
#     dico = cree_dico_intermediaire()

#     path = os.getcwd()
#     path_fichier = path + "\\fichiers fournis\\megatuile"

#     for megatuile in os.listdir(path_fichier) :
#         dico[megatuile[4:8]] = f"tuiles\\{megatuile}"


    return dico

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

# def emplacement_valide_mega(grille: List[List[Optional[str]]], *args) -> bool:
#     """
#     Vérifie si une tuile (classique ou mega) est valide à un emplacement donné.

#     - Tuile classique : emplacement_valide(grille, i, j, nom_tuile)
#     - MegaTuile  : emplacement_valide(grille, i, j, nom_tuile, hauteur, largeur)

#     """
#     if len(args) == 3:
#         i, j, nom_tuile = args 
#         hauteur, longeur = (1, 1) # les tuiles standard prennent 1x1 = 1 taille de case

#     elif len(args) == 5:
#         i, j, nom_tuile, hauteur, largeur = args # on fait le même procédé pour les megatuiles, qui prendront plus de cases

#     # Pour chaque case bordure de la zone (taille x taille)
#     # for di in range(hauteur):
#     #     for dj in range(longueur):
#     #         x, y= i + di, j + dj # on crée des nouvelles coordonnées par rapport au décalage en taille et en hauteur
#     #         voisins = [(x-1, y), (x, y+1), (x+1, y), (x, y-1)]

#     #         for index, (vx, vy) in enumerate(voisins):
#     #             if 0 <= vx < len(grille) and 0 <= vy < len(grille[0]):
#     #                 voisin = grille[vx][vy]
#     #                 if voisin is not None:
#     #                     indice_voisin = (index + 2) % 4
#     #                     if voisin[indice_voisin] != nom_tuile[index]:
#     #                         return False
#     # return True

#     for nb_largeur in range(hauteur) :
#         for nb_longueur in range(largeur) :



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

# def ajoute_megatuiles(grille: List[List[Optional[str]]], height_megatuile: int, width_megatuile: int, i_clic: int, j_clic:int) -> None :
#     """
#     Permet d'ajouter des megatuiles dans la fenêtre ainsi que dans la grille.
#     On calcule d'abord le nombre de cases nécessaires pour placer la megatuile,
#     puis on ajoute sur le bon nombre de cases la tuile dans la grille et dans la 
#     fenêtre. 

#     Args :
#         grille (list) : matrice représentative

#         height_megatuile (int) : hauteur de la megatuile

#         width_megatuile (int) : longueur de la megatuile

#         i_clic, j_clic (int) : coordonnées du clic dans le repère de la fenêtre (10x10 cases de 75px)
    
#     Retours :
#         None
#     """
#     height_dans_grille, width_dans_grille = height_megatuile//75, width_megatuile//75

#     cases_prises_j = [tuple(f"({i_clic}, {j_clic +x})") for x in range(width_dans_grille)]

#     cases_prises_i = [tuple(f"({i_clic +x}, {j_clic})") for x in range(height_dans_grille)]

#     # faire un try catch pour être sûr que cela rentre dans la grille

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
        
        
        if grille[i][j] is None: # process ajouter une case au tableau : vérifier si la case est vide, vérifier si bien placé -> place l'image
            if 0 <= i < len(grille) and 0 <= j < len(grille[0]) :  
                dico = cree_dico()
                compatibles = tuiles_possibles(grille, i, j)
    
                if compatibles:
                    tuile = random.choice(compatibles)  # On prend une case aléatoire parmi les voisins compatibles
                    
                    grille[i][j] = tuile # ajoute notre tuile à la matrice de représentation
                    
                    chemin = f"{os.getcwd()}\\fichiers fournis\\{dico[tuile]}" # récudpération du chemin dans l'arborescence
                    
                    fltk.image(j * 75, i * 75, chemin, ancrage = "nw", largeur=75, hauteur=75, tag=tag_case)
                    
                else: # message d'erreur si aucune tuile n'est posable
                    rectangle_pb = fltk.rectangle(15, 15, 375, 80, remplissage="white", tag = "aucune_tuile")
                    texte_pb = fltk.texte(195, 45, "Aucune tuile compatible", ancrage="center", couleur="red", tag="aucune_tuile")

            
        else : # la case n'est pas vide donc il faut supprimer l'image à cet emplacement
            grille[i][j] = None # enlève la case de la matrice de représentation
            fltk.efface(tag_case) # efface la case avec les coordonnées (i, j)
            
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

    elif touche == "space": # gère le placement manuel des tuiles sur le tableau
        solveur_n3_visuel(grille, dico, visuel= dico_etat_visuel["visuel_actif"]) # complète (si possible) la matrice


    elif touche in ["Up", "Left", "Down", "Right"] :
        decale_grille(grille, touche)
        clear_fenetre()
        fltk.mise_a_jour()
        affiche_nv_fenetre(grille, touche, dico)
        solveur_n1_visuel(grille, dico)


    elif touche == "c" :
        for i in range(10) :
            for j in range(10) :
                fltk.efface(f"case_{i}_{j}")
                grille[i][j] == None
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



def affiche_nv_fenetre(grille: List[List[Optional[str]]], direction_scroll: str, dico_tuiles: Dict[str, str]) -> None :
    """

    après avoir décalé la grille dans la direction appropriée,
    et rendu la fenêtre vierge, 
    on peut replace chaque image dans la bonne nouvelle case.
    On supprimera les images qui sortent du champ dans une autre
    fonction.

    Args :
        direction_scroll (str) : reprend la valeur de la touche 
            pressée. Indique dans quelle direction décaler les images.

        dico_tuiles (dict) : dictionnaire contenant tous les chemins
    Retours : 
        None
    """

    path_dossier_tuiles = os.getcwd() + "\\fichiers fournis\\"

    for i in range(len(grille)):
        for j in range(len(grille[0])):

            tuile = grille[i][j] 

            if tuile:  # si la tuile est None, on ne l'affiche pas -> évite de faire des disjonctions de cas

                fltk.image(j*75, i*75, path_dossier_tuiles + dico_tuiles[tuile],
                           ancrage="nw", hauteur=75, largeur=75, tag=f"case_{i}_{j}")

                

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
        return True
    else :
        i, j = choisit_case_vide_slv1(grille) # coordonnées de la première case vide
        liste_tuiles = tuiles_possibles(grille, i, j)
        random.shuffle(liste_tuiles)
        
        fltk.efface(f"case_{i}_{j}")

        for index, tuile in enumerate(liste_tuiles) :
            grille[i][j] = tuile # on ajoute une tuile dans la case vide
            
            chemin = f"{os.getcwd()}\\fichiers fournis\\{dico[tuile]}" # récupération du chemin dans l'arborescence
                    
            fltk.image(j * 75, i * 75, chemin, ancrage = "nw", largeur=75, hauteur=75, tag = f"case_{i}_{j}")
            
            fltk.mise_a_jour()
            
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
        for case in ligne :
            if case is None :
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
    """
    On parcourt l'entièreté de la liste afin de trouver 
    la case la plus contrainte et on base notre 
    algorithme de backtracking dessus, à chaque itération
    du solveur. Ce système est basé sur la recherche 
    de la Minimum Remaining Value (RMV), solution utilisée en Constraint
    Satisfaction Problems. La différence avec la fonction "solveur_n3" est 
    que celle-ci affiche toutes les étapes une par une de la création de la 
    carte.
    
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

            chemin = f"{os.getcwd()}\\fichiers fournis\\{dico[tuile]}" # récupération du chemin dans l'arborescence
                    
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
    
#     grille_test = [["PFMP", "HFHS" , None ],[None    , None , None ],[None    , None , None ]]

    cree_UI()

    etat_visuel = {"visuel_actif" : False} # désactive par défaut l'affichage dynamique 
    while True :
        gere_clic_v1(grille, etat_visuel)


if __name__ == "__main__" :
    mapmaker()



    
