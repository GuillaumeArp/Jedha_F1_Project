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


#Récupération du csv avec les points au championnat

drivers_standings = pd.read_csv('D:\Data analyst\Jedha\Projet\Projet F1\Data\drivers_standings.csv', index_col = 0)


#Récupération des noms et des couleurs à partir d'une course

race = ff1.get_session(2022, 3, 'R')
race.load()
df_race = race.results
df_race.drop(columns=["Position", "GridPosition", "Q1", "Q2", "Q3", "Time", "Status", "Points"],inplace=True)
df_race.reset_index()


#Jointure entre les deux dataframe

df_class = df_race.merge(drivers_standings, how='right', left_on = ['Abbreviation'], right_index = True).reset_index()


#Modifie le dataframe pour avoir les courses en lignes

nb = len(drivers_standings.transpose())+1
df_final = pd.DataFrame(columns=['DriverNumber', 'BroadcastName', 'Abbreviation', 'TeamName', 'TeamColor', 'FirstName', 'LastName', 'FullName','Points', 'Race'])
for i in range(1,nb):
    df_class_ligne = df_class.loc[:,['DriverNumber', 'BroadcastName', 'Abbreviation', 'TeamName', 'TeamColor', 'FirstName', 'LastName', 'FullName',str(i)]]
    df_class_ligne['Race'] = i
    df_class_ligne.rename(columns={str(i): 'Points'}, inplace = True)
    df_final = pd.concat([df_final, df_class_ligne])
    
df_final.reset_index(drop = True, inplace = True)


#Ajoute une colonne classement avec la position au championnat à l'issue de chaque course

df_final = df_final.sort_values(by=['Race', 'Points'], ascending = [True, False])
df_final['classement']=0
longueur = len(df_final)
df_final.iloc[0,10] = 1

for i in range(1,longueur -1):
    if df_final.iloc[i,9] == df_final.iloc[i-1,9]:
        df_final.iloc[i,10] = df_final.iloc[i-1,10] +  1
    else :
        df_final.iloc[i,10] = 1
        
        
# Paramétrage du dictionnaire des couleurs

colorMap ={}
df_class = pd.DataFrame(df_class)

for i in df_class.itertuples() :
    if i.Abbreviation == 'HUL' :
        colorMap[i.Abbreviation] = '#' + '2d826d'
    else :
        colorMap[i.Abbreviation] = '#' + i.TeamColor
        
        
#Création du graphique


def champ_pos(df_final):
    df_final = df_final.sort_values(by=['Race', 'classement'], ascending = [True, True])

    maxY = df_final['Points'].max() + 20

    fig = px.bar(df_final, x="Abbreviation", y="Points",  color = "Abbreviation", color_discrete_map = colorMap, animation_frame="Race", 
                labels=dict(Abbreviation="Name", classement="Ranking", FullName = "Pilot"), width = 1000, height=800, text = df_final['classement'])


    fig.update_layout(title_text='Evolution of points in the championship', title_x=0.5, transition = {'duration': 1000})

    fig.update_traces(textposition='inside', hovertemplate='Points: %{y}' )

    fig.update_yaxes(range=[0, maxY])

    return(fig)

champ_pos(df_final)