# -*- coding: utf-8 -*-
"""
Created on Tue May 26 14:30:27 2020

@author: AntoJ
"""

import numpy as np
from scipy import integrate as i
from matplotlib import pyplot as plt

print('qVM lijn links ingeklemde balk')

q1=10
q2=20
L1=10
L2=20
Ra=-(q1*(L2-L1)+(q2-q1)*(L2-L1)*.5)
Ma=-(q1*(L2-L1)*(L2-L1)/2+(q2-q1)*(L2-L1)*.5*(L2-L1)*2/3)

# q(x)=a*x+B
# q(L1)=q1
# q(L2)=q2

matrix_A=np.array([[L1,1],[L2,1]])
print('matrix A \n',matrix_A)

vector_b=np.array([-q1,-q2])
print('vector b \n',vector_b)

R=np.linalg.solve(matrix_A,vector_b)

a=R[0]
b=R[1]

stappen=100

qlist=[]
Vlist=[]
Mlist=[]
xlist=[]

def qlijn(x,a,b):
    q=a*x+b
    return q

for stap in range(stappen):
    x=L1+(L2-L1)*stap/stappen
    q=qlijn(x,a,b)
    qlist.append(q)
    xlist.append(x)
    #print(x,q)
    
#Nu tekenen we onze qlijn
plt.plot(xlist,qlist,color='blue')
#We voegen een titel toe
plt.title('Verdeelde Belasting')
#We beschrijven de x-as
plt.xlabel('Lengte balk X (m)')
#We beschrijven de y-as
plt.ylabel('Verdeelde belasting (kN/m)')
#We voegen een rooster toe om dit beter af te lezen
plt.grid()
#We voegen een horizontale x-as toe voor de duidelijkheid met een kleur zwart
plt.axhline(color='black')
#We slaan de plot op als een plaatje
plt.savefig('verdeeldebelasting.png', bbox_inches='tight')
#En we laten het plaatje ook even zien in de console (rechts)
plt.show()
#We maken de plot weer leeg voor de volgende tekening
plt.clf()

def Vlijn(x,a,b,Ra):
    V=Ra-i.quad(lambda x: qlijn(x,a,b),L1,x)[0]
    return V

for stap in range(stappen):
    x=L1+(L2-L1)*stap/stappen
    V=Vlijn(x,a,b,Ra)
    Vlist.append(V)
    #xlist.append(x)
    #print(x,V)

#Nu tekenen we onze dwarskrachtlijn
plt.plot(xlist,Vlist,color='red')
#We voegen een titel toe
plt.title('Dwarskracht')
#We beschrijven de x-as
plt.xlabel('Lengte balk X (m)')
#We beschrijven de y-as
plt.ylabel('Kracht V (kN)')
#We voegen een rooster toe om dit beter af te lezen
plt.grid()
#We voegen een horizontale x-as toe voor de duidelijkheid met een kleur zwart
plt.axhline(color='black')
#We slaan de plot op als een plaatje
plt.savefig('Dwarskracht.png', bbox_inches='tight')
#En we laten het plaatje ook even zien in de console (rechts)
plt.show()
#We maken de plot weer leeg voor de volgende tekening
plt.clf()

def Mlijn(x,a,b,Ra,Ma):
    M=Ma-i.quad(lambda x: Vlijn(x,a,b,Ra),L1, x)[0]
    return M

for stap in range(stappen):
    x=L1+(L2-L1)*stap/stappen
    M=Mlijn(x,a,b,Ra,Ma)
    Mlist.append(M)
    #xlist.append(x)
    #print(x,M)
    
#Nu tekenen we onze momentlijn
plt.plot(xlist,Mlist,color='green')
#We voegen een titel toe
plt.title('Moment')
#We beschrijven de x-as
plt.xlabel('Lengte balk X (m)')
#We beschrijven de y-as
plt.ylabel('Moment (kNm)')
#We voegen een rooster toe om dit beter af te lezen
plt.grid()
#We voegen een horizontale x-as toe voor de duidelijkheid met een kleur zwart
plt.axhline(color='black')
#We slaan de plot op als een plaatje
plt.savefig('Moment.png', bbox_inches='tight')
#En we laten het plaatje ook even zien in de console (rechts)
plt.show()
#We maken de plot weer leeg voor de volgende tekening
plt.clf()