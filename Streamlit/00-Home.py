import fastf1 as ff1
from fastf1 import plotting
plotting.setup_mpl()
ff1.Cache.enable_cache('cache/')
import plotly.io as pio
from plotly.subplots import make_subplots
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

# Display page title
image = Image.open('images/title.png')
st.image(image, caption='', use_column_width="always")

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
    st.write('\n')
    st.write('\n')
    """
    Content:
    * F1 Season 2022: Provides informations about the current rankings, and offers a visualization of the points comparison between two drivers.
    * Race Strategy: A prediction of the optimal pit strategies for a race, based on the free practice sessions, and sprint when applicable.
    * Session Analysis: Various visualizations and informations regarding one session, and comparing data between two drivers.
    
    Note : All the visualizations on this dashboard can be opened in full screen using the top right button that appears on mouse hover.
    """
    st.write('\n')
    st.write('\n')
    """
    Team:
    * Adrien: [Linkedin](https://www.linkedin.com/in/adrienory) / [Github](https://github.com/AdrienOry)
    * Bérenger: [Linkedin](https://www.linkedin.com/in/berenger-queune/) / [Github](https://github.com/BerengerQueune)
    * Christophe: [Linkedin](https://www.linkedin.com/in/clefebvre78/) / [Github](https://github.com/clefebvre2021)
    * Guillaume: [Linkedin](https://www.linkedin.com/in/guillaumearp/) / [Github](https://github.com/GuillaumeArp)
    """ 