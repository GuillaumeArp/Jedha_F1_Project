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



my_raceplot = barplot(new_df,  item_column='Driver', value_column='Time_Diff', time_column='LapNumber')
fig = my_raceplot.plot(item_label = 'Drivers', value_label = 'pop', frame_duration = 600)

st.plotly_chart(fig, use_container_width=True)





db = pd.read_csv('https://raw.githubusercontent.com/pythoninoffice/pythonio_examples/main/matplotlib_bar_chart_race/dragon_ball_pl.csv')

db.head()

one_row = db.iloc[0]
one_row_ascending = one_row.sort_values()
characters = db.columns

fix, ax = plt.subplots(figsize=(10,10))
ax.barh(y = range(len(characters)), 
        tick_label = one_row_ascending.index,
        width = one_row_ascending.values, 
        align='center',
        color = plt.cm.Set1(range(len(characters))))


db.head(3)


num = 3
fig, axs = plt.subplots(nrows = 1, ncols = num, figsize = (10, 5), tight_layout = True)
for i, ax in enumerate(axs):
    ax.barh(y=db.iloc[i].rank(),
            tick_label = db.iloc[i].index,
            width = db.iloc[i].values,
            color = plt.cm.Set1(range(6)))
    ax.set_title(f'{i}-th row', fontsize='larger')
    [spine.set_visible(False) for spine in ax.spines.values()]  # remove chart outlines

from matplotlib.animation import FuncAnimation

db.index = range(0,21*10,10)
print(list(db.index))
[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]

row_nums = [i for i in range(0,210) if i % 10 != 0 ]
empty = pd.DataFrame(np.nan, index= row_nums, columns = db.columns)

expand_df = pd.concat([db, empty]).sort_index()

rank_df = expand_df.rank(axis=1)

expand_df = expand_df.interpolate()
rank_df = rank_df.interpolate()

num = 3
fig, axs = plt.subplots(nrows = 1, ncols = num, figsize = (10, 5), tight_layout = True)
for i, ax in enumerate(axs):
    ax.barh(y=rank_df.iloc[i].values,
            tick_label = expand_df.iloc[i].index,
            width = expand_df.iloc[i].values,
            color = plt.cm.Set1(range(6)))
    ax.set_title(f'{i}-th row', fontsize='larger')
    [spine.set_visible(False) for spine in ax.spines.values()]  # remove chart outlines


def update(i):
    ax.clear()
    ax.set_facecolor(plt.cm.Dark2(0.9))
    [spine.set_visible(False) for spine in ax.spines.values()]
    hbars = ax.barh(y = rank_df.iloc[i].values,
           tick_label=expand_df.iloc[i].index,
           width = expand_df.iloc[i].values,
           height = 0.8,
           color = plt.cm.Dark2(range(11))
           )
    ax.set_title(f'Frame: {i}')
    ax.bar_label(hbars, fmt='%.2d')
    

fig,ax = plt.subplots(#figsize=(10,7),
                      facecolor = plt.cm.Dark2(0.9),
                      dpi = 150,
                      tight_layout=True
                     )


data_anime = FuncAnimation(
    fig = fig,
    func = update,
    frames= len(expand_df),
    interval=100
)

data_anime.save("test.gif")


import base64

"""### gif from local file"""
file_ = open("test.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
    unsafe_allow_html=True,
)