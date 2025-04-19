import os
import fltk
import random
import time
import doctest
from typing import List, Dict, Tuple, Union, Optional

################################# GESTION DES FICHIERS ###########################################
def cree_dico() -> Dict[str, str] : 
    """
    Récupère l'ensemble des titres de chaque fichier image, stockés respectivement
    dans les dossiers "decors", "megatuile" et "tuiles" du dossier "fichiers fournis".
    Le programme et le dossier "fichiers fournis" doivent être stockés au même endroit de
    l'arborescence et chaque dossier contenant des images doit être stocké dans le dossier
    "fichiers fournis".
    
    Args :
        None
        
    Retours :
        dict : dictionnaire dont les clés sont les noms des tuiles et leurs valeurs
            des string représentant le chemin de la tuile à partir du dossier parent.
    """
    
    path = os.getcwd() # chemin actuel de l'arborescence
    fichiers_images = ("decors", "megatuile", "tuiles") #dossier contenant des tuiles
    
    dico_path = {}
    
#     for dossier in fichiers_images :
#         path_fichier = path + f"\\fichiers fournis\\{dossier}" # crée le bon path pour chaque dossier d'images
#         
#         for image in os.listdir(path_fichier) :
#             dico_path[image[:4]] = f"{dossier}\\{image}"
# Version with the Megatuile and the decors included

    path_fichier = path + "\\fichiers fournis\\tuiles"
    
    for tuile in os.listdir(path_fichier) :
        dico_path[tuile[:4]] = f"tuiles\\{tuile}"

    return dico_path

###################################################################################################

################################# PLACEMENT DES TUILES  ###########################################
def emplacement_valide(grille : List[List[Optional[int]]] , i:int, j:int, nom_tuile: str) -> bool :
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



def tuiles_possibles(grille: List[List[Optional[int]]], i: int, j:int) -> List[str] :
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
    fltk.cree_fenetre(750, 750, affiche_repere = True, redimension=False)


def gere_clic(grille: List[List[Optional[int]]]) -> None :
    """
    Gère un clic gauche de la souris sur la grille :
     Convertit les coordonnées en indices de case.
    Tente de placer une tuile aléatoire compatible.
     Affiche un message si aucune tuile n'est compatible.
     
     Args :
        grille (list) : tableau
         
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
                    
                    chemin = f"{os.getcwd()}\\fichiers fournis\\{dico[tuile]}" # récupération du chemin dans l'arborescence
                    
                    fltk.image(j * 75, i * 75, chemin, ancrage = "nw", largeur=75, hauteur=75, tag=tag_case)
                    
                else: # message d'erreur si aucune tuile n'est posable
                    rectangle_pb = fltk.rectangle(15, 15, 375, 80, remplissage="white", tag = "aucune_tuile")
                    texte_pb = fltk.texte(195, 45, "Aucune tuile compatible", ancrage="center", couleur="red", tag="aucune_tuile")

            
        else : # la case n'est pas vide donc il faut supprimer l'image à cet emplacement
            grille[i][j] = None # enlève la case de la matrice de représentation
            fltk.efface(tag_case) # efface la case avec les coordonnées (i, j)
            
    elif tev == "Touche":
        gere_clavier(grille, ev)
            
        fltk.mise_a_jour() # rafraîchit la page pour supprimer tout ce qui est nécessaire




def gere_clavier(grille: List[List[Optional[int]]], ev: tuple) -> None :
    """
    Gère les évènements clavier :
        l'utilisateur doit appuyer sur :
            - espace pour déclencher le solveur
            - les flèches clavier (haut, droite, bsa, gauche pour activer le défilement infini)
     
     Args :
         grille(list) : tableau
         
    Returns :
        None
    """
    touche = fltk.touche(ev)

    dico = cree_dico()
    
    if touche == "space": # gère le placement manuel des tuiles sur le tableau

        solveur_n3_visuel(grille, dico) # complète (si possible) la matrice
    


#     # FAIRE EN SORTE DE SUPPRIMER LES IMAGES DE LA FENETRE EN DELETANT LE TAG
#      IL FAUT DECALER UNE PAR UNE TOUTES LES IMAGES DE LA GRILLE 
#     if touche == "Up" :
#         ligne = grille.pop() # retire la première ligne du tableau
#         
#         i=1 # numéro de la ligne supprimée, constant
#         
#         for index, image in enumerate(ligne) :
#             fltk.efface
#             
#         solveur_n1_visuel(grille, dico) # complète (si possible) la matrice
#         
#     if touche == "Down":
#         grille.pop(-1)
#         solveur_n1_visuel(grille, dico) # complète (si possible) la matrice
#         
#     if touche == "Left" :
#         for ligne in grille :
#             ligne.pop()
#         solveur_n1_visuel(grille, dico) # complète (si possible) la matrice
#     
#     if touche == "Right" :
#         for ligne in grille :
#             ligne.pop(-1)
#         solveur_n1_visuel(grille, dico) # complète (si possible) la matrice
        
        
    fltk.mise_a_jour()

#####################################################################################   

################################# SOLVEUR ###########################################

def choisit_case_vide_slv1(grille: List[List[Optional[int]]]) -> Tuple[int, int]  :
    """
    Prend la première case vide afin de faire l'algorithme de backtracking
    dessus.
    
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



