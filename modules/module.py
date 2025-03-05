import streamlit as st
import pandas as pd
import plotly.express as px
from decimal import Decimal, ROUND_HALF_UP


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
            lambda x: Decimal(str(x)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if pd.notna(x) else x)
        df[col] = df[col].astype('float64')

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
            lambda x: Decimal(str(x)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if pd.notna(x) else x)
        df[col] = df[col].astype('float64')

    return df

import pandas as pd
from decimal import Decimal, ROUND_HALF_UP


def summary_tab(df, title_str):
    """
    This function takes a DataFrame 'df' containing financial data and performs various calculations
    such as adjusting the 'List Price', calculating 'Discount Value', 'Net Price', 'COGS', 'Gross Margin',
    and performing group-by operations. It returns a DataFrame with the aggregated results and rounded values.
    """
    # Step 1: Add the 'Title' column
    df['Title'] = title_str
    
    # Step 2: Calculate Discount Value
    df['Discount Value'] = df['Discount'] * df['List Price'] * df['Quantity']
    
    # Step 3: Group the data by 'Title' and aggregate the numeric columns
    df_grouped = df.groupby('Title')[['Quantity', 'Sales', 'Discount Value', 'Profit']].sum()
    
    # Step 4: Calculate the rest of financial metrics
    df_grouped['Net Price'] = df_grouped['Sales'] / df_grouped['Quantity']
    df_grouped['COGS'] = (df_grouped['Sales'] - df_grouped['Profit']) / df_grouped['Quantity']
    df_grouped['List Price'] = (df_grouped['Sales'] + df_grouped['Discount Value']) / df_grouped['Quantity']
    df_grouped['Discount'] = 1 - (df_grouped['Net Price'] / df_grouped['List Price'])
    df_grouped['Gross Margin'] = df_grouped['Profit'] / df_grouped['Sales']
        
    # Step 5: Reorder the columns
    new_column_order = ['COGS', 'List Price', 'Net Price', 'Discount', 'Quantity', 'Sales', 'Profit', 'Gross Margin']
    df_grouped = df_grouped[new_column_order]
    
    # Step 6: Round the values in the DataFrame
    for col in df_grouped.columns:
        df_grouped[col] = df_grouped[col].apply(
            lambda x: Decimal(str(x)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if pd.notna(x) else x)
        df_grouped[col] = df_grouped[col].astype('float64')
    
    return df_grouped

    