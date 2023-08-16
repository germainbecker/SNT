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
    # numéro de ligne appelant la fonction
    ligne = currentframe().f_back.f_lineno
    # mise à jour de la position actuelle
    alien['pos'] = {
        'x': alien['pos']['x'],
        'y': alien['pos']['y'] + n,
        'ligne': ligne,
        'etape': alien['pos']['etape'] + 1
    }
    # ajout de cette nouvelle position à la liste de toutes les positions
    alien['positions'].append(alien['pos'])
    
def bas(n=1):
    """
    Déplace l'alien de n cases vers le bas.
    Si n est négatif, le déplacement se fait de -n cases vers le haut.
    """
    if not isinstance(n, int):
        raise TypeError("Le paramètre de la fonction bas doit être un nombre entier.")
    ligne = currentframe().f_back.f_lineno
    alien['pos'] = {
        'x': alien['pos']['x'],
        'y': alien['pos']['y'] - n,
        'ligne': ligne,
        'etape': alien['pos']['etape'] + 1
    }
    alien['positions'].append(alien['pos'])

def gauche(n=1):
    """
    Déplace l'alien de n cases vers la gauche.
    Si n est négatif, le déplacement se fait de -n cases vers la droite.
    """
    if not isinstance(n, int):
        raise TypeError("Le paramètre de la fonction gauche doit être un nombre entier.")
    ligne = currentframe().f_back.f_lineno
    alien['pos'] = {
        'x': alien['pos']['x'] - n,
        'y': alien['pos']['y'],
        'ligne': ligne,
        'etape': alien['pos']['etape'] + 1
    }
    alien['positions'].append(alien['pos'])
    
def droite(n=1):
    """
    Déplace l'alien de n cases vers la droite.
    Si n est négatif, le déplacement se fait de -n cases vers la gauche.
    """
    if not isinstance(n, int):
        raise TypeError("Le paramètre de la fonction droite doit être un nombre entier.")
    ligne = currentframe().f_back.f_lineno
    alien['pos'] = {
        'x': alien['pos']['x'] + n,
        'y': alien['pos']['y'],
        'ligne': ligne,
        'etape': alien['pos']['etape'] + 1
    }
    alien['positions'].append(alien['pos'])


def afficher_deplacement(etapes=False, num_lignes=True, animation=False):
    """
    Affiche tout le déplacement à l'écran en appelant la fonction run().
    
    Paramètres
    ----------
    etapes
        booléen dont la valeur détermine si on affiche le numéro des étapes
        à côté de chaque position. Par défaut, ce n'est pas affiché.
    num_lignes
        booléen dont la valeur détermine si on affiche le numéro de la ligne
        du script à côté de chaque position. Par défaut, c'est affiché.
    animation
        booléen dont la valeur détermine si l'animation est lancée.
        L'animation consiste à pouvoir animer le déplacement de l'alien, avec
        un mode pas à pas possible.
        Par défaut, l'animation n'est pas lancée : on obtient le déplacement
        complet directement.
    """    
    if not etapes:
        alien['etapes'] = False
        alien['num_lignes'] = True
    else:
        alien['etapes'] = True
        alien['num_lignes'] = False
    if not num_lignes:
        alien['num_lignes'] = False
    else:
        alien['num_lignes'] = True
    
    if animation:
        alien['animation'] = True
    
    if alien['etapes']:
        print("Les nombres correspondent aux différentes étapes.")
        
    elif alien['num_lignes']:
        print("Les nombres correspondent aux numéros de lignes du programme.")
    run(preload=preload)  # lance les fonctions preload et setup (une fois) et draw (en boucle infinie)


def est_case_valide(case):
    """ Renvoie True si et seulement si case est valide (de "A1" à "O15"). """
    if not isinstance(case, str):
        raise TypeError("une case doit être une chaîne de caractères (ne pas oublier les guillemets)")
    assert len(case) >= 1, "case invalide"
    if (case[0].upper() not in LETTRES) or (int(case[1:]) not in NOMBRES):
        return False
    return True
  


def conversion_case_en_coordonnees(case):
    """ 
    Convertit une case en coordonnées.
    
    Paramètres
    ----------
    case
        chaine de caractères entre 'A1' et 'O15'
    
    Renvoie
    -------
    Une liste de deux éléments
    
    Exemples
    --------
    >>> conversion_case_en_coordonnees('H8')
    [0, 0]
    >>> conversion_case_en_coordonnees('F11')
    [3, 2]
    >>> conversion_case_en_coordonnees('A1')
    [-7, 7]
    """
    assert est_case_valide(case), "case non valide"
    lettre_choisie = case[0].upper()
    nb_choisi = int(case[1:])
    pos_lettre = LETTRES.index(lettre_choisie)
    coord = [nb_choisi - 8, 7 - pos_lettre]  # 7 est la position de la lettre H
    return coord

