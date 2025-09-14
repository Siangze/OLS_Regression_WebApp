import streamlit as st
from app_state import initialize_session_state
from tabs.upload_data_tab import upload_data_tab
from tabs.descriptive_stats_tab import descriptive_stats_tab
from tabs.batch_results_tab import batch_results_tab
from tabs.batch_conclusion_tab import batch_conclusion_tab
from tabs.forecast_tab import forecast_tab

initialize_session_state()
# Set
st.set_page_config(
    page_title="OLS Regression WebApp",  
    page_icon="📊",               
    layout="wide"                 
)

# Define tabs and their corresponding functions
tabs_config = [
    {"title": "1. Upload Data & Variable Configuration", "function": upload_data_tab},
    {"title": "2. Descriptive Statistics & Charts", "function": descriptive_stats_tab},
    {"title": "3. Batch Results", "function": batch_results_tab},
    {"title": "4. Batch Conclusion", "function": batch_conclusion_tab},
    {"title": "5. Forecast", "function": forecast_tab},
]

# Create tabs with disabled state management
tabs = st.tabs([config["title"] for config in tabs_config])

for i, tab in enumerate(tabs):
    with tab:
        if st.session_state.next_tab_enabled[i]:
            tabs_config[i]["function"]()
        else:
            st.warning("Please complete the previous step to access this page.")

