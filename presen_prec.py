import csv
import matplotlib.pyplot as plt
import statistics as ss
import numpy as np

def conv_num(a):
    inc=0
    b=len(a)
    c=[]
    while inc<b:
        c.append(float(a[inc]))
        inc+=1
    return c

def date_corona(ecart_temps='jour'):
    if ecart_temps=='semaine':
        val_x=1
    if ecart_temps=='jour':
        val_x=7
    plt.axvline(x=12*val_x,color='red',linestyle='--',label='1 conf')
    plt.axvline(x=20*val_x,color='red',linestyle='--')
    plt.axvline(x=44*val_x,color='orange',linestyle='--',label='2 conf')
    plt.axvline(x=51*val_x,color='orange',linestyle='--')
    plt.axvline(x=48*val_x,color='green',linestyle='-.',label='deconf')
    plt.axvline(x=42*val_x,color='green',linestyle='-',label='CV')

def comparaison_graph(fichier='comp_p5_jour_prec'):
    "permet d'afficher les graph du facteur gamma et du decallage"
    fichier+='.csv'
    fichier_lecture=open(fichier,'r')
    read=csv.reader(fichier_lecture,delimiter=";",dialect='excel')
    
    #traitement gamma
    row=read.__next__()
    absi=[]
    a=0
    while a<51:
        absi.append(7*a+6)
        absi.append(4+7*a+6)
        absi.append(5+7*a+6)
        a+=1
    print(len(row),len(row)/3,len(absi))
    plt.figure('comparaison',figsize=(12,8))
    plt.subplot(121)
    plt.grid=(True)
    val=conv_num(row)
    plt.title('max gamma factor')
    plt.ylabel('max gamma value')
    plt.plot(absi,val,label='gamma')
    date_corona()
    plt.legend()
    
    #traitement shift
    row=read.__next__()
    plt.subplot(122)
    plt.title('shift in the time of rental')
    plt.ylabel('shift (min)')
    val=conv_num(row)
    plt.plot(absi,val,label='shift')
    date_corona()
    plt.xlabel('weeks')
    plt.legend()
    
    #traitement pluie 2019
    row=read.__next__()
    absi=[]
    a=0
    while a<51:
        absi.append(7*a+7)
        a+=1
    #plt.subplot(212)
    #plt.grid=(True)
    #val=conv_num(row)
    #plt.plot(absi,val,label='pluie 2019')
    
    #pluie 2020
    row=read.__next__()
    #plt.grid=(True)
    #val=conv_num(row)
    #plt.grid=(True)
    #plt.plot(absi,val,label='pluie 2020')
    #date_corona()
    #plt.legend()
    
    a=0
    while a<3:
        if a==0:
            titre="week"
        if a==1:
            titre="friday"
        if a==2:
            titre="week end"
        #traitement vis a vis
        ampl_2019=np.array(conv_num(read.__next__()))
        ampl_2020=np.array(conv_num(read.__next__()))
        x0_2019=np.array(conv_num(read.__next__()))
        x0_2020=np.array(conv_num(read.__next__()))
        sig_2019=conv_num(read.__next__())
        sig_2020=conv_num(read.__next__())
        plt.figure('vis a vis '+titre,figsize=(10,10))
        #plt.errorbar(x0_2019,x0_2020,xerr=sig_2019,yerr=sig_2020,fmt='none',capsize=5,ecolor='red')
        #graph=plt.scatter(x0_2019,x0_2020,c=ampl_2019*max(ampl_2020)/(ampl_2020*max(ampl_2019)),s=0.1,cmap='jet')
        graph=plt.scatter(x0_2019,x0_2020,s=0.5)
        ABSI=[i for i in np.arange(0,24*60,1)]
        plt.plot(ABSI,ABSI,'black')
        #plt.colorbar(graph)
        plt.title(titre)
        plt.xlabel('x0 2019')
        plt.ylabel('x0 2020')
        plt.xlim(left=-100,right=24*60)
        plt.ylim(top=24*60,bottom=-100)
        a+=1
    
    fichier_lecture.close()
    plt.show()
        