def conversion_coordonnees_en_case(x, y):
    """
    Convertit les coordonnées x, y en la bonne case.
    
    Exemples
    --------
    >>> conversion_coordonnees_en_case(0, 0)
    'H8'
    >>> conversion_coordonnees_en_case(-7, 7)
    'A1'
    """
    assert -7 <= x <= 7, "case inatteignable (en dehors de la grille)"
    assert -7 <= y <= 7, "case inatteignable (en dehors de la grille)"
    pos_lettre = 7 - y
    lettre = LETTRES[pos_lettre]
    nb = x + 8
    return lettre + str(nb)

def cases_du_parcours(positions=None):
    """
    Renvoie la liste des cases correspondant aux différentes positions 
    du parcours de l'alien.
    
    Paramètres
    ---------
    positions
        une liste de dictionnaires contenant les coordonnées de chaque position
    c
    Renvoie
    ------
    Une liste de cases (str) du parcours.
    
    Exemple
    -------
    >>> pos = [{'x': 0, 'y': 0}, {'x': 2, 'y': 0}, {'x': 2, 'y': -3}]
    >>> cases_du_parcours(pos)
    ['H8', 'H10', 'K10'] 
    """
    if positions == None:
        positions = alien['positions']
    liste_positions = [[p['x'], p['y']] for p in positions]
    liste_cases = [conversion_coordonnees_en_case(p[0], p[1]) for p in liste_positions]
    return liste_cases

def est_une_chaine_vide_ou_constituee_d_espace(chaine):
    """Renvoie True si et seulement si la chaine est vide ou constituée
    uniquement d'espaces."""
    if chaine == '':
        return True
    elif all(carac == ' ' for carac in chaine):
        return True
    return False

def compter_chaines_non_vides(liste_de_chaines):
    """
    Renvoie le nombre de chaînes de liste qui sont différentes de la chaîne vide
    ou d'une chaîne constituée uniquement d'espaces.
    
    Paramètres
    ----------
    liste_de_chaines
        une liste de chaînes de caractères
        
    Sortie
    ------
    Un entier positif ou nul
    """
    n = len(liste_de_chaines)
    c = 0
    for chaine in liste_de_chaines:
        if est_une_chaine_vide_ou_constituee_d_espace(chaine):
            c = c + 1
    return n - c

def creer_liste_sans_chaine_vide_ou_d_espaces_en_debut_et_fin(liste_de_chaines):
    """
    Crée une nouvelle liste mais sans les éléments 
    """
    return [chaine for chaine in liste_de_chaines if not est_une_chaine_vide_ou_constituee_d_espace(chaine)]

def nb_lignes_python_derniere_cellule_executee():
    """
    Analyse le programme écrit dans la dernière cellule exécutée par l'utilisateur.
    Renvoie un tuple dont le premier élément est la liste des lignes de la dernière 
    cellule exécutée et dont le second est le nombre de lignes contenant du code Python
    dans celle-ci.
    """
    # ligne d'appel à la fonction `verification_programme`
    # il faut revenir deux frames en arrière !
    ligne = currentframe().f_back.f_back.f_lineno
    
    # le code exécuté dans la dernière cellule
    programme_cellule = __main__.In[-1]
    # la liste avec les lignes de ce code jusqu'à l'appel à `verification_programme` (exclue)
    lignes_programme = programme_cellule.split('\n')[:ligne-1]
    
    # le nombre de lignes Python de la dernière cellule de code exécutée
    nb_lignes = compter_chaines_non_vides(lignes_programme)
    
    # la liste des lignes Python nettoyée au début et à la fin
    # (ne sert pas pour le moment : peut être utilisée pour récrire le code dans la fenêtre ou dans une image)
    lignes_programme_nettoyee = creer_liste_sans_chaine_vide_ou_d_espaces_en_debut_et_fin(lignes_programme)
    
    return nb_lignes

