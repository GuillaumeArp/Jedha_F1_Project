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

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

image = Image.open('images/season_2022_title.png')

st.image(image, caption='', use_column_width="always")


st.write('\n')
st.write('\n')
st.write('\n')


col1, col2, col3, col4, col5, col6 = st.columns([4, 2, 2, 2, 2, 4])

with col3:
    driver_1 = st.selectbox('First driver', (session.results["Abbreviation"]), index = 0)

with col4:
    driver_2 = st.selectbox('Second driver', (session.results["Abbreviation"]), index = 1)













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

