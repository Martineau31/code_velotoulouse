import csv #biblio pour lire les .csv
from outil_calcul import *
import networkx as nx
import osmnx as ox


def lecture_n_n(debut='01/01',heure_debut='00:00',fin='31/12',heure_fin='00:00',pas=24*60,fichier_lecture='TOULOUSE TRAJETS 2019',annee='2019'):
    "permet de renvoyer les donnée dans un tableau organisé\nles variable avec les valeur par defaut sont:debut='01/01',heure_debut='00:00',fin='31/12',heure_fin='23:59',pas=24*60,fichier_lecture='TOULOUSE TRAJETS 2019',fichier_enregistrer='test' et annee=2019"

    #initialisation des nom de lecture
    fichier_lecture+='.csv'
    #ouverture des fichier de lecture et d'écriture
    fichier=open(fichier_lecture,'r',errors='ignore')
    #permet de lire le fichier et de dire que les colone sont delimiter pas ";"
    read=csv.reader(fichier,delimiter=";",dialect='excel')
    #permet d'écire delimiter permet de définir le symbole qui separe les colone, lineterminator evite les retour a la ligne inutil dans le doc final
    enr_erreur=open('erreur_lecture.txt','w')
    station_max=400 #numero de la station maximal accepter
    #calcul nombre de case dans le tableau
    minute_debut=conv_minute(debut,heure_debut,annee)
    minute_fin=conv_minute(fin,heure_fin,annee)
    nombre_case=(minute_fin-minute_debut)//pas
    #creation du tableau d'enregistrement, pour simplifier on pourrai utilisé zeros dans numpy a demander
    tableau=[]
    a=0
    while a<nombre_case:
        tableau.append([])
        a+=1

    #permet d'ignorer la premiere ligne qui est du texte
    read.__next__()

    #compteur d'echantillons
    nombretotal=0 #enregistrement réussi
    max_station=0 #trouver la valeur max du numero de station
    for row in read: #boucle qui permet de lire les ligne du tableau une a une
        a=(row[0],row[2],row[3]) #choisi les colone a lire (commence a zero)
        stop=1
        #jusqu'a la ligne 30, retourne le numero du jour
        date=row[2][8:10]+"/"+row[2][5:7]
        heure=row[2][11:13]+":"+row[2][14:16]
        annees=row[2][0:4]
        temps=conv_minute(date,heure,annees)
        try:
            depart=int(row[0]) #numerotation station commence a zero
            arrive=int(row[3])
            #enregustre la valeur de la station max
            if (depart>max_station) & (depart<station_max):
                max_station=depart
            if (arrive>max_station) & (arrive<station_max):
                max_station=arrive
            if (arrive>=station_max) or (depart>=station_max):
                provoque_erreur[2]=1 #provoque une erreur pour allé a l'endroit voulu plus bas
        except ValueError: #valeur manquante
            enr_erreur.write(row[2]+" ValueError: depart="+row[0]+" arrive="+row[3]+"\n")
            stop=0
        except NameError: #valeur aberante
            enr_erreur.write(row[2]+" IndexError: depart="+row[0]+" arrive="+row[3]+"\n")
            stop=0
        if (temps>minute_debut) & (temps<minute_fin) & (stop):
            case=(temps-minute_debut)//pas
            try: #si pas d'erreur, ajoute un pour le comptage des trajet
                tableau[case][depart][arrive]+=1
                nombretotal+=1
            except: #si erreur, ajoute les case manquante jusqu'au numero de station
                while len(tableau[case])<=depart:
                    tableau[case].append([])
                while len(tableau[case][depart])<=arrive:
                    tableau[case][depart].append(0)
                tableau[case][depart][arrive]+=1
                nombretotal+=1
    #mise sous forme carree des matrice
    c=0 #compteur
    while c<len(tableau):
        while (len(tableau[c])<=max_station):
            tableau[c].append([])
        d=0
        while d<=max_station:
            while len(tableau[c][d])<=max_station:
                tableau[c][d].append(0)
            d+=1
        c+=1
    fichier.close()
    enr_erreur.close()
    return tableau,[debut,heure_debut,fin,heure_fin,pas,annee]


