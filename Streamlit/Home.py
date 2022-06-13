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

# st.markdown(
#     """
# <style>
# .css-17ziqus.e1fqkh3o3 {
# background-color: black;
# background-image: none;
# color: #ffffff
# }


# </style>
# """,
#     unsafe_allow_html=True,
# )



image = Image.open('images/title.png')

st.image(image, caption='', use_column_width="always")

# image2 = Image.open('images/logoF1.jpg')

# st.sidebar.image(image2, caption='', use_column_width="always")






st.write('\n')
st.write('\n')
st.write('\n')

col1, col2, col3 = st.columns([3, 8, 3])

with col2:

    "The goal of F1 Insights is to provide a platform for the analysis of the 2022 season for the F1 World Championship."

    """
    * Made in June 2022 as a final project for the course [Data Fullstack](https://en.jedha.co/formations/formation-data-scientist)
    * Tech Stack: Docker, Python, Streamlit, Pandas, Plotly, Matplotlib
    * Data Source: [FastF1](https://theoehrly.github.io/Fast-F1/index.html), [F1 API](https://ergast.com/api/f1)
    """

    """
    Content:
    * F1 Season 2022: Provides informations about the current rankings, and offers a visualization of the points comparison between two drivers.
    * Race Strategy: A prediction of the optimal pit strategies for a race, based on the free practice sessions, and sprint when applicable.
    * Session Analysis: Various visualizations and informations regarding one session, and comparing data between two drivers.
    """

    """
    Team:
    * Adrien: [Linkedin](https://www.linkedin.com/in/adrienory) / [Github](https://github.com/AdrienOry)
    * Bérenger: [Linkedin](https://www.linkedin.com/in/berenger-queune/) / [Github](https://github.com/BerengerQueune)
    * Christophe: [Linkedin](https://www.linkedin.com/in/clefebvre78/) / [Github](https://github.com/clefebvre2021)
    * Guillaume: [Linkedin](https://www.linkedin.com/in/guillaumearp/) / [Github](https://github.com/GuillaumeArp)
    """ 