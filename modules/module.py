import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import math
from datetime import datetime
import os
import csv


def fill_selector(df, col_name):
    """
    Description: generates a list of selectable options for a user interface element, such as a dropdown menu.

    Parameters:
    - `df` (pandas.DataFrame): The DataFrame from which the function will extract unique values.
    - `col_name` (str): The name of the column in the DataFrame from which unique values are to be retrieved.

    Return:
    - `choices_lst` (list): A list of unique values from the specified column, sorted in ascending order, with
    `'All'` as the first item.
    """
    choices_lst = list(df[col_name].unique())  # Convert unique values to a list
    choices_lst.sort()  # Sort the list in ascending order
    choices_lst.insert(0, 'All')  # Insert 'All' at the beginning of the list
    return choices_lst


def select_name(df, level):
    """
    Description: Returns a list of selectable options for a given level, using the `fill_selector` function to
    generate the list of options.

    Parameters:
    - `df` (pandas.DataFrame): The DataFrame from which the function will extract unique values for the selected
    level.
    - `level` (str): The level of selection (e.g., 'All', 'Category', 'Product ID').

    Return:
    - `selection_options` (list): A list of selectable options for the user interface, either a placeholder
    `['--']` if 'All' is selected, or a sorted list of unique values from the specified level.
    """
    if level == 'All':
        return ['--']  # Return a placeholder for 'All'
    else:
        selection_options = fill_selector(df, level)
        return selection_options
    

def apply_filter(df, col_name, selector):
    """    
    Description: Filters a DataFrame based on a specified column and selector value. If the selector is 'All',
    no filtering is applied; otherwise, the DataFrame is filtered to include only the rows where the column's value
    matches the selector.

    Parameters:
    - `df` (pandas.DataFrame): The DataFrame to be filtered.
    - `col_name` (str): The name of the column to apply the filter on.
    - `selector` (str): The value to filter the column by. If 'All' is selected, no filtering is applied.

    Return:
    - `data_selection` (pandas.DataFrame): The filtered DataFrame based on the selector value. If 'All' is selected,
    the original DataFrame is returned unmodified.
    """
    if selector != 'All':
        data_selection = df[df[col_name] == selector]
        return data_selection
    else:
        return df
    

def profit_calc(df, col_lst):
    df['Net Price'] = df['List Price'] * (1 - df['Discount'])
    df['Sales'] = df['Net Price'] * df['Quantity']
    df['Profit'] = (df['Net Price'] - df['COGS']) * df['Quantity']
    df['Gross Margin'] = df['Profit'] / df['Sales']
    
    # formatting
    for col in col_lst:
        
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].apply(
                        lambda x: math.ceil(x * 100) / 100 if pd.notna(x) and np.isfinite(x) else x)
        #df[col] = df[col].astype('float64')

    return df


def gross_margin_calc(df, col_lst):
    df['Net Price'] = df['COGS'] / (1 - df['Gross Margin'])
    df['Sales'] = df['Net Price'] * df['Quantity']
    df['List Price'] = df['Net Price'] / (1 - df['Discount'])
    df['Profit'] = (df['Net Price'] - df['COGS']) * df['Quantity']
    df['Gross Margin'] = df['Profit'] / df['Sales']
    
    # formatting
    for col in col_lst:
        
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].apply(
                        lambda x: math.ceil(x * 100) / 100 if pd.notna(x) and np.isfinite(x) else x)
        #df[col] = df[col].astype('float64')

    return df


def summary_tab(df, version_str, selected_year):
    """
    This function takes a DataFrame 'df' containing financial data and performs various calculations
    such as adjusting the 'List Price', calculating 'Discount Value', 'Net Price', 'COGS', 'Gross Margin',
    and performing group-by operations. It returns a DataFrame with the aggregated results and rounded values.
    """
    # Step 1: Filter by 'Order Year'

    if selected_year != 'All':
        df = df[df['Order Year'] == selected_year]
    else:
        pass
    
    # Step 2: Add the 'Title' column
    df['Version'] = version_str
    
    # Step 3: Calculate Discount and COGS Total value
    df['Discount Value'] = df['Discount'] * df['List Price'] * df['Quantity']
    df['Total COGS'] = df['COGS'] * df['Quantity']
    
    # Step 4: Group the data by 'Title' and aggregate the numeric columns
    df_grouped = df.groupby(['Version'])[['Quantity', 'Sales', 'Discount Value', 'Total COGS', 'Profit']].sum()
    
    # Step 5: Calculate the rest of financial metrics
    df_grouped['Net Price'] = df_grouped['Sales'] / df_grouped['Quantity']
    df_grouped['COGS'] = (df_grouped['Sales'] - df_grouped['Profit']) / df_grouped['Quantity']
    df_grouped['List Price'] = (df_grouped['Sales'] + df_grouped['Discount Value']) / df_grouped['Quantity']
    df_grouped['Disc. %'] = np.where(df_grouped['List Price'] != 0, 
                                 1 - (df_grouped['Net Price'] / df_grouped['List Price']), 
                                 0)
    df_grouped['GM %'] = df_grouped['Profit'] / df_grouped['Sales']
        
    # Step 6: Reorder the columns
    new_column_order = ['COGS', 'List Price', 'Net Price', 'Disc. %', 'Quantity', 'Sales', 'Total COGS', 'Profit', 'GM %']
    df_grouped = df_grouped[new_column_order]
    
    # Step 7: Round the values in the DataFrame
    for col in df_grouped.columns:
        df_grouped[col] = pd.to_numeric(df_grouped[col], errors='coerce')
        df_grouped[col] = df_grouped[col].apply(
            lambda x: math.ceil(x * 100) / 100 if pd.notna(x) and np.isfinite(x) else x)
        #df_grouped[col] = df_grouped[col].astype('float64')
    
    return df_grouped




    
