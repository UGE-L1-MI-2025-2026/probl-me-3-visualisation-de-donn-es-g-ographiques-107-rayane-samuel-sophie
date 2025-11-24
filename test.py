from shapefile import * 
from fltk import *

shp = Reader("departements-20180101")
departements = []

x1,y1,x2,y2 = shp.bbox
offset_x = abs(x1)
offset_y = abs(y1)


cree_fenetre(500,500,redimension=True)
points = [((elem1+offset_x)*15, (elem2+offset_y)*15) for elem1, elem2 in shp.shape(1).points ]
polygone(points)
mise_a_jour()
attend_fermeture()
ferme_fenetre()