def verifier_programme(liste_bonnes_cases, nb_max_lignes=None, animation=False, etapes=True):
    """
    Vérifie si le programme écrit correspond au bon parcours `liste_bonnes_cases`,
    et éventuellement que le nombre de lignes ne dépasse `nb_max_lignes`. 
    
    Paramètres
    ----------
    liste_bonnes_cases
        une liste avec les cases du parcours
    nb_max_lignes
        un entier correspond au nombre maximal de lignes autorisé (optionnel)
    animation
        booléen dont la valeur détermine si l'animation est lancée.
        L'animation consiste à pouvoir animer le déplacement de l'alien, avec
        un mode pas à pas possible.
        Par défaut, l'animation n'est pas lancée : on obtient le déplacement
        complet directement.
    
    Si on utilise cette fonction, l'affichage des numéros de lignes est
    automatiquement désactivée car on ne dispose pas de ces numéros pour
    le parcours réponse.
    """
    # mise à jour des modalités du parcours
    alien['comparaison'] = True  # il y a une comparaison entre deux parcours
    if not animation:
        alien['deux_grilles'] = True  # deux grilles affichées si pas d'animation
    else:
        alien['deux_grilles'] = False  # sinon une seule grille
        alien['animation'] = True  # et une animation
    
    # nb de ligne de la dernière cellule exécutée    
    nb_lignes = nb_lignes_python_derniere_cellule_executee()
    
    # comparaison du programme proposé à la liste de cases attendue
    correct = liste_bonnes_cases == cases_du_parcours(alien['positions'])
    
    # test de la longueur du programme proposé
    if nb_max_lignes:  # si nb_max_lignes n'est pas None
        # comparaison de la longueur du prog proposé avec le nombre max de lignes attendu
        
        longueur = nb_lignes <= nb_max_lignes
    else:  # si la valeur associée à la clé `nb_max_lignes` est None
        longueur = True  
    
    # affichage de la correction
    if correct:
        #alien['comparaison'] = False
        if longueur:
            if alien['deux_grilles']:
                print("✅ Excellent !\n Ci-dessous à gauche votre déplacement et à droite celui qu'il faut obtenir.")
            else:
                print("✅ Excellent !\n Ci-dessous vous pouvez animer votre déplacement en bleu et vérifier qu'il correspond bien à celui attendu en blanc.")
        else:
            print(f"⚠️ Le parcours est bon mais votre programme fait {nb_lignes} lignes alors qu'il doit en faire au plus {nb_max_lignes}.")
            if alien['deux_grilles']:
                print("Ci-dessous à gauche votre déplacement et à droite celui qu'il faut obtenir.")
            else:
                print("Ci-dessous vous pouvez animer votre déplacement en bleu et le comparer à celui qu'il faut obtenir en blanc.")
    else:
        if alien['deux_grilles']:
            print("❌ C'est à revoir. Ci-dessous à gauche votre déplacement et à droite celui qu'il faut obtenir :")
        else:
            if alien['animation']:
                print("❌ C'est à revoir. Ci-dessous vous pouvez animer votre déplacement en bleu et le comparer au déplacement blanc qu'il faut obtenir :")
            else:
                print("❌ C'est à revoir. Ci-dessous votre déplacement.")
        #alien['comparaison'] = True
    creer_bonnes_positions_a_partir_listes_de_cases(liste_bonnes_cases)
    afficher_deplacement(etapes=etapes, num_lignes=False)  # OBLIGATOIREMENT num_lignes=False !!



def creer_bonnes_positions_a_partir_listes_de_cases(liste_cases):
    """
    Crée la liste des coordonnées à partir d'une liste de cases.
    Utilisé uniquement à la fin de la fonction `verification_programme` pour 
    créer les bonnes positions à partir d'une correction donnée dans le 
    dictionnaire `REPONSES_EXERCICES`
    """
    bonnes_positions = []
    for etape, case in enumerate(liste_cases):
        coord = conversion_case_en_coordonnees(case)
        bonnes_positions.append({'x': coord[0], 'y': coord[1], 'etape': etape})
    alien['bonnes_positions'] = bonnes_positions  # mise à jour du dictionnaire `alien`
    

####---- BOUTONS D'ANIMATIONS ----####

def dessiner_boutons_animation():
    """
    Dessine les boutons d'animation.
    Ne se positionnent pas bien selon la taille des cases.
    """
    fill(239)
    stroke(0)
    strokeWeight(1)
    for i in range(5):
        rect(75 * i + 45, alien['hauteur'] + 20, 65, 25, 2)

def ecrire_texte_boutons_animation():
    """
    Écrit le texte sur chaque bouton.
    """
    textSize(12)
    textFont('Consolas')
    noStroke()
    fill(20)
    textes = ["▶Lecture", "<< Début", " < Préc.", " Suiv. >", " Fin >>"]
    for i in range(5):
        text(textes[i], 75 * i + 50, alien['hauteur'] + 38)