def utilisation_graph_comparaison(fichier='graph_p5',choix=[]):
    "permet d'afficher l'utilisation des semaine"
    pourcent=0.75
    if choix!=[]:
        a=0
        while a<len(choix):
            choix[a]=choix[a]-2
            a+=1
    if len(choix)>1:
        controle=0
        while controle<len(choix): #met les semaine das=ns l'ordre croissant
            a=0
            while a<len(choix)-1:
                if choix[a]>choix[a+1]:
                    choix[a],choix[a+1]=choix[a+1],choix[a]
                    controle=0
                else:
                    controle+=1
                a+=1
    fichier+='.csv'
    fichier_lecture=open(fichier,'r')
    read=csv.reader(fichier_lecture,delimiter=";",dialect='excel')
    if choix==[]:
        a=0
        for row in read:
            c=0
            val=[]
            somme=0
            while c<len(row):
                val.append(float(row[c]))
                somme+=val[c]
                c+=1
            val_pourcent=somme*pourcent
            somme=0
            inc_2020=0
            while inc_2020<len(val):
                if val_pourcent<=somme:
                    break
                somme+=val[inc_2020]
                inc_2020+=1
            l=len(val)
            plt.figure(a,figsize=(12,12))
            plt.plot(val,label="2020")
            row=read.__next__()
            c=0
            val=[]
            somme=0
            while c<len(row):
                val.append(float(row[c]))
                somme+=val[c]
                c+=1
            val_pourcent=somme*pourcent
            somme=0
            l=(len(val)-l)//2
            inc_2019=l            
            while inc_2019<len(val[l:len(val)-l]):
                if val_pourcent<=somme:
                    break
                somme+=val[inc_2019]
                inc_2019+=1
            plt.axvline(x=inc_2019-l,color='red',linestyle='--',label='seuil a '+str(100*pourcent)+" annee 2019")
            plt.axvline(x=inc_2020,color='green',linestyle='--',label='seuil a '+str(100*pourcent)+" annee 2020")
            plt.plot(val[l:len(val)-l],label="2019")
            plt.title("week "+str(a+2)+" decallage (nombre point): "+str(inc_2020-(inc_2019-l)))
            plt.legend()
            a+=1
        plt.grid(True)
        plt.show()
        fichier_lecture.close()
    if choix!=[]:
        a=0
        b=0
        while a<len(choix):
            while b<choix[a]:
                read.__next__()
                read.__next__()
                b+=1
            row=read.__next__()
            c=0
            val=[]
            somme=0
            while c<len(row):
                val.append(float(row[c]))
                somme+=val[c]
                c+=1
            val_pourcent=somme*pourcent
            somme=0
            inc_2020=0
            while inc_2020<len(val):
                if val_pourcent<=somme:
                    break
                somme+=val[inc_2020]
                inc_2020+=1
            l=len(val)
            plt.figure("semaine :"+str(choix[a]+2),figsize=(12,12))
            plt.grid(True)
            plt.plot(val,label="2020")
            row=read.__next__()
            c=0
            val=[]
            while c<len(row):
                val.append(float(row[c]))
                c+=1
            val_pourcent=somme*pourcent
            somme=0
            l=(len(val)-l)//2
            inc_2019=l            
            while inc_2019<len(val[l:len(val)-l]):
                if val_pourcent<=somme:
                    break
                somme+=val[inc_2019]
                inc_2019+=1
            plt.axvline(x=inc_2019-l,color='red',linestyle='--',label='seuil a '+str(100*pourcent)+" annee 2019")
            plt.axvline(x=inc_2020,color='green',linestyle='--',label='seuil a '+str(100*pourcent)+" annee 2020")
            plt.title("week "+str(choix[a]+2)+" decallage (nombre point): "+str(inc_2020-(inc_2019-l)))
            plt.plot(val[l:len(val)-l],label="2019")
            plt.legend()
            b+=1
            a+=1
        plt.show()            
        fichier_lecture.close()
    plt.show()

    
def comp_2020(fichier='comp_p5_2020'):
    fichier+='.csv'
    fichier_lecture=open(fichier,'r')
    read=csv.reader(fichier_lecture,delimiter=";",dialect='excel')
    decallage_mean=[]
    decallage_ecart_inf=[]
    decallage_ecart_sup=[]
    gamma_mean=[]
    gamma_ecart_inf=[]
    gamma_ecart_sup=[]
    for row in read:
        a=0
        val=[]
        while a<len(row):
            val.append(float(row[a]))
            a+=1
        gamma_mean.append(ss.mean(val))
        gamma_ecart_inf.append(gamma_mean[len(gamma_mean)-1]-ss.pstdev(val))
        gamma_ecart_sup.append(gamma_mean[len(gamma_mean)-1]+ss.pstdev(val))
        row=read.__next__()
        a=0
        val=[]
        while a<len(row):
            val.append(float(row[a]))
            a+=1
        decallage_mean.append(ss.mean(val))
        decallage_ecart_inf.append(decallage_mean[len(decallage_mean)-1]-ss.pstdev(val))
        decallage_ecart_sup.append(decallage_mean[len(decallage_mean)-1]+ss.pstdev(val))
    plt.figure(figsize=(16,10))
    plt.subplot(121)
    plt.title('max gamma factor')
    plt.plot(gamma_mean,label='mean')
    plt.plot(gamma_ecart_inf,color='c',linestyle='--',label='ecart type')
    plt.plot(gamma_ecart_sup,color='c',linestyle='--')
    plt.axvline(x=12,color='red',linestyle='--',label='1st confinement')
    plt.axvline(x=20,color='red',linestyle='--')
    plt.axvline(x=44,color='orange',linestyle='--',label='2cd confinement')
    plt.axvline(x=51,color='orange',linestyle='--')
    plt.axvline(x=48,color='green',linestyle='-.',label='containment relief')
    plt.axvline(x=42,color='green',linestyle='-',label='curfew')
    plt.legend()
    plt.subplot(122)
    plt.title('shift')
    plt.plot(decallage_mean,label='mean')
    plt.plot(decallage_ecart_inf,color='c',linestyle='--',label='ecart type')
    plt.plot(decallage_ecart_sup,color='c',linestyle='--')
    plt.axvline(x=12,color='red',linestyle='--',label='1st confinement')
    plt.axvline(x=20,color='red',linestyle='--')
    plt.axvline(x=44,color='orange',linestyle='--',label='2cd confinement')
    plt.axvline(x=51,color='orange',linestyle='--')
    plt.axvline(x=48,color='green',linestyle='-.',label='containment relief')
    plt.axvline(x=42,color='green',linestyle='-',label='curfew')
    plt.legend()
    plt.show()
            