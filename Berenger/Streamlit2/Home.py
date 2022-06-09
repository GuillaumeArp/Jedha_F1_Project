#Import des librairies

import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils
ff1.Cache.enable_cache('cache/')
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
pio.templates.default = "plotly_dark"
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import requests

import pandas as pd
import streamlit as st

import numpy as np


#Récupération des noms et des couleurs à partir d'une course

year = 2022
gp_round = st.radio("Choisissez le round", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
ses = 'R'

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_session(year, gp_round, ses):
    session = ff1.get_session(year, gp_round, ses)
    session.load()
    return session


#Début de la fonction
@st.cache()
def champ_pos(year, gp_round, ses):
    session = get_session(year, gp_round, ses)
    #Récupération du csv avec les points au championnat

    drivers_standings = pd.read_csv('drivers_standings.csv', index_col = 0)
    
    
    #Génération du dataframe
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
    df_race = session.results
    try:
        df_race.drop(columns=["Position", "GridPosition", "Q1", "Q2", "Q3", "Time", "Status", "Points"],inplace=True)
        df_race.reset_index()

    except:
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
        df_final['classement']=30
        longueur = len(df_final)
        df_final.iloc[0,10] = 1

        for i in range(1,longueur -1):
            if df_final.iloc[i,9] == df_final.iloc[i-1,9]:
                df_final.iloc[i,10] = df_final.iloc[i-1,10] +  1
            else :
                df_final.iloc[i,10] = 1
                
                
        #Génère une course 0 avec le classement cumulé de la dernière (permet de mettre les pilotes dans l'ordre du dernier classement)

        df_init = df_final[df_final['Race']==nb-1]
        df_init['Race'] = 0
        df_init['Points'] = 0
        df_final = pd.concat([df_final, df_init])

                
                
        # Paramétrage du dictionnaire des couleurs

        colorMap ={}
        df_class = pd.DataFrame(df_class)

        for i in df_class.itertuples() :
            if i.Abbreviation == 'HUL' :
                colorMap[i.Abbreviation] = '#' + '2d826d'
            else :
                colorMap[i.Abbreviation] = '#' + i.TeamColor
                
                
        #Création du graphique


    #def champ_pos(df_final):

        df_final = df_final.sort_values(by=['Race', 'classement'], ascending = [True, True])

        maxY = df_final['Points'].max() + 20

        fig = px.bar(df_final, x="Abbreviation", y="Points",  color = "Abbreviation", color_discrete_map = colorMap, animation_frame="Race", 
                    labels=dict(Abbreviation="Name", classement="Ranking", FullName = "Pilot"), width = 1000, height=800, text = df_final['classement'])


        fig.update_layout(title_text='Evolution of points in the championship', title_x=0.5, transition = {'duration': 1000}, showlegend = False)

        fig.update_traces(textposition='inside', hovertemplate='Points: %{y}' )

        fig.update_yaxes(range=[0, maxY])

        return(fig)

st.plotly_chart(champ_pos(year, gp_round, ses))