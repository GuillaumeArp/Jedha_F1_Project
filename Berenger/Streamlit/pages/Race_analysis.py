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



### Config
st.set_page_config(
    page_title="FastF1",
    page_icon=":racing_car:",
    layout="wide"
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



st.markdown("<h1 style='text-align: center;'>Race Analysis</h1>", unsafe_allow_html=True)
st.write('\n')
st.write('\n')
st.write('\n')


col1, col2, col3 = st.columns([2, 3, 2])

with col1:
    st.selectbox(
        'Select a racetrack',
        ('Track 1', 'Track 2', 'Track 3'))


st.write('\n')
st.write('\n')
st.write('\n')

"""
Race ranking

Starting Grid

Race chart ?

Best lap comparison
"""
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