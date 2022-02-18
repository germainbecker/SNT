'''
Module définissant des fonctions pour calculer les caractéristiques
d'un graphe définie par un dictionnaire associant à chaque sommet
une liste de ses voisins.
'''

# --- Distances d'un sommet aux autres ---
def distances_sommet(graphe, depart):
    """Renvoie les distances du sommet depart aux autres sommets du graphe"""
    visites = {depart: 0} # debut est à distance 0 de lui-même
    file = [depart]
    while len(file) > 0:
        s = file.pop(0)
        # (on ne marque plus les sommets non visités)
        for voisin in graphe[s]:
            if voisin not in visites:
                file.append(voisin)
                visites[voisin] = visites[s] + 1 # la distance est celle de s (d'où l'on vient) + 1
    return visites

# --- Écartement d'un sommet ---
def ecartement(graphe, s):
    """Renvoie l'écartement du sommet s dans graphe"""
    # on calcule les distances entre le sommet s et les autres sommets
    distances = distances_sommet(graphe, s)
    # l'écartement du sommet s est la distance maximale avec les autres sommets
    ecartement_graphe = max(distances.values())
    return ecartement_graphe

# --- Les écartements de chaque sommet ---
def sommets_ecartements(graphe):
    """Renvoie les écartements de chaque sommet du graphe"""
    ecartements = {sommet: ecartement(graphe, sommet) for sommet in graphe}
    return ecartements

# --- Rayon d'un graphe ---
def rayon(graphe):
    """Renvoie le rayon du graphe"""
    # le rayon est le minimum des écartements
    r = min(ecartement(graphe, sommet) for sommet in graphe)
    return r

# --- Centre d'un graphe ---
def centre(graphe):
    """Renvoie la liste des sommets du centre du graphe"""
    rayon_graphe = rayon(graphe)
    # le centre est l'ensemble des sommets du graphe dont l'écartement est égal au rayon
    centre_graphe = [sommet for sommet in graphe if ecartement(graphe, sommet) == rayon_graphe]
    return centre_graphe

# --- Diamètre d'un graphe ---
def diametre(graphe):
    """Renvoie le diamètre du graphe"""
    d = max(ecartement(graphe, sommet) for sommet in graphe)
    return d
