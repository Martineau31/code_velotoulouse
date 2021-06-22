import numpy as np
import matplotlib.pyplot as plt
import csv
import networkx as nx
from outil_calcul import *
from import_export import *
import statistics as ss
from matplotlib.cm import ScalarMappable


def utilisation_graph(fichier=['test']):
    "permet d'afficher les graphique du temps en fonction du nombre d'usager\n en entrer mettre le nom d'un fichier du type .csv sans noter le .csv"
    #trace le graph
    x,valeur,place,y=utilisation_lecture(fichier)
    plt.figure(figsize=(15,12))
    if (len(valeur)==6) and (len(fichier)==1):
         plt.title('attendance graphic from '+valeur[0]+' to '+valeur[2])
    elif (len(valeur)!=6) and (len(fichier)==1):
        plt.title('graph de comparaison de fréquentation du '+valeur[0]+' au '+valeur[2]+" (positif) et du "+valeur[5]+" au "+valeur[7]+" (negatif)")
    a=0
    plt.xticks(place,y[0],rotation=60)
    plt.subplots_adjust(bottom=0.15)
    plt.grid(True)
    while (a<len(fichier)):
        plt.plot(x[a],label=fichier[a])
        a+=1
    plt.legend()
    plt.show()


def reseau(fichier='test'):
    "permet d'afficher le réseau a partir d'une matrice carrer\nl'entrer est le nom du fichier avec le tableau dedans"
    fichier+=".csv"
    ouvrir=open(fichier,'r')
    read=csv.reader(ouvrir,delimiter=";",lineterminator="\n")
    valeur=read.__next__()
    pas_temps=int(valeur[4])
    if len(valeur)==6:
        temps=conv_minute(valeur[0],valeur[1],valeur[5])
    else:
        temps_1=conv_minute(valeur[0],valeur[1],valeur[5])
        temps_2=conv_minute(valeur[6],valeur[8],valeur[11])
    pos=position()
    G=nx.DiGraph() #mettre DiGraph a la place de Graph pour avoir un graph orienter
    compteurpoint=0
    if len(valeur)==5:
        max_legende=5
        min_legende=1
    else:
        max_legende=0.01
        min_legende=-0.01
    premier=1
    couleur=[]
    for row in read:
        if row[0]!="\n":
            a=0
            while a<len(row):
                if premier:
                    G.add_node(a)
                if (float(row[a])!=0):
                    G.add_weighted_edges_from([(compteurpoint,a,float(row[a]))])
                    couleur.append(float(row[a]))
                    if float(row[a])>max_legende:
                        max_legende=float(row[a])
                    if (float(row[a])<min_legende) & (float(row[a])!=0):
                        min_legende=float(row[a])
                a+=1
            compteurpoint+=1
        if row[0]=="\n":
            if premier:
                premier=0
            plt.figure(figsize=(15,12))
            if len(valeur)==6:
                date,heure_debut,_=conv_date(temps,valeur[5]) #affichage du titre
                date,heure_fin,_=conv_date(temps+pas_temps,valeur[5])
                plt.suptitle("network of "+date+" from "+heure_debut+" to "+heure_fin)
                temps+=pas_temps
            else:
                date_1,heure_debut_1,_=conv_date(temps_1,valeur[5]) #affichage du titre
                date_1,heure_fin_1,_=conv_date(temps_1+pas_temps,valeur[5])
                date_2,heure_debut_2,_=conv_date(temps_2,valeur[11]) #affichage du titre
                date_2,heure_fin_2,_=conv_date(temps_2+pas_temps,valeur[11])
                plt.suptitle("reseau de comparaison du "+date_1+" (positif) et du "+date_2+" (negatif) de "+heure_debut_1+"  à "+heure_fin_1)
                temps_1+=pas_temps
                temps_2+=pas_temps
            option={'edge_cmap':plt.get_cmap('jet')}
            nc=nx.draw_networkx_edges(G,pos=pos,edge_color=couleur,edge_vmin=min_legende,edge_vmax=max_legende,arrows=False,ax=plt.axes(box_aspect=1),**option)
            color_bar=plt.colorbar(nc)
            color_bar.set_label("nombre of trips")
            nx.draw_networkx_nodes(G,pos=pos,node_size=15,node_color='black')
            G.clear_edges()
            compteurpoint=0
            couleur=[]
    plt.show()
    #ferme le fichier
    ouvrir.close()


