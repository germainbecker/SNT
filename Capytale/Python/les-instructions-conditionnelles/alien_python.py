"""
Module permettant d'écrire des programmes déplaçant un alien dans une grille.
Adaptation du travail de Mathieu Degrange (https://github.com/DegrangeM/alien-python)

Auteur : Germain BECKER
Licence : CC BY-NC-SA

//!\\ ATTENTION
Ce module ne fonctionne qu'avec Basthon et donc aussi sur Capytale.
En effet, il est basé sur le module p5 porté dans Basthon par Romain Casati, module
lui-même basé sur la bibliothèque JavaScript p5.js (qui diffère du module p5 que l'on
peut obtenir avec la commande pip install p5).
"""

from p5 import *
from inspect import currentframe
import __main__

# Variables partagées
TAILLE_CASE = 30
MARGE_HAUT = 5
MARGE_BAS = 50
LETTRES = "ABCDEFGHIJKLMNO"
NOMBRES = [n for n in range(1, 16)]
alien = {
    'taille_case': TAILLE_CASE,
    'largeur': TAILLE_CASE * 15,
    'hauteur': TAILLE_CASE * 15 + MARGE_HAUT,
    'pos': {'x': 0, 'y': 0, 'ligne': 0, 'etape': 0},
    'positions': [{'x': 0, 'y': 0, 'ligne': 0, 'etape': 0}],
    'num_lignes': True,
    'etapes': False,
    'comparaison': False,
    'bonnes_positions': [],
    'coord_repere_animation': [(0, 0)],
    'coord_fenetre_animation': [],
    'etape': 0,
    'animation': False,
    'animation_en_cours': False,
    'deux_grilles': False,
    'canvas_id': None,
    'parcours_libre': False,
    'parcours_propose': [{'x': 0, 'y': 0, 'etape': 0}],
    'selectionner_case': False,
    'case_selectionnee': None,
    'indication_parcours': False
    
}