#### ---- GESTION DES CLICS ---- ####
        
def survol_lecture(x, y):
    """ Renvoie True si les coordonnées (x, y) de la souris sont sur le bouton lecture. """
    return 45 <= x <= 45 + 60 and alien['hauteur'] + 20 <= y <= alien['hauteur'] + 45 

def survol_debut(x, y):
    """ Renvoie True si les coordonnées (x, y) de la souris sont sur le bouton début. """
    return 120 <= x <= 120 + 60 and alien['hauteur'] + 20 <= y <= alien['hauteur'] + 45 

def survol_reculer(x, y):
    """ Renvoie True si les coordonnées (x, y) de la souris sont sur le bouton reculer. """
    return 195 <= x <= 195 + 60 and alien['hauteur'] + 20 <= y <= alien['hauteur'] + 45

def survol_avancer(x, y):
    """ Renvoie True si les coordonnées (x, y) de la souris sont sur le bouton avancer. """
    return 270 <= x <= 270 + 60 and alien['hauteur'] + 20 <= y <= alien['hauteur'] + 45

def survol_fin(x, y):
    """ Renvoie True si les coordonnées (x, y) de la souris sont sur le bouton fin. """
    return 345 <= x <= 345 + 60 and alien['hauteur'] + 20 <= y <= alien['hauteur'] + 45

def demarrer_lecture():
    """
    (Re)démarre l'animation automatique.
    """
    if alien['etape'] < len(alien['positions']) - 1:
        alien['animation_en_cours'] = True
    else:
        alien['animation_en_cours'] = False

def debut():
    """
    Dessine l'alien à sa position de départ (et stoppe l'animation automatique).
    """
    alien['animation_en_cours'] = False
    alien['etape'] = 0  # première étape
    stroke(50)
    dessiner_grille()
    stroke(255)
    if alien['comparaison']:
        dessiner_deplacement(alien['bonnes_positions'], img=image_alien, num_grille=1)
        dessiner_deplacement(alien['positions'], img=image_alien2, etape_fin=alien['etape'], num_grille=1)
    else:
        dessiner_deplacement(alien['positions'], img=image_alien, etape_fin=alien['etape'], num_grille=1)
    
def reculer():
    """
    Recule l'alien d'une position (et stoppe l'animation automatique).
    """
    alien['animation_en_cours'] = False
    if alien['etape'] > 0:
        alien['etape'] = alien['etape'] - 1
        stroke(50)
        dessiner_grille()
        stroke(255)
        if alien['comparaison']:
            dessiner_deplacement(alien['bonnes_positions'], img=image_alien, num_grille=1)
            dessiner_deplacement(alien['positions'], img=image_alien2, etape_fin=alien['etape'], num_grille=1)
        else:
            dessiner_deplacement(alien['positions'], img=image_alien, etape_fin=alien['etape'], num_grille=1)
        
def avancer():
    """
    Avance l'alien d'une position (et stoppe l'animation automatique).
    """
    alien['animation_en_cours'] = False
    if alien['etape'] < len(alien['positions']) - 1:
        alien['etape'] = alien['etape'] + 1
        stroke(50)
        dessiner_grille()
        stroke(255)
        if alien['comparaison']:
            dessiner_deplacement(alien['bonnes_positions'], img=image_alien, num_grille=1)
            dessiner_deplacement(alien['positions'], img=image_alien2, etape_fin=alien['etape'], num_grille=1)
        else:
            dessiner_deplacement(alien['positions'], img=image_alien, etape_fin=alien['etape'], num_grille=1)

def fin():
    """
    Dessine l'alien à sa position finale (et stoppe l'animation automatique).
    """
    alien['animation_en_cours'] = False
    alien['etape'] = len(alien['positions']) - 1
    stroke(50)
    dessiner_grille()
    stroke(255)
    #strokeWeight(1)
    if alien['comparaison']:
        dessiner_deplacement(alien['bonnes_positions'], img=image_alien, num_grille=1)
        dessiner_deplacement(alien['positions'], img=image_alien2, etape_fin=alien['etape'], num_grille=1)
    else:
        dessiner_deplacement(alien['positions'], img=image_alien, etape_fin=alien['etape'], num_grille=1)


