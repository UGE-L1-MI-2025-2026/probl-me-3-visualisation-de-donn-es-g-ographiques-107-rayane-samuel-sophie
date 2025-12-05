from fltk import *

cree_fenetre(1440, 720, redimension=True)
x_1 = 1400 
y_1 = 0
x_2 = 1439
y_2 = 18


r1 = 0
b1 = 255
v1 = 20


def conversion(x):
    x=hex(x)
    lettre=list(x)[2:]
    print(lettre)
    str(lettre)
    if len(lettre)==2:
        somme=lettre[0]+lettre[1]
    else:
        somme="0"+lettre[0]
        
    return somme

liste_couleur=[]
for i in range(40):
    couleur_hex = "#" + conversion(r1) + conversion(v1) + conversion(b1)
    liste_couleur.append(couleur_hex)
    r1 += 5
    b1 -= 5
    v1 += 5


print(liste_couleur)
for i in range(40):
    rectangle(x_1, y_1, x_2, y_2, couleur = liste_couleur[i], remplissage = liste_couleur[i])
    y_1 += 18
    y_2 += 18
    mise_a_jour()



attend_fermeture()
 