def dessiner_grille(x=0, y=0):
    """
    Dessine la grille complète.
    
    Paramètres
    ------
    x : abscisse du coin supérieur gauche
    y : ordonnée du coin supérieur gauche
    (utile pour dessiner deux grilles)
    """
    textFont("Calibri")
    strokeWeight(1)
    textSize(TAILLE_CASE // 3)
    for i in range(len(LETTRES)):
        for j in range(len(NOMBRES)):
            # couleur de la case
            if LETTRES[i] in ("A", "H", "O") or NOMBRES[j] in (1, 8, 15):
                fill(255, 166, 166)
            else:
                fill(255, 215, 215)
            # dessin de la case
            square(x + j * TAILLE_CASE , MARGE_HAUT + y + i * TAILLE_CASE, TAILLE_CASE)
            # écriture du numéro de la case
            num_case = LETTRES[i] + str(NOMBRES[j])
            fill(50)
            if NOMBRES[j] >= 10:
                text(num_case, x + j * TAILLE_CASE + TAILLE_CASE//4 , \
                 MARGE_HAUT + y + i * TAILLE_CASE + 2*TAILLE_CASE//3)
            else:
                text(num_case, x + j * TAILLE_CASE + TAILLE_CASE//3 , \
                 MARGE_HAUT + y + i * TAILLE_CASE + 2*TAILLE_CASE//3)

def dessiner_deplacement(positions, img, etape_fin=None, num_grille=1):
    """
    Dessine le déplacement de l'alien.
    
    Paramètres
    ----------
    positions
        une liste de dictionnaires contenant les différentes positions de l'alien
    img
        l'image de l'alien
    etape_fin
        un entier correspondant à l'étape finale souhaitée du déplacement
        Par exemple, si etape_fin = 3, le déplacement est dessiné des positions 0 à 3. 
        Vaut None par défaut : tout le déplacement est dessiné
    num_grille
        un entier (1 ou 2) correspondant à la grille dans laquelle l'alien est dessiné
        Par défaut, il est dessiné dans la grille 1
    """
    # Dessin de la première position
    dessiner_alien(0, positions, img, num_grille)
    # Écriture du numéro de ligne du script ou de l'étape du déplacement
    if not alien['etapes']:
        if alien['num_lignes']:
            ecrire_numero_ligne(0, positions, img, num_grille)
    else:
        ecrire_numero_etape(0, positions, img, num_grille)
    # Position finale souhaitée
    if etape_fin is not None:
        if etape_fin <= len(positions) - 2:
            position_finale = etape_fin
        else:
            position_finale = len(positions) - 1
    else:
        position_finale = len(positions) - 1
    # Dessin des positions suivantes
    for i in range(position_finale):
        dessiner_segment(i, positions, img, num_grille)
        dessiner_alien(i+1, positions, img, num_grille)            
        if not alien['etapes']:
            if alien['num_lignes']:
                ecrire_numero_ligne(i+1, positions, img, num_grille)
        else:
            ecrire_numero_etape(i+1, positions, img, num_grille)

def dessiner_case_finale(num_grille=1):
    """Marque la case finale"""
    if num_grille == 1:
        abs_centre = 7 * TAILLE_CASE
    elif num_grille == 2:
        abs_centre = 7 * TAILLE_CASE + 16 * TAILLE_CASE
    ord_centre = MARGE_HAUT + 7 * TAILLE_CASE
    abscisse = abs_centre + alien['positions'][-1]['x'] * TAILLE_CASE
    ordonnee = ord_centre - alien['positions'][-1]['y'] * TAILLE_CASE
    stroke(255)
    strokeWeight(5)
    noFill()
    rect(abscisse, ordonnee, TAILLE_CASE)
    
def dessiner_alien(i, positions, img, num_grille):
    """
    Dessine l'alien à l'étape i.
    
    Paramètres
    ----------
    i
        un entier égal à l'étape à dessiner
    positions
        une liste de dictionnaires contenant les différentes positions de l'alien
    img
        l'image de l'alien
    num_grille
        un entier (1 ou 2) correspondant à la grille dans laquelle l'alien est dessiné
    """
    if num_grille == 1:
        abs_centre = 7 * TAILLE_CASE
    elif num_grille == 2:
        abs_centre = 7 * TAILLE_CASE + 16 * TAILLE_CASE
    ord_centre = MARGE_HAUT + 7 * TAILLE_CASE
    abscisse = abs_centre + positions[i]['x'] * TAILLE_CASE
    ordonnee = ord_centre - positions[i]['y'] * TAILLE_CASE
    image(img, abscisse, ordonnee, TAILLE_CASE, TAILLE_CASE)
    

def dessiner_segment(i, positions, img, num_grille):
    """ Dessine le segment reliant les étapes i et i+1. """
    if num_grille == 1:
        abs_centre = 7 * TAILLE_CASE
    elif num_grille == 2:
        abs_centre = 7 * TAILLE_CASE + 16 * TAILLE_CASE
    ord_centre = MARGE_HAUT + 7 * TAILLE_CASE
    abs1 = abs_centre + positions[i]['x'] * TAILLE_CASE 
    ord1 = ord_centre - positions[i]['y'] * TAILLE_CASE
    abs2 = abs_centre + positions[i+1]['x'] * TAILLE_CASE 
    ord2 = ord_centre - positions[i+1]['y'] * TAILLE_CASE
    if img == image_alien:
        stroke(255)
    elif img == image_alien2:
        stroke(129, 185, 221)
    strokeWeight(3)
    line(abs1 + TAILLE_CASE // 2, ord1 + TAILLE_CASE // 2, abs2 + TAILLE_CASE // 2, ord2 + TAILLE_CASE // 2)

def ecrire_numero_ligne(i, positions, img, num_grille):
    """ Écrit à côté de l'alien le numéro de la ligne du script qui amène 
    l'alien à l'étape i. """
    if num_grille == 1:
        abs_centre = 7 * TAILLE_CASE
    elif num_grille == 2:
        abs_centre = 7 * TAILLE_CASE + 16 * TAILLE_CASE
    ord_centre = MARGE_HAUT + 7 * TAILLE_CASE
    abscisse = abs_centre + positions[i]['x'] * TAILLE_CASE 
    ordonnee = ord_centre - positions[i]['y'] * TAILLE_CASE
    stroke(255)
    strokeWeight(3)
    fill(0)
    textSize(TAILLE_CASE // 3 + 2)
    text(positions[i]['ligne'], abscisse + 3*TAILLE_CASE//4, ordonnee + TAILLE_CASE)

def ecrire_numero_etape(i, positions, img, num_grille):
    """ Écrit à côté de l'alien le numéro de l'étape i. 
    On numérote les étapes à partir de 1. """
    if num_grille == 1:
        abs_centre = 7 * TAILLE_CASE
    elif num_grille == 2:
        abs_centre = 7 * TAILLE_CASE + 16 * TAILLE_CASE
    ord_centre = MARGE_HAUT + 7 * TAILLE_CASE
    abscisse = abs_centre + positions[i]['x'] * TAILLE_CASE 
    ordonnee = ord_centre - positions[i]['y'] * TAILLE_CASE
    stroke(255)
    strokeWeight(3)
    fill(0)
    textSize(TAILLE_CASE // 3 + 2)
    text(positions[i]['etape'] + 1, abscisse + 3*TAILLE_CASE//4, ordonnee + TAILLE_CASE//4)
    
    
def centrer_alien():
    """ 
    Réinitialise un déplacement.
    
    //!\\ ATTENTION //!\\
    
    Doit obligatoirement être utilisée en première ligne d'un programme car
    réinitialise tout le dictionnaire correspondant au déplacement de l'alien.
    """
    alien['taille_case'] = TAILLE_CASE
    alien['hauteur'] = TAILLE_CASE * 15
    alien['largeur'] = TAILLE_CASE * 15 + MARGE_HAUT
    # on récupère le numéro de ligne appelant cette fonction
    ligne = currentframe().f_back.f_lineno
    alien['pos'] = {'x': 0, 'y': 0, 'ligne': ligne, 'etape': 0}
    alien['positions'] = [{'x': 0, 'y': 0, 'ligne': ligne, 'etape': 0}]
    alien['coord_repere_animation'] = [(0, 0)]
    alien['coord_fenetre_animation'] = []
    alien['comparaison'] = False
    alien['bonnes_positions'] = []
    alien['etape'] = 0
    alien['animation'] = False
    alien['animation_en_cours'] = False
    alien['deux_grilles'] = False
    alien['canvas_id'] = None
    alien['parcours_libre'] = False
    alien['parcours_propose'] = [{'x': 0, 'y': 0, 'etape': 0}]
    alien['selectionner_case'] = False
    alien['case_selectionnee'] = None
    alien['indication_parcours'] = False
    
def haut(n=1):
    """
    Déplace l'alien de n cases vers le haut.
    Si n est négatif, le déplacement se fait de -n cases vers le bas.
    """
    if not isinstance(n, int):
        raise TypeError("Le paramètre de la fonction haut doit être un nombre entier.")
    # numéro de ligne appelant la fonctio