def enregistrement_n_n(fichier_enregistrement,tableau,val):
    "permet d'enregistrer les données organiser sous forme de tableau nxn dans des fichier CSV"
    fichier_enregistrement+='.csv'
    ecrit=open(fichier_enregistrement,'w')
    nouveau=csv.writer(ecrit,delimiter=";",lineterminator="\n")
    compteurcase=0
    t=conv_minute(val[0],val[1],val[5])
    minute_debut=t
    nouveau.writerow(val)
    while (compteurcase<len(tableau)):
        compteurdepart=0
        while (compteurdepart<len(tableau[compteurcase])):
            nouveau.writerow(tableau[compteurcase][compteurdepart])
            compteurdepart+=1
        nouveau.writerow("\n")
        t+=val[4]
        compteurcase=(t-minute_debut)//val[4]

        
def matrice_n_n(debut='01/01',heure_debut='00:00',fin='31/12',heure_fin='23:59',pas=24*60,fichier_lecture='TOULOUSE TRAJETS 2019',fichier_enregistrer='test',annee='2019'):
    "permet de lire et enregistrer les données sous forme de tableau nxn\ndebut='01/01',heure_debut='00:00',fin='31/12',heure_fin='23:59',pas=24*60,fichier_lecture='TOULOUSE TRAJETS 2019',fichier_enregistrer='test'"
    tableau,val=lecture_n_n(debut,heure_debut,fin,heure_fin,pas,fichier_lecture,annee=annee)
    enregistrement_n_n(fichier_enregistrer,tableau,val)

    
def matrice_n_n_dif(debut_1='01/01',debut_2='01/01',heure_debut='00:00',fin_1='31/12',fin_2='31/12',heure_fin='23:59',pas=24*60,fichier_lecture_1='TOULOUSE TRAJETS 2019',fichier_lecture_2='TOULOUSE TRAJETS 2019',fichier_enregistrer='test',norme=True):
    "permet de lire et enregistrer les données sous forme de tableau nxn en comparant interval_1-interval_2\ndebut_1='01/01',debut_2='01,01',heure_debut='00:00',fin_1='31/12',fin_2='01/01',heure_fin='23:59',pas=24*60,fichier_lecture_1='TOULOUSE TRAJETS 2019',fichier_lecture_2='TOULOUSE TRAJETS 2019',fichier_enregistrer='test',norme=True"
    tableau_1,val_1=lecture_n_n(debut_1,heure_debut,fin_1,heure_fin,pas,fichier_lecture_1)
    tableau_2,val_2=lecture_n_n(debut_2,heure_debut,fin_2,heure_fin,pas,fichier_lecture_2)
    print('fin_lecture')
    val=[]
    val.append(val_1[0])
    val.append(val_1[1])
    val.append(val_1[2])
    val.append(val_1[3])
    val.append(val_1[4])
    val.append(val_2[0])
    val.append(val_2[1])
    val.append(val_2[2])
    val.append(val_2[3])
    val.append(val_2[4])
    a=0
    difference=[]
    while a<len(tableau_1):
        difference.append([])
        if norme:
            somme_1=0
            somme_2=0
            b=0
            while b<len(tableau_1[a]):
                c=0
                while c<len(tableau_1[a][b]):
                    somme_1+=tableau_1[a][b][c]
                    somme_2+=tableau_2[a][b][c]
                    c+=1
                b+=1
        b=0
        while b<len(tableau_1[a]):
            difference[a].append([])
            c=0
            while c<len(tableau_1[a][b]):
                if norme:
                    try:
                        difference[a][b].append((tableau_1[a][b][c]/somme_1)-(tableau_2[a][b][c]/somme_2))
                    except ZeroDivisionError:
                        if not c:
                            print('rentrer if :',somme_1,somme_2)
                        if somme_1==0:
                            difference[a][b].append(-tableau_2[a][b][c]/somme_2)
                        elif somme_2==0:
                            difference[a][b].append(tableau_1[a][b][c]/somme_1)
                        else:
                            difference[a][b].append(0)
                else:
                    difference[a][b].append(tableau_1[a][b][c]-tableau_2[a][b][c])
                c+=1
            b+=1
        a+=1
    print('enregistrement')
    enregistrement_n_n(fichier_enregistrer,difference,val)

    
    
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


