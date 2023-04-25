from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

#create a pie chart that displays the 20 most utilized airlines in the world
import pandas as pd
import matplotlib.pyplot as plt

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
plt.show()