def degree_reseau(fichier='test'):
    "permet d'afficher les degree par point d'un reseau a partir d'une matrice carrer\nl'entrer est le nom du fichier avec le tableau dedans"
    #ouverture du fichier
    fichier+=".csv"
    ouvrir=open(fichier,'r')
    read=csv.reader(ouvrir,delimiter=";",lineterminator="\n")
    #determination des variable d'enregistrement
    valeur=read.__next__()
    pas_temps=int(valeur[4])
    temps=conv_minute(valeur[0],valeur[1],valeur[5])
    pos=position()
    #création du graph vide
    G=nx.Graph()
    compteurpoint=0 #permet de savoir a quel point en est le code
    premier=1 #permet de créer tout les point dans les graph a la première itération
    max_degree=15 #permet de mettre une valeur max a la legende
    for row in read:
        if row[0]!="\n":
            a=0
            while a<len(row): #création du réseau
                if premier:
                    G.add_node(a)
                if (row[a]!="0"):
                    G.add_weighted_edges_from([(compteurpoint,a,float(row[a]))])
                a+=1
            compteurpoint+=1
        if row[0]=="\n": #affichage du graph quand on fini un bloc
            if premier:
                premier=0 #les point sont créer
            date,heure_debut,_=conv_date(temps,valeur[5]) #affichage du titre
            date,heure_fin,_=conv_date(temps+pas_temps,valeur[5])
            plt.figure(figsize=(15,12))
            plt.suptitle("degree of "+date+" from "+heure_debut+" to "+heure_fin)
            if max(np.array(G.degree())[:,1])>max_degree:
                max_degree=max(np.array(G.degree())[:,1])
            couleur=[]
            n_point=0
            while n_point<len(G):
                couleur.append(G.degree(n_point))
                n_point+=1
            #option du graph
            options={'cmap':plt.get_cmap('jet')}
            nc=nx.draw_networkx_nodes(G,pos=pos,node_color=couleur,node_size=20,vmin=0,vmax=max_degree,ax=plt.axes(box_aspect=1),**options)
            color_bar=plt.colorbar(nc)
            color_bar.set_label("point's degree")
            plt.pause(0.01)
            plt.clf() #netoye le graph
            G.clear_edges() #netoye les pond en gardant les point
            compteurpoint=0 #remise a zéro des station pour repartir
            temps+=pas_temps #changement de temps
    plt.show()
    #ferme le fichier
    ouvrir.close()


