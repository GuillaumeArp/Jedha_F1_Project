import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils
from fastf1.core import Laps
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
pio.templates.default = "plotly_dark"
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import requests
import streamlit as st
from PIL import Image

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


# Functions
def get_start_line_data():
    '''
    Returns a dict with the start line postitions
    '''
    start_line_dict_temp = requests.get('https://f1-jedha-bucket.s3.eu-west-3.amazonaws.com/data/start_line_dict.json').json()
    return {int(k): v for k, v in start_line_dict_temp.items()} 

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
    start_line_dict = get_start_line_data()
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
    '''
    Plots the fastest lap gears usage on track for the selected driver
    '''   
    # Variables definitions
    start_line_dict = get_start_line_data()
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
    '''
    Plots the delta time comparison for the fastests laps on track for the selected drivers
    '''   
    # Variables definitions
    start_line_dict = get_start_line_data()
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
    drivers_standings = pd.read_csv('https://f1-jedha-bucket.s3.eu-west-3.amazonaws.com/data/drivers_standings.csv', index_col=0)
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
        return results_formatted
        
    elif session_type == 'Qualifying':
        results_formatted = pd.DataFrame(results.copy())
        temp_q1 = format_time(results['Q1'], 11)
        results_formatted['Q1_time'] = temp_q1
        temp_q2 = format_time(results['Q2'], 11)
        results_formatted['Q2_time'] = temp_q2
        temp_q3 = format_time(results['Q3'], 11)
        results_formatted['Q3_time'] = temp_q3        
        results_formatted = results_formatted[['FullName','TeamName','Position','Q1_time','Q2_time','Q3_time']]
        results_formatted = results_formatted.rename(columns = {'FullName': 'Name'})
        results_formatted['Position'] = results_formatted['Position'].astype(int)
        return results_formatted

def fastest_lap_comparison(fastest_laps):
    # Pass session.laps.pick_fastest() as argument when calling the function
    '''
    Plots the comparison of the best lap times of the selected session
    '''
    drivers = session.laps.pick_quicklaps()['Driver'].unique()

    list_fastest_laps = []
    for drv in drivers:
        drvs_fastest_lap = session.laps.pick_quicklaps().pick_driver(drv).pick_fastest()
        list_fastest_laps.append(drvs_fastest_lap)
    fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)

    pole_lap = fastest_laps.pick_fastest()
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']

    fastest_laps_final = fastest_laps.dropna(subset=['Time']).copy()

    teamcol = {}
    df_results = pd.DataFrame(session.results)

    for i in df_results.itertuples():
        if i.Abbreviation in fastest_laps_final['Driver'].unique():        
            teamcol[i.Abbreviation] = '#' + i.TeamColor    

    timestr = format_time(fastest_laps_final['LapTimeDelta'],13)
    timelap = format_time(fastest_laps_final['LapTime'],11)

    fastest_laps_final['Delta'] = timestr
    fastest_laps_final['BestLapstr'] = timelap
    fastest_laps_final['Delta'] = fastest_laps_final['Delta'].apply(lambda x: x + ' sec')
    fastest_laps_final['BestLapstr'] = fastest_laps_final['BestLapstr'].apply(lambda x: x + ' sec')

    plot_title = f"{session.event.year} {session.event.EventName} - {session.name} - Fastest Lap : {fastest_laps_final['BestLapstr'].iloc[0]} - {fastest_laps_final['Driver'].iloc[0]}"

    fig = px.bar(fastest_laps_final, 
                x="LapTimeDelta", 
                y="Driver", 
                color='Driver',
                color_discrete_map=teamcol ,
                orientation='h',
                width=1000, height=600,
                template='plotly_dark',
                hover_data={'Delta':True,'LapTimeDelta':False})

    fig.update_layout(showlegend=False, title_text=plot_title)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(categoryorder='total descending')

    return fig

@st.cache(allow_output_mutation=True)
def load_data_session(year, gp_round, ses):
    session = ff1.get_session(year, gp_round, ses)
    session.load(weather=False, telemetry=True, messages=False)
    add_driver_info()
    return session

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Display page title
image = Image.open('images/session_analysis_title.png')
st.image(image, caption='', use_column_width="always")

st.write('\n')
st.write('\n')
st.write('\n')

col1, col2, col3 = st.columns([3, 8, 3])

with col2:
    """
    * On this page, you can pick an event, and one of its sessions, then two of the drivers that participated in the session.
    * You can pick up to two different visualizations to display of each side of the page. Please note that the session results table is not avaible for Free Practice sessions.
    * Please let the page load entirely before trying to use another dropdown menu. If that session data has not be loaded to the cache yet, it may take up to a minute to load.
    """

col1, col2, col3, col4, col5, col6 = st.columns([4, 2, 2, 2, 2, 4])

with col3:
    gp_name = st.selectbox('Event', (events_list["EventName"]), index = 6)
        
gp_round = events_list[events_list['EventName'] == gp_name]['RoundNumber'].values[0]

