# Imports

import streamlit as st
import pandas as pd
import plotly.express as px
import math
pd.set_option('display.max_columns', None)
import os
import csv
from modules import module as mod

col_list = ['List Price', 'Net Price', 'Sales', 'COGS', 'Profit', 'Gross Margin']


# Streamlit cheat-sheet https://docs.streamlit.io/develop/quick-reference/cheat-sheet


# Pipeline

st.image("https://www.flaticon.es/icono-gratis/aplicacion-de-bolsa-de-valores_3781647")




##### Sidebar title 1

st.sidebar.header("Baseline for Simulation")

##### Select Baseline

# Define a list with all Versions:

# Initialize baseline list
# baseline_list = ['Baseline.csv']

simulations_file_path = './data/simulations_list.csv'
baseline_list = mod.read_list_from_csv(simulations_file_path)

baseline_data = tuple(baseline_list) # define selector options
selector01 = st.sidebar.selectbox("Version", baseline_data, key='Version') # display selector
path = './data/' + selector01 # apply selection
df = pd.read_csv(path)

##### Select Year

years = mod.fill_selector(df, 'Order Year') # define selector options
selector02 = st.sidebar.selectbox("Year", years, key='Year') # display selector
selected_data = mod.apply_filter(df, 'Order Year', selector02) # apply selection


##### Sidebar title 2

st.sidebar.header("Simulation Parameters")

##### Select Product

product_level = ('All', 'Category', 'Sub-Category', 'Product ID') # define selector options

col1, col2 = st.sidebar.columns(2)
with col1:
    selector04 =  st.selectbox("Product level", product_level, key='Product Level') # display level selector

with col2:
    name = mod.select_name(selected_data, selector04)
    selector05 = st.selectbox("Product name", name, key='Product name') # display name selector

if selector04 != "All":
    selected_data = mod.apply_filter(selected_data, selector04, selector05) # apply selection
else:
    pass

##### Select Geography

geography_level = ('All', 'Region', 'State', 'City', 'Postal Code') # define selector options

col1, col2 = st.sidebar.columns(2)
with col1:
    selector06 =  st.selectbox("Geography level", geography_level, key='Geography level') # display level selector

with col2:
    name = mod.select_name(selected_data, selector06)
    selector07 = st.selectbox("Geography name", name, key='Geography name') # display name selector

if selector06 != "All":
    selected_data = mod.apply_filter(selected_data, selector06, selector07) # apply selection
else:
    pass

##### Output table

st.title("Simulation Overview")

baseline_view = mod.summary_tab(selected_data, 'Baseline', selector02)

simulation = selected_data.copy()


##### Sidebar title 3

st.sidebar.header("Simulation Metrics")

##### List Price operations

st.sidebar.text("List Price") # metric title

calc_methods1 = ('Increase in %', 'Target Value') # define method options

col1, col2 = st.sidebar.columns(2)
with col1:
    selector08 = st.pills("Select method", calc_methods1, key='Select method LP') # display method selector

if selector08 == 'Increase in %':
    selector18 = col2.number_input("Enter a value between -100 and 100:", min_value=-100.00, max_value=100.00, step=1.00) # display data entry

    simulation['List Price'] = simulation['List Price'] * (1 + selector18 / 100) # run simulation
    simulation = mod.profit_calc(simulation, col_list)
    #simulation

elif selector08 == 'Target Value':
    selector18 = col2.number_input("Enter target value", min_value=0.00) # display data entry

    if selector04 != 'Product ID':
        st.error('Error: Please select Product ID in _Product level_')
    else:
        simulation['List Price'] = selector18 # run simulation
        simulation = mod.profit_calc(simulation, col_list)
        #simulation
else: 
    pass

##### Discount operations

st.sidebar.text("Discount Percentage") # metric title

calc_methods2 = ('Target %', 'Max Treshold %') # define method options

col1, col2 = st.sidebar.columns(2)
with col1:
    selector09 = st.pills("Select method", calc_methods2, key='Select method Disc') # display method selector

