from shapefile import Reader
from fltk import cree_fenetre, polygone, mise_a_jour, attend_fermeture
from math import radians, cos, sin

shp = Reader("departements-20180101")

rotation_deg = -1

x1, y1, x2, y2 = shp.bbox
center_x = (x1 + x2) / 2
center_y = (y1 + y2) / 2

win_w, win_h = 1440, 720
cree_fenetre(win_w, win_h, redimension=True, affiche_repere=True)

zoom = 1
map_w = x2 - x1
map_h = y2 - y1
margin = 100
scale = (min((win_w - margin) / map_w, (win_h - margin) / map_h)) * zoom

theta = radians(rotation_deg)
c, s = cos(theta), sin(theta)

screen_cx = win_w / 2
screen_cy = win_h / 2

for shape in shp.shapes():
    pts = []
    for lon, lat in shape.points:
        dx = (lon - center_x) * cos(radians(center_y)) 
        dy = (lat - center_y)
        rx = dx * c - dy * s
        ry = dx * s + dy * c
        sx = rx * scale
        sy = -ry * scale

        screen_x = sx + screen_cx
        screen_y = sy + screen_cy
        pts.append((screen_x, screen_y))
    polygone(pts)

mise_a_jour()
attend_fermeture()
