import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils
plotting.setup_mpl()
ff1.Cache.enable_cache('../../cache/')
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
from PIL import Image

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

# Global variables

events_list = ff1.get_event_schedule(2022)[2:]
country_abbrev = ['BHR','SAU','AUS','ERO','MIA','ESP','MCO','AZE','CAN','GBR','AUT','FRA','HUN','BEL','NLD','ITA','SGP','JPN','USA','MXC','SAO','ABD']
events_list['CountryAbbreviation'] = country_abbrev
session_dict = {'conventional': ['Practice 1', 'Practice 2', 'Practice 3', 'Qualifying', 'Race'],
                'sprint': ['Practice 1', 'Qualifying', 'Practice 2', 'Sprint', 'Race']}
year = 2022
gp_round = 7
ses = 'R'
start_line_dict =  {1: [120, 1280, '^'],
                    2: [-1341, 2800, '<'],
                    3: [-1228, 100, '<'],
                    4: [-1533, -650, '<'],
                    5: [2633, 128, '>'],
                    6: [25, -469, '<'],
                    7: [-8065, -6549, '^'],
                    8: [700, 350, '>'],
                    9: [0, 0, '<'],
                    10: [0, 0, '<'],
                    11: [0, 0, '<'],
                    12: [0, 0, '<'],
                    13: [0, 0, '<'],
                    14: [0, 0, '<'],
                    15: [0, 0, '<'],
                    16: [0, 0, '<'],
                    17: [0, 0, '<'],
                    18: [0, 0, '<'],
                    19: [0, 0, '<'],
                    20: [0, 0, '<'],
                    21: [0, 0, '<'],
                    22: [0, 0, '<']}


# Functions

def format_time(timedelta_series, num):
    '''
    Format timedelta Series as list of strings
    '''
    t_list_str = []
    for i in timedelta_series:
        i = str(i)
        t_list_str.append(i[num:-3])
        
    return t_list_str

def get_fastest_laps(session, driver_1, driver_2):
    '''
    Gets the fastest laps for the 2 selected drivers
    '''
    fastest_driver_1 = session.laps.pick_driver(driver_1).pick_fastest()
    fastest_driver_2 = session.laps.pick_driver(driver_2).pick_fastest()
    
    return fastest_driver_1, fastest_driver_2

def get_car_data(fastest_driver_1, fastest_driver_2):
    '''
    Gets the car data for the 2 selected drivers on their fastest laps
    '''
    car_data_1 = fastest_driver_1.get_car_data().add_distance()
    car_data_1['Distance'] = round(car_data_1['Distance'])
    car_data_2 = fastest_driver_2.get_car_data().add_distance()
    car_data_2['Distance'] = round(car_data_2['Distance'])
    
    return car_data_1, car_data_2

def plot_stacked_data(session, car_data_1, car_data_2, driver_1, driver_2, ref_tel, delta_time):
    '''
    Plots stacked telemetry data for the 2 selected drivers
    '''
    plot_title = f"{session.event.year} {session.event.EventName} - {session.name} - {driver_1} vs {driver_2}"
    hovertemplate_speed = 'Speed: %{y} km/h'+'<br>Distance: %{x} meters'
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=car_data_1['Distance'], y=car_data_1['Speed'], name=driver_1, line_color=ff1.plotting.driver_color(driver_1), hovertemplate = hovertemplate_speed, opacity=0.8), secondary_y=False)
    fig.add_trace(go.Scatter(x=car_data_2['Distance'], y=car_data_2['Speed'], name=driver_2, line_color=ff1.plotting.driver_color(driver_2), hovertemplate = hovertemplate_speed, opacity=0.8), secondary_y=False)
    fig.add_trace(go.Scatter(x=ref_tel['Distance'], y=delta_time, line_color='white', name='Delta Time', hovertemplate = 'Delta Time: %{y:.3f} sec', opacity=0.8, line_width=1), secondary_y=True)

    fig.update_yaxes(title_text="Speed (km/h)", secondary_y=False)
    fig.update_yaxes(title_text=f"<-- {driver_2} ahead | {driver_1} ahead -->", secondary_y=True)
    fig.update_layout(width=1200, height=600, title_text=plot_title, xaxis_title='Distance (m)', title_x=0.5)
    
    return fig