def degree_in_out_reseau(fichier='test'):
    "permet d'afficher les degree d'entrer et sorti par point d'un reseau a partir d'une matrice carrer\nl'entrer est le nom du fichier avec le tableau dedans"
    #ouverture du fichier
    fichier+=".csv"
    ouvrir=open(fichier,'r')
    read=csv.reader(ouvrir,delimiter=";",lineterminator="\n")
    #determination des variable d'enregistrement
    valeur=read.__next__()
    pas_temps=int(valeur[4])
    temps=conv_minute(valeur[0],valeur[1],valeur[5])
    pos=position()
    #création du graph vide
    G=nx.DiGraph()
    compteurpoint=0 #permet de savoir a quel point en est le code
    premier=1 #permet de créer tout les point dans les graph a la première itération
    max_degree=15 #permet de mettre une valeur max a la legende
    for row in read:
        if row[0]!="\n":
            a=0
            while a<len(row): #création du réseau
                if premier:
                    G.add_node(a)
                if (row[a]!="0"):
                    G.add_weighted_edges_from([(compteurpoint,a,float(row[a]))])
                a+=1
            compteurpoint+=1
        if row[0]=="\n": #affichage du graph quand on fini un bloc
            if premier:
                premier=0 #les point sont créer
            if max(np.array(G.degree())[:,1])>max_degree:
                max_degree=max(np.array(G.degree())[:,1])
            deg_in=[]
            deg_out=[]
            n_point=0
            while n_point<len(G):
                deg_in.append(G.in_degree(n_point))
                deg_out.append(G.out_degree(n_point))
                n_point+=1
            #option du graph
            options={'cmap':plt.get_cmap('jet')}
            date,heure_debut,_=conv_date(temps,valeur[5]) #affichage du titre
            date,heure_fin,_=conv_date(temps+pas_temps,valeur[5])
            plt.figure(figsize=(30,12))
            plt.suptitle("degrée du "+date+" de "+heure_debut+" à "+heure_fin)
            plt.subplot(121,aspect=1)
            nc_in=nx.draw_networkx_nodes(G,pos=pos,node_color=deg_in,node_size=20,vmin=0,vmax=max_degree,**options)
            color_bar_in=plt.colorbar(nc_in)
            color_bar_in.set_label("degree du point en entrer")
            plt.subplot(122,aspect=1)
            nc_out=nx.draw_networkx_nodes(G,pos=pos,node_color=deg_out,node_size=20,vmin=0,vmax=max_degree,**options)
            color_bar_out=plt.colorbar(nc_out)
            color_bar_out.set_label("degree du point en sorti")
            plt.pause(0.01)
            plt.clf() #netoye le graph
            G.clear_edges() #netoye les pond en gardant les point
            compteurpoint=0 #remise a zéro des station pour repartir
            temps+=pas_temps #changement de temps
    plt.show()
    #ferme le fichier
    ouvrir.close()


def clustering_reseau(fichier='test'):
    "permet d'afficher les clustering par point d'un reseau a partir d'une matrice carrer\nl'entrer est le nom du fichier avec le tableau dedans"
    #ouverture du fichier
    fichier+=".csv"
    ouvrir=open(fichier,'r')
    read=csv.reader(ouvrir,delimiter=";",lineterminator="\n")
    #determination des variable d'enregistrement
    valeur=read.__next__()
    pas_temps=int(valeur[4])
    temps=conv_minute(valeur[0],valeur[1],valeur[5])
    #création du graph vide
    pos=position()
    G=nx.DiGraph()
    compteurpoint=0 #permet de savoir a quel point en est le code
    premier=1 #permet de créer tout les point dans les graph a la première itération
    max_clustering=0.6 #permet de mettre une valeur max a la legende
    for row in read:
        if row[0]!="\n":
            a=0
            while a<len(row): #création du réseau
                if premier:
                    G.add_node(a)
                if (row[a]!="0"):
                    G.add_weighted_edges_from([(compteurpoint,a,float(row[a]))])
                a+=1
            compteurpoint+=1
        if row[0]=="\n": #affichage du graph quand on fini un bloc
            if premier:
                premier=0 #les point sont créer
            date,heure_debut,_=conv_date(temps,valeur[5]) #affichage du titre
            date,heure_fin,_=conv_date(temps+pas_temps,valeur[5])
            clustering=[]
            n_point=0
            while n_point<len(G):
                clustering.append(nx.clustering(G,n_point))
                if nx.clustering(G,n_point)>max_clustering:
                    max_clustering=nx.clustering(G,n_point)
                n_point+=1
            #option du graph
            options={'cmap':plt.get_cmap('jet')}
            plt.figure(figsize=(15,12))
            plt.suptitle("clustering du "+date+" de "+heure_debut+" à "+heure_fin)
            nc=nx.draw_networkx_nodes(G,pos=pos,node_color=clustering,node_size=20,vmin=0,vmax=max_clustering,ax=plt.axes(box_aspect=1),**options)
            color_bar=plt.colorbar(nc)
            color_bar.set_label("clustering du point")
            plt.pause(0.01)
            plt.clf() #netoye le graph
            G.clear_edges() #netoye les pond en gardant les point
            compteurpoint=0 #remise a zéro des station pour repartir
            temps+=pas_temps #changement de temps
    plt.show()
    #ferme le fichier
    ouvrir.close()


