from shapefile import Reader
from fltk import cree_fenetre, polygone, mise_a_jour, attend_fermeture
from math import radians, cos, sin
import csv
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
        self.dict = {}
        self.departements_temp = {}
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
        print(len(self.dict))

        return self.center_x, self.center_y, self.scale, self.c, self.s
    
    
    def get_points(self):
        #Création d'une liste de points, séparant les îles des départements pour éviter illisibilité de la Carte
            for shape in self.shp.shapes():
                lst = []
                if self.shp.record(self.code_postal)[0] not in self.outres_mer:
                    if len(shape.parts) > 1:
                        for i in range(len(shape.parts)):
                            start = shape.parts[i]
                            if i + 1 < len(shape.parts):
                                end = shape.parts[i + 1]
                            else:
                                end = len(shape.points)
                            part_points = shape.points[start:end]
                            lst.append(part_points)
                    else:
                        lst.append(shape.points)
                    self.dict[self.shp.record(self.code_postal)[0]] = lst
                self.code_postal += 1
            return self.liste_points

    def draw_map(self):
        self.screen_cx = W / 2
        self.screen_cy = H / 2
        self.center_x, self.center_y, self.scale, self.c, self.s = self.get_values()
        self.open_file()
        for code in self.dict:
            points = self.dict[code]

            for shape in points:
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
                if code == '69D' or code == '69M':
                    code = '69'
                if self.departements_temp[code] >= 5:
                    polygone(pts, remplissage='green')
                elif self.departements_temp[code] < 10:
                    polygone(pts, remplissage='blue')
                else:
                    polygone(pts, remplissage='red')
        mise_a_jour()
        attend_fermeture()

    def open_file(self):
        ligne = 0
        clefs =[]   
        with open('departements-20180101-shp/temperature-quotidienne-departementale.csv', newline='') as csvfile:
            
            spamreader = csv.reader(csvfile,delimiter=';')
            dico = {}
            for row in spamreader:
                if ligne == 0:
                    for cle in row:
                        cle = cle.strip('\ufeff')
                        dico[cle]=[]
                        clefs.append(cle)
                else:
                    for i in range(len(row)):
                        dico[clefs[i]].append(row[i])
                ligne +=1
            i = 0
            for keys in dico['Code INSEE département']:
                if len(dico['TMoy (°C)'][i]) > 0:
                    self.departements_temp[keys] = round(float(dico['TMoy (°C)'][i]))

                i += 1

            print(i)
            print(self.departements_temp)
        