def distance(fichier='distance_dijkstra'):
    "permet de déterminer la distance entre chaque point a partir des position et du réseau de vélo\nretourne une matrice carré des distance"
    G=ox.graph_from_point((43.59933,1.43912),dist=10000,network_type='bike')
    print("reseau construit, debut du traitement")
    fichier+='.csv'
    fichier_enr=open(fichier,'w')
    enr=csv.writer(fichier_enr,delimiter=';',lineterminator='\n')
    pos=position()
    dist=[[],[]]
    ini=0
    R=6371e3
    point=[]
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
        print('avancement premiere etape: ',100*ini/len(pos))
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
            if distance==[]:
                print('probleme: ',ini,fin)
                val_enr.append('NetworkXNoPath')
            else:
                val_enr.append(min(distance))
            fin+=1
        enr.writerow(val_enr)
        ini+=1
        print('avancement seconde etape: ',(ini*100)/len(pos))
    print(probleme)
    fichier_enr.close()

def lecture_chro(debut='01/01',heure_debut='00:00',fin='31/12',heure_fin='23:59',pas=24*60,fichier_lecture='TOULOUSE TRAJETS 2019',fichier_distance='distance_dijkstra',annee='2019'):
    "permet de renvoyer le traitement statistique des vitesse\nles variable avec les valeur par defaut sont:debut='01/01',heure_debut='00:00',fin='31/12',heure_fin='23:59',pas=24*60,fichier_lecture='TOULOUSE TRAJETS 2019',fichier_enregistrer='test',fichier_distance='distance_dijkstra'\nrenvoie une matrice de vitesse, une de temps, une des trajet de station, les temps de trajet et les valeur utilisé au debut"
    #initialisation des nom de lecture
    fichier_lecture+='.csv'
    fichier_distance+='.csv'
    #ouverture des fichier de lecture et d'écriture
    fichier=open(fichier_lecture,'r')
    #permet de lire le fichier et de dire que les colone sont delimiter pas ";"
    read=csv.reader(fichier,delimiter=";",dialect='excel')
    #permet d'écire delimiter permet de définir le symbole qui separe les colone, lineterminator evite les retour a la ligne inutil dans le doc final
    distanc=open(fichier_distance,'r')
    dist=csv.reader(distanc,delimiter=";",dialect='excel')
    station_max=400 #numero de la station maximal accepter
    #calcul nombre de case dans le tableau
    minute_debut=conv_minute(debut,heure_debut,annee)
    minute_fin=conv_minute(fin,heure_fin,annee)
    nombre_case=(minute_fin-minute_debut)//pas
    #création des tableau
    parcourt=[]
    temps=[]
    vitesse=[]
    station=[]
    L=[]
    a=0
    while a<=nombre_case:
        parcourt.append([])
        temps.append([])
        vitesse.append([])
        station.append([])
        a+=1
    #lis la matrice des distance
    for row in dist:
        L.append(row)
    distanc.close()
    #permet d'ignorer la premiere ligne qui est du texte
    read.__next__()
    dist_manq=0
    for row in read:
        date=row[2][8:10]+"/"+row[2][5:7]
        heure=row[2][11:13]+":"+row[2][14:16]
        annees=row[2][0:4]
        temps_debut=conv_minute(date,heure,annees)
        stop=1
        try:
            depart=int(row[0]) #numerotation station commence a zero
            arriver=int(row[3])
            if (arriver>=station_max) or (depart>=station_max):
                provoque_erreur[2]=1 #provoque une erreur pour allé a l'endroit voulu plus bas
        except ValueError: #valeur manquante
            stop=0
        except NameError: #valeur aberante
            stop=0
        if (temps_debut>minute_debut) & (temps_debut<minute_fin) & (stop):
            case=(temps_debut-minute_debut)//pas
            #tmps en minute arriver
            date=row[5][8:10]+"/"+row[5][5:7]
            heure=row[5][11:13]+":"+row[5][14:16]
            annees=row[2][0:4]
            temps_trajet=conv_minute(date,heure,annees)-temps_debut
            try:
                temps[case].append(temps_trajet)
                parcourt[case].append(float(L[depart][arriver]))
                station[case].append(row[0]+'>'+row[3])
                try:
                    vitesse[case].append(0.06*float(L[depart][arriver])/temps_trajet)
                except ZeroDivisionError:
                    vitesse[case].append(0)
            except ValueError:
                dist_manq+=1
    val=[debut,heure_debut,fin,heure_fin,pas,annee]
    fichier.close()
    return station,parcourt,temps,vitesse,val

