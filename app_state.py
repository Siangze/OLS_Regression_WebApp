import streamlit as st
import pandas as pd # Re-importing pandas

def initialize_session_state():
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = 0 # 0 for Upload Data
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'regression_configs' not in st.session_state:
        st.session_state.regression_configs = [{
            'id': 0,
            'y_var': None,
            'x_vars': [],
            'is_executed': False,
            'results': None
        }]
    if 'exec_button_clicked' not in st.session_state:
        st.session_state.exec_button_clicked = False
    if 'next_tab_enabled' not in st.session_state:
        st.session_state.next_tab_enabled = [True, False, False, False, False] # [Upload, Descriptive, Batch Results, Batch Conclusion, Forecast]
    if 'selected_group_idx' not in st.session_state:
        st.session_state.selected_group_idx = 0 # Default to the first group
    if 'forecast_input_df' not in st.session_state:
        st.session_state.forecast_input_df = pd.DataFrame() # DataFrame to store forecast input
    if 'time_series_column' not in st.session_state:
        st.session_state.time_series_column = None
    if 'forecast_results' not in st.session_state:
        st.session_state.forecast_results = None
    if 'numeric_columns' not in st.session_state:
        st.session_state.numeric_columns = [] # To store numeric columns from uploaded data
