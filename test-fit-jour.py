import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def gaus(x,a_1,a_2,a_3,a_4,a_5,x0_1,x0_2,x0_3,x0_4,x0_5,sigma_1,sigma_2,sigma_3,sigma_4,sigma_5):
    return a_1*np.exp(-(x-x0_1)**2/(2*sigma_1**2))+a_2*np.exp(-(x-x0_2)**2/(2*sigma_2**2))+a_3*np.exp(-(x-x0_3)**2/(2*sigma_3**2))+a_4*np.exp(-(x-x0_4)**2/(2*sigma_4**2))+a_5*np.exp(-(x-x0_5)**2/(2*sigma_5**2))

def gaus_1(x,a_1,x0_1,sigma_1):
    return a_1*np.exp(-(x-x0_1)**2/(2*sigma_1**2))

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


fichier='graph_p5_jour.csv'
fichier_lecture=open(fichier,'r')
read=csv.reader(fichier_lecture,delimiter=";",dialect='excel')
date_2019=6*24*60
date_2020=5*24*60
pas=5
for row in read:
    mat=conv_num(row)
    a_1=max(mat[0:11*60//5])
    a_2=max(mat[11*60//5:13*60//5])
    a_3=max(mat[13*60//5:15*60//5])
    a_4=max(mat[15*60//5:21*60//5])
    a_5=max(mat[21*60//5::])
    date,_,_=conv_date(date_2020,'2020')
    absi_x=[i for i in np.arange(0,5*len(mat),5)]
    var,_=curve_fit(gaus,absi_x,mat,p0=[a_1,a_2,a_3,a_4,a_5,5*mat[0:11*60//5].index(a_1),5*(mat[11*60//5:13*60//5].index(a_2)+11*60//5),5*(mat[13*60//5:15*60//5].index(a_3)+13*60//5),5*(mat[15*60//5:21*60//5].index(a_4)+15*60//5),5*(mat[21*60//5::].index(a_5)+15*60//5),1,1,1,1,1],maxfev=int(1e7))
    plt.figure('2020',figsize=(10,10))
    plt.subplot(211)
    plt.title(date+' 2020')
    plt.plot(absi_x,mat,label='original 2020')
    plt.axvline(x=5*mat[0:11*60//5].index(a_1),color='red',linestyle='--',label='maximum mis dans fit')
    plt.axvline(x=5*(mat[11*60//5:13*60//5].index(a_2)+11*60//5),color='red',linestyle='--')
    plt.axvline(x=5*(mat[13*60//5:15*60//5].index(a_3)+13*60//5),color='red',linestyle='--')
    plt.axvline(x=5*(mat[15*60//5:21*60//5].index(a_4)+15*60//5),color='red',linestyle='--')
    plt.axvline(x=5*(mat[21*60//5::].index(a_5)+15*60//5),color='red',linestyle='--')

    plt.axvline(x=5*11*60/5,color='green',linestyle='--',label='séparation crenaux')
    plt.axvline(x=5*13*60/5,color='green',linestyle='--')
    plt.axvline(x=5*15*60/5,color='green',linestyle='--')
    plt.axvline(x=5*21*60/5,color='green',linestyle='--')

    plt.plot(absi_x,gaus(absi_x,var[0],var[1],var[2],var[3],var[4],var[5],var[6],var[7],var[8],var[9],var[10],var[11],var[12],var[13],var[14]),label='fit 2020')
    plt.legend()

    plt.subplot(212)
    plt.title('tracer gaussienne')
    plt.plot(absi_x,gaus_1(absi_x,var[0],var[5],var[10]),label='gaussienne 1')
    plt.plot(absi_x,gaus_1(absi_x,var[1],var[6],var[11]),label='gaussienne 2')
    plt.plot(absi_x,gaus_1(absi_x,var[2],var[7],var[12]),label='gaussienne 3')
    plt.plot(absi_x,gaus_1(absi_x,var[3],var[8],var[13]),label='gaussienne 4')
    plt.plot(absi_x,gaus_1(absi_x,var[4],var[9],var[14]),label='gaussienne 5')
    plt.axvline(x=5*mat[0:11*60//5].index(a_1),color='red',linestyle='--')
    plt.axvline(x=5*(mat[11*60//5:13*60//5].index(a_2)+11*60//5),color='red',linestyle='--')
    plt.axvline(x=5*(mat[13*60//5:15*60//5].index(a_3)+13*60//5),color='red',linestyle='--')
    plt.axvline(x=5*(mat[15*60//5:21*60//5].index(a_4)+15*60//5),color='red',linestyle='--')
    plt.axvline(x=5*(mat[21*60//5::].index(a_5)+21*60//5),color='red',linestyle='--')

    plt.axvline(x=5*11*60/5,color='green',linestyle='--')
    plt.axvline(x=5*13*60/5,color='green',linestyle='--')
    plt.axvline(x=5*15*60/5,color='green',linestyle='--')
    plt.axvline(x=5*21*60/5,color='green',linestyle='--')
    plt.legend()

    row=read.__next__()
    mat=conv_num(row)
    print(6*60/5,11*60/5,13*60/5,15*60/5)
    a_1=max(mat[0:(3+11)*60//5])
    a_2=max(mat[(3+11)*60//5:(3+13)*60//5])
    a_3=max(mat[(3+13)*60//5:(3+15)*60//5])
    a_4=max(mat[(3+15)*60//5:(3+21)*60//5])
    a_5=max(mat[(3+21)*60//5::])
    absi_x=[i for i in np.arange(0,5*len(mat),5)]
    var,_=curve_fit(gaus,absi_x,mat,p0=[a_1,a_2,a_3,a_4,a_5,5*mat[0:(3+11)*60//5].index(a_1),5*(mat[(3+11)*60//5:(3+13)*60//5].index(a_2)+(3+11)*60//5),5*(mat[(3+13)*60//5:(3+15)*60//5].index(a_3)+(3+13)*60//5),5*(mat[(3+15)*60//5:(3+21)*60//5].index(a_4)+(3+15)*60//5),5*(mat[(3+21)*60//5::].index(a_5)+(3+21)*60//5),3,3,3,3,3],maxfev=int(1e7))
    plt.figure('2019',figsize=(10,10))
    plt.subplot(211)
    date,_,_=conv_date(date_2019,'2019')
    plt.title(date+' 2019')
    plt.plot(absi_x,mat,label='original 2019')
    plt.plot(absi_x,gaus(absi_x,var[0],var[1],var[2],var[3],var[4],var[5],var[6],var[7],var[8],var[9],var[10],var[11],var[12],var[13],var[14]),label='fit 2019')
    plt.axvline(x=5*mat[0:(3+11)*60//5].index(a_1),color='red',linestyle='--',label='maximum mis dans fit')
    plt.axvline(x=5*(mat[(3+11)*60//5:(3+13)*60//5].index(a_2)+(3+11)*60//5),color='red',linestyle='--')
    plt.axvline(x=5*(mat[(3+13)*60//5:(3+15)*60//5].index(a_3)+(3+13)*60//5),color='red',linestyle='--')
    plt.axvline(x=5*(mat[(3+15)*60//5:(3+21)*60//5].index(a_4)+(3+15)*60//5),color='red',linestyle='--')
    plt.axvline(x=5*(mat[(3+21)*60//5::].index(a_5)+(3+21)*60//5),color='red',linestyle='--')

    plt.axvline(x=5*(3+11)*60/5,color='green',linestyle='--',label='séparation crenaux')
    plt.axvline(x=5*(3+13)*60/5,color='green',linestyle='--')
    plt.axvline(x=5*(3+15)*60/5,color='green',linestyle='--')
    plt.axvline(x=5*(3+21)*60/5,color='green',linestyle='--')

    plt.legend()

    plt.subplot(212)
    plt.title('tracer gaussienne')
    plt.plot(absi_x,gaus_1(absi_x,var[0],var[5],var[10]),label='gaussienne 1')
    plt.plot(absi_x,gaus_1(absi_x,var[1],var[6],var[11]),label='gaussienne 2')
    plt.plot(absi_x,gaus_1(absi_x,var[2],var[7],var[12]),label='gaussienne 3')
    plt.plot(absi_x,gaus_1(absi_x,var[3],var[8],var[13]),label='gaussienne 4')
    plt.plot(absi_x,gaus_1(absi_x,var[4],var[9],var[14]),label='gaussienne 5')

    plt.axvline(x=5*mat[0:(3+11)*60//5].index(a_1),color='red',linestyle='--')
    plt.axvline(x=5*(mat[(3+11)*60//5:(3+13)*60//5].index(a_2)+(3+11)*60//5),color='red',linestyle='--')
    plt.axvline(x=5*(mat[(3+13)*60//5:(3+15)*60//5].index(a_3)+(3+13)*60//5),color='red',linestyle='--')
    plt.axvline(x=5*(mat[(3+15)*60//5::].index(a_4)+(3+15)*60//5),color='red',linestyle='--')

    plt.axvline(x=5*(3+11)*60/5,color='green',linestyle='--')
    plt.axvline(x=5*(3+13)*60/5,color='green',linestyle='--')
    plt.axvline(x=5*(3+15)*60/5,color='green',linestyle='--')

    plt.legend()

    date_2019+=24*60
    date_2020+=24*60

    plt.legend()
    plt.show()
