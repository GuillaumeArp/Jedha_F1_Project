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
import pandas as pd

#Chargement du calendrier

events_list = ff1.get_event_schedule(2022)[2:]


#Chargement des données pour une course

year = 2022
gp_round = 5
ses = 'R'
session = ff1.get_session(year, gp_round, ses)
session.load(weather=True, telemetry=True)


#Début de la fonction

def dif_start_end(df1, df2):
    
    #Calcul le gain de position entre la grille de départ et l'arrivée
    df1['Nombre de places gagnées'] = df1['GridPosition'] - df1['Position']

    #Recherche le nom du GP
    #df2=pd.DataFrame(df2)
    event_name = df2[df2['RoundNumber'] == gp_round].iloc[0,3]

    #Affichage du graphique
    hovertemplate_gap = 'Finishing place : %{text}'+'<br>Difference from Grid : %{x:.0f} position(s)'
    df1 = df1.sort_values(by = 'Position', ascending = False)

    fig = go.Figure(
        data = go.Bar(
            x = df1['Nombre de places gagnées']+0.1, 
            y = df1['FullName'],
            text = df1['Position'], marker_color="#" + df1['TeamColor'], textposition = "outside", hovertemplate = hovertemplate_gap,
            name = "", 
            orientation = 'h'),    
        layout = go.Layout(
            title = go.layout.Title(text = (event_name + "<br>Position at finish and gap from grid position"), x = 0.5), width = 800, height = 600, template = 'plotly_dark'
        )
    )
            
    fig.update_layout(hovermode='y unified')
    
    return fig

    
dif_start_end(session.results, events_list)