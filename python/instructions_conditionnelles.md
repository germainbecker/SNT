# Instructions conditionnelles

Une instruction conditionnelle, ou instruction de test, permet de faire des choix en fonction de la valeur d’une condition. On parle souvent d’une instruction *si-alors*.

Une **condition** est une instruction qui est soit vraie, soit fausse. On dit qu'il s'agit d'un *booléen*.

Prenons un exemple simple : on souhaite afficher le vainqueur d'un match de football connaissant le score des deux équipes A et B . L'algorithme pourrait être :

```
si scoreA > scoreB
    alors afficher "L'équipe A a gagné !"
sinon si scoreA < scoreB
    alors afficher "L'équipe B a gagné !"
sinon
    afficher "Match nul !"
```

Dans cette exemple, il y a deux conditions `scoreA > scoreB` et `scoreA < scoreB` et chacune est soit vraie soit fausse. On voit bien qu'un choix (pour l'affichage dans notre cas) est effectué selon la valeur de ces conditions.

## Syntaxe en Python

Pour écrire des instructions conditionnelles en Python, il faut utiliser la syntaxe suivante :

```python
if condition1:
    instructions1 à effectuer
elif condition2:
    instructions 2 à effectuer
else:
    instructions 3 à effectuer
```

Les mots-clés `if`, `elif` (contraction de *else if*) et `else` sont les traductions respectives de `si`, `sinon si` et `sinon`

**Remarques importantes**

- Il ne faut **pas oublier les deux points** (`:`) à la fin des lignes avec `if`, `elif` et `else`

- Vous constatez que les lignes correspondant aux instructions à effectuer selon le cas sont écrites avec un "*décalage vers la droite*" : on parle d'**indentation**. Ces indentations sont obligatoires dans la syntaxe Python. Si vous n'oubliez pas les deux points et que vous passez à la ligne en appuyant sur la touche `Entrée` du clavier, l'indentation se fait automatiquement.

- Si vous devez ajouter vous-même une indentation, il faut utiliser la touche de tabulation : `Tab` (située au-dessus de la touche majuscule).

- Il peut y avoir plusieurs lignes d'instructions et elles doivent toutes êtres *indentées* (cela se fait automatiquement si rien n'a été oublié).

- Les mots clés `elif` et `else` sont optionnels, c'est-à-dire que l'on peut avoir seulement un `if` comme ceci :
  
  ```python
  if condition:
      instructions à effectuer    
  ```

Ceci étant dit, l'algorithme de départ donnant le vainqueur d'un match se traduit par le programme Python suivant.

```python
  if scoreA > scoreB:
    print("L'équipe A a gagné !")
  elif scoreA < score B:
    print("L'équipe B a gagné !")
  else:
    print("Match nul !")    
```

## A faire n°1

Regardez la vidéo suivante qui vous montre comment écrire et exécuter ce programme dans un éditeur Python.

## A faire n°2

Écrivez maintenant vous-même ce programme Python puis testez-le.


## A faire n°3

Ecrivez un programme Python qui demande à l'utilisateur sa moyenne au bac et qui affiche selon le cas, "Vous n'avez pas votre bac", "Vous avez votre bac" ou "Vous avez votre bac avec mention !".


