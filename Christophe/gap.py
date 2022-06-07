
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

#Chargement du calendrier
events_list = ff1.get_event_schedule(2022)[2:]

#Numéro de la course
#round_number = input("Quel est le numéro de la course ?")
round_number = 5

#Recherche le nom du GP
event_name = events_list[events_list['RoundNumber'] == round_number].iloc[0,3]

#Chargement des données pour une course
race = ff1.get_session(2022, round_number, 'R')
race.load(weather=True, telemetry=True)

#Calcul le gain de position entre la grille de départ et l'arrivée
df = race.results
df['Nombre de places gagnées'] = df['GridPosition'] - df['Position']

#Affichage du graphique
def dif_start_end(df):
    hovertemplate_gap = 'Finishing place : %{text}'+'<br>Difference from Grid : %{x:.0f} position(s)'
    df = df.sort_values(by = 'Position', ascending = False)

    fig = go.Figure(
        data = go.Bar(
            x = df['Nombre de places gagnées']+0.1, 
            y = df['FullName'],
            text = df['Position'], marker_color="#" + df['TeamColor'], textposition = "outside", hovertemplate = hovertemplate_gap,
            name = "", 
            orientation = 'h'),    
        layout = go.Layout(
            title = go.layout.Title(text = (event_name + "<br>Position at finish and gap from grid position"), x = 0.5), width = 800, height = 600, template = 'plotly_dark'
        )
    )
            
    fig.update_layout(hovermode='y unified')
    
    return fig

    
dif_start_end(df)