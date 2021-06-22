import numpy as np
import matplotlib.pyplot as plt
import csv

def conv_num(a):
    inc=0
    b=len(a)
    c=[]
    while inc<b:
        c.append(float(a[inc]))
        inc+=1
    return c

def date_corona(ecart_temps='semaine'):
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


def pres_comp_distrib(fichier='comp_distrib_p1440_vitesse'):
    fichier+='.csv'
    fichier_lecture=open(fichier,'r')
    read=csv.reader(fichier_lecture,delimiter=";",dialect='excel')

    plt.figure('comparaison',figsize=(16,10))
    plt.subplot(121)
    #plt.grid(True)
    plt.title('gamma')
    l_v_2020=conv_num(read.__next__()) #lecture gamma
    l_d_2020=conv_num(read.__next__())
    l_t_2020=conv_num(read.__next__())
    plt.plot(l_v_2020,label='v')
    plt.plot(l_d_2020,label='d')
    plt.plot(l_t_2020,label='t')
    date_corona()
    plt.legend()


    plt.subplot(222)
    plt.grid(True)
    plt.title('shift')
    l_v_2020=conv_num(read.__next__()) #lecture Cab
    l_d_2020=conv_num(read.__next__())
    l_t_2020=conv_num(read.__next__())
    v_2019=np.array(conv_num(read.__next__())) #lecture shift fit 2019
    d_2019=np.array(conv_num(read.__next__()))
    t_2019=np.array(conv_num(read.__next__()))
    v_2020=np.array(conv_num(read.__next__())) #lecture shift fit 2020
    d_2020=np.array(conv_num(read.__next__()))
    t_2020=np.array(conv_num(read.__next__()))
    plt.plot(l_v_2020,label='v cor')
    #plt.plot(v_2019-v_2020,label='v fit')
    plt.plot(l_t_2020,label='t cor')
    #plt.plot(t_2019-t_2020,label='t fit')
    date_corona()
    plt.legend()
    plt.subplot(224)
    plt.title('shift (distance)')
    plt.grid(True)
    plt.plot(l_d_2020,label='cor')
    #plt.plot(d_2019-d_2020,label='fit')
    date_corona()
    plt.legend()

    plt.figure('valeur fit x0',figsize=(16,10))
    plt.subplot(121)
    plt.grid(True)
    plt.title('valeur x0')
    plt.plot(v_2019,label='v 2019')
    plt.plot(v_2020,label='v 2020')
    plt.plot(t_2019,label='t 2019')
    plt.plot(t_2020,label='t 2020')
    date_corona()
    plt.legend()
    plt.subplot(122)
    plt.title('valeur x0 (distance)')
    plt.grid(True)
    plt.plot(d_2019,label='2019')
    plt.plot(d_2020,label='2020')
    date_corona()
    plt.legend()

    plt.figure("sert a rien")
    plt.subplot(222)
    plt.grid(True)
    plt.title('A_2020/A_2019')
    plt.plot(conv_num(read.__next__()),label='v')
    plt.plot(conv_num(read.__next__()),label='d')
    plt.plot(conv_num(read.__next__()),label='t')
    date_corona()
    plt.legend()

    #ajouté
    plt.subplot(224)
    plt.grid(True)
    plt.title('A_0/A_max')
    plt.plot(conv_num(read.__next__()),label='v 2019') #lecture amplitude 2019
    plt.plot(conv_num(read.__next__()),label='d 2019')
    plt.plot(conv_num(read.__next__()),label='t 2019')
    plt.plot(conv_num(read.__next__()),label='v 2020')
    plt.plot(conv_num(read.__next__()),label='d 2020')
    plt.plot(conv_num(read.__next__()),label='t 2020')
    date_corona()
    plt.legend()

    plt.figure('valeur sigma',figsize=(16,10))
    v_2019=np.array(conv_num(read.__next__()))
    d_2019=np.array(conv_num(read.__next__()))
    t_2019=np.array(conv_num(read.__next__()))
    v_2020=np.array(conv_num(read.__next__()))
    d_2020=np.array(conv_num(read.__next__()))
    t_2020=np.array(conv_num(read.__next__()))
    plt.subplot(121)
    plt.grid(True)
    plt.title('valeur sigma')
    plt.plot(v_2019,label='v 2019')
    plt.plot(v_2020,label='v 2020')
    plt.plot(t_2019,label='t 2019')
    plt.plot(t_2020,label='t 2020')
    date_corona()
    plt.legend()
    plt.subplot(122)
    plt.grid(True)
    plt.title('valeur sigma (distance)')
    plt.plot(d_2019,label='2019')
    plt.plot(d_2020,label='2020')
    date_corona()
    plt.legend()

    #plt.subplot(122)
    #plt.grid(True)
    #plt.title('rapport sigma 2020/2019')
    #plt.plot(v_2020/v_2019,label='v')
    #plt.plot(d_2020/d_2019,label='d')
    #plt.plot(t_2020/t_2019,label='t')
    #date_corona()
    #plt.legend()

    plt.show()
