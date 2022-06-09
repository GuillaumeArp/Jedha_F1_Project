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


### Config
st.set_page_config(
    page_title="FastF1",
    page_icon=":racing_car:",
    layout="wide"
)

# Functions

#Récupération des noms et des couleurs à partir d'une course



@st.cache()
def plot_champ_pos():
    '''
    Plots the evolution of the drivers standings
    '''
    drv = pd.read_csv('../data/drivers_standings.csv', index_col=0)
    drivers_info = pd.read_csv('../data/drivers_info.csv', index_col=0)
    
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
        colorMap[i.Abbreviation] = '#' + i.TeamColor
            
    df_final = df_final.sort_values(by=['Race', 'classement'], ascending = [True, True])
    maxY = df_final['Points'].max() + 20
    
    fig = px.bar(df_final, x="Abbreviation", y="Points",  color = "Abbreviation", color_discrete_map = colorMap, animation_frame="Race", 
                labels=dict(Abbreviation="Name", classement="Ranking", FullName = "Pilot"), width = 1000, height=800, text = df_final['classement'])

    fig.update_layout(title_text='Evolution of points in the championship', title_x=0.5, transition = {'duration': 1000}, showlegend = False)
    fig.update_traces(textposition='inside', hovertemplate='Points: %{y}' )
    fig.update_yaxes(range=[0, maxY])

    return fig
















@st.cache(allow_output_mutation=True)
def get_drivers_standings():
    return pd.read_csv('data/drivers_standings.csv', index_col=0)

@st.cache(allow_output_mutation=True)
def get_constructors_standings():
    return pd.read_csv('data/constructors_standings.csv', index_col=0)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

image = Image.open('images/season_2022_title.png')

st.image(image, caption='', use_column_width="always")

st.write('\n')
st.write('\n')
st.write('\n')

"""
Race calendar
* Point 1
* Point 2
"""
st.write('\n')
st.write('\n')
"""
Season ranking
* Drivers
    * VER
    * CRO
* Team
    * Renault
    * Peugeot
"""
st.write('\n')
st.write('\n')

"""
Racetrack shapes


"""

col1, col2, col3 = st.columns([2, 3, 2])

with col1:
    st.selectbox(
        'Select a racetrack',
        ('Track 1', 'Track 2', 'Track 3'))

with col3:
    st.write("Racetrack Placeholder")