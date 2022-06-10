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

driver_dict = {
        'VER': "Max Verstappen",
        "SAI": "Carlos Sainz",
        'MSC': "Mick Schumacher",
        "HAM": "Lewis Hamilton",
        'OCO': "Esteban Ocon",
        "HUL": "Nico Hulkenberg",
        'ZHO': "Guanyu Zhou",
        "ALB": "Alexander Albon",
        'TSU': "1",
        "MAG": "2",
        'STR': "1",
        "LEC": "2",
        'ALO': "1",
        "PER": "2",
        'GAS': "1",
        "LAT": "2",
        'NOR': "1",
        "RIC": "2",
        'RUS': "1",
        "BOT": "2"
}


year = 2022
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
    drivers_info = pd.read_csv('drivers_info.csv', index_col=0)
    drivers_standings = pd.read_csv('drivers_standings.csv', index_col=0)
    missing_drivers = [x for x in drivers_standings.index.tolist() if x not in drivers_info['Abbreviation'].tolist()]
    if len(missing_drivers) > 0:
        df = session.results.copy().drop(columns=["Position", "GridPosition", "Q1", "Q2", "Q3", "Time", "Status", "Points"])
        for i in missing_drivers:
            df_missing = df[df['Abbreviation'] == i]
            df_full = pd.concat([drivers_info, df_missing])
        df_full.to_csv('drivers_info.csv')

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
def load_data_session(year, gp_round, ses):
    session = ff1.get_session(year, gp_round, ses)
    session.load(weather=True, telemetry=True)
    add_driver_info()
    return session





with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

image = Image.open('images/session_analysis_title.png')

st.image(image, caption='', use_column_width="always")





st.write('\n')
st.write('\n')
st.write('\n')


col1, col2, col3, col4, col5, col6 = st.columns([4, 2, 2, 2, 2, 4])

with col3:
    gp_name = st.selectbox('Event', (events_list["EventName"]))
        
gp_round = events_list[events_list['EventName'] == gp_name]['RoundNumber'].values[0]

if gp_round is not None:

    # try:
    with col4:
        if list(events_list[events_list["RoundNumber"] == gp_round]["EventFormat"])[0] == list(session_dict.keys())[0]:
            ses = st.selectbox("Session", (list(session_dict.values())[0]), key=list(session_dict.values())[0])
        else:
            ses =st.selectbox("Session", (list(session_dict.values())[1]), key=list(session_dict.values())[1])

    session = load_data_session(year, gp_round, ses)
    
    col1, col2, col3, col4, col5, col6 = st.columns([4, 2, 2, 2, 2, 4])

    with col3:
        driver_1 = st.selectbox('First driver', (session.results["FullName"]), index = 0)
        # Get Abbreviation of the first driver name
        driver_1 = session.results[session.results["FullName"] == driver_1]["Abbreviation"].values[0]

    with col4:
        driver_2 = st.selectbox('Second driver', (session.results["FullName"]), index = 1)
        # Get Abbreviation of the first driver name
        driver_2 = session.results[session.results["FullName"] == driver_2]["Abbreviation"].values[0]

    fastest_driver_1, fastest_driver_2 = get_fastest_laps(session, driver_1, driver_2)
    delta_time, ref_tel, compare_tel = utils.delta_time(fastest_driver_1, fastest_driver_2)
    car_data_1, car_data_2 = get_car_data(fastest_driver_1, fastest_driver_2)
    lap_1, lap_2 = get_telemetry_data(fastest_driver_1, fastest_driver_2)


    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
    with col2:
        visualisation_1 = st.selectbox("Visualisation 1", ("Drivers speed comparison", "Session results"), key = 1)

    with col5:
        visualisation_2 = st.selectbox("Visualisation 2", ("Drivers speed comparison", "Session results"), key = 2)
    
    col1, col2, col3, col4, col5, col6 = st.columns([1, 15, 1, 1, 15, 1])


    with col2:
        if visualisation_1 == "Drivers speed comparison":
            st.plotly_chart(plot_stacked_data(session, car_data_1, car_data_2, driver_1, driver_2, ref_tel, delta_time), use_container_width=True)
        elif visualisation_2 == "Session results":
            st.dataframe(format_results_race(ses))

    with col5:
        if visualisation_2 == "Drivers speed comparison":
            st.plotly_chart(plot_stacked_data(session, car_data_1, car_data_2, driver_1, driver_2, ref_tel, delta_time), use_container_width=True)
        elif visualisation_2 == "Session results":
            format_results_race(ses)
    
        

            


    # except:
    #     st.write("No data available for this event")


    



    



    st.write('\n')
    st.write('\n')
    st.write('\n')


    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')

    st.write('\n')
    st.write('\n')
    st.write('\n')

    """
    * Speed comparison on fatest lap

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

    * Time delta on fastest lap

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    """