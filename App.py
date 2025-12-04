from shapefile import Reader
from fltk import cree_fenetre, polygone, mise_a_jour, attend_fermeture
from math import radians, cos, sin

W = 1440
H = 720
ZOOM = 1
MARGIN = 100

class Geo:
    def __init__(self):
        self.outres_mer = ["971", "972", "973","974", "975", "976", "977" "978", "984", "986", "987", "988", "989"]
        self.min_max = [1000,1000,-1000,-1000]
        self.rotation_deg = -1
        self.shp = Reader("departements-20180101-shp/departements-20180101.shp")
        self.center_x, self.center_y = 0, 0
        self.liste_points = []
        self.map_w, self.map_h, self.scale, self.theta, self.c, self.s, self.cx, self.cy, self.code_postal = 0, 0, 0, 0, 0, 0, 0, 0, 0
        
    def get_values(self):
    #Cacul de la bbox de la France métropolitaine
        for i in range(len(self.min_max)):
            for j in range(len(self.shp.shapes())):
                if self.shp.record(j)[0] not in self.outres_mer:
                    if i < 2:
                        if self.shp.shape(j).bbox[i] < self.min_max[i]:
                            self.min_max[i] = self.shp.shape(j).bbox[i]
                    else:
                        if self.shp.shape(j).bbox[i] > self.min_max[i]:
                            self.min_max[i] = self.shp.shape(j).bbox[i]

        #Cacul des dimensions à prendre pour cadrer la France métropoilitaine uniquement
        x1, y1, x2, y2 = self.min_max[0], self.min_max[1], self.min_max[2], self.min_max[3]

        self.center_x = (x1 + x2) / 2
        self.center_y = (y1 + y2) / 2

        self.map_w = x2 - x1
        self.map_h = y2 - y1

        #Calcul d'une échelle pour que la France ne dépasse pas sur les bord
        self.scale = (min((W - MARGIN) / self.map_w, (H - MARGIN) / self.map_h)) * ZOOM

        self.theta = radians(self.rotation_deg)
        self.c, self.s = cos(self.theta), sin(self.theta)
        self.get_points()

        return self.center_x, self.center_y, self.scale, self.c, self.s
    
    def get_points(self):
    #Création d'une liste de points, séparant les îles des départements pour éviter illisibilité de la Carte
        for shape in self.shp.shapes():
            if self.shp.record(self.code_postal)[0] not in self.outres_mer:
                if len(shape.parts) > 1:
                    not_iles = []
                    index_liste = []

                    for parts in shape.parts:
                        index_liste.append(int(parts))
                    for i in range (shape.parts[1]):
                        not_iles.append(shape.points[i])

                    self.liste_points.append(not_iles)
                    for elem in index_liste:
                        self.liste_points.append([shape.points[elem]])

                    not_iles = []
                    for i in range (index_liste[len(index_liste)-1], len(shape.points)-1):
                        not_iles.append(shape.points[i])
                else:
                    self.liste_points.append(shape.points)
            self.code_postal += 1
        return self.liste_points

    def draw_map(self):
        self.screen_cx = W / 2
        self.screen_cy = H / 2
        self.center_x, self.center_y, self.scale, self.c, self.s = self.get_values()

        for shape in self.liste_points:
            pts = []
            for lon, lat in shape:
                dx = (lon - self.center_x) * cos(radians(self.center_y)) 
                dy = (lat - self.center_y)
                rx = dx * self.c - dy * self.s
                ry = dx * self.s + dy * self.c
                sx = rx * self.scale
                sy = -ry * self.scale

                screen_x = sx + self.screen_cx
                screen_y = sy + self.screen_cy

                pts.append((screen_x, screen_y))
            polygone(pts)
        mise_a_jour()
        attend_fermeture()