def centrality_clo_reseau(fichier='test'):
    "permet d'afficher la centralité de closeness par point d'un reseau a partir d'une matrice carrer\nl'entrer est le nom du fichier avec le tableau dedans"
    #ouverture du fichier
    fichier+=".csv"
    ouvrir=open(fichier,'r')
    read=csv.reader(ouvrir,delimiter=";",lineterminator="\n")
    #determination des variable d'enregistrement
    valeur=read.__next__()
    pas_temps=int(valeur[4])
    temps=conv_minute(valeur[0],valeur[1],valeur[5])
    #création du graph vide
    pos=position()
    G=nx.DiGraph()
    compteurpoint=0 #permet de savoir a quel point en est le code
    premier=1 #permet de créer tout les point dans les graph a la première itération
    max_closeness=0.01 #permet de mettre une valeur max a la legende
    for row in read:
        if row[0]!="\n":
            a=0
            while a<len(row): #création du réseau
                if premier:
                    G.add_node(a)
                if (row[a]!="0"):
                    G.add_weighted_edges_from([(compteurpoint,a,float(row[a]))])
                a+=1
            compteurpoint+=1
        if row[0]=="\n": #affichage du graph quand on fini un bloc
            if premier:
                premier=0 #les point sont créer
            date,heure_debut,_=conv_date(temps,valeur[5]) #affichage du titre
            date,heure_fin,_=conv_date(temps+pas_temps,valeur[5])
            closeness=[]
            n_point=0
            while n_point<len(G):
                closeness.append(nx.closeness_centrality(G,n_point))
                if nx.closeness_centrality(G,n_point)>max_closeness:
                    max_closeness=nx.closeness_centrality(G,n_point)
                n_point+=1
            #option du graph
            options={'cmap':plt.get_cmap('jet')}
            plt.figure(figsize=(15,12))
            plt.suptitle("centralité de closeness du "+date+" de "+heure_debut+" à "+heure_fin)
            nc=nx.draw_networkx_nodes(G,pos=pos,node_color=closeness,node_size=20,vmin=0,vmax=max_closeness,ax=plt.axes(box_aspect=1),**options)
            color_bar=plt.colorbar(nc)
            color_bar.set_label("centralité de closeness du point")
            plt.pause(0.01)
            plt.clf() #netoye le graph
            G.clear_edges() #netoye les pond en gardant les point
            compteurpoint=0 #remise a zéro des station pour repartir
            temps+=pas_temps #changement de temps
    plt.show()
    #ferme le fichier
    ouvrir.close()