def grille_remplie(grille : List[List[Optional[int]]]) -> bool :
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



def solveur_n1(grille : List[List[Optional[int]]]) -> bool :
    """
    Algorithme de backtracking, basé sur un parcours itératif
    pour trouver la première case vide sur laquelle baser l'algorithme.
    On choisit la case en parcourant la liste dans le sens de lecture occidental
    (i.e. de gauche à droite puis de haut en bas).
    
    Args :
        grille (list) : liste de listes représentant le tableau 10x10 de base
    
    Retours :
        None
    """
    if grille_remplie(grille) :
        return True
    else :
        i, j = choisit_case_vide_slv1(grille) # coordonnées de la première case vide
        liste_tuiles = tuiles_possibles(grille, i, j)
        for tuile in liste_tuiles :
            
            grille[i][j] = tuile # on ajoute une tuile dans la case vide
            if solveur_n1(grille): #on lance la recherche récursive pour compléter la grille
                return True
            else :
                grille[i][j] = None
        return False
    
def affiche_cases_latentes(grille: List[List[Optional[int]]]) -> None :
    """
    upload les images sur la fenêtre mais ne les met
    à jour qu'à la fin du programme, afin que l'utilisateur
    ne voit pas le process.
    """
    
def solveur_n1_visuel(grille : List[List[Optional[int]]], dico: Dict[str, str]) -> None :
    """
    Algorithme de backtracking, basé sur un parcours itératif
    pour trouver la première case vide sur laquelle baser l'algorithme.
    On choisit la case en parcourant la liste dans le sens de lecture occidental
    (i.e. de gauche à droite puis de haut en bas).
    
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
        return False
    



def plus_contrainte(grille: List[List[Optional[int]]]) -> Tuple[int, int] :
    """
    Pour chaque étape du solving, on compte le nombre
    de tuiles disponibles pour chaque case vide. La case
    avec le moins de tuiles (i.e. la case la plus contrainte)
    est celle qui sera remplie. Ce système est basé sur la recherche 
    du Minimum Remaining Value, solution utilisée en Constraint
    Satisfaction Problems. 
    
    Args :
        grille (list) : matrice des tuiles
        
    Retours :
        i, j (int) : coordonnées de la case la plus contrainte

    """
    # on considère que la case la plus contrainte est la première
    plus_contrainte = float('inf') # toutes les cases ont un nombre fini de contraintes (donc inférieur à inf) 

    coordonnees_plus_contrainte = (-1, -1) # pour l'instant, la case avec le plus de contraintes n'existe pas donc on la met hors-grille


    for i, ligne in enumerate(grille) :
        
        for j, case in enumerate(ligne) :
            
            nb_tuiles = len(tuiles_possibles(grille, i, j)) # on compte le nombre de tuiles dispo pour la case (i, j)
            
            if nb_tuiles < plus_contrainte and grille[i][j] is None: # on tombe sur une case vide plus contrainte que notre plus contrainte

                # on assigne donc la nouvelle MRV 
                plus_contrainte = nb_tuiles
                coordonnees_plus_contrainte = (i, j)
    return coordonnees_plus_contrainte



def solveur_n3(grille: List[List[Optional[int]]]) -> None :
    """
    Pour chaque étape du solving, on compte le nombre
    de tuiles disponibles pour chaque case vide. La case
    avec le moins de tuiles (i.e. la case la plus contrainte)
    est celle qui sera remplie. Ce système est basé sur la recherche 
    du Minimum Remaining Value, solution utilisée en Constraint
    Satisfaction Problems.
    
    Args :
        grille (list) : matrice des tuiles
        
    Retours :
        None    
    """
    if grille_remplie(grille) :
        return True 

    else :
        i, j = plus_contrainte(grille) # on séléctionne la case la plus contrainte (étape 2)

        lst_tuiles = tuiles_possibles(grille, i, j) 

        for tuile in lst_tuiles :
            grille[i][j] = tuile

            if solveur_n3(grille): #on lance la recherche récursive pour compléter la grille
                return True
            else :
                grille[i][j] = None
        return False


def solveur_n3_visuel(grille : List[List[Optional[int]]], dico : Dict[str, str]) -> None :
    """
    Pour chaque étape du solving, on compte le nombre
    de tuiles disponibles pour chaque case vide. La case
    avec le moins de tuiles (i.e. la case la plus contrainte)
    est celle qui sera remplie. Ce système est basé sur la recherche 
    de la Minimum Remaining Value (RMV), solution utilisée en Constraint
    Satisfaction Problems 
    
    Args :
        grille (list) : matrice des tuiles

        dico (dict) : dictionnaire qui contient les noms des tuiles en clés et leurs chemins en valeurs
        
    Retours :
        None    
    """
    if grille_remplie(grille) :
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
            
            fltk.mise_a_jour()
            

            if solveur_n3_visuel(grille, dico): #on lance la recherche récursive pour compléter la grille
                return True
            else :
                grille[i][j] = None
        return False

def cases_inchangees(grille:List[List[Optional[int]]],     i: int, j:int) -> List[Tuple[int, int]] :
    """
    # TODO : vérifier comment la fonction marche dans le cas du backtracking qui modifie une case déjà placée 


    
    Fonction appelée dans le niveau 4 du solveur.
    Renvoie la liste dont les voisins n'ont pas été changées 
    et donc par définition, qui gardent le même niveau de
    contrainte. Les cases dont les voisins sont déjà 
    complétées sont considérées inchangées aussi.

    si 8 voisins tous non-vides ou tous vides -> append

    dans le solveur_n4, au lieu de rappeler la fonction pour connaître
    les cases inchangées, on supprime de la liste des cases inchangées 
    les cases voisines de la dernière case modifiée 

    Args :
        grille (list) : matrice

        # i, j (int) : coordonnées de la dernière tuile placée 

    Retours :
        list : liste de couples d'entiers représentant les coordonnées où ce n'est pas utile
                de checker la contrainte.
    """


    voisins = [(i-1, j), (i, j+1), (i+1, j), (i, j-1)]

    res = grille.copy() # on considère que la liste des cases inchangées vaut la matrice grille, puis on retire les voisins de la dernière case

    for voisin in voisins :
        if voisin is None : # on s'intéresse uniquement aux cases qui ne sont pas déjà placées, donc celles vides
            i_voisin, j_voisin = voisin
            del res[i_voisin][j_voisin] # on supprime cette case de la liste des cases inchangées 
    return res 








    

    












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
    while True :
        gere_clic(grille)


if __name__ == "__main__" :
    mapmaker()


    