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
pio.templates.default = "plotly_dark"
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
from st_aggrid import AgGrid
from raceplotly.plots import barplot
from collections import deque


### Config
st.set_page_config(
    page_title="FastF1",
    page_icon=":red_car:",
    layout="wide"
)

year = 2022
gp_round = 7
ses = 'FP3'
driver_1 = 'LEC'
driver_2 = 'GAS'

# events_list = ff1.get_event_schedule(2022)[2:]

# session = ff1.get_session(year, gp_round, ses)
# session.load(weather=True, telemetry=True)


session = ff1.get_session(2022, 4 , 'R')
session.load()
session.laps

df = session.laps


raceplot = barplot(df,  item_column='Driver', value_column='LapNumber', time_column='Time')

raceplot.plot(item_label = 'Top 10 Countries', value_label = 'GDP ($)', frame_duration = 800)



st.write('---')
st.markdown('<p class="font">Set Parameters...</p>', unsafe_allow_html=True)
column_list=list(df)
column_list = deque(column_list)
column_list.appendleft('-')
with st.form(key='columns_in_form'):
    text_style = '<p style="font-family:sans-serif; color:red; font-size: 15px;">***These input fields are required***</p>'
    st.markdown(text_style, unsafe_allow_html=True)
    col1, col2, col3 = st.columns( [1, 1, 1])
    with col1:
        item_column=st.selectbox('Bar column:',column_list, index=0, help='Choose the column in your data that represents the bars, e.g., countries, teams, etc.') 
    with col2:    
        value_column=st.selectbox('Metric column:',column_list, index=0, help='Choose the column in your data that represents the value/metric of each bar, e.g., population, gdp, etc.') 
    with col3:    
        time_column=st.selectbox('Time column:',column_list, index=0, help='Choose the column in your data that represents the time series, e.g., year, month, etc.')   

    text_style = '<p style="font-family:sans-serif; color:blue; font-size: 15px;">***Customize and fine-tune your plot (optional)***</p>'
    st.markdown(text_style, unsafe_allow_html=True)
    col4, col5, col6 = st.columns( [1, 1, 1])
    with col4:
        direction=st.selectbox('Choose plot orientation:',['-','Horizontal','Vertical'], index=0, help='Specify whether you want the bar chart race to be plotted horizontally or vertically. The default is horizontal' ) 
        if direction=='Horizontal'or direction=='-':
            orientation='horizontal'
        elif  direction=='Vertical':   
            orientation='vertical'
    with col5:
        item_label=st.text_input('Add a label for bar column:', help='For example: Top 10 countries in the world by 2020 GDP')  
    with col6:
        value_label=st.text_input('add a label for metric column', help='For example: GDP from 1965 - 2020') 

    col7, col8, col9 = st.columns( [1, 1, 1])
    with col7:
        num_items=st.number_input('Choose how many bars to show:', min_value=5, max_value=50, value=10, step=1,help='Enter a number to choose how many bars ranked by the metric column. The default is top 10 items.')
    with col8:
        format=st.selectbox('Show by Year or Month:',['-','By Year','By Month'], index=0, help='Choose to show the time series by year or month')
        if format=='By Year' or format=='-':
            date_format='%Y'
        elif format=='By Month':
            date_format='%x'   
    with col9:
        chart_title=st.text_input('Add a chart title', help='Add a chart title to your plot')    
    
    col10, col11, col12 = st.columns( [1, 1, 1])
    with col10:
        speed=st.slider('Animation Speed',10,500,100, step=10, help='Adjust the speed of animation')
        frame_duration=500-speed  
    with col11:
        chart_width=st.slider('Chart Width',500,1000,500, step=20, help='Adjust the width of the chart')
    with col12:    
        chart_height=st.slider('Chart Height',500,1000,600, step=20, help='Adjust the height of the chart')

    submitted = st.form_submit_button('Submit')


st.write('---')
if submitted:        
    if item_column=='-'or value_column=='-'or time_column=='-':
        st.warning("You must complete the required fields")
    else: 
        st.markdown('<p class="font">Generating your bar chart race plot... And Done!</p>', unsafe_allow_html=True)   
        df['time_column'] = pd.to_datetime(df[time_column])
        df['value_column'] = df[value_column].astype(float)

        raceplot = barplot(df,  item_column=item_column, value_column=value_column, time_column=time_column,top_entries=num_items)
        fig=raceplot.plot(item_label = item_label, value_label = value_label, frame_duration = frame_duration, date_format=date_format,orientation=orientation)
        fig.update_layout(
        title=chart_title,
        autosize=False,
        width=chart_width,
        height=chart_height,
        paper_bgcolor="lightgray",
        )
        st.plotly_chart(fig, use_container_width=True)