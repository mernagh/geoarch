# main.py
import streamlit as st
import geopandas as gpd
import folium

# Load Amsterdam GeoData
amsterdam_data = gpd.read_file('data/input/amsterdam_points.geojson')

# Default category and subcategory
default_category = 'Architecture'
default_subcategory = 'Amsterdam School'

# Sidebar for Dropdown Menu
st.sidebar.header('Select Category')
category = st.sidebar.selectbox('Choose a category', amsterdam_data['Category'].unique(), index=amsterdam_data['Category'].unique().tolist().index(default_category))

# If 'Architecture' is selected, activate 'Amsterdam School' subcategory
if category == default_category:
    st.sidebar.header('Select Subcategory')
    subcategory = st.sidebar.selectbox('Choose a subcategory', amsterdam_data[amsterdam_data['Category'] == default_category]['Subcategory'].unique(), index=amsterdam_data[amsterdam_data['Category'] == default_category]['Subcategory'].unique().tolist().index(default_subcategory))
    filtered_data = amsterdam_data[(amsterdam_data['Category'] == category) & (amsterdam_data['Subcategory'] == subcategory)]
else:
    filtered_data = amsterdam_data[amsterdam_data['Category'] == category]

# Create a clustered map using folium
m = folium.Map(location=[filtered_data['geometry'].y.mean(), filtered_data['geometry'].x.mean()], zoom_start=12)

for idx, row in filtered_data.iterrows():
    folium.Marker([row['geometry'].y, row['geometry'].x], popup=row['Name']).add_to(m)

# Display the clustered map in Streamlit
st.header(f'Map of Amsterdam - {category}')
st.folium_chart(m)

# Hover Information
hovered_point = st.selectbox('Hover over a point for more info', options=filtered_data['Name'])

# Display Detailed Information
selected_info = filtered_data[filtered_data['Name'] == hovered_point]
st.subheader(f'Detailed Information - {hovered_point}')
st.write(selected_info)
