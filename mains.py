from shapefile import Reader
from fltk import cree_fenetre, polygone, mise_a_jour, attend_fermeture
from App import Geo

cree_fenetre(1440, 720, affiche_repere=True)

geo = Geo()
geo.draw_map()