def insert_changes(original_df, updated_rows_df):
    new_df = original_df.copy()
    new_df.set_index('Row ID', inplace=True)
    updated_rows_df.set_index('Row ID', inplace=True)
    new_df.update(updated_rows_df)
    new_df.reset_index(inplace=True)
    return new_df


def comparison_bar_charts(df, df_name='df'):
    """
    Function to generate and display three side-by-side bar charts for 'Sales', 'Total COGS', and 'Profit'.
    The charts are created using Plotly Express and displayed in a Streamlit app. Each bar is colored based on the 'Version'.
    The axis titles and legends are hidden, and the chart titles are centered.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data for the charts, including 'Version', 'Sales', 'Total COGS', and 'Profit'.
    df_name (str): A unique name or identifier for the DataFrame, used to create unique chart keys. Default is 'df'.
    """
    # Reset index and add a 'Color' column based on the 'Version' column
    df_reset = df.reset_index()
    df_reset['Color'] = df_reset['Version']

    # Create three columns in the Streamlit layout for displaying the charts
    col1, col2, col3 = st.columns(3)

    # First chart (Sales)
    with col1:
        fig_sales = px.bar(df_reset, 
                           x='Version', 
                           y='Sales', 
                           color='Color', 
                           height=300, 
                           width=400)
        fig_sales.update_layout(title={'text': 'Sales', 'x': 0.5, 'xanchor': 'center'},
                                xaxis_title="",
                                yaxis_title="",
                                showlegend=False)
        st.plotly_chart(fig_sales, key=f'{df_name}_sales_chart')

    # Second chart (Total COGS)
    with col2:
        fig_cogs = px.bar(df_reset, 
                          x='Version', 
                          y='Total COGS', 
                          color='Color', 
                          height=300, 
                          width=400)
        fig_cogs.update_layout(title={'text': 'Total COGS', 'x': 0.5, 'xanchor': 'center'},
                               xaxis_title="",
                               yaxis_title="",
                               showlegend=False)
        st.plotly_chart(fig_cogs, key=f'{df_name}_cogs_chart')

    # Third chart (Profit)
    with col3:
        fig_profit = px.bar(df_reset, 
                            x='Version', 
                            y='Profit', 
                            color='Color', 
                            height=300, 
                            width=400)
        fig_profit.update_layout(title={'text': 'Profit', 'x': 0.5, 'xanchor': 'center'},
                                 xaxis_title="",
                                 yaxis_title="",
                                 showlegend=False)
        st.plotly_chart(fig_profit, key=f'{df_name}_profit_chart')


# Define the function to run when the "Save" button is clicked


'''
def save_simulation(df, file_name, file_list):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    full_name = file_name + '_' + timestamp + '.csv'
    file_list.append(full_name)
    path = './data/' + full_name
    df.to_csv(path, index=False)
    st.write(f"Simulation '{full_name}' saved successfully!")
'''

# Function to save the simulation and track the file name
def save_simulation(df, file_name):
    """
    This function saves the given DataFrame to a CSV file with the specified file name and timestamp.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame to be saved.
    file_name (str): The base name of the file to be saved.
    """
    # Get the current timestamp in 'YYYY-MM-DD_HH-MM-SS' format
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Generate the full name by appending timestamp
    full_name = file_name + '_' + timestamp + '.csv'
    
    # Define the path where the file will be saved
    path = './data/' + full_name
    
    # Save the DataFrame to CSV
    df.to_csv(path, index=False)
    
    # Inform the user the simulation was saved
    st.write(f"Simulation '{full_name}' saved successfully!")

    return full_name


def save_list_to_csv(my_list, file_path):
    """
    This function saves a list of simulation names to a CSV file.
    
    Parameters:
    my_list (list): The list of simulation names to be saved.
    file_name (str): The name of the CSV file to save the list to.
    """
    # Open the file in write mode and use csv.writer
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header (optional)
        writer.writerow(['Simulation Name'])
        
        # Write each item from the list as a new row
        for item in my_list:
            writer.writerow([item])  # Each list item as a new row



def read_list_from_csv(file_path):
    """
    This function reads a CSV file and retrieves the list of simulation names.
    
    Parameters:
    file_name (str): The name of the CSV file to read the list from.
    
    Returns:
    list: A list of simulation names.
    """
    simulation_list = []
    
    # Open the file in read mode and use csv.reader
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        
        # Skip the header row
        next(reader)
        
        # Append each row (simulation name) to the list
        for row in reader:
            simulation_list.append(row[0])  # row[0] holds the simulation name
    
    return simulation_list