def plot_unstacked_data(session, car_data_1, car_data_2, driver_1, driver_2, ref_tel, delta_time):
    '''
    Plots unstacked telemetry data for the 2 selected drivers
    '''
    hovertemplate_speed = 'Speed: %{y} km/h'+'<br>Distance: %{x} meters'
    hovertemplate_gear = 'Gear: %{y}'+'<br>Distance: %{x} meters'
    plot_title = f"{session.event.year} {session.event.EventName} - {session.name} - {driver_1} vs {driver_2}"
    
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=('Speed', 'Gear', 'Delta Time'), vertical_spacing=0.1)

    fig.append_trace(go.Scatter(x=car_data_1['Distance'], y=car_data_1['Speed'], name=driver_1, line_color=ff1.plotting.driver_color(driver_1), hovertemplate = hovertemplate_speed, opacity=0.8), 1, 1)
    fig.append_trace(go.Scatter(x=car_data_2['Distance'], y=car_data_2['Speed'], name=driver_2, line_color=ff1.plotting.driver_color(driver_2), hovertemplate = hovertemplate_speed, opacity=0.8), 1, 1)

    fig.append_trace(go.Scatter(x=car_data_1['Distance'], y=car_data_1['nGear'], name=driver_1, line_color=ff1.plotting.driver_color(driver_1), hovertemplate = hovertemplate_gear, opacity=0.8, showlegend=False), 2, 1)
    fig.append_trace(go.Scatter(x=car_data_2['Distance'], y=car_data_2['nGear'], name=driver_2, line_color=ff1.plotting.driver_color(driver_2), hovertemplate = hovertemplate_gear, opacity=0.8, showlegend=False), 2, 1)

    fig.append_trace(go.Scatter(x=ref_tel['Distance'], y=delta_time, line_color='white', mode='lines', name='Delta Time', hovertemplate = 'Delta Time: %{y:.3f} sec', opacity=0.8), 3, 1)

    fig.update_yaxes(title_text="Speed (km/h)", row=1, col=1)
    fig.update_yaxes(title_text="Gear", row=2, col=1)
    fig.update_yaxes(title_text=f"<-- {driver_2} ahead | {driver_1} ahead -->", row=3, col=1)
    fig.update_xaxes(title_text="Distance (m)", row=3, col=1)

    fig.update_layout(width=1200, height=1200, title_text=plot_title, title_x=0.1)
    return fig

def get_telemetry_data(fastest_driver_1, fastest_driver_2):
    '''
    Returns advanced telemetry data for the 2 selected drivers
    '''
    lap_1 = fastest_driver_1.telemetry
    lap_2 = fastest_driver_2.telemetry
    lap_1 = lap_1[lap_1['Source'] != 'pos'].reset_index(drop=True)
    lap_2 = lap_2[lap_2['Source'] != 'pos'].reset_index(drop=True)
    return lap_1, lap_2

def plot_track_speed(session, lap_1, driver_1):
    '''
    Plots the fastest lap speed on track for the selected driver
    '''    
    # Variables definitions
    colormap_speed = mpl.cm.RdYlGn
    points = np.array([lap_1['X'], lap_1['Y']]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    start_x = points[0][0][0]
    start_y = points[0][0][1]
    direction_x = start_line_dict[gp_round][0]
    direction_y = start_line_dict[gp_round][1]
    direction_marker = start_line_dict[gp_round][2]
    px = 1/plt.rcParams['figure.dpi']

    # Setup plot
    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(800*px, 800*px))
    fig.suptitle(f"{session.event.year} {session.event.EventName} - {session.name} - {driver_1}", size=24, y=0.97)

    # Adjust margins and turn of axis
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')

    # Create background track line
    ax.plot(lap_1['X'], lap_1['Y'], color='black', linestyle='-', linewidth=16, zorder=1)

    # Add start line marker
    plt.scatter(start_x, start_y, color='white', s=400, zorder=1)
    plt.scatter(direction_x, direction_y, color='white', s=400, zorder=1, marker=direction_marker)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(lap_1['Speed'].min(), lap_1['Speed'].max())
    lc = LineCollection(segments, cmap=colormap_speed, norm=norm, linestyle='-', linewidth=5)

    # Set the values used for colormapping
    lc.set_array(lap_1['Speed'])

    # Merge all line segments together
    line = ax.add_collection(lc)

    # Finally, we create a color bar as a legend.
    cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
    normlegend = mpl.colors.Normalize(vmin=lap_1['Speed'].min(), vmax=lap_1['Speed'].max())
    legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap_speed, orientation="horizontal", label='Speed (km/h)')

    # Set background color to transparent
    # fig.patch.set_alpha(0)
    fig.patch.set_facecolor('#111111')

    # Show the plot
    return fig

