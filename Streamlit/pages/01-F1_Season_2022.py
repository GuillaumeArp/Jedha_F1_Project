import fastf1 as ff1
from fastf1 import plotting
plotting.setup_mpl()
ff1.Cache.enable_cache('cache/')
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "plotly_dark"
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
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

# Functions
@st.cache()
def plot_champ_pos():
    '''
    Plots the evolution of the drivers standings
    '''
    drv = pd.read_csv('https://f1-jedha-bucket.s3.eu-west-3.amazonaws.com/data/drivers_standings.csv', index_col=0)
    drivers_info = pd.read_csv('drivers_info.csv', index_col=0)
    
    df_class = drivers_info.merge(drv, how='right', left_on = ['Abbreviation'], right_index = True).reset_index()

    nb = len(drv.transpose())+1
    df_final = pd.DataFrame(columns=['DriverNumber', 'BroadcastName', 'Abbreviation', 'TeamName', 'TeamColor', 'FirstName', 'LastName', 'FullName','Points', 'Race'])
    for i in range(1,nb):
        df_class_ligne = df_class.loc[:,['DriverNumber', 'BroadcastName', 'Abbreviation', 'TeamName', 'TeamColor', 'FirstName', 'LastName', 'FullName',str(i)]]
        df_class_ligne['Race'] = i
        df_class_ligne.rename(columns={str(i): 'Points'}, inplace = True)
        df_final = pd.concat([df_final, df_class_ligne])
    df_final.reset_index(drop = True, inplace = True)

    df_final = df_final.sort_values(by=['Race', 'Points'], ascending = [True, False])
    df_final['classement']=len(drv)
    longueur = len(df_final)
    df_final.iloc[0,10] = 1

    for i in range(1,longueur -1):
        if df_final.iloc[i,9] == df_final.iloc[i-1,9]:
            df_final.iloc[i,10] = df_final.iloc[i-1,10] +  1
        else :
            df_final.iloc[i,10] = 1

    df_init = df_final[df_final['Race']==nb-1].copy()
    df_init['Race'] = 0
    df_init['Points'] = 0

    df_final = pd.concat([df_final, df_init])
            
    colorMap ={}
    df_class = pd.DataFrame(df_class)
    for i in df_class.itertuples() :
        if type(i.TeamColor) != str:
            colorMap[i.Abbreviation] = '#FFFFFF'
        else:
            colorMap[i.Abbreviation] = '#' + i.TeamColor
        
            
    df_final = df_final.sort_values(by=['Race', 'classement'], ascending = [True, True])
    maxY = df_final['Points'].max() + 20
    
    fig = px.bar(df_final, x="Abbreviation", y="Points",  color = "Abbreviation", color_discrete_map = colorMap, animation_frame="Race", 
                labels=dict(Abbreviation="Name", classement="Ranking", FullName = "Pilot"), width = 1000, height=800, text = df_final['classement'])

    fig.update_layout(title_text='Evolution of points in the championship', title_x=0.5, transition = {'duration': 1000}, showlegend = False)
    fig.update_traces(textposition='inside', hovertemplate='Points: %{y}' )
    fig.update_yaxes(range=[0, maxY])

    return fig

def get_round_mapping():
    '''
    Returns a round to event name mapping dictionary
    '''
    round_mapping = {}
    for i in events_list.itertuples():
        round_mapping[str(i.RoundNumber)] = i.CountryAbbreviation
    return round_mapping

@st.cache(allow_output_mutation=True)
def get_drivers_standings_df():
    '''
    Displays the drivers standings
    '''
    df = pd.read_csv('https://f1-jedha-bucket.s3.eu-west-3.amazonaws.com/data/drivers_standings.csv', index_col=0)
    round_mapping = get_round_mapping()        
    df.columns = df.columns.map(round_mapping)
    return df

