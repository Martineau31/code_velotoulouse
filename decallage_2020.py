import csv
import numpy as np

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


def comparaison_numpy(tabi_1,tabi_2):
    tab_1=list(tabi_1)
    tab_2=list(tabi_2)
    c_1=np.correlate(tab_1,tab_1,'same')
    c_2=np.correlate(tab_2,tab_2,'same')
    val=np.correlate(tab_1,tab_2)/np.sqrt(max(c_1)*max(c_2))
    return val

def lecture_n_n(debut='01/01',heure_debut='00:00',fin='31/12',heure_fin='23:59',pas=24*60,fichier_lecture='TOULOUSE TRAJETS 2019',annee='2019'):
    "permet de renvoyer les donnee dans un tableau organise\nles variable avec les valeur par defaut sont:debut='01/01',heure_debut='00:00',fin='31/12',heure_fin='23:59',pas=24*60,fichier_lecture='TOULOUSE TRAJETS 2019',fichier_enregistrer='test' et annee=2019"

    #initialisation des nom de lecture
    fichier_lecture+='.csv'
    #ouverture des fichier de lecture et d'ecriture
    fichier=open(fichier_lecture,'r',errors='ignore')
    #permet de lire le fichier et de dire que les colone sont delimiter pas ";"
    read=csv.reader(fichier,delimiter=";",lineterminator="\n")
    #permet d'ecire delimiter permet de definir le symbole qui separe les colone, lineterminator evite les retour a la ligne inutil dans le doc final
    enr_erreur=open('erreur_lecture.txt','w')
    station_max=400 #numero de la station maximal accepter
    #calcul nombre de case dans le tableau
    minute_debut=conv_minute(debut,heure_debut,annee)
    minute_fin=conv_minute(fin,heure_fin,annee)
    nombre_case=(minute_fin-minute_debut)//pas
    #creation du tableau d'enregistrement, pour simplifier on pourrai utilise zeros dans numpy a demander
    tableau=[]
    a=0
    while a<nombre_case:
        tableau.append([])
        a+=1

    #permet d'ignorer la premiere ligne qui est du texte
    read.__next__()

    #compteur d'echantillons
    nombretotal=0 #enregistrement reussi
    max_station=0 #trouver la valeur max du numero de station

    for row in read:
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
                provoque_erreur[2]=1 #provoque une erreur pour alle a l'endroit voulu plus bas
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
    "permet d'enregistrer les donnees organiser sous forme de tableau nxn dans des fichier CSV"
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
    "permet de lire et enregistrer les donnees sous forme de tableau nxn\ndebut='01/01',heure_debut='00:00',fin='31/12',heure_fin='23:59',pas=24*60,fichier_lecture='TOULOUSE TRAJETS 2019',fichier_enregistrer='test'"
    tableau,val=lecture_n_n(debut,heure_debut,fin,heure_fin,pas,fichier_lecture,annee)
    enregistrement_n_n(fichier_enregistrer,tableau,val)


def utilisation_lecture(fichier=['test']):
    "permet de lire la matrice d'utilisation du temps en fonction du nombre d'usager\n en entrer mettre le nom d'un fichier du type .csv sans noter le .csv"
    #ouverture du fichier a tracer
    x,y=[],[] #tableau de valeur, x etant les ordonnees et y les legende en x
    place=[] #enregistrement des place des legende en x
    b=0
    while b<len(fichier):
        if b!=0:
            lire.close()
        fichier[b]+='.csv'
        lire=open(fichier[b],'r')
        read=csv.reader(lire,delimiter=";",lineterminator="\n")
        compteur_legende=0 #permet de numeroter l'endroit des legende en x
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


pas=5
fichier_comp='comp_p'+str(pas)+'_2020.csv'
ecrit_comp=open(fichier_comp,'w')
compcsv=csv.writer(ecrit_comp,delimiter=";",lineterminator="\n")
minute_2019_debut=6*24*60-6*60
minute_2019_fin=(6+7)*24*60+6*60
fichier_enr_2019='fichier_enr_2019_'+str(pas)
fichier_enr_2020='fichier_enr_2020_'+str(pas)
fichier_lec_2019="TOULOUSE TRAJETS 2019"
fichier_lec_2020='2020-12-31_TOULOUSE TRAJETS 2020_ANNEE COMPLETE'
a=0
while a<51:
    minute_2020_debut=5*24*60
    minute_2020_fin=(5+7)*24*60
    date_debut_2019,heure_debut_2019,annee_1=conv_date(minute_2019_debut,'2020')
    date_fin_2019,heure_fin_2019,_=conv_date(minute_2019_fin,'2020')
    matrice_n_n(date_debut_2019,heure_debut_2019,date_fin_2019,heure_fin_2019,pas,fichier_lec_2019,fichier_enr_2019,'2020')
    val=[[],[]]
    b=0
    while b<51:
        date_debut_2020,heure_debut_2020,annee_2=conv_date(minute_2020_debut,'2020')
        date_fin_2020,heure_fin_2020,_=conv_date(minute_2020_fin,'2020')
        matrice_n_n(date_debut_2020,heure_debut_2020,date_fin_2020,heure_fin_2020,pas,fichier_lec_2020,fichier_enr_2020,'2020')
        x,_,_,_=utilisation_lecture([fichier_enr_2019,fichier_enr_2020])
        comp=comparaison_numpy(x[0],x[1])
        max_comp=max(comp)
        val[0].append(max_comp)
        where_comp=np.argmax(comp)
        decallage=where_comp-(len(comp)//2) #bloquer si len(comp)/2 pas entier
        val[1].append(decallage*pas)
        minute_2020_debut+=7*24*60
        minute_2020_fin+=7*24*60
        b+=1
    minute_2019_debut+=7*24*60
    minute_2019_fin+=7*24*60
    a+=1
    compcsv.writerow(val[0])
    compcsv.writerow(val[1])
ecrit_comp.close()