def depl_crenau_graph(fichier='test_distance',pas_vitesse=1,pas_distance=100,pas_temps=1,pas_temps_graph=60*24):
    [val_vitesse,val_distance,val_temps],valeur=depl_crenau_lecture(fichier,pas_vitesse,pas_distance,pas_temps,pas_temps_graph)
    print('1:',len(val_vitesse),len(val_distance),len(val_temps))
    legende_vitesse=[]
    legende_temps=[]
    legende_distance=[]
    pas=int(valeur[4])
    while len(legende_distance)<len(val_distance[0]):
        legende_distance.append((len(legende_distance)+1)*pas_distance)
    while len(legende_temps)<len(val_temps[0]):
        legende_temps.append((len(legende_temps)+1)*pas_temps)
    while len(legende_vitesse)<len(val_vitesse[0]):
        legende_vitesse.append((len(legende_vitesse)+1)*pas_vitesse)
    print('2:',len(val_vitesse),len(val_distance),len(val_temps))
    a=0
    temps_graph=conv_minute(valeur[0],valeur[1],valeur[5])
    print('debut affichage')
    while a<len(val_vitesse):
        print(a, ': ',len(val_vitesse))
        date,heure_debut,_=conv_date(temps_graph,valeur[5]) #affichage du titre
        date,heure_fin,_=conv_date(temps_graph+pas,valeur[5])
        plt.figure(figsize=(15,12))
        plt.suptitle("distribution from "+valeur[0]+" to "+valeur[2]+" from "+heure_debut+" to "+heure_fin)
        plt.subplot(221)
        plt.grid(True)
        plt.title('distance distribution')
        plt.plot(legende_distance,val_distance[a])
        plt.xlabel('distance (m)')
        plt.ylabel('nombre of people')
        plt.subplot(222)
        plt.title('travel time distribution')
        plt.xlabel('time (min)')
        plt.ylabel('nombre of people')
        plt.grid(True)
        plt.plot(legende_temps,val_temps[a])
        plt.subplot(212)
        plt.title('speed distribution')
        plt.xlabel('speed (km/h)')
        plt.ylabel('nombre of people')
        plt.grid(True)
        plt.plot(legende_vitesse,val_vitesse[a])
        a+=1
        temps_graph+=pas
    plt.show()


def freq_graph(fichier='test_distance'):
    "permet de tracer la vitesse,distance et temps de trajet moyen et leur espérance en fonction du temps\nEn entrer le tableau des distance, temps et vitesse"
    #ouverture du fichier a tracer
    fichier+='.csv'
    lire=open(fichier,'r')
    read=csv.reader(lire,delimiter=";",lineterminator="\n")
    valeur=read.__next__()
    pas=int(valeur[4])
    nombre_legende=20
    intervalle=(conv_minute(valeur[2],valeur[3],valeur[5])-conv_minute(valeur[0],valeur[1],valeur[5]))//nombre_legende
    moy_distance=[] #moyenne
    moy_temps=[]
    moy_vitesse=[]
    ecart_inf_distance=[] #espérance supérieur
    ecart_inf_temps=[]
    ecart_inf_vitesse=[]
    ecart_sup_distance=[] #espérance inferieur
    ecart_sup_temps=[]
    ecart_sup_vitesse=[]
    for row in read:
        liste=[]
        a=0
        row=read.__next__()
        while a<len(row):
            liste.append(float(row[a]))
            a+=1
        try:
            moy_distance.append(ss.mean(liste))
            ecart_inf_distance.append(ss.mean(liste)-ss.pstdev(liste))
            ecart_sup_distance.append(ss.mean(liste)+ss.pstdev(liste))
        except ss.StatisticsError:
            moy_distance.append(0)
            ecart_inf_distance.append(0)
            ecart_sup_distance.append(0)
        row=read.__next__()
        liste=[]
        a=0
        while a<len(row):
            if abs(float(row[a]))<=4*60:
                liste.append(float(row[a]))
            a+=1
        try:
            moy_temps.append(ss.mean(liste))
            ecart_inf_temps.append(ss.mean(liste)-ss.pstdev(liste))
            ecart_sup_temps.append(ss.mean(liste)+ss.pstdev(liste))
        except ss.StatisticsError:
            moy_temps.append(0)
            ecart_inf_temps.append(0)
            ecart_sup_temps.append(0)
        row=read.__next__()
        liste=[]
        a=0
        while a<len(row):
            liste.append(float(row[a]))
            a+=1
        try:
            moy_vitesse.append(ss.mean(liste))
            ecart_inf_vitesse.append(ss.mean(liste)-ss.pstdev(liste))
            ecart_sup_vitesse.append(ss.mean(liste)+ss.pstdev(liste))
        except ss.StatisticsError:
            moy_vitesse.append(0)
            ecart_inf_vitesse.append(0)
            ecart_sup_vitesse.append(0)
    print('lecture fini')
    a=0
    distance_legende=len(moy_distance)//nombre_legende
    print(distance_legende)
    temps=conv_minute(valeur[0],valeur[1],valeur[5])
    place=[] #enregistrement des place des legende en x
    legende=[]
    while a*distance_legende<=len(moy_distance):
        date,heure,_=conv_date(temps,valeur[5])
        legende.append(date+" "+heure)
        place.append(a*distance_legende)
        temps+=pas*distance_legende
        a+=1
    plt.figure(figsize=(15,12))
    plt.suptitle("distribution from "+valeur[0]+" at "+valeur[1]+" to "+valeur[2]+" at "+valeur[3])
    plt.subplot(221)
    plt.grid(True)
    plt.title('distance statistics')
    plt.plot(moy_distance,label='mean')
    plt.plot(ecart_inf_distance,'+',label='lower standart deviation')
    plt.plot(ecart_sup_distance,'+',label='highter standart deviation')
    plt.xticks(place,legende,rotation=60,fontsize=8)
    plt.xlabel('date')
    plt.ylabel('distance (m)')
    plt.subplots_adjust(bottom=0.15)
    plt.legend()
    plt.subplot(222)
    plt.grid(True)
    plt.title('time statistics')
    plt.plot(moy_temps,label='mean')
    plt.plot(ecart_inf_temps,'+',label='lower standart deviation')
    plt.plot(ecart_sup_temps,'+',label='highter standart deviation')
    plt.xticks(place,legende,rotation=60,size=8)
    plt.ylabel('time (min)')
    plt.subplots_adjust(bottom=0.15)
    plt.legend()
    plt.subplot(212)
    plt.grid(True)
    plt.title('Speed')
    plt.plot(moy_vitesse,label='mean')
    plt.plot(ecart_inf_vitesse,'+',label='lower standart deviation')
    plt.plot(ecart_sup_vitesse,'+',label='highter standart deviation')
    plt.xticks(place,legende,rotation=60)
    plt.ylabel('speed (km/h)')
    plt.subplots_adjust(bottom=0.15)
    plt.legend()
    plt.show()
    #ferme le fichier
    lire.close()


