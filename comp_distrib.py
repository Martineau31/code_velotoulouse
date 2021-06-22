import csv
import numpy as np
from math import sqrt
from scipy.optimize import curve_fit

def conv_minute(date,horaire,annee):
    "convertion en minute la date et l'heure mise en entrer"
    jour=int(date[0:2])-1
    mois=int(date[3:5])-1
    heure=int(horaire[0:2])
    minute=int(horaire[3:5])
    nombreminute=jour*24*60+heure*60+minute
    if annee=='2019':
        nombrejour=[31,28,31,30,31,30,31,31,30,31,30,31]
    if annee=='2020':
        nombrejour=[31,29,31,30,31,30,31,31,30,31,30,31]
    a=0
    while (a<mois):
        nombreminute+=nombrejour[a]*24*60
        a+=1
    return nombreminute

def conv_date(minute,annee):
    "convertie en date et heure le nombre de minute mis en entrer"
    if annee=='2019':
        nombrejour=[31,28,31,30,31,30,31,31,30,31,30,31]
    if annee=='2020':
        nombrejour=[31,29,31,30,31,30,31,31,30,31,30,31]
    minute=int(minute)
    heure=minute//60
    minute=minute%60
    jour=heure//24
    heure=heure%24
    mois=0
    jour+=1
    while (jour>0):
        jour-=nombrejour[mois]
        mois+=1
    jour+=nombrejour[mois-1]
    mois,jour,heure,minute=str(mois),str(jour),str(heure),str(minute)
    if len(mois)<2:
        mois="0"+mois
    if len(jour)<2:
        jour="0"+jour
    if len(heure)<2:
        heure="0"+heure
    if len(minute)<2:
        minute="0"+minute
    date=jour+"/"+mois
    heure=heure+":"+minute
    return date,heure,annee

def gaus(x,a,x0,sigma,b):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))*(1+np.exp(-(b**2)*((x-x0)**2)/(2*sigma**2)))


def comparaison_numpy(tabi_1,tabi_2):
    tab_1=list(tabi_1)
    tab_2=list(tabi_2)
    c_1=np.correlate(tab_1,tab_1,'same')
    c_2=np.correlate(tab_2,tab_2,'same')
    max_c_1=np.array(max(c_1),dtype=np.float64)
    max_c_2=np.array(max(c_2),dtype=np.float64)
    normalisation=np.array(sqrt(max_c_1*max_c_2),dtype=np.float64)
    val=np.correlate(tab_1,tab_2,"same")/normalisation
    val=val*val
    return val

def lecture_chro(debut='01/01',heure_debut='00:00',fin='31/12',heure_fin='23:59',pas=24*60,fichier_lecture='TOULOUSE TRAJETS 2019',fichier_distance='distance_dijkstra',annee='2019'):
    "permet de renvoyer le traitement statistique des vitesse\nles variable avec les valeur par defaut sont:debut='01/01',heure_debut='00:00',fin='31/12',heure_fin='23:59',pas=24*60,fichier_lecture='TOULOUSE TRAJETS 2019',fichier_enregistrer='test',fichier_distance='distance_dijkstra'\nrenvoie une matrice de vitesse, une de temps, une des trajet de station, les temps de trajet et les valeur utilisé au debut"
    #initialisation des nom de lecture
    fichier_lecture+='.csv'
    fichier_distance+='.csv'
    #ouverture des fichier de lecture et d'écriture
    fichier=open(fichier_lecture,'r',errors='ignore')
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

