# Mapmaker_project

how to use :
- barre espace pour activer le solveur 
- clic une fois pour ajouter une case aléatoire, deuxième clic sur l'image pour la supprimer
- v pour activer/désactiver l'aspect visuel du solveur
- flèches directionnelles pour le défilement infini
- rectangle rouge : case vide la plus contrainte
- grand rectangle rouge vide quand on place une tuile -> le solveur ne peut plus être complété et il faut retirer des tuiles (écran de warning à faire)
  
TODO : 
- faire le niveau 2 et 3 de la tâche 3 afin de mieux pouvoir sélectionner les cases
- enregistrement de la carte (dans son état partiel ou fini) ? 
- niveau 4 du solveur
- rivieres
- decors
- lundi de la rentrée -> amphi qui aidera pour les rivières
- améliorer l'apparence des messages d'erreurs (lignes 642 et 230 (peut-être) à vérifier)


Tâche 2 :
- vérification des raccords -> FAIT
- rivières naturelles -> PAS ENCORE FAIT
- décors ->  PAS ENCORE FAIT

tâche 3 :
  - tuile aléatoire -> FAIT
  - menu de sélection -> PAS ENCORE FAIT
  - menu de sélection déroulant -> PAS ENCORE FAIT 
 
tâche 4 :

 - AXE 1 :
    - niveau 3 : algorithme de la case la plus contrainte -> FAIT 
    - sélection efficace de la case la plus contrainte -> PAS ENCORE FAIT
-  AXE 2 :
    - niveau 1 : complétion automatique de la carte -> FAIT
    - niveau 2 : défilement infini -> FAIT 
    - niveau 3 : assistant de conception -> FAIT 


reste à faire pour les megatuiles : 
- gérer l'ajout aux fichiers
- trouver un moyen de détecter les appels aux fonctions megatuiles ( utilisr la menu d'affichage ?) trouver un moyen de tester avant que faid le fasse
- CREER UNE STRUCTURE DE DONNEES QUI CONTIENT LA TAILLE DES TUILES EN ATTENDANT DE FAIRE UNE FONCTION AVEC PIL (déterminer la taille de la tuile modulo 75)
- SI LE CLIC EST DANS UN COIN DIFFERENT DE HAUT GAUCHE, ADAPTER LA MANIERE DONT LA TUILE EST PLACEE