def trajet_vitesse_graph(fichier='test_distance',choix_station=[],trier_anormal=None,trier_normal=None):
    "affiche les graphique baton des arriver au station en fonction des vitesse\nen entrer tableau de deplacement_chro"
    fichier+='.csv'
    lire=open(fichier,'r')
    read=csv.reader(lire,delimiter=";",lineterminator="\n")
    valeur=read.__next__()
    pas=int(valeur[4])
    station=[]
    for row in read:
        depart=[]
        arriver=[]
        a=0
        while a<len(row):
            b=0
            dep=''
            while row[a][b]!=">":
                dep+=row[a][b]
                b+=1
            arr=int(row[a][b+1::])
            depart.append(int(dep))
            arriver.append(int(arr))
            a+=1
        read.__next__()
        read.__next__()
        row=read.__next__()
        a=0
        while a<len(depart):
            try:
                station[depart[a]][arriver[a]].append(float(row[a]))
            except:
                while len(station)<=depart[a]:
                    station.append([])
                while len(station[depart[a]])<=arriver[a]:
                    station[depart[a]].append([])
                station[depart[a]][arriver[a]].append(float(row[a]))
            a+=1
    legende=[]
    legende_titre=[]
    a=0
    while a<len(station):
        b=0
        legende.append([])
        legende_titre.append(str(a))
        while b<len(station[a]):
            legende[a].append(str(b))
            b+=1
        a+=1
    a=0
    while a<len(station):
        auga=1
        if station[a]!=[]:
            b=0
            while b<len(station[a]):
                augb=1
                if station[a][b]!=[]:
                    c=0
                    while c<len(station[a][b]):
                        augc=1
                        if station[a][b][c]==0:
                            del station[a][b][c]
                            augc=0
                        if augc:
                            c+=1
                if station[a][b]==[]:
                    del station[a][b]
                    del legende[a][b]
                    augb=0
                if augb:
                    b+=1
        if station[a]==[]:
            del station[a]
            del legende[a]
            del legende_titre[a]
            auga=0
        if auga:
            a+=1
    a=0
    if choix_station==[]: #deplacer
        choix_station=legende_titre
    c=0
    a=0
    moy=[]
    couleur=[]
    ec=[]
    while a<len(station):
        moy.append([])
        couleur.append([])
        ec.append([])
        b=0
        while b<len(station[a]):
            #try:
            moy[a].append(ss.mean(station[a][b]))
            ec[a].append(ss.pstdev(station[a][b]))
            couleur[a].append(len(station[a][b]))
            b+=1
        a+=1
    a=0
    seuil_vit_sup,seuil_vit_inf,seuil_pop=20,10,0.33
    if trier_normal: #garde les valeur "anormal"
        while a<len(station):
            auga=1
            b=0
            max_echantillon=0
            while b<len(station[a]):
                if len(station[a][b])>max_echantillon:
                    max_echantillon=len(station[a][b])
                b+=1
            b=0
            while b<len(station[a]):
                augb=1
                if (abs(moy[a][b])>seuil_vit_sup) or (abs(moy[a][b])<seuil_vit_inf):# & (len(station[a][b])<max_echantillon*seuil_pop):
                    del moy[a][b]
                    del station[a][b]
                    del legende[a][b]
                    del couleur[a][b]
                    del ec[a][b]
                    augb=0
                if augb:
                    b+=1
            if station[a]==[]:
                del moy[a]
                del station[a]
                del legende[a]
                del couleur[a]
                del ec[a]
                auga=0
            if auga:
                a+=1
    if trier_anormal: #garde les valeur dans "la norme"
        while a<len(station):
            auga=1
            b=0
            max_echantillon=0
            while b<len(station[a]):
                if len(station[a][b])>max_echantillon:
                    max_echantillon=len(station[a][b])
                b+=1
            b=0
            while b<len(station[a]):
                augb=1
                if (abs(moy[a][b])<seuil_vit_sup) and (abs(moy[a][b])>seuil_vit_inf):# & (len(station[a][b])<max_echantillon*seuil_pop):
                    del moy[a][b]
                    del station[a][b]
                    del legende[a][b]
                    del couleur[a][b]
                    del ec[a][b]
                    augb=0
                if augb:
                    b+=1
            if station[a]==[]:
                del moy[a]
                del station[a]
                del legende[a]
                del couleur[a]
                del ec[a]
                auga=0
            if auga:
                a+=1
    station_manque=[]
    while c<len(choix_station):
        a=0
        manque=1
        while a<len(legende_titre):
            if int(choix_station[c])==int(legende_titre[a]):
                manque=0
                augc=0
                b=0
                loc=[]
                while b<len(legende[a]):
                    loc.append(b)
                    b+=1
                plt.figure(str(legende_titre[a]),figsize=(20,10))
                plt.suptitle('departure from the station: '+legende_titre[a]+', from '+valeur[0]+' to '+valeur[2]+"\n nombre d'utilisateur sur se graph: "+str(sum(couleur[a])))
                couleurs=[x/max(couleur[a]) for x in couleur[a]]
                set_choix=plt.cm.get_cmap('jet')
                sm=ScalarMappable(cmap=set_choix,norm=plt.Normalize(0,max(couleur[a])))
                sm.set_array([])
                colors=set_choix(couleurs)
                plt.bar(loc,moy[a],yerr=ec[a],color=colors)
                cbar=plt.colorbar(sm)
                cbar.set_label('nombre of peuple')
                plt.xticks(loc,legende[a],rotation=60)
                plt.xlabel('numero de station')
                plt.ylabel('vitesse (km/h)')
                plt.grid(True,axis='y')
                plt.show()
                break
            a+=1
        if manque:
            station_manque.append(choix_station[c])
        c+=1
    if station_manque!=[]:
        print('manque de donnees sur les station: ',station_manque)
