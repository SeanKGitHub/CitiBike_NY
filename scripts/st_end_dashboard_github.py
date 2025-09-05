# Import Libraries
import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image

########################### Initial settings for dashboard ####################################################


st.set_page_config(page_title = 'Citibike NY Strategy Dashboard', layout='wide')

# define pages and navigation logic
pages = [
    "Intro page",
    "When and how are people using Citibike?",
    "Membership and Vehicle Types",
    "Most Popular Bike Routes", 
    "Busiest stations",
    "Expansion Considerations: Population, Income and Subway Network",
    "Recommendations"
]

# Initialize session state for page index
if "page_idx" not in st.session_state:
    st.session_state.page_idx = 0

# Sidebar selector (keeps direct access)
selected_page = st.sidebar.selectbox(
    'Select an aspect of the analysis',
    pages,
    index=st.session_state.page_idx
)
if selected_page != pages[st.session_state.page_idx]:
    st.session_state.page_idx = pages.index(selected_page)
page = pages[st.session_state.page_idx]

# Arrow navigation buttons
col_prev, col_next = st.columns([1, 1])
with col_prev:
    if st.button("⬅️ Previous") and st.session_state.page_idx > 0:
        st.session_state.page_idx -= 1
with col_next:
    if st.button("Next ➡️") and st.session_state.page_idx < len(pages) - 1:
        st.session_state.page_idx += 1

# Set current page from session state
page = pages[st.session_state.page_idx]

########################## Import data ###########################################################################################
df_sample_100 = pd.read_csv("Data/df_sample_100.csv", index_col=False)
df_weather = pd.read_csv("Data/df_weather.csv", index_col = False)
# Making sure date is datetime and df is sorted by date
df_weather = df_weather.sort_values('date')
df_weather['date'] = pd.to_datetime(df_weather['date'])

df_dow = df_weather[['date', 'trip_count']].copy()
df_dow['day_of_week'] = df_dow['date'].dt.day_name()

  # Determine order of days (it was starting with Satruday)
dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Get average daily trips to plot
avg_trips = df_dow.groupby('day_of_week')['trip_count'].mean().reset_index()
avg_trips['day_of_week'] = pd.Categorical(avg_trips['day_of_week'], categories=dow_order, ordered=True)
avg_trips = avg_trips.sort_values('day_of_week')


######################################### DEFINE THE PAGES #####################################################################

### Intro page

if page == "Intro page":
    
    st.title("Citibike NY Strategy Dashboard")

    col1, col2 = st.columns([1, 2])  # adjust ratio for image vs text space

    with col1:
        try:
          bikes = Image.open("visualisations/vertical_bikes_redbrick.png")   # Photo by <a href="https://unsplash.com/@hanyangzhang?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Hanyang Zhang</a> on <a href="https://unsplash.com/photos/bicycles-parked-on-the-side-of-a-street-KcOoW1Tv06Q?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>
          st.image(bikes, use_container_width=True)
        except Exception as e:
          st.warning(f"Image could not be loaded: {e}")

    with col2:
      st.markdown("#### This dashboard provides insights for the expansion plans of Citibike and gives a helpful overview of usage patterns")
      st.markdown(" The dashboard is separated into 6 sections:")
      st.markdown("- When and how are people using Citibike?")
      st.markdown("- Membership and Vehicle Types")
      st.markdown("- Most Popular Bike Routes")
      st.markdown("- Busiest stations")
      st.markdown("- Expansion Considerations: Population, Income and Subway Network")
      st.markdown("- Recommendations")
      st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis")


##### When and how are people using Citibike page ###############

elif page == "When and how are people using Citibike?":

  st.title("When and how are people using Citibike?")

  # Line plot of daily trips annotated with seasonal averages

  st.image("visualisations/season_annotated.png")
  st.markdown(
      "There is a clear seasonal pattern to the number of daily trips, with the summer months having over double"
      "the average daily # of trips compared to Winter. If cost-effective, there is large scope here"
      " to reduce capacities in the Winter months."
  )

#              Average trips per day of week plot 
  fig_dow = go.Figure(go.Bar(x=avg_trips['day_of_week'], y=avg_trips['trip_count']))
# Add figure title
  fig_dow.update_layout(
    title_text="Bar Chart of Average Daily Trips by Day of the Week",
    yaxis_range=[0, 100000]  
  )
  st.plotly_chart(fig_dow, use_container_width=True)
  st.markdown(
   "We see a midweek peak for average trips per day of the week, ramping up "
   "from Monday, peaking on Wednesday, and Sunday being the least busy day. "
   "As evidenced by the consistently high number of trips from Tuesday to Friday, we see "
   "that midweek ridership is strong and steady. The lower numbers on Monday could be "
   "due to fatigue from the weekend or more people in home office.")

