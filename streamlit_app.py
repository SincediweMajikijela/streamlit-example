from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

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
plt.pie(top_airlines_df["Count"], labels=top_airlines_df["Airline"], autopct='%1.1f%%')
plt.title("Top 10 Most Used Airlines")
plt.axis('equal')
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
top_planes_df = pd.DataFrame({"Plane": top_planes.index, "Count": top_planes.values})

# Create a bar chart using matplotlib
plt.bar(top_planes_df["Plane"], top_planes_df["Count"])
plt.xticks(rotation=90)
plt.xlabel("Plane")
plt.ylabel("Count")
plt.title("Top 10 Most Used Planes")

st.bar_chart(top_planes_df)

