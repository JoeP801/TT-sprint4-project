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
filter_price = st.checkbox("Show only vehicles priced under $60,000")

# filter based on checkbox selection
if filter_price:
    filtered_price_df = vehicles_df[vehicles_df['price'] < 60000]
else:
    filtered_price_df = vehicles_df

price_histogram = px.histogram(filtered_price_df, 
                                x='price', 
                                nbins=50, 
                                title='Price Distribution of Vehicles')
st.plotly_chart(price_histogram)


# model Year Distribution
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


# scatter plot of price vs. model_year
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

# price vs. odometer
st.subheader("Price vs. Odometer Reading")
price_vs_odometer = px.scatter(vehicles_df, x='odometer', y='price', 
                                title='Vehicle Price vs. Odometer Reading', 
                                labels={'odometer': 'Odometer Reading (miles)', 'price': 'Price ($)'},
                                hover_data=['manufacturer'])

st.plotly_chart(price_vs_odometer)
