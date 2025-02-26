# Imports

import streamlit as st
import pandas as pd
import plotly.express as px
from modules import module as mod

# Streamlit cheat-sheet https://docs.streamlit.io/develop/quick-reference/cheat-sheet

st.sidebar.title("Simulation Parameters")

baseline_data = ('Baseline.csv')
years = ('All', '2014', '2015', '2016')
months = ('All', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')
product_level = ('All', 'Category', 'Sub-Category', 'Product ID')
categories = ('Furniture', 'Office Supplies') #formular
sub_categories = ('Tables', 'Bookcases', 'Phones') #formular
products = ('Tables', 'Bookcases', 'Phones') #formular
geography_level = ('All', 'Region', 'State', 'City', 'Postal Code')
regions = ('West', 'East', 'Center') #formular
states = ('Texas', 'Ohio', 'New York') #formular
cities = ('Houston', 'Columbus', 'New York City') #formular
postal_codes = ('77070', '43229', '10035') #formular
calc_methods1 = ('Increase in %', 'Target Value')
calc_methods2 = ('Target %', 'Max Treshold %')
calc_methods3 = ('Increase in % ', 'Target Value ') # space after text mandatory
calc_methods4 = ('Target % ', 'Min Treshold % ') # space after text mandatory


def select_prod(level):
    if level == 'All':
        return ['--']  # Return a placeholder for 'All'
    elif level == 'Category':
        return categories
    elif level == 'Sub-Category':
        return sub_categories
    elif level == 'Product ID':
        return products
    else:
        return ["Something went wrong, try again"]
    
def select_geo(level):
    if level == 'All':
        return ['--']  # Return a placeholder for 'All'
    elif level == 'Region':
        return regions
    elif level == 'State':
        return states
    elif level == 'City':
        return cities
    elif level == 'Postal Code':
        return postal_codes
    else:
        return ["Something went wrong, try again"]
    

# Select data for simulation

selector01 = st.sidebar.selectbox("Baseline", baseline_data)

# Select period

selector02 = st.sidebar.selectbox("Year", years)
selector03 = st.sidebar.selectbox("Month", months)

# Select Product

col1, col2 = st.sidebar.columns(2)
with col1:
    selector04 =  st.selectbox("Product level", product_level)

with col2:
    name = select_prod(selector04)
    selector05 = st.selectbox("Product name", name)

# Select Geography

col1, col2 = st.sidebar.columns(2)
with col1:
    selector06 =  st.selectbox("Geography level", geography_level)

with col2:
    name = select_geo(selector06)
    selector07 = st.selectbox("Geography Name", name)

st.sidebar.title("Simulation Metrics")

# Select Metrics

st.sidebar.text("List Price")

col1, col2 = st.sidebar.columns(2)
with col1:
    selector08 = st.pills("Select method", calc_methods1)

if selector08 == 'Increase in %':
    col2.number_input("Enter a value between -100 and 100:", min_value=-100.00, max_value=100.00, step=1.00)
elif selector08 == 'Target Value':
    col2.number_input("Enter target value", min_value=0.00)
else: 
    pass

#

st.sidebar.text("Discount Percentage")

col1, col2 = st.sidebar.columns(2)
with col1:
    selector10 = st.pills("Select method", calc_methods2)

if selector10 == 'Target %':
    col2.number_input("Enter a value between 0 and 100: ", min_value=0.00, max_value=100.00, step=1.00)
elif selector10 == 'Max Treshold %':
    col2.number_input("Enter a value between 0 and 100: ", min_value=0.00, max_value=100.00, step=1.00)
else: 
    pass

#

st.sidebar.text("COGS")

col1, col2 = st.sidebar.columns(2)
with col1:
    selector12 =  st.pills("Select method", calc_methods3)

if selector12 == 'Increase in % ': 
    col2.number_input("Enter a value between -100 and 100:  ", min_value=-100.00, max_value=100.00, step=1.00)
elif selector12 == 'Target Value ':
    col2.number_input("Enter target value  ", min_value=0.00)
else:   
    pass

#

st.sidebar.text("Gross Margin Percentage")

col1, col2 = st.sidebar.columns(2)
with col1:
    selector14 =  st.pills("Select method", calc_methods4)

if selector14 == 'Target % ':
    col2.number_input("Enter a value between 0 and 100:   ", min_value=0.00, max_value=100.00, step=1.00)
elif selector14 == 'Min Treshold % ':
    col2.number_input("Enter a value between 0 and 100:   ", min_value=0.00, max_value=100.00, step=1.00)
else:
    pass




path = './data/' + selector01
df = pd.read_csv(path)