import csv
import matplotlib.pyplot as plt
import statistics as ss


def comparaison_graph(fichier=['test']):
    "permet d'afficher les graph du facteur gamma et du decallage"
    a=0
    plt.figure(figsize=(12,12))
    while a<len(fichier):
        fichier[a]+='.csv'
        fichier_lecture=open(fichier[a],'r')
        read=csv.reader(fichier_lecture,delimiter=";",dialect='excel')
        b=121
        for row in read:
            if b==121 or b==122:
                plt.subplot(b)
                plt.grid=(True)
                if b==121:
                    plt.title('max gamma factor')
                    plt.ylabel('max gamma value')
                else:
                    plt.title('shift in the time of rental')
                    plt.ylabel('shift (min)')
                c=0
                val=[]
                ab=[]
                while c<len(row):
                    val.append(float(row[c]))
                    ab.append(c+2)
                    c+=1
                plt.plot(ab,val,label=fichier[a])
                plt.axvline(x=12*7,color='red',linestyle='--',label='1st confinement')
                plt.axvline(x=20*7,color='red',linestyle='--')
                plt.axvline(x=44*7,color='orange',linestyle='--',label='2cd confinement')
                plt.axvline(x=51*7,color='orange',linestyle='--')
                plt.axvline(x=48*7,color='green',linestyle='-.',label='containment relief')
                plt.axvline(x=42*7,color='green',linestyle='-',label='curfew')
                plt.xlabel('weeks')
                plt.legend()
            b+=1
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
            