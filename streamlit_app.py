from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from shapely.geometry import point


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Flights Dashboard", page_icon=":bar_chart:", layout="wide")
"""
# ---- READ FILES ----
dfairports = pd.read_file('airports.dat')
dfairlines = pd.read_file('airliness.dat')
dfplanes=pd.read_file('planes.dat')
dfcountries=pd.read_file('countries.dat')
dfroutes=pd.read_file('routes.dat')
"""
# ---- READ FILES ----
dfairports = pd.read_csv("/content/drive/MyDrive/Assignment 2 /airports.dat")
dfairlines = pd.read_csv("/content/drive/MyDrive/Assignment 2 /airlines.dat")
dfplanes=pd.read_csv("/content/drive/MyDrive/Assignment 2 /planes.dat")
dfcountries=pd.read_csv("/content/drive/MyDrive/Assignment 2 /countries.dat")
dfroutes=pd.read_csv("/content/drive/MyDrive/Assignment 2 /routes.dat")

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
country = st.sidebar.multiselect(
    "Select the country:",
    options=dfairports["Name"].unique(),
    default=dfairports["Name"].unique()
)

plane_type = st.sidebar.multiselect(
    "Select the plane type:",
    options=dfplanes["Name"].unique(),
    default=dfplanes["Name"].unique(),
)

airline_name = st.sidebar.multiselect(
    "Select the airline:",
    options=dfairlines["Name"].unique(),
    default=dfairlines["Name"].unique()
)

airport_name = st.sidebar.multiselect(
    "Select the airport:",
    options=dfairlines["Name"].unique(),
    default=dfairlines["Name"].unique()
)


# ---- MAINPAGE ----
st.title(":bar_chart: Flights Dashboard")
st.markdown("##")
#create a pie chart that displays the 10 most utilized airlines in the world
# Set file paths
routes_file = "/content/drive/MyDrive/Assignment 2 /routes.dat"
airlines_file = "/content/drive/MyDrive/Assignment 2 /airlines.dat"

# Read routes and airlines files using pandas
routes = pd.read_csv(routes_file, header=None, names=["Airline", "Airline ID", "Source airport", "Source airport ID", "Destination airport", "Destination airport ID", "Codeshare", "Stops", "Equipment"])
airlines = pd.read_csv(airlines_file, header=None, names=["Airline ID", "Name", "Alias", "IATA", "ICAO", "Callsign", "Country", "Active"])
airlines["Airline ID"]= airlines["Airline ID"].astype(str)
# Merge routes and airlines dataframes based on Airline ID column
merged = pd.merge(routes, airlines, how="left", on="Airline ID")

# Group by airline name and count the number of occurrences
airline_counts = merged["Name"].value_counts()

# Select the top 10 most frequent airlines
top_airlines = airline_counts.nlargest(10)

# Create a new dataframe with the top 10 airlines and their counts
top_airlines_df = pd.DataFrame({"Airline": top_airlines.index, "Count": top_airlines.values})

# Create a pie chart using matplotlib
fig, ax = plt.subplots()
ax.pie(top_airlines_df["Count"], labels=top_airlines_df["Airline"], autopct='%1.1f%%')
ax.set_title("Top 10 Most Used Airlines")
ax.axis('equal')
#st.pie(top_airlines_df = pd.DataFrame({"Airline": top_airlines.index, "Count": top_airlines.values})
st.pyplot(top_airlines_df)

#Show the 10 most frequent planes with a bar chart 
# Set file paths
routes_file = "/content/drive/MyDrive/Assignment 2 /routes.dat"
planes_file = "/content/drive/MyDrive/Assignment 2 /planes.dat"

# Read routes and planes files using pandas
routes = pd.read_csv(routes_file, header=None, names=["Airline", "Airline ID", "Source airport", "Source airport ID", "Destination airport", "Destination airport ID", "Codeshare", "Stops", "Equipment_Type"])
planes = pd.read_csv(planes_file, header=None, names=["Name", "IATA", "ICAO"])

# Merge routes and planes dataframes based on Equipment_Type column
merged = pd.merge(routes, planes, how="left", left_on="Equipment_Type", right_on="IATA")

