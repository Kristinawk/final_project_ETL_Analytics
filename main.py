# Imports

import streamlit as st
import pandas as pd
import plotly.express as px
from modules import module as mod

# Streamlit cheat-sheet https://docs.streamlit.io/develop/quick-reference/cheat-sheet

# Temporary Module:


# Pipeline


##### Sidebar title 1

st.sidebar.title("Simulation Parameters")

##### Select Baseline

baseline_data = ('Baseline.csv') # define selector options
selector01 = st.sidebar.selectbox("Baseline", baseline_data) # display selector
path = './data/' + selector01 # apply selection
df = pd.read_csv(path)

##### Select Year

years = mod.fill_selector(df, 'Order Year') # define selector options
selector02 = st.sidebar.selectbox("Year", years) # display selector
selected_data = mod.apply_filter(df, 'Order Year', selector02) # apply selection

##### Select Month

months = mod.fill_selector(selected_data, 'Order Month') # define selector options
selector03 = st.sidebar.selectbox("Month", months) # display selector
selected_data = mod.apply_filter(selected_data, 'Order Month', selector03) # apply selection

##### Select Product

product_level = ('All', 'Category', 'Sub-Category', 'Product ID') # define selector options

col1, col2 = st.sidebar.columns(2)
with col1:
    selector04 =  st.selectbox("Product level", product_level) # display level selector

with col2:
    name = mod.select_name(selected_data, selector04)
    selector05 = st.selectbox("Product name", name) # display name selector

if selector04 != "All":
    selected_data = mod.apply_filter(selected_data, selector04, selector05) # apply selection
else:
    pass

##### Select Geography

geography_level = ('All', 'Region', 'State', 'City', 'Postal Code') # define selector options

col1, col2 = st.sidebar.columns(2)
with col1:
    selector06 =  st.selectbox("Geography level", geography_level) # display level selector

with col2:
    name = mod.select_name(selected_data, selector06)
    selector07 = st.selectbox("Geography name", name) # display name selector

if selector06 != "All":
    selected_data = mod.apply_filter(selected_data, selector06, selector07) # apply selection
else:
    pass

##### Output table

st.title("Simulation Overview")

selected_data

##### Sidebar title 2

st.sidebar.title("Simulation Metrics")

##### List Price operations

st.sidebar.text("List Price") # metric title

calc_methods1 = ('Increase in %', 'Target Value') # define method options

col1, col2 = st.sidebar.columns(2)
with col1:
    selector08 = st.pills("Select method", calc_methods1) # display method selector

if selector08 == 'Increase in %':
    col2.number_input("Enter a value between -100 and 100:", min_value=-100.00, max_value=100.00, step=1.00) # display data entry
elif selector08 == 'Target Value':
    col2.number_input("Enter target value", min_value=0.00) # display data entry
else: 
    pass

##### Discount operations

st.sidebar.text("Discount Percentage") # metric title

calc_methods2 = ('Target %', 'Max Treshold %') # define method options

col1, col2 = st.sidebar.columns(2)
with col1:
    selector09 = st.pills("Select method", calc_methods2) # display method selector

if selector09 == 'Target %':
    col2.number_input("Enter a value between 0 and 100: ", min_value=0.00, max_value=100.00, step=1.00) # display data entry (space after text mandatory!)
elif selector09 == 'Max Treshold %':
    col2.number_input("Enter a value between 0 and 100: ", min_value=0.00, max_value=100.00, step=1.00) # display data entry (space after text mandatory!)
else: 
    pass

##### COGS operations

st.sidebar.text("COGS")

calc_methods3 = ('Increase in % ', 'Target Value ') # define method options (space after text mandatory!)

col1, col2 = st.sidebar.columns(2)
with col1:
    selector10 =  st.pills("Select method", calc_methods3) # display method selector

if selector10 == 'Increase in % ': 
    col2.number_input("Enter a value between -100 and 100:  ", min_value=-100.00, max_value=100.00, step=1.00) # display data entry (space after text mandatory!)
elif selector10 == 'Target Value ':
    col2.number_input("Enter target value  ", min_value=0.00) # display data entry (space after text mandatory!)
else:   
    pass

##### Gross Margin operations

st.sidebar.text("Gross Margin Percentage")

calc_methods4 = ('Target % ', 'Min Treshold % ') # define method options (space after text mandatory!)

col1, col2 = st.sidebar.columns(2)
with col1:
    selector11 =  st.pills("Select method", calc_methods4) # display method selector

if selector11 == 'Target % ':
    col2.number_input("Enter a value between 0 and 100:   ", min_value=0.00, max_value=100.00, step=1.00) # display data entry (space after text mandatory!)
elif selector11 == 'Min Treshold % ':
    col2.number_input("Enter a value between 0 and 100:   ", min_value=0.00, max_value=100.00, step=1.00) # display data entry (space after text mandatory!)
else:
    pass










