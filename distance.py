import osmnx as ox
import networkx as nx
import csv
from math import sin,cos,sqrt,atan2,radians

def position():
    ouvrir=open('velo-toulouse.csv','r')
    read=csv.reader(ouvrir,delimiter=",",lineterminator="\n")
    read.__next__()
    pos=[]
    for row in read:
        try:
            pos[int(row[4])]=(float(row[0]),float(row[1]))
        except:
            while len(pos)<=int(row[4]):
                pos.append((0,0))
            pos[int(row[4])]=(float(row[0]),float(row[1]))
    ouvrir.close()
    return pos

G=ox.graph_from_point((43.59933,1.43912),dist=10000,network_type='walk')
print("reseau construit, debut du traitement")
fichier='distance_dijkstra_walk.csv'
fichier_enr=open(fichier,'w')
enr=csv.writer(fichier_enr,delimiter=';',lineterminator='\n')
pos=position()
dist=[[],[]]
R=6371e3
point=[]
ini=0
while ini<len(pos):
    point.append(ox.get_nearest_edge(G,(pos[ini][0],pos[ini][1])))
    lat=[radians(pos[ini][1]),radians(G.nodes[point[ini][0]]['x'])]
    long=[radians(pos[ini][0]),radians(G.nodes[point[ini][0]]['y'])]
    delta_lat=lat[1]-lat[0]
    delta_long=long[1]-long[0]
    c1=(sin(delta_lat/2)**2)+cos(lat[0])*cos(lat[1])*(sin(delta_long/2)**2)
    c2=2*atan2(sqrt(c1),sqrt(1-c1))
    Dd0=R*c2
    dist[0].append(Dd0)
        
    lat=[radians(pos[ini][1]),radians(G.nodes[point[ini][1]]['x'])]
    long=[radians(pos[ini][0]),radians(G.nodes[point[ini][1]]['y'])]
    delta_lat=lat[1]-lat[0]
    delta_long=long[1]-long[0]
    c1=sin(delta_lat/2)**2+cos(lat[0])*cos(lat[1])*(sin(delta_long/2)**2)
    c2=2*atan2(sqrt(c1),sqrt(1-c1))
    Dd1=R*c2
    dist[1].append(Dd1)
    ini+=1
print('fin etape une')
ini=0
probleme=0
while ini<len(pos):
    val_enr=[]
    fin=0
    while fin<len(pos):
        distance=[]
        if ini!=fin:
            try:
                distance.append(nx.shortest_path_length(G,source=point[ini][0],target=point[fin][0],weight='length')+dist[0][ini]+dist[0][fin])
            except nx.NetworkXNoPath:
                probleme+=1
            try:
                distance.append(nx.shortest_path_length(G,source=point[ini][1],target=point[fin][0],weight='length')+dist[1][ini]+dist[0][fin])
            except nx.NetworkXNoPath:
                probleme+=1
            try:
                distance.append(nx.shortest_path_length(G,source=point[ini][0],target=point[fin][1],weight='length')+dist[0][ini]+dist[1][fin])
            except nx.NetworkXNoPath:
                probleme+=1
            try:
                distance.append(nx.shortest_path_length(G,source=point[ini][1],target=point[fin][1],weight='length')+dist[1][ini]+dist[1][fin])
            except nx.NetworkXNoPath:
                probleme+=1
        else:
            distance=[0]
        if distance!=[]:
            val_enr.append(min(distance))
        fin+=1
    enr.writerow(val_enr)
    ini+=1
print('fini')
fichier_enr.close()