pas=24*60
pas_vitesse=1
pas_distance=100
pas_temps=1
fichier_comp='comp_distrib_p'+str(pas)+'_vitesse.csv'
ecrit_comp=open(fichier_comp,'w')
compcsv=csv.writer(ecrit_comp,delimiter=";",lineterminator="\n")
minute_2019_debut=6*24*60
minute_2019_fin=(6+7)*24*60
minute_2020_debut=5*24*60
minute_2020_fin=(5+7)*24*60
fichier_enr_2019='fichier_enr_2019_'+str(pas)
fichier_enr_2020='fichier_enr_2020_'+str(pas)
fichier_lec_2019="TOULOUSE TRAJETS 2019"
fichier_lec_2020='2020-12-31_TOULOUSE TRAJETS 2020_ANNEE COMPLETE'
val_vitesse=[[],[],[],[],[],[],[],[],[]] #0:gamma2,1:decallage cor,2:decallage fit 2019,3::decallage fit 2020,4:amplitude2020/amplitude/2019,5:rapport 0/max 2019, 6: rapport 0/max 2020 7:sigma 2019,8:sigma 2020
val_distance=[[],[],[],[],[],[],[],[],[]]
val_temps=[[],[],[],[],[],[],[],[],[]]
a=0
while a<51: #51
    date_debut_2019,heure_debut_2019,_=conv_date(minute_2019_debut,'2019')
    date_fin_2019,heure_fin_2019,_=conv_date(minute_2019_fin,'2019')
    depl_chro(date_debut_2019,heure_debut_2019,date_fin_2019,heure_fin_2019,pas,fichier_lec_2019,fichier_enr_2019,'distance_dijkstra','2019')
    date_debut_2020,heure_debut_2020,_=conv_date(minute_2020_debut,'2020')
    date_fin_2020,heure_fin_2020,_=conv_date(minute_2020_fin,'2020')
    depl_chro(date_debut_2020,heure_debut_2020,date_fin_2020,heure_fin_2020,pas,fichier_lec_2020,fichier_enr_2020,'distance_dijkstra','2020')
    x_2019,_=depl_crenau_lecture(fichier_enr_2019,pas_vitesse,pas_distance,pas_temps,60*24)
    x_2020,_=depl_crenau_lecture(fichier_enr_2020,pas_vitesse,pas_distance,pas_temps,60*24)

    #traitement vitesse
    comp_vitesse=comparaison_numpy(x_2019[0][0],x_2020[0][0])
    max_comp_vitesse=max(comp_vitesse)
    val_vitesse[0].append(max_comp_vitesse)
    where_comp_vitesse=np.argmax(comp_vitesse)
    if len(x_2019[0][0])<len(x_2020[0][0]):
        decallage_vitesse=where_comp_vitesse-(max(len(x_2020[0][0]),len(x_2019[0][0]))-min(len(x_2020[0][0]),len(x_2019[0][0]))//2)
    else:
        decallage_vitesse=where_comp_vitesse-min(len(x_2020[0][0]),len(x_2019[0][0]))//2
    val_vitesse[1].append(decallage_vitesse*pas_vitesse)
    val_vitesse[4].append(max(x_2020[0][0][1::])/max(x_2019[0][0][1::]))
    val_vitesse[5].append(x_2019[0][0][0]/max(x_2019[0][0][1::]))
    val_vitesse[6].append(x_2020[0][0][0]/max(x_2020[0][0][1::]))
    absi_x=np.array([i for i in np.arange(0,pas_vitesse*len(x_2019[0][0]),pas_vitesse)])
    var_vitesse_2019,_=curve_fit(gaus,absi_x[1::],x_2019[0][0][1::],p0=[max(x_2019[0][0][1::]),x_2019[0][0][1::].index(max(x_2019[0][0][1::]))*pas_vitesse,3*pas_vitesse,1],maxfev=int(1e7))
    val_vitesse[7].append(var_vitesse_2019[2])
    absi_x=np.array([i for i in np.arange(0,pas_vitesse*len(x_2020[0][0]),pas_vitesse)])
    var_vitesse_2020,_=curve_fit(gaus,absi_x[1::],x_2020[0][0][1::],p0=[max(x_2020[0][0][1::]),x_2020[0][0][1::].index(max(x_2020[0][0][1::]))*pas_vitesse,3*pas_vitesse,1],maxfev=int(1e7))
    val_vitesse[8].append(var_vitesse_2020[2])
    val_vitesse[3].append(var_vitesse_2020[1])
    val_vitesse[2].append(var_vitesse_2019[1])

    #traitement distance
    comp_distance=comparaison_numpy(x_2019[1][0],x_2020[1][0])
    max_comp_distance=max(comp_distance)
    val_distance[0].append(max_comp_distance)
    where_comp_distance=np.argmax(comp_distance)
    if len(x_2019[1][0])<len(x_2020[1][0]):
        decallage_distance=where_comp_distance-(max(len(x_2020[1][0]),len(x_2019[1][0]))-min(len(x_2020[1][0]),len(x_2019[1][0]))//2)
    else:
        decallage_distance=where_comp_distance-min(len(x_2020[1][0]),len(x_2019[1][0]))//2
    val_distance[1].append(decallage_distance*pas_distance)
    val_distance[4].append(max(x_2020[1][0])/max(x_2019[1][0]))
    val_distance[5].append(x_2019[1][0][0]/max(x_2019[1][0][1::]))
    val_distance[6].append(x_2020[1][0][0]/max(x_2020[1][0][1::]))
    absi_x=np.array([i for i in np.arange(0,pas_distance*len(x_2019[1][0]),pas_distance)])
    var_distance_2019,_=curve_fit(gaus,absi_x[1::],x_2019[1][0][1::],p0=[max(x_2019[1][0][1::]),x_2019[1][0][1::].index(max(x_2019[1][0][1::]))*pas_distance,4*pas_distance,1],maxfev=int(1e7))
    val_distance[7].append(var_distance_2019[2])
    absi_x=np.array([i for i in np.arange(0,pas_distance*len(x_2020[1][0]),pas_distance)])
    var_distance_2020,_=curve_fit(gaus,absi_x[1::],x_2020[1][0][1::],p0=[max(x_2020[1][0][1::]),x_2020[1][0][1::].index(max(x_2020[1][0][1::]))*pas_distance,4*pas_distance,1],maxfev=int(1e7))
    val_distance[8].append(var_distance_2020[2])
    val_distance[3].append(var_distance_2020[1])
    val_distance[2].append(var_distance_2019[1])

    #traitement temps
    comp_temps=comparaison_numpy(x_2019[2][0],x_2020[2][0])
    max_comp_temps=max(comp_temps)
    val_temps[0].append(max_comp_temps)
    where_comp_temps=np.argmax(comp_temps)
    if len(x_2019[2][0])<len(x_2020[2][0]):
        decallage_temps=where_comp_temps-(max(len(x_2020[2][0]),len(x_2019[2][0]))-min(len(x_2020[2][0]),len(x_2019[2][0]))//2)
    else:
        decallage_temps=where_comp_temps-min(len(x_2020[2][0]),len(x_2019[2][0]))//2
    val_temps[1].append(decallage_temps*pas_temps)
    val_temps[4].append(max(x_2020[2][0])/max(x_2019[2][0]))
    val_temps[5].append(x_2019[2][0][0]/max(x_2019[2][0][1::]))
    val_temps[6].append(x_2020[2][0][0]/max(x_2020[2][0][1::]))
    absi_x=np.array([i for i in np.arange(0,pas_temps*len(x_2019[2][0]),pas_temps)])
    var_temps_2019,_=curve_fit(gaus,absi_x[1::],x_2019[2][0][1::],p0=[max(x_2019[2][0][1::]),x_2019[2][0][1::].index(max(x_2019[2][0]))*pas_temps,3*pas_temps,1],maxfev=int(1e7))
    val_temps[7].append(var_temps_2019[2])
    absi_x=np.array([i for i in np.arange(0,pas_temps*len(x_2020[2][0]),pas_temps)])
    var_temps_2020,_=curve_fit(gaus,absi_x[1::],x_2020[2][0][1::],p0=[max(x_2020[2][0][1::]),x_2020[2][0][1::].index(max(x_2020[2][0][1::]))*pas_temps,3*pas_temps,1],maxfev=int(1e7))
    val_temps[8].append(var_temps_2020[2])
    val_temps[3].append(var_temps_2020[1])
    val_temps[2].append(var_temps_2019[1])

    minute_2019_debut+=7*24*60
    minute_2020_debut+=7*24*60
    minute_2020_fin+=7*24*60
    minute_2019_fin+=7*24*60
    a+=1
compcsv.writerow(val_vitesse[0])
compcsv.writerow(val_distance[0])
compcsv.writerow(val_temps[0])
compcsv.writerow(val_vitesse[1])
compcsv.writerow(val_distance[1])
compcsv.writerow(val_temps[1])
compcsv.writerow(val_vitesse[2])
compcsv.writerow(val_distance[2])
compcsv.writerow(val_temps[2])
compcsv.writerow(val_vitesse[3])
compcsv.writerow(val_distance[3])
compcsv.writerow(val_temps[3])
compcsv.writerow(val_vitesse[4])
compcsv.writerow(val_distance[4])
compcsv.writerow(val_temps[4])
compcsv.writerow(val_vitesse[5])
compcsv.writerow(val_distance[5])
compcsv.writerow(val_temps[5])
compcsv.writerow(val_vitesse[6])
compcsv.writerow(val_distance[6])
compcsv.writerow(val_temps[6])
compcsv.writerow(val_vitesse[7])
compcsv.writerow(val_distance[7])
compcsv.writerow(val_temps[7])
compcsv.writerow(val_vitesse[8])
compcsv.writerow(val_distance[8])
compcsv.writerow(val_temps[8])
ecrit_comp.close()