def plot_track_gear(session, lap_1, driver_1):

    # Variables definitions
    colormap_gear = mpl.cm.get_cmap('RdYlGn', 8)
    points = np.array([lap_1['X'], lap_1['Y']]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    start_x = points[0][0][0]
    start_y = points[0][0][1]
    direction_x = start_line_dict[gp_round][0]
    direction_y = start_line_dict[gp_round][1]
    direction_marker = start_line_dict[gp_round][2]
    px = 1/plt.rcParams['figure.dpi']
    
    # Setup plot
    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(800*px, 800*px))
    fig.suptitle(f"{session.event.year} {session.event.EventName} - {session.name} - {driver_1}", size=24, y=0.97)

    # Adjust margins and turn of axis
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')

    # Create background track line
    ax.plot(lap_1['X'], lap_1['Y'], color='black', linestyle='-', linewidth=16, zorder=1)

    # Add start line marker
    plt.scatter(start_x, start_y, color='white', s=400, zorder=1)
    plt.scatter(direction_x, direction_y, color='white', s=400, zorder=1, marker=direction_marker)

    # Create a norm to map from data points to colors
    norm = plt.Normalize(1, colormap_gear.N+1)
    lc = LineCollection(segments, cmap=colormap_gear, norm=norm, linestyle='-', linewidth=5)

    # Set the values used for colormapping
    lc.set_array(lap_1['nGear'].to_numpy().astype(float))

    # Merge all line segments together
    line = ax.add_collection(lc)

    # Create a color bar as a legend
    cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
    normlegend = mpl.colors.Normalize(vmin=1, vmax=8)
    legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap_gear, orientation="horizontal", label='Gear')

    # Set background color to transparent
    # fig.patch.set_alpha(0)
    fig.patch.set_facecolor('#111111')

    # Show the plot
    return fig

def delta_bounds(vmin, vmax):
    '''
    Returns the bounds of the delta time colorbar legend
    '''
    if abs(vmin) < abs(vmax):
        vmin = -(vmax)
    else:
        vmax = -(vmin)
    return vmin, vmax

def plot_track_delta(session, lap_1, driver_1, driver_2, delta_time):

    # Variables definitions
    colormap_speed = mpl.cm.RdYlGn
    points = np.array([lap_1['X'], lap_1['Y']]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    start_x = points[0][0][0]
    start_y = points[0][0][1]
    direction_x = start_line_dict[gp_round][0]
    direction_y = start_line_dict[gp_round][1]
    direction_marker = start_line_dict[gp_round][2]
    px = 1/plt.rcParams['figure.dpi']

    # Determine boundaries for the colorbar
    vmin, vmax = delta_bounds(delta_time.min(), delta_time.max())

    # Setup plot
    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(800*px, 800*px))
    fig.suptitle(f"{session.event.year} {session.event.EventName} - {session.name} - {driver_1} vs {driver_2}", size=24, y=0.97)

    # Adjust margins and turn of axis
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')

    # After this, we plot the data itself.
    # Create background track line
    ax.plot(lap_1['X'], lap_1['Y'], color='black', linestyle='-', linewidth=16, zorder=1)

    # Add start line marker
    plt.scatter(start_x, start_y, color='white', s=400, zorder=1)
    plt.scatter(direction_x, direction_y, color='white', s=400, zorder=1, marker=direction_marker)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(vmin, vmax)
    lc = LineCollection(segments, cmap=colormap_speed, norm=norm, linestyle='-', linewidth=5)

    # Set the values used for colormapping
    lc.set_array(delta_time)

    # Merge all line segments together
    line = ax.add_collection(lc)

    # Finally, we create a color bar as a legend.
    cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
    normlegend = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap_speed, orientation="horizontal", label=f"<-- {driver_2} ahead | {driver_1} ahead -->")

    # Set background color to transparent
    # fig.patch.set_alpha(0)
    fig.patch.set_facecolor('#111111')

    # Show the plot
    return fig

