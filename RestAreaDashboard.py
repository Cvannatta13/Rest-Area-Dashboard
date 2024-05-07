"""
Name: Christopher Van Natta
CS230: Section 4
Data: Rest Areas in California
URL:

Description: This program takes data about rest areas in California and displays it in a way that
allows users to not only learn more about the rest areas, but also filter selections to allow them
to find one that has what they are looking for. Using the sidebar, you can filter by what
amenities are offered and view different lists, bar charts, and a map based on your selections. The
program also shows more general info in forms of pie charts, pivot tables, and expanders with list
comprehensions. My overall idea for this program was to create an interface that allowed users to
easily find a rest area that has what they need.
"""

import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_csv("Rest Area Data.csv")
    df.dropna(inplace=True) #[DA1]
    return df

df = load_data()


st.markdown('<h1 style="color: gold;">The California Rest Area Dashboard</h1>', unsafe_allow_html=True)

#Using California rest area picture as a banner
banner_path = "Rest Area Banner.jpg"
banner = Image.open(banner_path)
st.image(banner, use_column_width=True) #[ST4]


# Custom header with smaller font size and different color
st.markdown("""
## Use the filter selections on the left to find the rest area that has what you need
<style>
h2 {
    font-size: 20px;  /* Adjust the font size as needed */
    color: blue;  /* Sets the color to yellow */
}
</style>
""", unsafe_allow_html=True)

# Filtering data by amenities [DA4]
st.sidebar.header('Filter Amenities:')
restroom = st.sidebar.checkbox('Restroom', True)  #[ST1]
water = st.sidebar.checkbox('Water', True)
picnictab = st.sidebar.checkbox('Picnic Table', True)
phone = st.sidebar.checkbox('Phone', True)
handicap = st.sidebar.checkbox('Handicap Access', True)
rv_station = st.sidebar.checkbox('RV Station', True)
vending = st.sidebar.checkbox('Vending Machines', True)
pet_area = st.sidebar.checkbox('Pet Area', True)

# Filter data based on selections [DA5]
filtered_data = df[
    (df['RESTROOM'] == 'Yes' if restroom else True) &
    (df['WATER'] == 'Yes' if water else True) &
    (df['PICNICTAB'] == 'Yes' if picnictab else True) &
    (df['PHONE'] == 'Yes' if phone else True) &
    (df['HANDICAP'] == 'Yes' if handicap else True) &
    (df['RV_STATION'] == 'Yes' if rv_station else True) &
    (df['VENDING'] == 'Yes' if vending else True) &
    (df['PET_AREA'] == 'Yes' if pet_area else True)
]

# Slider to select the number of rest areas to display
number_to_display = st.sidebar.slider('Number of rest areas to display:', 1, len(filtered_data), 10) #[ST2]

st.markdown('<h2 style="color: gold; text-decoration: underline;">Filtered Rest Area List</h2>', unsafe_allow_html=True)
st.write(filtered_data.head(number_to_display))


# Function to get count of rest areas by county
def count_by_county(df): #[PY3]
    return df['COUNTY'].value_counts()

county_counts = count_by_county(filtered_data)
st.markdown('<h2 style="color: gold; text-decoration: underline;">Filtered Number of Rest Areas by County</h2>', unsafe_allow_html=True)
st.bar_chart(county_counts) #[VIZ1]

# Function to create a map visualization
def create_map(df): #[VIZ1]
    st.map(df[['LATITUDE', 'LONGITUDE']])

st.markdown('<h2 style="color: gold; text-decoration: underline;">Filtered Map of Rest Areas</h2>', unsafe_allow_html=True)
create_map(filtered_data)

# Function with two or more parameters, one with a default
def get_areas_by_district(df, district, columns=['NAME', 'ADDRESS', 'CITY']): #[PY1] [PY2]
    return df[df['DISTRICT'] == district][columns]


st.markdown('<h2 style="color: blue;">Just looking for one in your district? Select your district number on the left</h2>', unsafe_allow_html=True)

#Allows user to select their district number and see rest areas
district = st.sidebar.selectbox('Select a District:', df['DISTRICT'].unique())
st.markdown(f'<h2 style="color: gold; text-decoration: underline;">Rest Areas in District {district}</h2>', unsafe_allow_html=True)
district_data = get_areas_by_district(df, district)
st.write(district_data)

st.markdown('<h2 style="color: blue;">General Information</h2>', unsafe_allow_html=True)

# Bar chart based on rest areas by city using Altair
city_counts = df['CITY'].value_counts().reset_index()
city_counts.columns = ['City', 'Number of Rest Stops']

st.markdown('<h2 style="color: gold; text-decoration: underline;">Rest Areas by City</h2>', unsafe_allow_html=True)

chart = alt.Chart(city_counts).mark_bar().encode(
    x='City',
    y='Number of Rest Stops',
    color='Number of Rest Stops',
    tooltip=['City', 'Number of Rest Stops']
).properties(
    width=600,
    height=300
).interactive()

st.altair_chart(chart, use_container_width=True) #[VIZ2]

# Pivot Table [DA6]
df['RESTROOM'] = df['RESTROOM'] == 'Yes'
df['WATER'] = df['WATER'] == 'Yes'
df['PICNICTAB'] = df['PICNICTAB'] == 'Yes'
df['PHONE'] = df['PHONE'] == 'Yes'
df['HANDICAP'] = df['HANDICAP'] == 'Yes'
df['RV_STATION'] = df['RV_STATION'] == 'Yes'
df['VENDING'] = df['VENDING'] == 'Yes'
df['PET_AREA'] = df['PET_AREA'] == 'Yes'