@st.cache(allow_output_mutation=True)
def get_constructors_standings():
    '''
    Displays the constructors standings
    '''
    df = pd.read_csv('https://f1-jedha-bucket.s3.eu-west-3.amazonaws.com/data/constructors_standings.csv', index_col=0)
    round_mapping = get_round_mapping()        
    df.columns = df.columns.map(round_mapping)
    return df

def plot_compare_points(driver_1, driver_2):
    '''
    Plots the points comparison between two drivers
    '''
    round_mapping = get_round_mapping() 
    df_drivers = pd.read_csv('https://f1-jedha-bucket.s3.eu-west-3.amazonaws.com/data/drivers_standings.csv', index_col=0)
    df_colors = pd.read_csv('drivers_info.csv', index_col=0)

    df_drivers_line = df_drivers[(df_drivers.index == driver_1) | (df_drivers.index == driver_2)].transpose().reset_index().rename(columns={'index': 'Round'})
    df_drivers_line['country'] = df_drivers_line['Round'].map(round_mapping)
    # df_drivers_line

    driver_1_team_color = '#' + df_colors[df_colors['Abbreviation'] == driver_1].values[0][4]
    driver_2_team_color = '#' + df_colors[df_colors['Abbreviation'] == driver_2].values[0][4]
    hovertemplate = 'Points: %{y}'

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_drivers_line['country'], y=df_drivers_line[driver_1], name=driver_1, line_color=driver_1_team_color, hovertemplate=hovertemplate))
    fig.add_trace(go.Scatter(x=df_drivers_line['country'], y=df_drivers_line[driver_2], name=driver_2, line_color=driver_2_team_color, hovertemplate=hovertemplate))

    fig.update_xaxes(tickangle=45)
    fig.update_layout(width= 800, height = 600, title_text=f"Current Standings - {driver_1} vs {driver_2}", yaxis_title="Points", title_x=0.5)
    return fig

driver_info = pd.read_csv('drivers_info.csv', index_col=0)


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Display page title
image = Image.open('images/season_2022_title.png')
st.image(image, caption='', use_column_width="always")

st.write('\n')
st.write('\n')
st.write('\n')

col1, col2, col3 = st.columns([3, 8, 3])

with col2:
    """
    * On this page you will be able to pick two drivers and look at their points after each race on the left side.
    * On the right side, you will be able to watch the points evolution for the entire board after each race.
    """
st.write('\n')
st.write('\n')    

col1, col2, col3, col4, col5, col6 = st.columns([4, 2, 2, 2, 2, 4])

with col3:
    driver_1 = st.selectbox('First driver', (driver_info["FullName"]), index = 0)
    # Get Abbreviation of the first driver name
    driver_1 = driver_info[driver_info["FullName"] == driver_1]["Abbreviation"].values[0]

with col4:
    driver_2 = st.selectbox('Second driver', (driver_info["FullName"]), index = 1)
    # Get Abbreviation of the second driver name
    driver_2 = driver_info[driver_info["FullName"] == driver_2]["Abbreviation"].values[0]

col1, col2, col3, col4, col5, col6 = st.columns([1, 15, 1, 1, 15, 1])

with col2:
    st.plotly_chart(plot_compare_points(driver_1, driver_2), use_container_width=True)

with col5:
    st.plotly_chart(plot_champ_pos(), use_container_width=True)

col1, col2, col3 = st.columns([3, 8, 3])

with col2: 
    """
    * Below are displayed the drivers and constructors standings, showing their cumulated points after each race.
    * The tables can be resized at will by dragging the bottom right corner.
    * The default ranking is the one after the latest race, but the order can be changed to display the ranking after a particular race, by clicking on that race's column title.
    """
st.write('\n')
st.write('\n')

col1, col2, col3, col4, col5, col6 = st.columns([1, 15, 1, 1, 15, 1])

with col2:
    st.dataframe(get_drivers_standings_df())

with col5:
    st.dataframe(get_constructors_standings())