def gerer_animation_clic(x, y):
    """
    Détecte les clics sur les boutons et gère l'avancée de l'animation.
    """
    if mouseIsPressed and survol_lecture(x, y):
        demarrer_lecture()
    elif mouseIsPressed and survol_debut(x, y):
        debut()
        frameRate(3)  # POUR NE PAS DÉTECTER PLUSIEURS CLICS !!
    elif mouseIsPressed and survol_reculer(x, y):
        reculer()
        frameRate(3)
    elif mouseIsPressed and survol_avancer(x, y):
        avancer()
        frameRate(3)
    elif mouseIsPressed and survol_fin(x, y):
        fin()
        frameRate(3)
        



#### ---- ANIMATION ---- ####
        
def tester_fin_animation():
    """
    Teste si la dernière position du déplacement est atteinte.
    Sinon, itère d'une unité l'étape à afficher.
    """
    if alien['animation_en_cours'] and alien['etape'] == len(alien['positions']) - 1:
        alien['animation_en_cours'] = False
    else:
        alien['etape'] = alien['etape'] + 1

def animer():
    """
    Dessine l'alien à la position en cours.
    """
    if alien['comparaison']:
        dessiner_deplacement(alien['positions'], img=image_alien2, etape_fin=alien['etape'], num_grille=1)
    else:
        dessiner_deplacement(alien['positions'], img=image_alien, etape_fin=alien['etape'], num_grille=1)
    tester_fin_animation()
    frameRate(3)  # POUR NE PAS DÉTECTER PLUSIEURS CLICS !!
        
def taille(n=30):
    """
    Pour définir la taille d'une case en pixels.
    Ne pas choisir des valeurs trop petites ou trop grandes.
    """
    global TAILLE_CASE
    TAILLE_CASE = n



####---- TELECHARGER L'IMAGE DE LA FENETRE GRAPHIQUE ----####

def sauvegarder(nom_fichier=''):
    """
    Lance le téléchargement de la dernière fenêtre graphique.
    L'image est téléchargée au format PNG et porte le nom passé en paramètre
    sous forme d'une chaîne de caractères.
    """
    stop()
    save(nom_fichier)


####---- GESTION DU PARCOURS LIBRE ----####

def dessiner_parcours(indication=False):
    """
    Permet à l'utilisateur de dessiner le parcours de l'alien.
    """
    alien['parcours_libre'] = True
    alien['parcours_propose'] = [{'x': 0, 'y': 0, 'etape': 0}]
    alien['num_lignes'] = False  # OBLIGATOIRE
    alien['etapes'] = True
    alien['indication_parcours'] = indication
    print("Dessinez le parcours complet en cliquant sur les bonnes cases. Vous pouvez annuler la dernière position en cliquant dessus")
    run(preload=preload)


