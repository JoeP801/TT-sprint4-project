import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import plotly.express as px


# read dataset
vehicles_df = pd.read_csv('vehicles_us.csv')

# split manufacturer data from model column
vehicles_df[['manufacturer', 'model']] = vehicles_df['model'].str.extract(r'(\w+)\s+(.*)')
vehicles_df = vehicles_df[['price', 'model_year', 'manufacturer', 'model', 'condition', 'cylinders',
                           'fuel', 'odometer', 'transmission', 'type', 'paint_color', 'is_4wd', 'date_posted', 
                           'days_listed']]

# set up header
st.header("Vehicle Dataset Analysis Dashboard")

# price distribution
st.subheader("Price Distribution")
filter_price_60k = st.checkbox("Show only vehicles priced under $60,000")
filter_price_20k = st.checkbox("Show only vehicles priced under $20,000")

# filter based on checkbox selections
filtered_price_df = vehicles_df.copy()

if filter_price_60k:
    filtered_price_df = filtered_price_df[filtered_price_df['price'] < 60000]

if filter_price_20k:
    filtered_price_df = filtered_price_df[filtered_price_df['price'] < 20000]

price_histogram = px.histogram(filtered_price_df, 
                                x='price', 
                                nbins=50, 
                                title='Price Distribution of Vehicles')
st.plotly_chart(price_histogram)

# model Year distribution
st.subheader("Model Year Distribution")
show_recent_models = st.checkbox("Show only vehicles from model year 2000 and after")

# filter based on checkbox selection
if show_recent_models:
    filtered_df = vehicles_df[(vehicles_df['model_year'] != 0) & (vehicles_df['model_year'] > 2000)]
else:
    filtered_df = vehicles_df[vehicles_df['model_year'] != 0]

model_year_histogram = px.histogram(filtered_df, 
                                     x='model_year', 
                                     nbins=50, 
                                     title='Model Year Distribution of Vehicles')
st.plotly_chart(model_year_histogram)

# scatter plot of price vs model_year
st.subheader("Price vs. Model Year")
show_price_filter = st.checkbox("Show Only Vehicles Priced Above $20,000")

if show_price_filter:
    filtered_df = vehicles_df[vehicles_df['price'] > 20000]
else:
    filtered_df = vehicles_df

price_vs_year = px.scatter(
    filtered_df,
    x='model_year',
    y='price',
    title='Price vs. Model Year',
    hover_data=['price', 'model_year']  
    )

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

# price vs odometer
st.subheader("Price vs. Odometer Reading")

# create checkboxes for filtering
odometer_under_100k = st.checkbox('Odometer < 100,000 miles')
odometer_under_50k = st.checkbox('Odometer < 50,000 miles')
price_under_30k = st.checkbox('Price < $30,000')
price_under_15k = st.checkbox('Price < $15,000')

# create filtered dataframe
filtered_odometer_df = vehicles_df.copy()

if odometer_under_100k:
    filtered_odometer_df = filtered_odometer_df[filtered_odometer_df['odometer'] < 100000]
if odometer_under_50k:
    filtered_odometer_df = filtered_odometer_df[filtered_odometer_df['odometer'] < 50000]
if price_under_30k:
    filtered_odometer_df = filtered_odometer_df[filtered_odometer_df['price'] < 30000]
if price_under_15k:
    filtered_odometer_df = filtered_odometer_df[filtered_odometer_df['price'] < 15000]

# create scatter plot with filters
price_vs_odometer = px.scatter(
    filtered_odometer_df, 
    x='odometer', 
    y='price', 
    title='Vehicle Price vs. Odometer Reading', 
    labels={'odometer': 'Odometer Reading (miles)', 'price': 'Price ($)'},
    hover_data=['manufacturer']
)

st.plotly_chart(price_vs_odometer)
