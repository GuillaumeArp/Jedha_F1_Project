import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils

plotting.setup_mpl()
ff1.Cache.enable_cache('cache/')
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.animation import FuncAnimation
pio.templates.default = "plotly_dark"
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import streamlit as st

### Import Adrien ###
from fastf1.core import Laps
from timple.timedelta import strftimedelta
ff1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)
### Import Adrien ###


### Config
st.set_page_config(
    page_title="FastF1",
    page_icon=":racing_car:",
    layout="wide"
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

events_list = ff1.get_event_schedule(2022)[2:]

year = 2022
ses = 'R'



st.markdown("<h1 style='text-align: center;'>Race Analysis</h1>", unsafe_allow_html=True)
st.write('\n')
st.write('\n')
st.write('\n')


col1, col2, col3 = st.columns([2, 4, 4])

with col1:

    gp_name = st.selectbox(
        'Select an event',
        (events_list["EventName"]))
        
gp_round = events_list[events_list['EventName'] == gp_name]['RoundNumber'].values[0]
st.write (f'This event corresponds to round number : {gp_round}')

    # year = st.number_input('Select a year')

if gp_round is not None:

    session = ff1.get_session(year, gp_round, ses)
    session.load(weather=True, telemetry=True)


    st.write('\n')
    st.write('\n')
    st.write('\n')

    """
    Race ranking

    Starting Grid

    Race chart ?
    """

# Best lap comparison - Adrien - Start
# Best lap comparison - Adrien - Start
# Best lap comparison - Adrien - Start

    """
    Best lap comparison
    """

    drivers = pd.unique(session.laps['Driver'])
    list_fastest_laps = list()
    for drv in drivers:
        drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
        list_fastest_laps.append(drvs_fastest_lap)
        fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)

    pole_lap = fastest_laps.pick_fastest()
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']

    team_colors = list()
    for index, lap in fastest_laps.iterlaps():
        color = ff1.plotting.team_color(lap['Team'])
        team_colors.append(color)

    lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')

    def fastest_lap_comparison(fastest_laps):

        fig, ax = plt.subplots(figsize=(20, 5))

        plt.style.use('dark_background')

        ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'], color=team_colors, edgecolor='grey')
        ax.set_yticks(fastest_laps.index)
        ax.set_yticklabels(fastest_laps['Driver'])

        plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\n"
                f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")

        ax.invert_yaxis()

        ax.set_axisbelow(True)
        ax.xaxis.grid(True, which='major', linestyle='--', color='grey', zorder=-5000)

        return fig



    st.pyplot(fastest_lap_comparison(fastest_laps))

# Best lap comparison - Adrien - End
# Best lap comparison - Adrien - End
# Best lap comparison - Adrien - End

# Gap comparison - Christophe - Start
# Gap comparison - Christophe - Start
# Gap comparison - Christophe - Start

    """
    Gap Christophe
    """

    #Chargement du calendrier

    #Numéro de la course
    #round_number = input("Quel est le numéro de la course ?")

    #Recherche le nom du GP

    event_name = events_list[events_list['RoundNumber'] == gp_round].iloc[0,3]



    #Chargement des données pour une course

    #Calcul le gain de position entre la grille de départ et l'arrivée
    df = session.results
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
                title = go.layout.Title(text = (event_name + "<br>Position at finish and gap from grid position"), x = 0.5), width = 1300, height = 1000, template = 'plotly_dark'
            )
        )
                
        fig.update_layout(hovermode='y unified')

        return fig

        
    st.plotly_chart(dif_start_end(df))

# Gap comparison - Christophe - End
# Gap comparison - Christophe - End
# Gap comparison - Christophe - End


    col1, col2 = st.columns([2, 2])

    with col1:
        genre = st.radio("",
        ('Trial', 'Qualification', 'Sprint', 'Race'))

    with col2:
        if genre == 'Trial':
            st.write('You selected Trial.')

        elif genre == 'Qualification':
            st.write('You selected Qualification.')

        elif genre == 'Sprint':
            st.write('You selected Sprint.')

        else:
            st.write("You didn't select Race.")

    st.write('\n')
    st.write('\n')
    """
    Comparison of 2 drivers
    """

    col1, col2, col3 = st.columns([2, 3, 2])

    with col1:
        driver1 = st.selectbox(
            'Select a first driver',
            ('Driver 1', 'Driver 2', 'Driver 3'))

    with col1:
        driver2 = st.selectbox(
            'Select a second driver',
            ('Driver 1', 'Driver 2', 'Driver 3'))

    col1, col2 = st.columns([2, 2])

    with col1:
        genre = st.radio(" ",
        ('Trial', 'Qualification', 'Sprint', 'Race'))


    """
    * Speed comparison on fatest lap

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

    * Time delta on fastest lap

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    """