# Group by plane name and count the number of occurrences
plane_counts = merged["Name"].value_counts()

# Select the top 10 most frequent planes
top_planes = plane_counts.nlargest(10)

# Create a new dataframe with the top 10 planes and their counts
top_planes_df = pd.Dataframe({"Plane": top_planes.index, "Count": top_planes.values})

# Create a bar chart using matplotlib and display using Streamlit
st.bar_chart(top_planes_df.set_index('Plane'))
st.pyplot()


#Display an Interactive map showing the Top 20 airports in South Africa 
# Read airports and routes files using pandas
airports = pd.read_csv(airports_file, header=None, names=["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "Tz database time zone", "Type", "Source"])
routes = pd.read_csv(routes_file, header=None, names=["Airline", "Airline ID", "Source airport", "Source airport ID", "Destination airport", "Destination airport ID", "Codeshare", "Stops", "Equipment"])

# Filter routes to only include those with a source airport in South Africa
south_africa_routes = routes[routes["Source airport"].isin(airports[airports["Country"] == "South Africa"]["IATA"])]

# Group by source airport and count the number of occurrences
airport_counts = south_africa_routes["Source airport"].value_counts()

# Create a list of the top 5, 10, and 20 airports
top_airports = [airport_counts.nlargest(20)]

# Create a folium map centered on South Africa
south_africa_coords = [-30.5595, 22.9375]
map = folium.Map(location=south_africa_coords, zoom_start=5)

# Add markers for the top airports to the map
for i in range(len(top_airports)):
    for airport in top_airports[i].index:
        airport_coords = airports.loc[airports["IATA"] == airport, ["Latitude", "Longitude"]].iloc[0].values.tolist()
        popup_text = f"{airport}: {top_airports[i][airport]} flights"
        marker = folium.Marker(location=airport_coords, popup=popup_text)
        marker.add_to(map)

    # Add a legend to the map
    legend_text = f"Top {len(top_airports[i])} airports"
    legend_html = f"<div style='font-size: 14pt'>{legend_text}</div>"
    map.get_root().html.add_child(folium.Element(legend_html))
    

# Display the map
st.markdown(folium.Map()._repr_html_(), unsafe_allow_html=True)


@st.cache
def load_data():
    routes = pd.read_csv(routes_file, header=None, names=["Airline", "Airline ID", "Source airport", "Source airport ID", "Destination airport", "Destination airport ID", "Codeshare", "Stops", "Equipment"])
    airports = pd.read_csv(airports_file, header=None, names=["ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "Tz database time zone", "Type", "Source"])
    routes['Airline ID'] = routes['Airline ID'].astype(str)
    airports['ID'] = airports['ID'].astype(str)
    routes['Destination airport ID'] = routes['Destination airport ID'].astype(str)
    merged = pd.merge(routes, airports, how="left", left_on="Source airport ID", right_on="ID")
    merged = pd.merge(merged, airports, how="left", left_on="Destination airport ID", right_on="ID", suffixes=("_src", "_dest"))
    coord_counts = merged.groupby(["Latitude_src", "Longitude_src", "Latitude_dest", "Longitude_dest"]).size().reset_index(name="count")
    coord_counts = coord_counts.sort_values(by="count", ascending=False).head(100)
    return airports, coord_counts

airports, coord_counts = load_data()

st.title("Top 100 busiest flight routes on a map")
st.markdown("This app shows the top 100 busiest flight routes on a map.")

# Create a folium map centered on the first airport in the airports dataframe
map2 = folium.Map(location=[airports["Latitude"][0], airports["Longitude"][0]], zoom_start=3)

# Iterate over each coordinate group and add a polyline to the map
for index, row in coord_counts.iterrows():
    src_lat, src_lon, dest_lat, dest_lon = row["Latitude_src"], row["Longitude_src"], row["Latitude_dest"], row["Longitude_dest"]
    points = [(src_lat, src_lon), (dest_lat, dest_lon)]
    folium.PolyLine(points, color="Red", weight=1, opacity=0.5).add_to(map2)

# Display the map
folium_static(map2)