def coord_case_cliquee(x, y, taille_case):
    """ Renvoie les coordonnées de la case cliquée.
    ATTENTION ! x et y sont les coordonnées dans le repère (et non de la grille)"""
    return int(x//taille_case - 7), int(-y//taille_case + 8)


def gerer_clic_sur_grille(x, y):
    """Gère les clics sur la grille et le survol des boutons."""
    largeur = alien['largeur']
    hauteur = alien['hauteur']
    if mouseIsPressed and 0 <= x <= largeur and MARGE_HAUT <= y <= hauteur:
        # coordonnées de la case cliquée
        x_case, y_case = coord_case_cliquee(x, y, alien['taille_case'])
        # modification du parcours proposé
        modifier_parcours_propose(x_case, y_case)
        frameRate(3)
    if survol_btn_validation(x, y) or survol_btn_reinitialiser(x, y) or survol_btn_reponse(x, y):
        cursor('pointer')
    else:
        cursor(ARROW)


def modifier_parcours_propose(x_case, y_case):
    """Modifie le parcours proposé par l'utilisateur."""
    nb_etapes = len(alien['parcours_propose'])
    derniere_position = alien['parcours_propose'][-1]
    if (derniere_position['x'] == x_case) ^ (derniere_position['y'] == y_case):  # XOR
        alien['parcours_propose'].append({'x': x_case, 'y': y_case, 'etape': nb_etapes})
        stroke(50)
        strokeWeight(3)
        dessiner_grille()
    if derniere_position['x'] == x_case and derniere_position['y'] == y_case and len(alien['parcours_propose']) != 1:
        alien['parcours_propose'].pop()
        stroke(50)
        strokeWeight(3)
        dessiner_grille()


    
####---- GESTION DE LA SELECTION DE LA CASE FINALE ----####

def selectionner_case_finale():
    """
    Permet à l'utilisateur de sélectionner la case finale.
    """
    alien['selectionner_case'] = True
    print("Sélectionnez la case finale puis vérifiez votre réponse.")
    run(preload=preload)


def gerer_selection_case(x, y):
    """Pour gérer la sélection d'une case par un clic."""
    largeur = alien['largeur']
    hauteur = alien['hauteur']
    if mouseIsPressed and 0 <= x <= largeur and MARGE_HAUT <= y <= hauteur:
        # coordonnées de la case cliquée
        x_case, y_case = coord_case_cliquee(x, y, alien['taille_case'])
        marquer_case(x_case, y_case)


def marquer_case(x_case, y_case, correct=None):
    """
    Marque la case de coordonnées (x_case, y_case) dans la grille en dessinant
    un rectangle coloré sur ses contours.
    
    Parametres
    ----------
    x_case et y_case
        des entiers compris entre -7 et 7 correspondant aux coordonnées
        de la case dans la grille (coordonnées de la case centrale: (0, 0)).
    correct
        un booléen permettant de définir la couleur de la case
        (None : blanc, True: vert, False: rouge)
        
    """
    alien['case_selectionnee'] = (x_case, y_case)
    abs_centre = 7 * TAILLE_CASE
    ord_centre = MARGE_HAUT + 7 * TAILLE_CASE
    abscisse = abs_centre + x_case * TAILLE_CASE
    ordonnee = ord_centre - y_case * TAILLE_CASE

    stroke(50)
    strokeWeight(3)
    dessiner_grille()
    dessiner_alien(0, alien['positions'], img=image_alien, num_grille=1)

    if correct is None:
        stroke(255)  # en blanc
    elif correct == True:
        stroke(111, 196, 169)
    else:
        stroke(200, 0, 0)
    strokeWeight(5)
    noFill()  
    rect(abscisse , ordonnee, TAILLE_CASE)
    
    
####---- BOUTONS DESSIN LIBRE ----####

def dessiner_boutons_travail_autonome():
    """Dessine les boutons dans le cas où un parcours libre doit être construit."""
    dessiner_btn_validation()
    dessiner_btn_reinitialiser()
    dessiner_btn_reponse()

def dessiner_btn_validation():
    fill(239)
    stroke(0)
    strokeWeight(1)
    rect(2*alien['taille_case'], alien['hauteur'] + 15, 3*alien['taille_case'], 30)
    textSize(14)
    textFont('Consolas')
    noStroke()
    fill(20)
    text("Valider", 2*alien['taille_case'] + 17, alien['hauteur'] + 35)


def dessiner_btn_reinitialiser():
    fill(239)
    stroke(0)
    strokeWeight(1)
    rect(6*alien['taille_case'], alien['hauteur'] + 15, 3*alien['taille_case'], 30)
    textSize(14)
    textFont('Consolas')
    noStroke()
    fill(20)
    text("Effacer", 6*alien['taille_case'] + 16 , alien['hauteur'] + 35)
    

def dessiner_btn_reponse():
    fill(239)
    stroke(0)
    strokeWeight(1)
    rect(10*alien['taille_case'], alien['hauteur'] + 15, 3*alien['taille_case'], 30)
    textSize(14)
    textFont('Consolas')
    noStroke()
    fill(20)
    text("Réponse", 10*alien['taille_case'] + 16 , alien['hauteur'] + 35)

####---- GESTION DES BOUTONS -----####

# BOUTON DE VALIDATION

def survol_btn_validation(x, y):
    """ Renvoie True si les coordonnées (x, y) de la souris sont sur le bouton Valider. """
    abs_correcte = 2*alien['taille_case'] <= x <= 5*alien['taille_case']  # largeur = 3*alien['taille_case']
    ord_correcte = alien['hauteur'] + 15 <= y <= alien['hauteur'] + 15 + 30
    return abs_correcte and ord_correcte


def gerer_clic_btn_validation(x, y):
    """Teste si la case sélectionnée ou si le parcours proposé est correct
    lorsque l'utilisateur clique sur le bouton de validation."""
    if mouseIsPressed and survol_btn_validation(x, y):
        if alien['parcours_libre'] :  # cas d'un parcours à dessiner
            liste_bonnes_positions = [{'x': p['x'], 'y': p['y'], 'etape': p['etape']} for p in alien['positions']]
            if alien['parcours_propose'] == liste_bonnes_positions:
                print("✅ Excellent !")
                stop()
            elif alien['indication_parcours']:
                indice = comparer(alien['parcours_propose'], liste_bonnes_positions)
                if indice == "-":
                    print("❌ Le parcours proposé est incomplet, il manque des positions.")
                elif indice == "+":
                    print("❌ Le parcours proposé est trop long, il y a des positions en trop.")
                else:
                    print(f"❌ Le parcours proposé est incorrect, il y a un problème à partir de l'étape {indice + 1}.")
            else:
                print("❌ Le parcours proposé est incorrect.")
            frameRate(3)
        elif alien['selectionner_case']:  # cas de la case finale à sélectionner
            if alien['case_selectionnee'] is None:
                print("Vous devez sélectionner une case.")
            else:
                coord_case_finale = (alien['positions'][-1]['x'], alien['positions'][-1]['y'])
                if alien['case_selectionnee'] == coord_case_finale:

                    marquer_case(alien['case_selectionnee'][0], alien['case_selectionnee'][1], correct=True)
                    print("✅ Excellent !")
                    stop()
                else:
                    marquer_case(alien['case_selectionnee'][0], alien['case_selectionnee'][1], correct=False)
                    print("❌ C'est à revoir.")
            frameRate(3)
    

def comparer(liste_test, bonne_liste):
    """
    Renvoie -1 si les deux listes sont identiques.
    Sinon, renvoie :
        '-' si liste_test est le début de bonne_liste
        '+' si bonne_liste est le début de liste_test
        le premier indice i tel que liste_test[i] != bonne_liste[i], sinon.
    """
    if liste_test == bonne_liste:
        return -1
    n1 = len(liste_test)
    n2 = len(bonne_liste)
    n = min(n1, n2)  # n est la taille mini des deux listes
    i = 0
    while i < n:
        if liste_test[i] == bonne_liste[i]:
            i = i + 1
        else:
            break
    if i == n:  # si aucune différence sur les n premiers termes
        if n1 < n2:
            return '-'  # si liste_test est plus petite que bonne_liste
        else:
            return '+'  # si liste_test est plus grande que bonne_liste
    else:
        return i  # indice de la première différence

# BOUTON DE REINITIALISATION

def survol_btn_reinitialiser(x, y):
    """ Renvoie True si les coordonnées (x, y) de la souris sont sur le bouton Effacer. """
    abs_correcte = 6*alien['taille_case'] <= x <= 9*alien['taille_case']  # largeur = 3*alien['taille_case']
    ord_correcte = alien['hauteur'] + 15 <= y <= alien['hauteur'] + 15 + 30
    return abs_correcte and ord_correcte


def gerer_clic_btn_reinitialiser(x, y):
    """Réinitiatilise la case sélectionnée ou le parcours proposé 
    lorsque l'utilisateur clique sur le bouton de réinitialisation."""
    if mouseIsPressed and survol_btn_reinitialiser(x, y):
        if alien['parcours_libre'] :  # cas d'un parcours à dessiner
            alien['parcours_propose'] = [{'x': 0, 'y': 0, 'etape': 0}]
            stroke(50)
            strokeWeight(3)
            dessiner_grille()
            frameRate(3)
        elif alien['selectionner_case']:  # cas de la case finale à sélectionner
            alien['case_selectionnee'] = None
            stroke(50)
            strokeWeight(3)
            dessiner_grille()
            dessiner_alien(0, alien['positions'], img=image_alien, num_grille=1)
            frameRate(3)

# BOUTON DE REPONSE

def survol_btn_reponse(x, y):
    """ Renvoie True si les coordonnées (x, y) de la souris sont sur le bouton Reponse. """
    abs_correcte = 10*alien['taille_case'] <= x <= 13*alien['taille_case']  # largeur = 3*alien['taille_case']
    ord_correcte = alien['hauteur'] + 15 <= y <= alien['hauteur'] + 15 + 30
    return abs_correcte and ord_correcte


def gerer_clic_btn_reponse(x, y):
    """Affiche le bon déplacement et la case finale si l'utilisateur
    clique sur le bouton de réponse."""
    if mouseIsPressed and survol_btn_reponse(x, y):
        if alien['parcours_libre'] :  # cas d'un parcours à dessiner
            alien['parcours_libre'] = False
            
        elif alien['selectionner_case']:  # cas de la case finale à sélectionner
            alien['selectionner_case'] = False
            
        print("Voici la correction 👆")
        case_finale = conversion_coordonnees_en_case(alien['positions'][-1]['x'], alien['positions'][-1]['y'])
        print(f"La case finale était {case_finale}.")
        stroke(50)
        strokeWeight(3)
        dessiner_grille()
        dessiner_case_finale(num_grille=1)
        dessiner_deplacement(alien['positions'], img=image_alien, num_grille=1)
        stop()   



####---- FONCTIONS PRELOAD SETUP ET DRAW ----####
        
def preload():
    """ 
    Pour charger les deux images avant l'exécution de setup(). 
    La fonction run() doit alors préciser d'exécuter la fonction preload().
    """
    global image_alien, image_alien2
    image_alien = loadImage('https://raw.githubusercontent.com/germainbecker/SNT/master/Capytale/Python/alien_python/alien.svg')
    image_alien2 = loadImage('https://raw.githubusercontent.com/germainbecker/SNT/master/Capytale/Python/alien_python/alien2.svg')
    
def setup():
    """
    Fonction setup nécessaire au module p5.
    Définit tous les paramètres nécessaires à l'affichage et affiche 
    """
    # PARAMETRES ET CREATION DE LA FENETRE GRAPHIQUE
    if not alien['deux_grilles']:
        LARGEUR = TAILLE_CASE * 15
    else:
        LARGEUR = 2 * TAILLE_CASE * (15 + 1)
    if alien['animation'] or alien['parcours_libre'] or alien['selectionner_case']:
        HAUTEUR = TAILLE_CASE * 15 + MARGE_HAUT + MARGE_BAS
    else:
        HAUTEUR = TAILLE_CASE * 15 + MARGE_HAUT
    createCanvas(LARGEUR, HAUTEUR)
    textFont("Calibri")
    textSize(TAILLE_CASE // 3)
    
    
    # AFFICHAGES PRÉLIMINAIRES (ou définifs s'il n'y a pas d'animation)
    stroke(50)
    strokeWeight(3)
    if not alien['deux_grilles']:  # si une grille
        dessiner_grille()
        if alien['parcours_libre']:  #  pour dessiner le parcours avec la souris
            dessiner_deplacement(alien['parcours_propose'], img=image_alien, num_grille=1)
            dessiner_boutons_travail_autonome()
        elif alien['selectionner_case']:  #  pour sélectionner la case finale avec la souris
            dessiner_alien(0, alien['positions'], img=image_alien, num_grille=1)
            dessiner_boutons_travail_autonome()
        elif alien['comparaison']:
            # il y a nécessairement animation
            # on dessine le déplacement attendu
            dessiner_deplacement(alien['bonnes_positions'], img=image_alien, num_grille=1)
            # on dessine l'alien en position initiale (jusqu'à alien['etape'] qui vaut 1 initialement)
            dessiner_deplacement(alien['positions'], img=image_alien2, etape_fin=alien['etape'], num_grille=1)
            # on ajoute les boutons d'animations
            dessiner_boutons_animation()
            ecrire_texte_boutons_animation()
        elif alien['animation']:
            # on dessine l'alien en position initiale (jusqu'à alien['etape'] qui vaut 1 initialement)
            dessiner_deplacement(alien['positions'], img=image_alien, etape_fin=alien['etape'], num_grille=1)
            # on ajoute les boutons d'animations
            dessiner_boutons_animation()
            ecrire_texte_boutons_animation()
        else:
            dessiner_deplacement(alien['positions'], img=image_alien, num_grille=1)
            noLoop()
    else:  # si deux grilles
        # il y a nécessairement comparaison et pas d'animation !
        dessiner_grille()
        dessiner_grille(TAILLE_CASE*16, 0)  # deuxième grille
        dessiner_deplacement(alien['positions'], img=image_alien2, num_grille=1)
        dessiner_deplacement(alien['bonnes_positions'], img=image_alien, num_grille=2)
        noLoop()
    
def draw():
    """
    Fonction draw nécessaire au module p5.
    Actualise continuellement la fenêtre graphique.
    Ne sert qu'en cas d'animation.
    """
    frameRate(30)
    if alien['animation']:
        gerer_animation_clic(mouseX, mouseY)  # gestion clic sur boutons d'animations
        if alien['animation_en_cours']:
            animer()  # déplacement de l'alien
    if alien['parcours_libre']:
        gerer_clic_sur_grille(mouseX, mouseY)
        gerer_clic_btn_validation(mouseX, mouseY)
        gerer_clic_btn_reinitialiser(mouseX, mouseY)
        dessiner_deplacement(alien['parcours_propose'], img=image_alien, num_grille=1)
        gerer_clic_btn_reponse(mouseX, mouseY)
    if alien['selectionner_case']:
        gerer_selection_case(mouseX, mouseY)
        gerer_clic_btn_validation(mouseX, mouseY)
        gerer_clic_btn_reinitialiser(mouseX, mouseY)
        gerer_clic_btn_reponse(mouseX, mouseY)