# Importing Libraries
import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt 

####################### Configure the page ################################
st.set_page_config(page_title = 'Citibike NY Strategy Dashboard', layout='wide')

############################ Set title ###############################
st.title("Citibike NY Strategy Dashboard")

st.markdown("The dashboard will help us understand Citibike usage trends")

########################### Import Data ###############################
top_20 = pd.read_csv('C:/Data/Citibike_NY_2022/merged/top_20.csv', index_col=False)
routes = pd.read_csv("C:/Data/Citibike_NY_2022/merged/routes.csv", index_col=False)
df_weather = pd.read_csv("C:/Data/Citibike_NY_2022/merged/df_weather.csv", index_col = False)

######################### Creating Charts ###############################
###### Bar Graph of top 20 stations
fig = go.Figure(go.Bar(x=top_20['start_station_name'], y=top_20['num_trips']))

fig.update_layout(
    title = 'Top 20 most popular bike stations in New York City (2022)',
    xaxis_title = 'Start stations',
    yaxis_title ='Total trips started',
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width=True)


###### Dual axis line plot with temperature and total trips
# Making sure date is datetime and df is sorted by date
df_weather = df_weather.sort_values('date')
df_weather['date'] = pd.to_datetime(df_weather['date'])

# Create figure with secondary y-axis
fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig_2.add_trace(
    go.Scatter(x=df_weather['date'], y=df_weather['temperature'],name = 'daily temperature'),
    secondary_y=False
)

fig_2.add_trace(
    go.Scatter(x=df_weather['date'], y=df_weather['trip_count'],name='daily bike rides'),
    secondary_y=True
)

# Add figure title
fig_2.update_layout(
    title_text="Line Plot of Daily Citibike Trips and Temperature - New York 2022"
)

# Set x-axis title
fig_2.update_xaxes(title_text="Date")

# Set y-axes titles
fig_2.update_yaxes(title_text="Temperature (Daily Average °C)", secondary_y=False)
fig_2.update_yaxes(title_text="Number of Citibike Trips", secondary_y=True)

st.plotly_chart(fig_2, use_container_width=True)


######## Add the map

path_to_html = "visualisations/NY_trips.html"

# Read file and keep in variable
with open(path_to_html,'r', encoding="utf8") as f: 
    html_data = f.read()

## Show in webpage
st.header("Main Citibike Routes in New York City - 2022 (min 900 trips)")
st.components.v1.html(html_data,height=1000)