#           dual axis line plot with temperature and total trips
# Create figure with secondary y-axis
  fig_temp = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
  fig_temp.add_trace(
    go.Scatter(x=df_weather['date'], 
               y=df_weather['temperature'],
               name = 'daily temperature', 
               line=dict(color='red')),
    secondary_y=False
)

  fig_temp.add_trace(
    go.Scatter(x=df_weather['date'], 
               y=df_weather['trip_count'],
               name='daily bike rides',
               line=dict(color='blue')),
    secondary_y=True
)

# Add figure title
  fig_temp.update_layout(
    title_text="Line Plot of Daily Citibike Trips and Temperature - New York 2022"
)

# Set x-axis title
  fig_temp.update_xaxes(title_text="Date")

# Set y-axes titles
  fig_temp.update_yaxes(title_text="Temperature (Daily Average °C)", secondary_y=False)
  fig_temp.update_yaxes(title_text="Number of Citibike Trips", secondary_y=True)

  st.plotly_chart(fig_temp, use_container_width=True)
  st.markdown(
   "There is a clear link between temperature and the number of trips. The amount of "
   "Citibike trips generally rises and drops with the average daily temperature, corresponding with the"
   "above seasonal pattern." \
   "However since there are some strong dips despite higher temperature, we will look at "
   "precipiation also"
)

#           Dual axis line plot with percipitation and total trips

# Create figure with secondary y-axis
  fig_rain = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
  fig_rain.add_trace(
    go.Scatter(x=df_weather['date'], 
               y=df_weather['precipitation'],
               name = 'daily precipitation',
               line=dict(color='red')),
    secondary_y=False
  )
  fig_rain.update_yaxes(autorange='reversed', secondary_y=False)

  fig_rain.add_trace(
    go.Scatter(x=df_weather['date'], 
               y=df_weather['trip_count'],
               name='daily bike rides',
               line=dict(color='blue')),
    secondary_y=True
  )

# Add figure title
  fig_rain.update_layout(
    title_text="Line Plot of Daily Citibike Trips and Precipitation - New York 2022"
  )

# Set x-axis title
  fig_rain.update_xaxes(title_text="Date")

# Set y-axes titles
  fig_rain.update_yaxes(title_text="Precipitation (mm)", secondary_y=False)
  fig_rain.update_yaxes(title_text="Number of Citibike Trips", secondary_y=True)

  st.plotly_chart(fig_rain, use_container_width=True)
  st.markdown(
   "Looking into these seemingly random dips further, we see the extreme dips in number of trips align closely with very rainy days"
  )



##################### Membership and Vehicle Types page ###################

elif page == "Membership and Vehicle Types":
    
  st.title("Membership and Vehicle Types")

    # Define color mapping
  custom_colors = {
      'member': 'blue',
      'casual': 'orange'
  }

  fig_members = px.box(
      df_sample_100,
      x='rideable_type',
      y='trip_duration',
      color='member_casual',
      color_discrete_map=custom_colors,
      points='outliers', 
      title='Trip Duration by Ride Type and Membership',
      hover_data=[],
      labels={
          "rideable_type": "Bike Type",
          "trip_duration": "Trip Duration (mins)",
          "member_casual": "Membership Type"
      }
  )
  fig_members.update_traces(hoverinfo='skip', hovertemplate=None)

  st.plotly_chart(fig_members, use_container_width=True)
  st.markdown("Regardless of ride type, we see on the box plots that members (blue) tend to have shorter trips "
              "than casual users. This is likely due to members using the bikes for regular activities and errands, "
              "while casual members use them for recreational activities and sightseeing that are longer durations. " \
              "With casual members we see that their rides with classic bikes last longer than with electric bikes, "
              "but with members there's virtually no difference - they're taking quick trips with either type of bike")
  

########### top 1000 trips visualisation ############################