# Creating a pivot table
pivot = pd.pivot_table(df, values=['RESTROOM', 'WATER', 'PICNICTAB', 'PHONE', 'HANDICAP', 'RV_STATION', 'VENDING', 'PET_AREA'], index='CITY', aggfunc='sum')

# Print pivot table in Streamlit
st.write("Amenities by CIty", pivot)


# Bar chart based on rest areas by route using Altair
st.markdown('<h2 style="color: gold; text-decoration: underline;">Rest Areas by Route</h2>', unsafe_allow_html=True)

route_counts = df['ROUTE'].value_counts().reset_index()
route_counts.columns = ['Route', 'Number of Rest Areas']


chart = alt.Chart(route_counts).mark_bar().encode(
    x='Route:O',  # The ":O" denotes that the x-axis data is ordinal
    y='Number of Rest Areas:Q',  # The ":Q" denotes that the y-axis data is quantitative
    tooltip=['Route', 'Number of Rest Areas']  # Show tooltip on hover
).properties(
    width=600,
    height=300
)

st.altair_chart(chart, use_container_width=True)

#Pie charts for each ammenidity offered [DA7]
with st.expander("Click Here to See Rest Area Amenity Percentages in California"): #[ST3]
    st.markdown('<h2 style="color: gold; text-decoration: underline;">Restrooms</h2>', unsafe_allow_html=True)
    labels = 'Do Have','Do Not Have'
    sizes = [87, 0]
    explode = (0, 0.1,)  # "explode" the 2nd slice

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')

    st.pyplot(fig1) #[VIZ3]

    st.markdown('<h2 style="color: gold; text-decoration: underline;">Water</h2>', unsafe_allow_html=True)
    labels = 'Do Have', 'Do Not Have'
    sizes = [87, 0]
    explode = (0, 0.1,)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')

    st.pyplot(fig1)

    st.markdown('<h2 style="color: gold; text-decoration: underline;">Picnic Table</h2>', unsafe_allow_html=True)
    labels = 'Do Have', 'Do Not Have'
    sizes = [86, 1]
    explode = (0, 0.1,)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')

    st.pyplot(fig1)

    st.markdown('<h2 style="color: gold; text-decoration: underline;">Phone</h2>', unsafe_allow_html=True)
    labels = 'Do Have', 'Do Not Have'
    sizes = [78, 9]
    explode = (0, 0.1,)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')

    st.pyplot(fig1)

    st.markdown('<h2 style="color: gold; text-decoration: underline;">Handicap</h2>', unsafe_allow_html=True)
    labels = 'Do Have', 'Do Not Have'
    sizes = [87, 0]
    explode = (0, 0.1,)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')

    st.pyplot(fig1)

    st.markdown('<h2 style="color: gold; text-decoration: underline;">RV Station</h2>', unsafe_allow_html=True)
    labels = 'Do Have', 'Do Not Have'
    sizes = [71, 16]
    explode = (0, 0.1,)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')

    st.pyplot(fig1)

    st.markdown('<h2 style="color: gold; text-decoration: underline;">Vending Machines</h2>', unsafe_allow_html=True)
    labels = 'Do Have', 'Do Not Have'
    sizes = [30, 57]
    explode = (0, 0.1,)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')

    st.pyplot(fig1)

    st.markdown('<h2 style="color: gold; text-decoration: underline;">Pet Area</h2>', unsafe_allow_html=True)
    labels = 'Do Have', 'Do Not Have'
    sizes = [86, 1]
    explode = (0, 0.1,)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')

    st.pyplot(fig1)

#List Comprehension to view rest areas by direction [PY4] [DA8]
north_traffic_areas = [(entry['NAME'], entry['TRAFFICDIR']) for index, entry in df.iterrows() if entry['TRAFFICDIR'] == 'N']
south_traffic_areas = [(entry['NAME'], entry['TRAFFICDIR']) for index, entry in df.iterrows() if entry['TRAFFICDIR'] == 'S']
west_traffic_areas = [(entry['NAME'], entry['TRAFFICDIR']) for index, entry in df.iterrows() if entry['TRAFFICDIR'] == 'W']
east_traffic_areas = [(entry['NAME'], entry['TRAFFICDIR']) for index, entry in df.iterrows() if entry['TRAFFICDIR'] == 'E']

with st.expander("View North Traffic Rest Areas"):
    for area, direction in north_traffic_areas:
        st.write(f"Rest Area: {area}, Traffic Direction: {direction}")

with st.expander("View South Traffic Rest Areas"):
    for area, direction in south_traffic_areas:
        st.write(f"Rest Area: {area}, Traffic Direction: {direction}")

with st.expander("View West Traffic Rest Areas"):
    for area, direction in west_traffic_areas:
        st.write(f"Rest Area: {area}, Traffic Direction: {direction}")

with st.expander("View East Traffic Rest Areas"):
    for area, direction in east_traffic_areas:
        st.write(f"Rest Area: {area}, Traffic Direction: {direction}")



#Outside sources used include different pages from the streamlit website. The link is docs.streamlit.io
