import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from import_export import *

def gaus(x,a,x0,sigma,b):
    #return (a/(np.sqrt(2*np.pi)*sigma))*np.exp(-(x-x0)**2/(2*sigma**2))*(1+(2/np.sqrt(np.pi))*np.exp(-(b**2)*((x-x0)**2)/(2*sigma**2)))
    return a*np.exp(-(x-x0)**2/(2*sigma**2))*(1+(2/np.sqrt(np.pi))*np.exp(-(b**2)*((x-x0)**2)/(2*sigma**2)))


def gaus_1(x,a_1,x0_1,sigma_1):
    return a_1*np.exp(-(x-x0_1)**2/(2*sigma_1**2))

def factoriel(x):
    a=1
    resultat=np.array(1,dtype=np.float64)
    while a<=x:
        resultat=resultat*a
        a+=1
    return resultat

def f_gamma(x,alpha,beta,ampl,x_0):
    return ampl*((beta**int(alpha))*(x-x_0)**(int(alpha)-1)*np.exp(-beta*x))/factoriel(int(alpha)-1)
    
    
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


def conv_num(a):
    inc=0
    b=len(a)
    c=[]
    while inc<b:
        c.append(float(a[inc]))
        inc+=1
    return c

pas=24*60
pas_vitesse=1
pas_distance=100
pas_temps=1
minute_2019_debut=6*24*60
minute_2019_fin=(6+7)*24*60
minute_2020_debut=5*24*60
minute_2020_fin=(5+7)*24*60
fichier_enr_2019='fichier_enr_2019_'+str(pas)
fichier_enr_2020='fichier_enr_2020_'+str(pas)
fichier_lec_2019="TOULOUSE TRAJETS 2019"
fichier_lec_2020='2020-12-31_TOULOUSE TRAJETS 2020_ANNEE COMPLETE'
a=0
while a<51:
    date_debut_2019,heure_debut_2019,_=conv_date(minute_2019_debut,'2019')
    date_fin_2019,heure_fin_2019,_=conv_date(minute_2019_fin,'2019')
    depl_chro(date_debut_2019,heure_debut_2019,date_fin_2019,heure_fin_2019,pas,fichier_lec_2019,fichier_enr_2019,'distance_dijkstra','2019')
    print('fin 1:')
    date_debut_2020,heure_debut_2020,_=conv_date(minute_2020_debut,'2020')
    date_fin_2020,heure_fin_2020,_=conv_date(minute_2020_fin,'2020')
    depl_chro(date_debut_2020,heure_debut_2020,date_fin_2020,heure_fin_2020,pas,fichier_lec_2020,fichier_enr_2020,'distance_dijkstra','2020')
    print('fin 2:')
    x_2019,_=depl_crenau_lecture(fichier_enr_2019,pas_vitesse,pas_distance,pas_temps,60*24)
    print('fin 3:')
    x_2020,_=depl_crenau_lecture(fichier_enr_2020,pas_vitesse,pas_distance,pas_temps,60*24)
    print('fin 4:')
    #2020
    b=0
    while b<3:
        a_1=max(x_2020[b][0][1::])
        absi_x=np.array([i for i in np.arange(0,5*len(x_2020[b][0]),5)])
        var,_=curve_fit(gaus,absi_x[1::],x_2020[b][0][1::],p0=[a_1,5*(x_2020[b][0][1::].index(a_1)+1),1,1],maxfev=int(1e7))
        var_1,_=curve_fit(f_gamma,absi_x[1::],x_2020[b][0][1::],p0=[5*(x_2020[b][0][1::].index(a_1)+1)**2,1,a_1,5*(x_2020[b][0][1::].index(a_1)+1)],maxfev=int(1e7),bounds=(0.0,np.inf))
        print(var_1)
        if b==0:
            titre='vitesse'
        if b==1:
            titre='distance'
        if b==2:
            titre='temps'
        plt.figure('2020 '+titre,figsize=(10,10))
        plt.subplot(211)
        plt.title(' 2020')
        plt.plot(absi_x,x_2020[b][0],label='original 2020')
        plt.axvline(x=5*(x_2020[b][0][1::].index(a_1)+1),color='red',linestyle='--',label='maximum mis dans fit')
        plt.axvline(x=5*x_2020[b][0][1::].index(a_1)+1,color='green',linestyle='--',label='maximum mis dans fit')

        plt.plot(absi_x,gaus(absi_x,var[0],var[1],var[2],var[3]),label='fit 2020 ')
        plt.plot(absi_x,f_gamma(absi_x,var_1[0],var_1[1],var_1[2],var_1[3]),label='fit gamma 2020')

        plt.legend()

        plt.subplot(212)
        plt.title('tracer gaussienne')
        plt.plot(absi_x,gaus_1(absi_x,var[0],var[1],var[2]),label='gaussienne 1 '+titre)
        plt.plot(absi_x,gaus_1(absi_x,1,var[1]*var[3],var[2])*gaus_1(absi_x,var[0],var[1],var[2]),label='gaussienne 2 ')
        plt.axvline(x=5*(x_2020[b][0][1::].index(a_1)+1),color='red',linestyle='--',label='maximum mis dans fit')
        plt.axvline(x=5*x_2020[b][0][1::].index(a_1)+1,color='green',linestyle='--',label='maximum mis dans fit')

        plt.legend()
        b+=1


    #2019
    b=0
    while b<3:
        a_1=max(x_2019[b][0][1::])
        absi_x=np.array([i for i in np.arange(0,5*len(x_2019[b][0]),5)])
        var,_=curve_fit(gaus,absi_x[1::],x_2019[b][0][1::],p0=[a_1,5*(x_2019[b][0][1::].index(a_1)+1),1,1],maxfev=int(1e7))
        var_1,_=curve_fit(f_gamma,absi_x[1::],x_2019[b][0][1::],p0=[5*(x_2019[b][0][1::].index(a_1)+1)**2,1,a_1,5*(x_2019[b][0][1::].index(a_1)+1)],maxfev=int(1e7),bounds=(0.0,np.inf))
        print(var_1)
        if b==0:
            titre='vitesse'
        if b==1:
            titre='distance'
        if b==2:
            titre='temps'
        plt.figure('2019 '+titre,figsize=(10,10))
        plt.subplot(211)
        plt.title(' 2019')
        plt.plot(absi_x,x_2019[b][0],label='original 2020')
        plt.axvline(x=5*(x_2019[b][0][1::].index(a_1)+1),color='red',linestyle='--',label='maximum mis dans fit')

        plt.plot(absi_x,gaus(absi_x,var[0],var[1],var[2],var[3]),label='fit 2020 ')
        plt.plot(absi_x,f_gamma(absi_x,var_1[0],var_1[1],var_1[2],var_1[3]),label='fit gamma 2020')

        plt.legend()

        plt.subplot(212)
        plt.title('tracer gaussienne')
        plt.plot(absi_x,gaus_1(absi_x,var[0],var[1],var[2]),label='gaussienne 1 '+titre)
        plt.plot(absi_x,gaus_1(absi_x*var[3],1,var[1]*var[3],var[2])*gaus_1(absi_x,var[0],var[1],var[2]),label='gaussienne 2 ')
        plt.axvline(x=5*x_2019[b][0][1::].index(a_1)+1,color='red',linestyle='--',label='maximum mis dans fit')

        plt.legend()
        b+=1
    plt.show()
    minute_2019_debut+=7*60*24
    minute_2019_fin+=7*60*24
    minute_2020_debut+=7*60*24
    minute_2020_fin+=7*60*24
    a+=1