elif page == "Most Popular Bike Routes":

    st.title("Most Popular Bike Routes")

  ### Create the map ###

    st.write("Interactive map showing top 1000 most popular bike routes")

    path_to_html = "visualisations/routes.html" 

    # Read file and keep in variable
    with open(path_to_html, 'r', encoding='utf-8') as f: 
      html_data = f.read()

    ## Show in webpage
    st.header("Top 1000 Citibike routes in New York 2022")
    st.components.v1.html(html_data,height=500)
    st.caption("First of all we can see that of the top 1000 most popular routes, the vast majority "
                "are in Manhattan. We also see that there are a lot of North-South routes that are popular, " 
                "like those at Central Park and along the West coast of the island up until the Lincoln Bridge. " 
                "Around Midtown and Chelsea we see a large clustering of popular short-distance routes in all directions. " \
                "There is also the notable inclusion of routes around the main bridges, indicating people using the bikes"
                "as part of their journeys between boroughs." \
                "" \
                "Another interesting fact is while only 3% of all trips end at the same station they started from, "
                "14 of the top 20 most popular routes were such round trips."
                )
    

#################### Busiest station page #######################

elif page == "Busiest stations":
  st.title("Top 100 busiest citibike stations by daily departures")

  st.write("Scroll over the map for station statistics")

  path_to_html = "visualisations/top100_stations.html" 

  # Read file and keep in variable
  with open(path_to_html, 'r', encoding='utf-8') as f: 
      html_data = f.read()

    ## Show in webpage
  st.header("100 Busiest Citibike Stations in New York 2022")
  st.components.v1.html(html_data,height=500)
  st.markdown("Perhaps unsurprisingly, the busiest stations are on Manhattan, in particular midtown and the lower half of Manhattan."
              "For operations, it's worth noting that of these busiest stations, none have departures and arrivals that are extremely out-of-balance - "
              "no station sees more than a 5% difference between arrivals and departures")


################## Expansions condsiderations layered maps ###########################

elif page == "Expansion Considerations: Population, Income and Subway Network":

  st.title("Citibike station locations and NY Neighbourhood information")

  choice = st.selectbox("Choose map background:", ["Population Density", "Income"])

  if choice == "Population Density":
        html_file = "visualisations/stops_layers_pop.html"
        map_notes = """
        **Map Notes**
        - This map shows population density by NTA region.
        - Darker purple mean higher population density.
        - The three blue shapes (one in Brooklyn, one in Queens, one in the Bronx) are where we would suggest expansion efforts be focussed, if reaching the most amount of people is the primary consideration.
        - Use selector above to view income layer.
        """

  else:
        html_file = "visualisations/stops_layers_inc.html"
        map_notes = """
        **Map Notes**
        - This map shows median household income by NTA region.
        - Darker Grey means higher income.
        - Light colour areas (and especially those not close to a subway station) stand out from an accessibility perspective as major candidates for expansion.
        - The proposed expansion areas based on accessibility are virtually the same as the previous for population density, with the addition of another area in South Brooklyn with low income and limited Subway accessibility"""

  # --- Columns layout ---
  col1, col2 = st.columns([3, 1])  

  with col1:
      # Display html map
      with open(html_file, "r", encoding="utf-8") as f:
          html_content = f.read()
      st.components.v1.html(html_content, height=500)

  with col2:
      # Display map-specific notes
      st.markdown(map_notes)


########################### Final recommendations page #############################

