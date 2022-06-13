#Import des librairies

import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils
ff1.Cache.enable_cache('D:\Data analyst\Jedha\Projet\Projet F1\doc_cache')
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
pio.templates.default = "plotly_dark"
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import requests

import pandas as pd

# Définition des variables

# Course ??
tourTot = 78
perteArret = 25


#Génère le nombre de tour avec 2 arrêts

liste =[]
df_combi = pd.DataFrame(columns=['Train1', 'Train2', 'Train3'])

for i in range(1,tourTot-1):
    T1 = i
    
    
    for j in range(1, tourTot-1):
        
        if (i+j) > tourTot-1:
            continue
        T2 = j
        T3 = tourTot - j - i
        df_combi = df_combi.append({'Train1' : T1, 'Train2' : T2, 'Train3' : T3}, ignore_index = True)
        
        
#Génère le nombre de tour avec 1 arrêt

liste =[]
df_combi2 = pd.DataFrame(columns=['Train1', 'Train2'])

for i in range(1,tourTot):

    T1 = i
    T2 = tourTot-i
    df_combi2 = df_combi2.append({'Train1' : T1, 'Train2' : T2}, ignore_index = True)
        

# Ouvre le csv avec le temps par tour et type de pneu
dffp_complet = pd.read_csv('D:\Data analyst\Jedha\Projet\Projet F1\Data\dffp_complet.csv', sep = ";")
dffp_complet.head()


# Mets les temps sous forme de tableau

dffp_soft = dffp_complet[dffp_complet['Compound']=='SOFT']
dffp_soft.drop(columns = ['Compound'], inplace = True)
dffp_soft.rename(columns={'LapTime': 'S'}, inplace = True)

dffp_medium = dffp_complet[dffp_complet['Compound']=='MEDIUM']
dffp_medium.drop(columns = ['Compound'], inplace = True)
dffp_medium.rename(columns={'LapTime': 'M'}, inplace = True)

dffp_hard = dffp_complet[dffp_complet['Compound']=='HARD']
dffp_hard.drop(columns = ['Compound'], inplace = True)
dffp_hard.rename(columns={'LapTime': 'H'}, inplace = True)

dffp_final = dffp_soft.merge(dffp_medium, how = 'inner', left_on = 'tyreLife', right_on = 'tyreLife' )
dffp_final = dffp_final.merge(dffp_hard, how = 'inner', left_on = 'tyreLife', right_on = 'tyreLife' )


#Ouvre le csv avec les combinaisons pour 1 arrêts
tyreCombi2 = pd.read_csv('D:\Data analyst\Jedha\Projet\Projet F1\Data\TyreCombi2.csv', sep = ";")


#Ouvre le csv avec les combinaisons pour 2 arrêts
tyreCombi3 = pd.read_csv('D:\Data analyst\Jedha\Projet\Projet F1\Data\TyreCombi3.csv', sep = ";")



# Boucle sur tous les types de pneu pour 2 arrêts afin de générer tous les temps totaux pour la course

time1 = 0
time2 = 0
time3 = 0
listeT = []
liste_combi = []
df_timerace3 = pd.DataFrame(columns=['combiTyre','Train1', 'Train2', 'Train3','TimeT1', 'TimeT2', 'TimeT3', 'Total_time'])
df_timeracebis = pd.DataFrame(columns=['combiTyre','Train1', 'Train2', 'Train3','TimeT1', 'TimeT2', 'TimeT3', 'Total_time'])
df_timeraceter = pd.DataFrame(columns=['combiTyre','Train1', 'Train2', 'Train3','TimeT1', 'TimeT2', 'TimeT3', 'Total_time'])
df_timerace3= df_timeraceter

#Boucle sur le df tyre_combi

for a in range(0,len(tyreCombi3)):
    lig = a
    df_timeracebis = df_timeraceter

    # Calcul du T1 en fonction du type de pneu 
    col = 0
    liste_combi = []
    liste_combi.append(tyreCombi3.iloc[lig,col])
    
    if tyreCombi3.iloc[lig,col] == 'S':
        colT = 1
    elif tyreCombi3.iloc[lig,col] == 'M':
        colT = 2
    else :
        colT = 3
         
    #Boucle sur la longueur du df
    for l in range(len(df_combi)):
        #nombre de tour égal à la valeur de la 1ère colonne
        nbTour = df_combi.iloc[l,0]
            
        #Addition des nbTours premières lignes
            
        for i in range(nbTour): #J'itère autant de fois qu'il y a de tours
            time1 = time1 + dffp_final.iloc[i,colT]      
            
        df_timeracebis = df_timeracebis.append({'TimeT1' : time1}, ignore_index = True)
        df_timeracebis.iloc[l,1] = nbTour
        time1 = 0
        
        
# Calcul du T2 en fonction du type de pneu          
        
    col = 1
    liste_combi.append(tyreCombi3.iloc[lig,col])
    
    if tyreCombi3.iloc[lig,col] == 'S':
        colT = 1
    elif tyreCombi3.iloc[lig,col] == 'M':
        colT = 2
    else :
        colT = 3
        
        
    #Boucle sur la longueur du df    
    for l in range(len(df_combi)):
        #nombre de tour égal à la valeur de la 1ère colonne
        nbTour = df_combi.iloc[l,1]
        
        #Addition des nbTours premières lignes
        
        for i in range(nbTour): #J'itère autant de fois qu'il y a de tours
            time2 = time2 + dffp_final.iloc[i,colT]
            
        df_timeracebis.iloc[l,5]=time2
        df_timeracebis.iloc[l,2] = nbTour
        time2 = 0
        
        