def enregistrement_chro(station,parcourt,temps,vitesse,val,fichier_enregistrer='test_distance'):
    #enregistrement
    fichier_enregistrer+='.csv'
    ecrit=open(fichier_enregistrer,'w')
    nouveau=csv.writer(ecrit,delimiter=";",lineterminator="\n")
    a=0
    nouveau.writerow(val)
    while a<len(station):
        nouveau.writerow(station[a])
        nouveau.writerow(parcourt[a])
        nouveau.writerow(temps[a])
        nouveau.writerow(vitesse[a])
        a+=1
    #fermeture des fichier utilise

    ecrit.close()

def depl_chro(debut='01/01',heure_debut='00:00',fin='31/12',heure_fin='23:59',pas=24*60,fichier_lecture='TOULOUSE TRAJETS 2019',fichier_enregistrer='test_distance',fichier_distance='distance_dijkstra',annee='2019'):
    "permet d'afficher le traitement statistique des vitesse\nles variable avec les valeur par defaut sont:debut='01/01',heure_debut='00:00',fin='31/12',heure_fin='23:59',pas=24*60,fichier_lecture='TOULOUSE TRAJETS 2019',fichier_enregistrer='test',fichier_distance='distance_dijkstra'"
    s,p,t,v,val=lecture_chro(debut,heure_debut,fin,heure_fin,pas,fichier_lecture,fichier_distance,annee)
    enregistrement_chro(s,p,t,v,val,fichier_enregistrer)
    
    
def depl_chro_dif(debut_1='01/01',debut_2='01/01',heure_debut='00:00',fin_1='31/12',fin_2='31/12',heure_fin='23:59',pas=24*60,fichier_lecture_1='TOULOUSE TRAJETS 2019',fichier_lecture_2='TOULOUSE TRAJETS 2019',fichier_enregistrer='test_distance',fichier_distance='distance_dijkstra'):
    s_1,p_1,t_1,v_1,val_1=lecture_chro(debut_1,heure_debut,fin_1,heure_fin,pas,fichier_lecture_1,fichier_distance)
    s_2,p_2,t_2,v_2,val_2=lecture_chro(debut_2,heure_debut,fin_2,heure_fin,pas,fichier_lecture_2,fichier_distance)
    print('fin_lecture')
    parcourt=[]
    temps=[]
    vitesse=[]
    station=[]
    val=val_1+val_2
    print(val)
    a=0
    while a<len(s_1):
        parcourt.append([])
        temps.append([])
        vitesse.append([])
        station.append([])
        b=0
        while b<len(s_1[a]):
            parcourt[a].append(p_1[a][b])
            temps[a].append(t_1[a][b])
            vitesse[a].append(v_1[a][b])
            station[a].append(s_1[a][b])
            b+=1
        b=0
        while b<len(s_2[a]):
            parcourt[a].append(-p_2[a][b])
            temps[a].append(-t_2[a][b])
            vitesse[a].append(-v_2[a][b])
            station[a].append(s_2[a][b])
            b+=1
        a+=1
    print('fin traitement')
    enregistrement_chro(station,parcourt,temps,vitesse,val,fichier_enregistrer)
    print('enregistrer')

    
def utilisation_lecture(fichier=['test']):
    "permet de lire la matrice d'utilisation du temps en fonction du nombre d'usager\n en entrer mettre le nom d'un fichier du type .csv sans noter le .csv"
    #ouverture du fichier a tracer
    x,y=[],[] #tableau de valeur, x etant les ordonnées et y les legende en x
    place=[] #enregistrement des place des legende en x
    b=0
    while b<len(fichier):
        if b!=0:
            lire.close()
        fichier[b]+='.csv'
        lire=open(fichier[b],'r')
        read=csv.reader(lire,delimiter=";",lineterminator="\n")
        compteur_legende=0 #permet de numéroter l'endroit des legende en x
        somme=0 #valeur des trajet sur l'intervalle etudier
        compteur_temps=0 #donnera le mois et sert a savoir si on arrive au bout du mois dans le code
        valeur=read.__next__()
        pas=int(valeur[4])
        nombre_legende=21
        intervalle=(conv_minute(valeur[2],valeur[3],valeur[5])-conv_minute(valeur[0],valeur[1],valeur[5]))//nombre_legende
        debut_min=conv_minute(valeur[0],valeur[1],valeur[5])
        x.append([])
        y.append([])
        for row in read:
            a=0 #increment
            while a<len(row):
                if (row[0]!="\n"): #ajoute au la somme pour valeur
                    somme+=float(row[a])
                    a+=1
                if (row[0]=="\n"): #detecte la fin de la matrice des trajets et enregistre les valeurs
                    x[b].append(somme)
                    if compteur_temps%intervalle<pas: #enregistre la date et la possition de la date en x
                        date,heure,_=conv_date(debut_min+compteur_temps,valeur[5])
                        y[b].append(date+" "+heure)
                        if b==0:
                            place.append(compteur_legende)
                    compteur_temps+=pas
                    compteur_legende+=1
                    somme=0
                    break
        b+=1
    lire.close()
    return x,valeur,place,y

