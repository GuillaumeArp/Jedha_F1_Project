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



with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

image = Image.open('images/race_strategy_title.png')

st.image(image, caption='', use_column_width="always")


st.write('\n')
st.write('\n')
st.write('\n')

# Global variables

events_list = ff1.get_event_schedule(2022)[2:]

col1, col2, col3 = st.columns([3, 6, 3])

with col2:
    gp_name = st.selectbox('Event', (events_list["EventName"]))