# Calcul du T3 en fonction du type de pneu    
    
    col = 2
    liste_combi.append(tyreCombi3.iloc[lig,col])
    
    if tyreCombi3.iloc[lig,col] == 'S':
        colT = 1
    elif tyreCombi3.iloc[lig,col] == 'M':
        colT = 2
    else :
        colT = 3
        
    
    #Boucle sur la longueur du df    
    for l in range(len(df_combi)):
        #nombre de tour égal à la valeur de la 1ère colonne
        nbTour = df_combi.iloc[l,2]
        
        #Addition des nbTours premières lignes
        
        for i in range(nbTour): #J'itère autant de fois qu'il y a de tours
            time3 = time3 + dffp_final.iloc[i,colT]
            
        df_timeracebis.iloc[l,6]=time3
        df_timeracebis.iloc[l,3] = nbTour
        time3 = 0
        
        df_timeracebis.iloc[l,0] = "".join(liste_combi)

    df_timerace3 = pd.concat([df_timerace3,df_timeracebis], ignore_index = True)

#Calcul du temps total
df_timerace3['Total_time'] = df_timerace3['TimeT1'] + df_timerace3['TimeT2'] + df_timerace3['TimeT3'] + ( 2 * perteArret)


# Boucle sur tous les types de pneu pour 2 arrêts afin de générer tous les temps totaux pour la course

time1 = 0
time2 = 0
time3 = 0
listeT = []
liste_combi = []
df_timerace2 = pd.DataFrame(columns=['combiTyre','Train1', 'Train2', 'Train3','TimeT1', 'TimeT2', 'TimeT3', 'Total_time'])
df_timeracebis = pd.DataFrame(columns=['combiTyre','Train1', 'Train2', 'Train3','TimeT1', 'TimeT2', 'TimeT3', 'Total_time'])
df_timeracequa = pd.DataFrame(columns=['combiTyre','Train1', 'Train2', 'Train3','TimeT1', 'TimeT2', 'TimeT3', 'Total_time'])
df_timerace2 = df_timeracequa

#Boucle sur le df tyre_combi

for a in range(0,len(tyreCombi2)):
    lig = a
    df_timeracebis = df_timeraceter

    # Calcul du T1 en fonction du type de pneu 
    col = 0
    liste_combi = []
    liste_combi.append(tyreCombi2.iloc[lig,col])
    
    if tyreCombi2.iloc[lig,col] == 'S':
        colT = 1
    elif tyreCombi2.iloc[lig,col] == 'M':
        colT = 2
    else :
        colT = 3
         
    #Boucle sur la longueur du df
    for l in range(len(df_combi2)):
        #nombre de tour égal à la valeur de la 1ère colonne
        nbTour = df_combi2.iloc[l,0]
            
        #Addition des nbTours premières lignes
            
        for i in range(nbTour): #J'itère autant de fois qu'il y a de tours
            time1 = time1 + dffp_final.iloc[i,colT]      
            
        df_timeracebis = df_timeracebis.append({'TimeT1' : time1}, ignore_index = True)
        df_timeracebis.iloc[l,1] = nbTour
        time1 = 0
        
        
# Calcul du T2 en fonction du type de pneu          
        
    col = 1
    liste_combi.append(tyreCombi2.iloc[lig,col])
    
    if tyreCombi2.iloc[lig,col] == 'S':
        colT = 1
    elif tyreCombi2.iloc[lig,col] == 'M':
        colT = 2
    else :
        colT = 3
        
        
    #Boucle sur la longueur du df    
    for l in range(len(df_combi2)):
        #nombre de tour égal à la valeur de la 2ème colonne
        nbTour = df_combi2.iloc[l,1]
        
        #Addition des nbTours premières lignes
        
        for i in range(nbTour): #J'itère autant de fois qu'il y a de tours
            time2 = time2 + dffp_final.iloc[i,colT]
            
        df_timeracebis.iloc[l,5]=time2
        df_timeracebis.iloc[l,2] = nbTour
        time2 = 0
        
        
# Génération du Train3 et Time3 à 0    
  
    
    #Boucle sur la longueur du df    
    for l in range(len(df_combi2)):        
            
        df_timeracebis.iloc[l,6]=0
        df_timeracebis.iloc[l,3] = 0
        
        
        df_timeracebis.iloc[l,0] = "".join(liste_combi)

    df_timerace2 = pd.concat([df_timerace2,df_timeracebis], ignore_index = True)

#Calcul du temsp total
df_timerace2['Total_time'] = df_timerace2['TimeT1'] + df_timerace2['TimeT2'] + df_timerace2['TimeT3']  + ( perteArret)


#Concatène les 2 df
df_timerace = pd.concat([df_timerace2,df_timerace3], ignore_index = True)

# Affiche les 10 combinaisons les plus performantes
df_timerace.sort_values(['Total_time'], ascending=True).head(10)