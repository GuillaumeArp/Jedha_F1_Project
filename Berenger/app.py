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

import bar_chart_race as bcr


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

df = df[["Time", "LapNumber", "Driver"]]

import re
#Convert Time to seconds
def time_to_seconds(string):
    array = re.findall(r'[0-9]+', str(string))
    array = array[1:]
    array[0] = int(array[0]) * 3600
    array[1] = int(array[1]) * 60
    array = float(str(array[0] + array[1] + int(array[2])) + "." + array[3])
    
    return array

df["Time"] = df["Time"].apply(time_to_seconds)

df["LapNumber"] = df["LapNumber"].astype(int)
LapNumber = max(df["LapNumber"])

df = df[df["LapNumber"] != 0]

new_df = pd.DataFrame()
for i in range(1, LapNumber):
    df_i = df[df["LapNumber"] == i]
    minimum = min(df_i["Time"])
    df_i["Time_Diff"] = df_i["Time"] - minimum
    #concatenate new dataframe
    new_df = pd.concat([new_df, df_i])

new_df

my_raceplot = barplot(new_df,  item_column='Driver', value_column='Time_Diff', time_column='LapNumber')
fig = my_raceplot.plot(item_label = 'Drivers', value_label = 'pop', frame_duration = 600)

st.plotly_chart(fig, use_container_width=True)




data = pd.read_csv('https://raw.githubusercontent.com/lc5415/raceplotly/main/example/FAOSTAT_data.csv')

my_raceplot = barplot(data,  item_column='Item', value_column='Value', time_column='Year')

fig = my_raceplot.plot(item_label = 'Top 10 crops', value_label = 'Production quantity (tonnes)', frame_duration = 800)

st.plotly_chart(fig, use_container_width=True)


new_df2 = new_df.pivot_table(values='Time_Diff', index=df.LapNumber, columns=df.Driver)
new_df2.head()

fig = bcr.bar_chart_race(new_df2)

st.pyplot(fig)

