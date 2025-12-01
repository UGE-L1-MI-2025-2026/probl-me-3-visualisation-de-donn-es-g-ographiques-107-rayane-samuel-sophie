from shapefile import *
from fltk import cree_fenetre, polygone, mise_a_jour, attend_fermeture
from math import radians, cos, sin

shp = Reader("departements-20180101-shp/departements-20180101.shp")

rotation_deg = -1

outres_mer = ["971", "972", "973","974", "975", "976", "977" "978", "984", "986", "987", "988", "989"]
lst = [1000,1000,-1000,-1000]
for i in range(len(lst)):
    for j in range(len(shp.shapes())):
        if shp.record(j)[0] not in outres_mer:
            if i < 2:
                if shp.shape(j).bbox[i] < lst[i]:
                    lst[i] = shp.shape(j).bbox[i]
            else:
                if shp.shape(j).bbox[i] > lst[i]:
                    lst[i] = shp.shape(j).bbox[i]

x1, y1, x2, y2 = lst[0], lst[1], lst[2], lst[3]
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
cp = 0




print(shp.records())
dsitance = []
lst1 = []
for shape in shp.shapes():
    if shp.record(cp)[0] not in outres_mer:
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
    cp += 1
for i in range (0):
    print('a')
mise_a_jour()
attend_fermeture()