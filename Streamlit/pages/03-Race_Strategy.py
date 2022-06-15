import fastf1 as ff1
from fastf1 import plotting
plotting.setup_mpl()
ff1.Cache.enable_cache('cache/')
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
pio.templates.default = "plotly_dark"
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import streamlit as st
from PIL import Image

from timple.timedelta import strftimedelta
ff1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)

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
    fig.update_xaxes(title_text=f"Laps")
    fig.update_layout(width=1000,
                      height=700,
                      template='plotly_dark',
                      yaxis_range=[df_times['FinalLapTime'].min() - 2, df_times['LapTimeSeconds'].max() + 10],
                      hovermode='x',
                      title_text=plot_title,
                      title_x=0.5)
    return fig

def format_dataframe(gp_round):
    '''
    Returns a formatted dataframe suitable for plotting strategy predictions
    '''
    url = f'https://f1-jedha-bucket.s3.eu-west-3.amazonaws.com/data/predicted_strategy_round_{gp_round}.csv'
    df = pd.read_csv(url, index_col=0).reset_index(drop=True)
    
    compound_colors = {
        'SOFT': '#FF3333',
        'MEDIUM': '#FFF200',
        'HARD': '#EBEBEB',
        'INTERMEDIATE': '#39B54A',
        'WET': '#00AEEF',
    }
    
    def expand_strategy(string):
        return string.replace('S', 'SOFT,').replace('M', 'MEDIUM,').replace('H', 'HARD,').split(',')[:-1]

    def get_pit_list(df, pos):
        return df[['Train1', 'Train2', 'Train3']].iloc[pos].tolist()
    
    tyres_list_1 = expand_strategy(df['combiTyre'].iloc[0])
    tyres_list_2 = expand_strategy(df['combiTyre'].iloc[1])

    if len(tyres_list_1) == 2:
        
        dict_df_1 = {'Train1': [get_pit_list(df, 0)[0], tyres_list_1[0]],
                    'Train2': [get_pit_list(df, 0)[1], tyres_list_1[1]]}

        dict_df_2 = {'Train1': [get_pit_list(df, 1)[0], tyres_list_2[0]],
                    'Train2': [get_pit_list(df, 1)[1], tyres_list_2[1]],
                    'Train3': [get_pit_list(df, 1)[2], tyres_list_2[2]]}    
    else:
        
        dict_df_1 = {'Train1': [get_pit_list(df, 0)[0], tyres_list_1[0]],
                    'Train2': [get_pit_list(df, 0)[1], tyres_list_1[1]],
                    'Train3': [get_pit_list(df, 0)[2], tyres_list_1[2]]}
        
        dict_df_2 = {'Train1': [get_pit_list(df, 1)[0], tyres_list_2[0]],
                    'Train2': [get_pit_list(df, 1)[1], tyres_list_2[1]]}
        
    df_strat_1 = pd.DataFrame.from_dict(dict_df_1, orient='index', columns=['Lap', 'Tyre'])
    df_strat_1['Time'] = df['TotalTimeStr'].iloc[0]
    df_strat_1 = df_strat_1.reset_index().rename(columns={'index': 'Strategy'})
    df_strat_1['Order'] = 1

    if len(df_strat_1) == 2:
        df_strat_1['Strategy'] = 'Faster: 1-stop Strategy'
        
    else:
        df_strat_1['Strategy'] = 'Faster: 2-stops Strategy'
        
    df_strat_2 = pd.DataFrame.from_dict(dict_df_2, orient='index', columns=['Lap', 'Tyre'])
    df_strat_2['Time'] = df['TotalTimeStr'].iloc[1]
    df_strat_2 = df_strat_2.reset_index().rename(columns={'index': 'Strategy'})
    df_strat_2['Order'] = 2

    if len(df_strat_2) == 2:
        df_strat_2['Strategy'] = 'Slower: 1-stop Strategy'
        
    else:
        df_strat_2['Strategy'] = 'Slower: 2-stops Strategy'
        
    df_full = pd.concat([df_strat_1, df_strat_2])
    df_full['Colors'] = df_full['Tyre'].map(compound_colors)
    
    return df_full 

def plot_strategies(gp_round):
    '''
    Plots the strategy predictions for the given dataframe
    '''
    df = format_dataframe(gp_round)
    hovertemplate = '<b>Max Tyre Life:</b> %{x}<br><b>Total Race Time:</b> %{customdata}'
    event_name = events_list.iloc[gp_round]['EventName']
    plot_title = f"{event_name} - Optimal Strategies Prediction"

    fig = go.Figure()

    fig.add_trace(go.Bar(x=df['Lap'],
                        y=df['Strategy'],
                        orientation='h',
                        name='Strategy',
                        customdata=df['Time'],
                        marker_color=df['Colors'],
                        hovertemplate=hovertemplate,
                        width=[0.5, 0.5, 0.5, 0.5, 0.5]))

    fig.update_xaxes(title_text=f"Laps")
    fig.update_yaxes(categoryorder='category descending')
    fig.update_layout(width=1000,
                      height=700,
                      barmode='stack',
                      title_text=plot_title,
                      title_x=0.5)

    return fig  

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Display page title
image = Image.open('images/race_strategy_title.png')
st.image(image, caption='', use_column_width="always")

st.write('\n')
st.write('\n')
st.write('\n')

col1, col2, col3 = st.columns([3, 8, 3])

with col2:
    """
    * This pages provides an estimation of the tyre degradation, and our prediction for the optimal strategies.
    * On the left, the chart displays the estimated (and optimal) time per lap on each compound, based on free practice (and sprint) lap times.
    * The right side chart displays our prediction based on this data, and shows the optimal strategies for one and two stops. The mouseover shows the total race time for each one.
    """
    
# Duplicate a row as a new DataFrame
top_row = events_list.loc[[2]]

# Rename index of duplicated row
top_row.rename(index={2:1},inplace=True)

# Rename EventName to add it later in the Streamlit selectbox
top_row["EventName"] = "Select an event"

# Concatenate the two DataFrames to have the new row on top
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
            st.plotly_chart(plot_tyre_life(gp_round), use_container_width=True)
            
    with col5:
        if gp_name == "Select an event":
            st.write('\n')
            st.write('\n')
            st.write('\n')
            st.markdown("<h5 style='text-align: center; color: white;'>No selection made</h5>", unsafe_allow_html=True)
        else:
            df = format_dataframe(gp_round)
            st.plotly_chart(plot_strategies(gp_round), use_container_width=True)
    
except:
    st.write("")
    st.write("")
    st.markdown("<h1 style='text-align: center; color: red;'>No data available yet</h1>", unsafe_allow_html=True)