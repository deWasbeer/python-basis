# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 11:54:12 2019

@author: Johan Antonissen
"""

'''
Stap 1: Vraag om waarden

'''
print('Stap 1: Waarden invoeren')
#laten we beginnen met een tekening van het vraagstuk
print('Hieronder is een schets weergegeven van de som wie we willen oplossen:')
print('')
print('/^\ Ra        | F              /^\ Rb')
print(' |            |                 | ')
print(' |           \./                | ')
print('=A==============================B=')
print(' |--> x')
print(' |---------------------L1-------| ')
print(' |-----L2-----|                   ')

#We vragen dr kracht F aan de gebruiker en maken er een float van om er mee te kunnen rekenen
F=float(input('Hoeveel is de kracht (F kN)? '))

#We vragen lengte L1, de totale lengte van de balk en maken er een float van om er mee te kunnen rekenen
L1=float(input('Hoe lang is de balk (L1 m)? '))

#We vragen de afstanf van de kracht tot het beginpunt van de balk
L2=float(input('Op welke afstand van links is de balk belast op kracht (L2 m)? '))

#Nu mag natuurlijk de L2 niet langer zijn dan L1, anders valt de kracht buiten de balk. Dit moeten we dus controleren.
#We gebruiken hier een 'while' statement om de vraag net zo lang te blijven vragen tot onze waarde kloppen.
#Dit is een zogenaamde 'catch functie'
while L2 >= L1:
    print('Kracht L2 moet wel binnen het bereik van L1 liggen he!')
    L2=float(input('Op welke afstand van links is de balk belast op kracht (L2 m)? '))

print()
'''    
Stap 2: bereken de reactiekrachten

'''
print('Stap 2: Matrix rekenen')
#Matrix en vector berekeningen maken we met numpy, laten we eerst dus eens maar numpy erbij halen
import numpy as np
#https://docs.scipy.org/doc/numpy/index.html

#Nu gaan we onze matrix in numpy zetten, we stellen eerst onze krachtbalansen op
#In onze matrix staat:   [[1*Ra+1*Rb],
#                        [0*Ra+L1*Rb]]
matrix_A=np.array([[1,1],[0,L1]])
print('matrix A \n',matrix_A)

#In onze vector staat:  [F,
#                        F*L2]

#Ofwel:                 [1, 1] | [F]
#                       [0,L1] | [F*L2]
vector_b=np.array([F,F*L2])
print('vector b \n',vector_b)

#Nu lossen we de matrix op met lineare algebra:
#https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.solve.html
R=np.linalg.solve(matrix_A,vector_b)

#Het resultaat is onze vector R waarin Ra en Rb zijn verstopt
print('Oplossende vector voor de matrix \n',R)
Ra=R[0]
Rb=R[1]
print('Ofwel: Ra =',Ra,' en Rb =', Rb)

print()
'''
Stap 3: opstellenfuncties nvm lijnen

'''
print('Stap 3: Opstellen functies voor inwendige belasting')
#Functies manipuleren doen we met de scipy (science python) module, laten we deze eerst importeren
#In tegenstelling tot numpy is scipy een verzameling van modulen,
#We moeten dus eerst een module  uit scipy importeren voordat we er een naampje aan kunnen geven
from scipy import integrate as i
#https://docs.scipy.org/doc/scipy/reference/

#We beginnen met het opstellen van onze dwarskrachtlijn.
#Dit is een discontinue functie dus we moeten deze in meerdere stappen beschrijven.

def dwarskrachtlijn(x,F,Ra,Rb,L1,L2):
    #Als (if) x kleiner is dan 0 dan moet er 0 uit de functie komen
    if x < 0:
        V=0.
    #Als dat niet zo is en de x is kleiner dan L2 (elif = else if) dan moet er -Ra uit de functie komen
    #Ofwel 0 < x < L2
    elif x < L2:
        V=-Ra
    #Als dat niet zo is en de x is kleiner dan L1 (elif = else if) dan moet er Rb uit de functie komen
    #Ofwel L2 < x < L1
    elif x < L1:
        V=Rb
    #Voor alle andere waarden (bijvoorbeeld x > L2) moet er natuurlijk weer 0 uit komen
    else:
        V=0.
    return V

#De definitie (ofwel def = functie) beschrijven we met de variabele x, daarna zetten we de constanten neer waarmee we rekenen
def momentlijn(x,F,Ra,Rb,L1,L2):
    #Nu weten we dat het integraal van de dwarskrachtlijn het moment is, laten we dus de dwarskrachtlijn integreren
    #Als (if) x kleiner is dan 0 dan moet er 0 uit de functie komen
    if x < 0:
        M=0.
    #Als x tussen 0 en L1 ligt moet er M uitkomen:
    elif x < L1:
        #Voor het integreren van een enkele integraal gebruiken we de scipy quad functie
        #https://docs.scipy.org/doc/scipy/reference/integrate.html
        #We sturen hier naar quad onze functie voor de dwarskrachtlijn, de eerste integratiegrens (0) en de 2e grens (x)
        #We nemen hier als grens x in plaats van L2 omdat we dan ieder punt tussen 0 en L2 kunnen berekenen ipva alleen L2.
        #De niet-variabelen moeten we doorsturen als zogenaamde arguments (args) zoals beschreven in de documentatie.
        #Ofwel M=scipy.integrate.quad(functie voor moment, linkergrens, rechtergrens, args=(constanten))
        M=i.quad(dwarskrachtlijn,0,x,args=(F,Ra,Rb,L1,L2))
        M=M[0]
    else:
        M=0.
    return M

print()
'''
Stap 4: Berekenen nvm lijnen

'''
print('Stap 4: NVM lijnen berekenen')
#Nu we de functies hebben kunnen we deze berekenen

#We maken eerst een lijstje waar we onze waarden kunnen opslaan
DwarskrachtX=[]
DwarskrachtY=[]
MomentX=[]
MomentY=[]

#laten we in totaal 100 stappen nemen dan is het resultaat erg nouwkeurig.
#We berekenen dus de functies tussen x=0 en x=L2 in een totaal van 100 stappen
stappen=100
#We tellen van 0 tot 100
for stap in range(stappen):
    #We laten x van 0 naar L1 lopen per stap met in een totaal van 100 stappen
    x=L1*stap/stappen
    #We voegen x toe aan onze lijstjes
    DwarskrachtX.append(x)
    MomentX.append(x)
    
    #We berekenen de dwarskracht:
    #We roepen de functie op die we eerst hebben geschreven en sturen daar al onze waarden heen.
    V=dwarskrachtlijn(x,F,Ra,Rb,L1,L2)
    #En voegen V toe aan ons lijstje
    DwarskrachtY.append(V)
    
    #We berekenen nu het moment:
    #We roepen de functie op die we eerst hebben geschreven en sturen daar al onze waarden heen.
    M=momentlijn(x,F,Ra,Rb,L1,L2)
    #En voegen M toe aan ons lijstje
    MomentY.append(M)
    #En we herhalen dit nog een keer

#Laten we eens kijken hoe onze data eruit ziet
print('Dwarskracht:')
print('X=',DwarskrachtX)
print('Y=',DwarskrachtY)

print('Moment:')
print('X=',MomentX)
print('Y=',MomentY)

print()
'''
Stap 5: Tekenen nvm lijnen
'''

print('Stap 5: NVM lijnen tekenen')
#Om echt te weten of we onze data goed hebben berekend moeten we deze natuurlijk visualiser

#We beginnen met het importeren van onze matplotlib module
from  matplotlib import pyplot as plt
#https://matplotlib.org/3.1.1/users/index.html

#Nu tekenen we onze dwarskrachtlijn
plt.plot(DwarskrachtX,DwarskrachtY,color='red')
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

#Nu tekenen we onze momentlijn
#Laten we het maximale moment hierin aangeven
#Dat moeten we eerst uitzoeken waar dat dan is
#Het maximale moment is simpelweg de maximale waarde in de maxY lijst
#Let wel we moet het absolute maximum nemen anders komt er 0 uit en niet ons gezochte maximum!
maxY=max(MomentY,key=abs)
#Voor de x-locatie van het maximum moment moetten we de locatie in de lijst vinden dit doen we met de index functie
lijst_index=MomentY.index(maxY)
#Vervolgens pakken we de die specifieke locatie in de lijst met onze x-waarden
maxX=MomentX[lijst_index]
#Ofwel in totaal:
print('Maxima moment =',maxX,maxY)
#Nu plotten we de reguliere functie en geven hieraan het label 'Moment'
plt.plot(MomentX,MomentY,color='green',label='Moment')
#We plotten hierin het maximum met een rode punt 'ro' en het label 'Maximum'
plt.plot(maxX,maxY,'ro',label='Maximum')
#En we plaatsen de legenda in de grafiek
plt.legend()
#We voegen een titel toe
plt.title('Moment')
#We beschrijven de x-as
plt.xlabel('Lengte balk X (m)')
#We beschrijven de y-as
plt.ylabel('Moment M (kNm)')
#We voegen een rooster toe om dit beter af te lezen
plt.grid()
#We voegen een horizontale x-as toe voor de duidelijkheid met een kleur zwart (k)
plt.axhline(color='black')
#We slaan de plot op als een plaatje
plt.savefig('Moment.png', bbox_inches='tight')
#En we laten het plaatje ook even zien in de console (rechts)
plt.show()
#We maken de plot weer leeg voor de volgende tekening
plt.clf()

print()
'''
Stap 6: Alles samenvoegen
'''

print('Stap 6: Samengestelde tekening')
#Nu is het natuurlijk ook leuk om alle data in 1 tekening te setten samen met een schets van het VLS.
#We creeeren een nieuw figuur met herin 3 plots, links een schets van het VLS en rechts de V em M plot.
fig = plt.figure() 
#We defineren de assen (ax) waar we mee tekenen
ax = fig.gca()
#En beschrijven de grootte van het figuur dat we als uitkomst willen hebben (breedte 8 inch, hoogte 4 inch)
fig.set_size_inches(8, 4)
#Nu bouwen we de 3 deelplots die we willen maken van 2 rijen en 2 kolommen
ax1 = plt.subplot2grid((2, 2), (0, 0), rowspan = 2)     #Plaatje begit linksboven op rij 0 kolom 0 en leeft op 2 rijen
ax2 = plt.subplot2grid((2, 2), (0, 1))                  #V lijn begint rij 0 kolom 1
ax3 = plt.subplot2grid((2, 2), (1, 1))                  #M lijn begint rij 1 kolom 1

# We beschrijven de data van onze VLS tekening
ax1.set_xlabel('x (globaal)',fontsize=10)
ax1.set_ylabel('y (globaal)',fontsize=10)
#We voegen een rooster (tick) toe (De streepjes op de x- en y- as)
ax1.set_yticklabels([])
ax1.set_xticklabels([])
#En beschrijven de limieten van onze tekening
#We maken het plaatje iets groter dan L1 x L1 door de 1.1 factor
ax1.set_xlim(.1*-L1,1.1*L1)
ax1.set_ylim((1.1*-L1/2.,1.1*L1/2.))

# We beschrijven de data van onze dwars en moment lijn
ax2.set_ylabel('Dwars [kN]',fontsize=10)
ax2.axhline(color='black')
ax2.set_yticklabels([])
ax2.set_xticklabels([])
ax2.set_ylim(1.1*max(DwarskrachtY,key=abs),-1.1*max(DwarskrachtY,key=abs))
ax2.set_xlim(0,L1)

ax3.set_ylabel('Moment [kNm]',fontsize=10)
ax3.axhline(color='black')
ax3.set_yticklabels([])
ax3.set_xticklabels([])
ax3.set_ylim(-abs(max(MomentY,key=abs)),abs(max(MomentY,key=abs)))
ax3.set_xlim(0,L1)

#Voor het VLS willen we een vierkant tekenen in onze plot, hiervoor gebruiken we de patches module
import matplotlib.patches as patches
#https://matplotlib.org/3.1.1/api/patches_api.html

breedte=L1
hoogte=L1*.1

#We teken de balk en geven hier eerst het punt linksonder aan vanaf waar we tekenen en dan de breedte en hoogte
balk=patches.Rectangle((0,-hoogte/2.),breedte,hoogte,fill=True, color='grey',ec='black')
ax1.add_patch(balk)
#Nu tekenen we onze drie pijlen op het figuur
#Let op we moeten hier de pijlen parametrisch opzetten anders schalen ze heel raar met de afmetingen van de balk
krachtF=patches.Arrow(L2,0,0,-F/F*breedte/3.,color='red',width=hoogte/2.,ec='black')
krachtRa=patches.Arrow(0,0,0,Ra/F*breedte/3.,color='green',width=hoogte/2.,ec='black')
krachtRb=patches.Arrow(L1,0,0,Rb/F*breedte/3.,color='green',width=hoogte/2.,ec='black')
ax1.add_patch(krachtF)
ax1.add_patch(krachtRa)
ax1.add_patch(krachtRb)

#Nu gaan we onze plots tekenen, laten we beginnen met wat we al weten, de dwars en moment lijn
ax2.plot(DwarskrachtX,DwarskrachtY,color='red')
ax3.plot(MomentX,MomentY,color='green')

plt.savefig('Combi.png', bbox_inches='tight')
plt.show()
plt.clf()