import streamlit as st
import pandas as pd
from utils.regression_utils import generate_pearson_correlation, generate_scatter_plots
from utils.ui_utils import get_selected_regression_config

def descriptive_stats_tab():
    st.title("2. Descriptive Statistics & Charts")

    current_config, available_configs = get_selected_regression_config("Descriptive Statistics & Charts")

    if current_config is None:
        return

    df = st.session_state.df
    y_var = current_config['y_var']
    x_vars = current_config['x_vars']

    if y_var and x_vars:
        st.markdown("### Pearson Correlation Coefficient")
        selected_vars = [y_var] + x_vars
        corr_matrix, heatmap_fig = generate_pearson_correlation(df, selected_vars)

        if corr_matrix is not None:
            st.dataframe(corr_matrix) # Display as table
            st.pyplot(heatmap_fig) # Display as heatmap

        st.markdown("### Scatter Plots of Y vs X")
        scatter_plots = generate_scatter_plots(df, y_var, x_vars)
        for plot_fig in scatter_plots:
            st.pyplot(plot_fig)

    else:
        st.info("Please select Y and X variables for this group on the \"Upload Data & Variable Configuration\" page.")
