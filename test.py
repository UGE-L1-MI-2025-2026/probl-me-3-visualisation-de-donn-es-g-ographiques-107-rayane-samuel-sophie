from shapefile import * 
from fltk import *
from math import *

shp = Reader("departements-20180101.shp")
departements = []

x1,y1,x2,y2 = shp.shape(43).bbox
centre  = ((x1+x2)/2, (x1+x2)/2+10)
point_centre_x = 960
point_centre_y = 540

def wgs84_to_mercator(liste_points):
    liste_points_convertis = []
    for x,y in liste_points:
        y = log(tan(radians(y)/2+pi/4))
        liste_points_convertis.append((x,y))
    return liste_points_convertis
        

def get_distances(origine,liste_points):        #Permet d'obtenir la distance entre un point d'origine et les points d'une liste 
    x1,y1 = origine
    liste_distance = []
    for x2,y2 in liste_points:
        liste_distance.append((x2-x1,y2-y1))
    return liste_distance

def resize(liste_distances,ratio):       #Permet de redimensionner la forme en multipliant la distance
    liste_distance_resized = []
    for distance_x, distance_y in liste_distances:
        distance_x = distance_x * ratio
        distance_y = distance_y * ratio 
        distance = (distance_x, distance_y)
        liste_distance_resized.append(distance)
    return liste_distance_resized

def rotate(liste_distances,angle):       #Permet de tourner la forme avec un angle donnée
    liste_distance_rotated = []
    for distance_x,distance_y in liste_distances:
        distance_x = distance_x * cos(angle)
        distance_y = distance_y * sin(angle)
        distance = (distance_x,distance_y)
        liste_distance_rotated.append(distance)
        
def offset_map(centre_ecran,liste_distances):
    liste_points_centre = []
    centre_ecran_x,centre_ecran_y = centre_ecran
    for x,y in liste_distances:
        x += centre_ecran_x
        y += centre_ecran_y
        liste_points_centre.append((x,y))
    return liste_points_centre


cree_fenetre(1920,1080)
for i in range(102):
    print(shp.record(i))
    points = [elem for elem in shp.shape(i).points ]
    distances = get_distances(centre, points)
    distances = resize(distances,10)
    points = offset_map((point_centre_x,point_centre_y),distances)
    
    polygone(points)

mise_a_jour()
attend_fermeture()
ferme_fenetre()