def add_driver_info():
    '''
    Updates the drivers info csv
    '''
    drivers_info = pd.read_csv('../data/drivers_info.csv', index_col=0)
    drivers_standings = pd.read_csv('../data/drivers_standings.csv', index_col=0)
    missing_drivers = [x for x in drivers_standings.index.tolist() if x not in drivers_info['Abbreviation'].tolist()]
    if len(missing_drivers) > 0:
        df = session.results.copy().drop(columns=["Position", "GridPosition", "Q1", "Q2", "Q3", "Time", "Status", "Points"])
        for i in missing_drivers:
            df_missing = df[df['Abbreviation'] == i]
            df_full = pd.concat([drivers_info, df_missing])
        df_full.to_csv('../data/drivers_info.csv')
        
def format_results_race(session_type):
    '''
    Returns a formatted session results dataframe
    '''    
    results = session.results    
    if session_type == 'Race' or session_type == 'Sprint':
        # Get the results table, convert it to a dataframe and set the numeric columns to int        
        results_formatted = pd.DataFrame(results[['FullName','TeamName','Position','GridPosition','Time','Status','Points']].copy())
        results_formatted[['Points', 'Position', 'GridPosition']] = results_formatted[['Points', 'Position', 'GridPosition']].astype(int)
        results_formatted = results_formatted.rename(columns = {'FullName': 'Name'})
        
        # Compute time difference at finish
        time_difference = []
        time_1 = results_formatted['Time'][0]
        for i in results_formatted.itertuples():
            time_difference.append(i.Time - time_1)
            
        time_difference[0] = results_formatted['Time'][0]
        results_formatted['TimeDifference'] = time_difference
        
        # Format the time data as string
        time_str = []
        for i in results_formatted.itertuples():
            if i.Status == 'Finished':
                time = str(i.TimeDifference)
                time_str.append(time[8:-3])
            elif 'Lap' in i.Status:
                time_str.append(i.Status)
            else:
                time_str.append('DNF')
                
        results_formatted['TimeStr'] = time_str
        
        # Format the time data correctly
        time_str_2 = []
        for i in results_formatted.itertuples():
            if i.Position == 1 or len(i.TimeStr) != 11:
                time_str_2.append(i.TimeStr)
            elif len(i.TimeStr) == 11:
                time_subbed = '+' + i.TimeStr[3:]
                time_str_2.append(time_subbed)
                
        results_formatted['TimeFinish'] = time_str_2
        
        # Drop unnecessary columns
        results_formatted.drop(columns=['Status', 'Time', 'TimeStr', 'TimeDifference'], inplace=True)
        
    elif session_type == 'Qualifying':
        results_formatted = pd.DataFrame(results.copy())
        temp_q1 = format_time(results['Q1'], 11)
        results_formatted['Q1_time'] = temp_q1
        temp_q2 = format_time(results['Q2'], 11)
        results_formatted['Q2_time'] = temp_q2
        temp_q3 = format_time(results['Q3'], 11)
        results_formatted['Q3_time'] = temp_q3
        results_formatted = results_formatted[['Name','TeamName','Position','Q1_time','Q2_time','Q3_time']]
        results_formatted['Position'] = results_formatted['Position'].astype(int)
            
    return results_formatted  

@st.cache(allow_output_mutation=True)
def load_data_session():
    session = ff1.get_session(year, gp_round, ses)
    session.load(weather=True, telemetry=True)
    return session





with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

image = Image.open('images/session_analysis_title.png')

st.image(image, caption='', use_column_width="always")





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
drivers_standings = pd.read_csv("drivers_standings.csv", index_col = 0)
if gp_round is not None:



    session = load_data_session()
    



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

# champ_pos.py - Christophe - Start
# champ_pos.py - Christophe - Start
# champ_pos.py - Christophe - Start

    #Récupération du csv avec les points au championnat


    

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

    st.plotly_chart(champ_pos(df_final))

# champ_pos.py - Christophe - End
# champ_pos.py - Christophe - End
# champ_pos.py - Christophe - End


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