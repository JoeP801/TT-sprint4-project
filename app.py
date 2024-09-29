import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import plotly.express as px


# read dataset
vehicles_df = pd.read_csv('C:/Users/joe62/Git/TT-sprint4-project/vehicles_us.csv')

# set up header
st.header("Vehicle Dataset Analysis Dashboard")

# histogram of vehicle prices
st.subheader("Price Distribution")
price_histogram = px.histogram(vehicles_df, x='price', nbins=50, title='Price Distribution of Vehicles')
st.plotly_chart(price_histogram)

# histogram of model year distribution
st.subheader("Model Year Distribution")
model_year_histogram = px.histogram(vehicles_df[vehicles_df['model_year'] != 0], 
                                     x='model_year', nbins=50, 
                                     title='Model Year Distribution of Vehicles')
st.plotly_chart(model_year_histogram)

# scatter plot of price vs. model_year
st.subheader("Price vs. Model Year")
show_price_filter = st.checkbox("Show Only Vehicles Priced Above $20,000")

if show_price_filter:
    filtered_df = vehicles_df[vehicles_df['price'] > 20000]
else:
    filtered_df = vehicles_df

price_vs_year = px.scatter(filtered_df, x='model_year', y='price', 
                            title='Vehicle Price vs. Model Year', 
                            labels={'model_year': 'Model Year', 'price': 'Price ($)'},
                            hover_data=['manufacturer'])

st.plotly_chart(price_vs_year)

# manufacturer statistics
st.subheader("Manufacturer Statistics")

# bar plot for number of vehicles by manufacturer
manufacturer_counts = vehicles_df['manufacturer'].value_counts().reset_index()
manufacturer_counts.columns = ['Manufacturer', 'Number of Vehicles']
manufacturer_bar = px.bar(manufacturer_counts, x='Manufacturer', y='Number of Vehicles', 
                           title='Number of Vehicles by Manufacturer', 
                           labels={'Number of Vehicles': 'Number of Vehicles'})
st.plotly_chart(manufacturer_bar)

# bar plot for average price by manufacturer
average_price_by_manufacturer = vehicles_df.groupby('manufacturer')['price'].mean().reset_index()
average_price_by_manufacturer.columns = ['Manufacturer', 'Average Price']
average_price_bar = px.bar(average_price_by_manufacturer, x='Manufacturer', y='Average Price', 
                            title='Average Price by Manufacturer', 
                            labels={'Average Price': 'Average Price ($)'})
st.plotly_chart(average_price_bar)

# price vs. odometer
st.subheader("Price vs. Odometer Reading")
price_vs_odometer = px.scatter(vehicles_df, x='odometer', y='price', 
                                title='Vehicle Price vs. Odometer Reading', 
                                labels={'odometer': 'Odometer Reading (miles)', 'price': 'Price ($)'},
                                hover_data=['manufacturer'])

st.plotly_chart(price_vs_odometer)
