# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 03:19:19 2021

@author: denis
"""

import numpy as np
from random import randint, random
from numpy.random import shuffle
import matplotlib.pyplot as plt
from math import exp, floor, log
import pandas as pd
from scipy.stats import f_oneway



def rotura(x, c, d):
    return 1 / (1 + exp((c - x) / d))
 
def union(x, c):
    return exp(-x / c)
 

 
def romperse(tam, cuantos):
    if tam == 1: # no se puede romper
        return [tam] * cuantos
    res = []
    for cumulo in range(cuantos):
        if random() < rotura(tam, c, d):
            primera = randint(1, tam - 1)
            segunda = tam - primera
            assert primera > 0
            assert segunda > 0
            assert primera + segunda == tam
            res += [primera, segunda]
        else:
            res.append(tam) # no rompió
    assert sum(res) == tam * cuantos
    return res
 
def unirse(tam, cuantos):
    res = []
    for cumulo in range(cuantos):
        if random() < union(tam, c):
            res.append(-tam) # marcamos con negativo los que quieren unirse
        else:
            res.append(tam)
    return res

def filtro(cumulos, c, n):
    cum = []
    for valor in cumulos:
        if valor >= c:
            cum.append(valor)
    porcentaje = (sum(cum)*100)/n
    return porcentaje

eps = 0.5
k = 1000
ns = [16000,32000,64000,128000]
# porc = []

replica = 15
repeticion = 15
post = [],[],[]
pm = [],[],[]
vm = [],[],[]
for n in ns: 
    porct = []
    pos = [],[],[]
    for repet in range(repeticion):
        for r in range(replica):
            porc = []
            orig = np.random.normal(size = k)
            cumulos = orig - min(orig)
            cumulos += eps # ahora el menor vale epsilon
            cumulos = cumulos / sum(cumulos) # ahora suman a uno
            cumulos *= n # ahora suman a n, pero son valores decimales
            cumulos = np.round(cumulos).astype(int) # ahora son enteros
            diferencia = n - sum(cumulos) # por cuanto le hemos fallado
            cambio = 1 if diferencia > 0 else -1
            while diferencia != 0:
                p = randint(0, k - 1)
                if cambio > 0 or (cambio < 0 and cumulos[p] > 0): # sin vaciar
                    cumulos[p] += cambio
                    diferencia -= cambio
            assert (all([c != 0 for c in cumulos])) 
            assert sum(cumulos) == n
             
            c = np.median(cumulos) # tamaño crítico de cúmulos
            d = np.std(cumulos) / 4 # factor arbitrario para suavizar la curva
             
            duracion = 50
            digitos = floor(log(duracion, 10)) + 1
            c1 = 0.2*max(cumulos)
            c2 = np.median(cumulos)
            c3 = 0.8*max(cumulos)
            ct = [c1,c2,c3]
            cm=[]
            cumulosn=cumulos
            for c in ct:
                porc = []
                cumulos = cumulosn
                for paso in range(duracion):
                    
                    assert sum(cumulos) == n
                    assert (all([c > 0 for c in cumulos])) 
                    (tams, freqs) = np.unique(cumulos, return_counts = True)
                    cumulos = []
                    assert len(tams) == len(freqs)
                    for i in range(len(tams)):
                        cumulos += romperse(tams[i], freqs[i]) 
                    assert sum(cumulos) == n
                    assert (all([c > 0 for c in cumulos])) 
                    (tams, freqs) = np.unique(cumulos, return_counts = True)
                    cumulos = []
                    assert len(tams) == len(freqs)
                    for i in range(len(tams)):
                        cumulos += unirse(tams[i], freqs[i])
                    cumulos = np.asarray(cumulos)
                    neg = cumulos < 0
                    a = len(cumulos)
                    juntarse = -1 * np.extract(neg, cumulos) # sacarlos y hacerlos positivos
                    cumulos = np.extract(~neg, cumulos).tolist() # los demás van en una lista
                    assert a == len(juntarse) + len(cumulos)
                    nt = len(juntarse)
                    if nt > 1:
                        shuffle(juntarse) # orden aleatorio
                    j = juntarse.tolist()
                    while len(j) > 1: # agregamos los pares formados
                        cumulos.append(j.pop(0) + j.pop(0))
                    if len(j) > 0: # impar
                        cumulos.append(j.pop(0)) # el ultimo no alcanzó pareja
                    assert len(j) == 0
                    assert sum(cumulos) == n
                    assert (all([c != 0 for c in cumulos]))
    
                    porc.append(filtro(cumulos, c, n))
                cm.append(porc)
            porct.append(cm)
        P1 = []
        for x in range(len(porct)):
            P = porct[x][0]
            P1.append(P)
        P2 = []
        for x in range(len(porct)):
            P = porct[x][1]
            P2.append(P)
        P3 = []
        for x in range(len(porct)):
            P = porct[x][2]
            P3.append(P)
            
        PT1 = []
        for m in range(duracion):
            P = []
            for row in range(len(P1)):
                P.append(P1[row][m])
            PT1.append(P)
        
        PT2 = []
        for m in range(duracion):
            P = []
            for row in range(len(P1)):
                P.append(P2[row][m])
            PT2.append(P)
        
        PT3 = []
        for m in range(duracion):
            P = []
            for row in range(len(P1)):
                P.append(P3[row][m])
            PT3.append(P)
       
        
        
        medianas = [np.median(PT1[x]) for x in range(duracion)]  
        maximo  = max(medianas)
        posicion = medianas.index(max(medianas))+1
        pos[0].append(posicion)
        
        medianas = [np.median(PT2[x]) for x in range(duracion)]  
        maximo  = max(medianas)
        posicion = medianas.index(max(medianas))+1
        pos[1].append(posicion)
        
        medianas = [np.median(PT3[x]) for x in range(duracion)]  
        maximo  = max(medianas)
        posicion = medianas.index(max(medianas))+1
        pos[2].append(posicion)
        
    for j in range(3):    
        post[j].append(pos[j])
        mejor = 0
        for p in pos[j]:
            valor = pos[j].count(p)
            if valor > mejor:
                mejor = valor
                mejorv = p
            
        vm[j].append(mejorv)
        pm[j].append((mejor*100)/repeticion)

        plt.plot(pos[j])
        plt.ylabel('Iteración ideal')
        plt.xlabel('Repetición')
        plt.savefig('p8_v2_r1_c'+str(j)+'_n'+str(n)+'.png', dpi=300)
        plt.show()
        plt.close()
estadistica = f_oneway(post[0][0],post[1][0],post[2][0])
estadistica1 = f_oneway(post[0][1],post[1][1],post[2][1])
estadistica2 = f_oneway(post[0][2],post[1][2],post[2][2])
estadistica3 = f_oneway(post[0][3],post[1][3],post[2][3])

print(estadistica)
print(estadistica1)
print(estadistica2)
print(estadistica3)
# print(post)
# print(post[0][0],post[1][0],post[2][0])
graf = [post[0][0],post[1][0],post[2][0]],[post[0][1],post[1][1],post[2][1]],[post[0][2],post[1][2],post[2][2]],[post[0][3],post[1][3],post[2][3]]
for j in range(3):   
    plt.boxplot(graf[j])
    plt.ylabel('Iteración ideal')
    plt.xlabel('Punto critico')
    plt.xticks([1,2,3], ['C1', 'C2', 'C3'])
    plt.savefig('p8_v2_r1_c'+str(j)+'_n'+str(n)+'.png', dpi=300)
    plt.show()
    plt.close()
    
df = pd.DataFrame()
df['particulas']=ns
df['mejor valor c1']=vm[0]
df['mejor valor c2']=vm[1]
df['mejor valor c3']=vm[2]
df['porcentaje c1']=pm[0]
df['porcentaje c2']=pm[1]
df['porcentaje c3']=pm[2]
df.to_csv('tabla_de_mejor_v2.csv')