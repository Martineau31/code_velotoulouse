import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

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

def comparaison_numpy(tabi_1,tabi_2):
    tab_1=list(tabi_1)
    tab_2=list(tabi_2)
    c_1=np.correlate(tab_1,tab_1,'same')
    c_2=np.correlate(tab_2,tab_2,'same')
    print('len(tab_1): ',len(tabi_1),'max: ',np.where(c_1==max(c_1)),'len(tab_2): ',len(tabi_2),'max: ',np.where(c_2==max(c_2)))
    plt.figure(figsize=(10,10))
    plt.subplot(221)
    plt.grid(True)
    plt.plot(tab_1,label='tab_1')
    plt.plot(tab_2,label='tab_2')
    plt.legend()
    val=np.correlate(tab_1,tab_2)/sqrt(max(c_1)*max(c_2))
    print(max(c_1),max(c_2))
    print('longueur resultat: ',len(val))
    plt.subplot(222)
    plt.grid(True)
    plt.plot(val)
    plt.show()
    return val