if selector09 == 'Target %':
    selector19 = col2.number_input("Enter a value between 0 and 100: ", min_value=0.00, max_value=100.00, step=1.00) # display data entry (space after text mandatory!)

    simulation['Discount'] = selector19 / 100 # run simulation
    simulation = mod.profit_calc(simulation, col_list)
    #simulation

elif selector09 == 'Max Treshold %':
    selector19 = col2.number_input("Enter a value between 0 and 100: ", min_value=0.00, max_value=100.00, step=1.00) # display data entry (space after text mandatory!)

    simulation['Discount'] = simulation['Discount'].apply(lambda row: row if row < (selector19 / 100) else (selector19 / 100)) # run simulation
    simulation = mod.profit_calc(simulation, col_list)
    #simulation

else: 
    pass


##### COGS operations

st.sidebar.text("COGS")

calc_methods3 = ('Increase in % ', 'Target Value ') # define method options (space after text mandatory!)

col1, col2 = st.sidebar.columns(2)
with col1:
    selector10 =  st.pills("Select method", calc_methods3, key='Select method COGS') # display method selector

if selector10 == 'Increase in % ': 
    selector21 = col2.number_input("Enter a value between -100 and 100:  ", min_value=-100.00, max_value=100.00, step=1.00) # display data entry (space after text mandatory!)

    simulation['COGS'] = simulation['COGS'] * (1 + selector21 / 100) # run simulation
    simulation = mod.profit_calc(simulation, col_list)
    #simulation

elif selector10 == 'Target Value ':
    selector21 = col2.number_input("Enter target value  ", min_value=0.00) # display data entry (space after text mandatory!)

    if selector04 != 'Product ID':
        st.error('Error: Please select Product ID in _Product level_')
    else:
        simulation['COGS'] = selector21 # run simulation
        simulation = mod.profit_calc(simulation, col_list)
        #simulation
else:   
    pass


##### Gross Margin operations

st.sidebar.text("Gross Margin Percentage")

calc_methods4 = ('Target % ', 'Min Treshold % ') # define method options (space after text mandatory!)

col1, col2 = st.sidebar.columns(2)
with col1:
    selector11 =  st.pills("Select method", calc_methods4, key='Select method GM') # display method selector

if selector11 == 'Target % ':
    selector31 = col2.number_input("Enter a value between 0 and 100:   ", min_value=0.00, max_value=100.00, step=1.00) # display data entry (space after text mandatory!)

    simulation['Gross Margin'] = selector31 / 100 # run simulation
    simulation = mod.gross_margin_calc(simulation, col_list)
    #simulation

elif selector11 == 'Min Treshold % ':
    selector31= col2.number_input("Enter a value between 0 and 100:   ", min_value=0.00, max_value=100.00, step=1.00) # display data entry (space after text mandatory!)

    simulation['Gross Margin'] = simulation['Gross Margin'].apply(lambda row: row if row >= (selector31 / 100) else (selector31 / 100)) # run simulation
    simulation = mod.gross_margin_calc(simulation, col_list)
    #simulation

else:
    pass


##### Simulation output  - Selection

st.header('Selection')

simulation_view = mod.summary_tab(simulation, 'Simulation', selector02)
output_table_selection = pd.concat([baseline_view, simulation_view])
output_table_selection

mod.comparison_bar_charts(output_table_selection, df_name='selection')


##### Simulation output  - Total Business including Selection

st.header('Total Business including Selection')

baseline_total_view = mod.summary_tab(df, 'Baseline', selector02)

simulation_total = mod.insert_changes(df, simulation)
simulation_total_view = mod.summary_tab(simulation_total, 'Simulation', selector02)

output_table_total = pd.concat([baseline_total_view, simulation_total_view])
output_table_total


mod.comparison_bar_charts(output_table_total, df_name='total')


##### Save button

# Create a Save button with an icon
if st.button("💾 Save Simulation"):
    
    # If the button is clicked, show the text input for Simulation Name
    simulation_name = st.text_input("Enter Simulation Name:")
    
    # When the user enters a name, allow them to save it
    if simulation_name:
        saved_simulation = mod.save_simulation(simulation_total, simulation_name)
        baseline_list.append(saved_simulation)
        mod.save_list_to_csv(baseline_list, simulations_file_path)
    else:
        st.warning("Please enter a simulation name before saving.")

