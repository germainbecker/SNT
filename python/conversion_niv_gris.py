# copiez votre fonction gris à partir de la ligne suivante (puis exécuter le code)


# programme pour appliquer le filtre à toute une image

from PIL import Image
im = Image.open("girl.jpg")
(L, H) = im.size
# on crée une nouvelle image de même définition
im_grise = Image.new("RGB", (L, H))

# on parcourt chaque pixel de coordonnées (x,y) de l'image de départ
for y in range(H):
    for x in range(L):
        pix = im.getpixel((x, y))  # on récupère ses composantes R, V et B
        R = pix[0]
        V = pix[1]
        B = pix[2]
        G = gris(R, V, B)  # on les convertit en nuance de gris avec la fonction "gris"
        im_grise.putpixel((x, y), (G, G, G))  # on crée un pixel avec cette nuance de gris

# on affiche l'image en niveaux de gris ainsi créée :
im_grise.show()