def depl_crenau_lecture(fichier='test_distance',pas_vitesse=1,pas_distance=100,pas_temps=1,pas_temps_graph=60*24): #probleme sur pas_temps_graph
    "lis la répartition des vitesse,temps et distance sur l'interval moyenner sur un longtemps avec crenau"
    fichier+='.csv'
    lire=open(fichier,'r')
    read=csv.reader(lire,delimiter=";",lineterminator="\n")
    compteur_legende=0 #permet de numéroter l'endroit des legende en x
    valeur=read.__next__() #0 date debut,1 heure debut,2 date fin,3 heure fin,4 pas de temps
    pas=int(valeur[4])
    nombre_case=pas_temps_graph/pas
    val_vitesse=[]
    val_temps=[]
    val_distance=[]
    a=0
    while a<nombre_case:
        val_vitesse.append([])
        val_temps.append([])
        val_distance.append([])
        b=0
        val_vitesse[a].append(0)
        val_temps[a].append(0)
        val_distance[a].append(0)
        a+=1
        compteur=0
    for row in read:
        row=read.__next__()
        a=0
        while a<len(row):
            try:
                if float(row[a])>=0:
                    val_distance[int(compteur%nombre_case)][int(float(row[a])//pas_distance)]+=1
                else:
                    val_distance[int(compteur%nombre_case)][int(-float(row[a])//pas_distance)]-=1
            except:
                longueur=0
                if float(row[a])<0:
                    case=-float(row[a])
                else:
                    case=float(row[a])
                while longueur<nombre_case:
                    while len(val_distance[longueur])<=(case//pas_distance):
                        val_distance[longueur].append(0)                   
                    longueur+=1
                if float(row[a])>=0:
                    val_distance[int(compteur%nombre_case)][int(float(row[a])//pas_distance)]+=1
                else:
                    val_distance[int(compteur%nombre_case)][int(-float(row[a])//pas_distance)]-=1
            a+=1
        row=read.__next__()
        a=0
        while a<len(row):
            if (float(row[a])<=60) & (float(row[a])>=-60):
                try:
                    if float(row[a])>=0:
                        val_temps[int(compteur%nombre_case)][int(float(row[a])//pas_temps)]+=1
                    else:
                        val_temps[int(compteur%nombre_case)][int(-float(row[a])//pas_temps)]-=1
                except:
                    longueur=0
                    if float(row[a])<0:
                        case=-float(row[a])
                    else:
                        case=float(row[a])
                    while longueur<nombre_case:
                        while len(val_temps[longueur])<=(case//pas_temps):
                            val_temps[longueur].append(0)
                        longueur+=1
                    if float(row[a])>=0:
                        val_temps[int(compteur%nombre_case)][int(float(row[a])//pas_temps)]+=1
                    else:
                        val_temps[int(compteur%nombre_case)][int(-float(row[a])//pas_temps)]-=1
            a+=1
        row=read.__next__()
        a=0
        while a<len(row):
            try:
                if float(row[a])>=0:
                    val_vitesse[int(compteur%nombre_case)][int(float(row[a])//pas_vitesse)]+=1
                else:
                    val_vitesse[int(compteur%nombre_case)][int(-float(row[a])//pas_vitesse)]-=1
            except:
                longueur=0
                if float(row[a])<0:
                    case=-float(row[a])
                else:
                    case=float(row[a])
                while longueur<nombre_case:
                    while len(val_vitesse[longueur])<=(case//pas_vitesse):
                        val_vitesse[longueur].append(0)
                    longueur+=1
                if float(row[a])>=0:
                    val_vitesse[int(compteur%nombre_case)][int(float(row[a])//pas_vitesse)]+=1
                else:
                    val_vitesse[int(compteur%nombre_case)][int(-float(row[a])//pas_vitesse)]-=1
            a+=1
        compteur+=1
    lire.close()
    return [val_vitesse,val_distance,val_temps],valeur