else:
    
      # --- Page title and intro ---
  st.title("Conclusions and Recommendations")
  st.subheader("Priority actions for improving Citibike performance and expansion plan")

  st.markdown(
      "Based on the analysis of population density, income distribution, and ridership patterns, "
      "we recommend the following strategic interventions to improve accessibility, efficiency, "
      "and equity in the Citibike network." \
      "Implementation should be phased, prioritising high-impact, low-cost measures first. "
      "Community engagement is essential to ensure solutions align with local needs."
  )

  # --- Card-style layout ---
  col1, col2, col3 = st.columns(3)

  with col1:
      st.markdown("""
        <div style="background-color:#006BB6; border-radius:12px; min-height:220px; overflow:hidden;">
            <h4 style="
                background-color:#F58426; 
                color:#FFFFFF; 
                margin:0; 
                padding:12px;
            ">
                  Fleet Allocation
            </h4>
            <div style="padding:20px;">
                <ul style="color:#FFFFFF; margin:0;">
        <li>Increase bike availability mid-week (especially Wednesday and Thursday) to avoid shortages.</li> 
        <li>Shift some maintenance/repairs to low-demand days like Sunday or Monday.</li>
      </ul>
      </div>
      """, unsafe_allow_html=True)

  with col2:
      st.markdown("""
        <div style="background-color:#006BB6; border-radius:12px; min-height:220px; overflow:hidden;">
            <h4 style="
                background-color:#F58426; 
                color:#FFFFFF; 
                margin:0; 
                padding:12px;
            ">
                Promotions on low-demand days
            </h4>
            <div style="padding:20px;">
                <ul style="color:#FFFFFF; margin:0;">
        <li>Offer discounts or loyalty points on Sunday and Monday to encourage leisure or tourist trips. E.g., "Sunday Fun Ride: X% Off" could stimulate usage.</li>
        <li>Can also target tourist attractions, scenic routes, and group rides on weekend marketing campaigns.</li>
      </ul>
      </div>
      """, unsafe_allow_html=True)

  with col3:
      st.markdown("""
        <div style="background-color:#006BB6; border-radius:12px; min-height:220px; overflow:hidden;">
            <h4 style="
                background-color:#F58426; 
                color:#FFFFFF; 
                margin:0; 
                padding:12px;
            ">
                  Seasonal Operations
            </h4>
            <div style="padding:20px;">
                <ul style="color:#FFFFFF; margin:0;">
        <li>Increase operational capacities during the warmer months to handle increased demand.</li>
        <li>Reduce rebalancing resources in colder months and during forecasted heavy rain days</li>
      </ul>
      </div>
      """, unsafe_allow_html=True)

  # --- Another row of recommendations ---
  col4, col5, col6 = st.columns(3)

  with col4:
      st.markdown("""
        <div style="background-color:#006BB6; border-radius:12px; min-height:220px; overflow:hidden;">
            <h4 style="
                background-color:#F58426; 
                color:#FFFFFF; 
                margin:0; 
                padding:12px;
            ">
                  User Type and Trip Duration Recommendations
            </h4>
            <div style="padding:20px;">
                <ul style="color:#FFFFFF; margin:0;">
          <li><b>Casual Users</b> Market scenic and recreational routes (Central Park, Waterfront) and provide guides.</li>
          <li><b>Members</b> Ensure stations in high-density errand zones have sufficients docking spots.</li>
          <li><b>Members</b> Push promotions for off-peak quick trips to reduce congestion in rush hours. </li>
        </ul>
      </div>
      """, unsafe_allow_html=True)

  with col5:
      st.markdown("""
        <div style="background-color:#006BB6; border-radius:12px; min-height:220px; overflow:hidden;">
            <h4 style="
                background-color:#F58426; 
                color:#FFFFFF; 
                margin:0; 
                padding:12px;
            ">
                  Station-Level Actions
            </h4>
        <div style="padding:20px;">
                <ul style="color:#FFFFFF; margin:0;">
          <li>Evaluate if the popular round-trip stations could use extra docks to handle surges.</li>
          <li>Maintain current balance-focused station management as current rebalancing working well. Monitor and tweak the few exception stations</li>
        </ul>    
      </div>
      """, unsafe_allow_html=True)

  with col6:
      st.markdown("""
        <div style="background-color:#006BB6; border-radius:12px; min-height:220px; overflow:hidden;">
            <h4 style="
                background-color:#F58426; 
                color:#FFFFFF; 
                margin:0; 
                padding:12px;
            ">
                  Expansion Recommendations
            </h4>
        <div style="padding:20px;">
                <ul style="color:#FFFFFF; margin:0;">
          <li><b>Primary Focus Areas</b> Three new zones: one in Brooklyn, one in Queens and one in the Bronx capture the largest potential ridership increase and also serve lower income neighbourhoods</li>
          <li><b>Accessibility-based additional zone</b> A further South Brooklyn expansionary zone targeting low-income areas with poor subway access has high potential for improving transit equity.</li>     
          <li><b>Implementation Sequence</b>
            <ul>
              <li><b>Phase 1:</b> 3 new zones with highest projected ridership.</li>
              <li><b>Phase 2:</b> Equity-focused South Brooklyn expansion.</li>
              <li>Ensure each expansion phase is paired with awareness campaigns in those neighbourhoods.</li>
            </ul>
          </li>
        </ul>
      </div>
      """, unsafe_allow_html=True)

  zones = Image.open("visualisations/Expansion_zones.png")  #source: own KeplerGL image
  st.image(zones, use_container_width=True)

# --- Navigation buttons at the bottom ---
col_prev_btm, col_next_btm = st.columns([1, 1])
with col_prev_btm:
    if st.button("⬅️ Previous", key="prev_btm") and st.session_state.page_idx > 0:
        st.session_state.page_idx -= 1
with col_next_btm:
    if st.button("Next ➡️", key="next_btm") and st.session_state.page_idx < len(pages) - 1:
        st.session_state.page_idx += 1