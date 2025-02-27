import streamlit as st
import pandas as pd
import plotly.express as px

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