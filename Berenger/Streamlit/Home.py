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

st.markdown("<h1 style='text-align: center;'>F1 Jedha</h1>", unsafe_allow_html=True)

st.write('\n')
st.write('\n')
st.write('\n')

"Our project consists of XXXX and YYYY"

"""
* Point 1
* Point 2
* Point 3
* Point 4
"""


"Team: Adrien, Bérenger, Christophe, Guillaume"