try:
    with col4:
        if list(events_list[events_list["RoundNumber"] == gp_round]["EventFormat"])[0] == list(session_dict.keys())[0]:
            ses = st.selectbox("Session", (list(session_dict.values())[0]), key=10, index = 4)
        else:
            ses = st.selectbox("Session", (list(session_dict.values())[1]), key=11, index = 4)

    session = load_data_session(year, gp_round, ses)

    col1, col2, col3, col4, col5, col6 = st.columns([4, 2, 2, 2, 2, 4])

    if len(session.laps.pick_quicklaps()['Driver'].unique()) > 2:
        drivers = session.laps.pick_quicklaps()['Driver'].unique()
    else:
        drivers = session.laps['Driver'].unique()

    with col3:
        driver_1 = st.selectbox('First driver', (session.results[session.results.Abbreviation.isin(drivers)]["FullName"]), index = 0)
        # Get Abbreviation of the first driver name
        driver_1 = session.results[session.results["FullName"] == driver_1]["Abbreviation"].values[0]

    with col4:
        driver_2 = st.selectbox('Second driver', (session.results[session.results.Abbreviation.isin(drivers)]["FullName"]), index = 1)
        # Get Abbreviation of the first driver name
        driver_2 = session.results[session.results["FullName"] == driver_2]["Abbreviation"].values[0]

    fastest_driver_1, fastest_driver_2 = get_fastest_laps(session, driver_1, driver_2)
    delta_time, ref_tel, compare_tel = utils.delta_time(fastest_driver_1, fastest_driver_2)
    car_data_1, car_data_2 = get_car_data(fastest_driver_1, fastest_driver_2)
    lap_1, lap_2 = get_telemetry_data(fastest_driver_1, fastest_driver_2)

    col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 1, 1, 2, 1])
    with col2:
        if ses == 'Qualifying' or ses == 'Race' or ses == 'Sprint':
            decision_1 = st.selectbox(" ", ("Select a visualisation", "Speed comparison", "Session results", "Fastest laps", "Speed, Gears and Delta Time comparison", "Speed visualization on track layout for First Driver", "Gears visualization on track layout for First Driver", "Delta Time on track layout"), key = 1)
        else:
            decision_1 = st.selectbox(" ", ("Select a visualisation", "Speed comparison", "Fastest laps", "Speed, Gears and Delta Time comparison", "Speed visualization on track layout for First Driver", "Gears visualization on track layout for First Driver", "Delta Time on track layout"), key = 2)

    with col5:
        if ses == 'Qualifying' or ses == 'Race' or ses == 'Sprint':
            decision_2 = st.selectbox(" ", ("Select a visualisation", "Speed comparison", "Session results", "Fastest laps", "Speed, Gears and Delta Time comparison", "Speed visualization on track layout for First Driver", "Gears visualization on track layout for First Driver", "Delta Time on track layout"), key = 3)
        else:
            decision_2 = st.selectbox(" ", ("Select a visualisation", "Speed comparison", "Fastest laps", "Speed, Gears and Delta Time comparison", "Speed visualization on track layout for First Driver", "Gears visualization on track layout for First Driver", "Delta Time on track layout"), key = 4)

    col1, col2, col3, col4, col5, col6 = st.columns([1, 15, 1, 1, 15, 1])

    # Function to display visualisation selected
    def display_visualisation(decision):

        if decision == "Select a visualisation":
            return st.markdown("<h5 style='text-align: center; color: white;'>No selection made</h5>", unsafe_allow_html=True)

        if decision == "Speed comparison":
            viz1 = plot_stacked_data(session, car_data_1, car_data_2, driver_1, driver_2, ref_tel, delta_time)

        elif decision == "Session results":
            st.write("")
            st.write("")
            st.markdown("<h5 style='text-align: center; color: white;'>Session results</h5>", unsafe_allow_html=True)
            st.write("")
            st.write("")
            return st.dataframe(format_results_race(ses))

        elif decision == "Fastest laps":
            viz1 = fastest_lap_comparison(session.laps.pick_fastest())

        elif decision == "Speed, Gears and Delta Time comparison":
            viz1 = plot_unstacked_data(session, car_data_1, car_data_2, driver_1, driver_2, ref_tel, delta_time)

        elif decision == "Speed visualization on track layout for First Driver":
            return st.pyplot(plot_track_speed(session, lap_1, driver_1))

        elif decision == "Gears visualization on track layout for First Driver":
            return st.pyplot(plot_track_gear(session, lap_1, driver_1))

        elif decision == "Delta Time on track layout":
            return st.pyplot(plot_track_delta(session, lap_1, driver_1, driver_2, delta_time))
        
        return st.plotly_chart(viz1, use_container_width=True)

    with col2:
        display_visualisation(decision_1)

    with col5:
        display_visualisation(decision_2)
            
except:
    st.write("")
    st.write("")
    st.markdown("<h1 style='text-align: center; color: red;'>No data available yet</h1>", unsafe_allow_html=True)