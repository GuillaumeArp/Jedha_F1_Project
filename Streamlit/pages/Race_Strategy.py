import fastf1 as ff1
from fastf1 import plotting
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

compound_colors = {
    'SOFT': '#FF3333',
    'MEDIUM': '#FFF200',
    'HARD': '#EBEBEB',
}

# Functions

def plot_tyre_life(gp_round):
    '''
    Plots the evolution of the tyre life
    '''
    
    url = f'https://f1-jedha-bucket.s3.eu-west-3.amazonaws.com/data/tyre_life_data_{gp_round}.csv'
    df_times = pd.read_csv(url, index_col=0)
    event_name = events_list.iloc[gp_round]['EventName']
    plot_title = f"{event_name} - Tyre Life Prediction"
    hovertemplate = '<b>Lap:</b> %{x}<br><b>Time:</b> %{customdata}'

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_times[df_times['Tyre'] == 'SOFT']['Lap'],
                            y=df_times[df_times['Tyre'] == 'SOFT']['FinalLapTime'],
                            mode='lines',
                            name='Soft',
                            line_color=compound_colors['SOFT'],
                            customdata=df_times[df_times['Tyre'] == 'SOFT']['TimeStr'],
                            hovertemplate=hovertemplate))

    fig.add_trace(go.Scatter(x=df_times[df_times['Tyre'] == 'MEDIUM']['Lap'],
                            y=df_times[df_times['Tyre'] == 'MEDIUM']['FinalLapTime'],
                            mode='lines',
                            name='Medium',
                            line_color=compound_colors['MEDIUM'],
                            customdata=df_times[df_times['Tyre'] == 'MEDIUM']['TimeStr'],
                            hovertemplate=hovertemplate))

    fig.add_trace(go.Scatter(x=df_times[df_times['Tyre'] == 'HARD']['Lap'],
                            y=df_times[df_times['Tyre'] == 'HARD']['FinalLapTime'],
                            mode='lines',
                            name='Hard',
                            line_color=compound_colors['HARD'],
                            customdata=df_times[df_times['Tyre'] == 'HARD']['TimeStr'],
                            hovertemplate=hovertemplate))

    fig.update_yaxes(title_text="Lap Time (seconds)")
    fig.update_xaxes(title_text=f"Lap")
    fig.update_layout(width=1000,
                      height=700,
                      template='plotly_dark',
                      yaxis_range=[df_times['FinalLapTime'].min() - 2, df_times['LapTimeSeconds'].max() + 10],
                      hovermode='x',
                      title_text=plot_title,
                      title_x=0.5)
    return fig


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

image = Image.open('images/race_strategy_title.png')

st.image(image, caption='', use_column_width="always")


st.write('\n')
st.write('\n')
st.write('\n')


top_row = events_list.loc[[2]]
top_row.rename(index={2:1},inplace=True)
top_row["EventName"] = "Select an event"
events_list = pd.concat([top_row, events_list], axis=0)

col1, col2, col3 = st.columns([4, 2, 4])

with col2:
    gp_name = st.selectbox('', (events_list["EventName"]))

gp_round = events_list[events_list['EventName'] == gp_name]['RoundNumber'].values[0]

try:
    
    col1, col2, col3, col4, col5, col6 = st.columns([1, 15, 1, 1, 15, 1])
    
    with col2:
        if gp_name == "Select an event":
            st.write('\n')
            st.write('\n')
            st.write('\n')
            st.markdown("<h5 style='text-align: center; color: white;'>No selection made</h5>", unsafe_allow_html=True)
        else:
            st.plotly_chart(plot_tyre_life(gp_round))
    
except:
    st.write("")
    st.write("")
    st.markdown("<h1 style='text-align: center; color: red;'>No data available yet</h1>", unsafe_allow_html=True)