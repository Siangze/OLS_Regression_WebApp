import streamlit as st
import pandas as pd
from utils.regression_utils import perform_ols_regression, extract_summary_stats
import numpy as np

def upload_data_tab():
    st.title("1. Upload Data & Variable Configuration")

    st.markdown("Please upload an Excel file (.xlsx). The program will automatically read the 'Sheet1' worksheet with the first row as headers.")
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file, sheet_name="Sheet1", header=0)
            st.success("Data loaded successfully!")
            st.dataframe(df)
            st.session_state.df = df
            st.session_state.file_uploaded = True

            # Filter out non-numeric columns for regression analysis
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            st.session_state.numeric_columns = numeric_cols

            # Move to the next tab if file uploaded and displayed
            st.session_state.next_tab_enabled[1] = True

        except Exception as e:
            st.error(f"Loading Error: {e}")
            st.session_state.file_uploaded = False
            st.session_state.df = None
            st.session_state.next_tab_enabled[1] = False

    if st.session_state.df is not None:
        # Use only numeric columns for variable selection
        columns = st.session_state.numeric_columns
        if not columns:
            st.warning("No numeric columns found in the uploaded data for regression analysis.")
            return

        st.sidebar.subheader("Regression Group Configuration")

        if st.sidebar.button("Add Group", key="add_config_btn"):
            if len(st.session_state.regression_configs) < 10:
                st.session_state.regression_configs.append({
                    'id': len(st.session_state.regression_configs),
                    'y_var': None,
                    'x_vars': [],
                    'is_executed': False,
                    'results': None
                })
            else:
                st.sidebar.warning("You can configure a maximum of 10 regression groups.")

        for i, config in enumerate(st.session_state.regression_configs):
            print(f"--- Debug: Group {i+1} Configuration ---")
            print(f"  Initial y_var: {config['y_var']}")
            print(f"  Initial x_vars: {config['x_vars']}")
            print(f"  Available columns: {columns}")

            st.sidebar.markdown(f"**Group {i+1}**")
            # Allow deleting a config, but not the last one
            if len(st.session_state.regression_configs) > 1 and st.sidebar.button(f"Delete Group {i+1}", key=f"delete_config_btn_{i}"):
                st.session_state.regression_configs.pop(i)
                st.rerun() # Re-enable rerun to update the list of configs immediately

            y_var = st.sidebar.selectbox(
                f"Select Y Variable (Group {i+1})",
                ["None"] + columns,
                index=(["None"] + columns).index(config['y_var']) if config['y_var'] in columns else 0,
                key=f"y_var_select_{i}"
            )
            if y_var == "None":
                y_var = None
            st.session_state.regression_configs[i]['y_var'] = y_var

            # Filter x_vars to only include those present in current numeric columns
            current_x_vars = [x for x in config['x_vars'] if x in columns and x != y_var]
            print(f"  Filtered x_vars for multiselect: {current_x_vars}")

            x_vars = st.sidebar.multiselect(
                f"Select X Variables (Group {i+1})",
                [col for col in columns if col != y_var],
                default=current_x_vars,
                key=f"x_vars_select_{i}"
            )
            # Always update session state and rerun after multiselect change to ensure immediate UI refresh
            if st.session_state.regression_configs[i]['x_vars'] != x_vars:
                st.session_state.regression_configs[i]['x_vars'] = x_vars
                st.rerun() 

            st.sidebar.markdown("--- ")
        
        st.sidebar.markdown("--- ")
        execute_button = st.sidebar.button("Execute All Regressions", key="execute_ols_btn")

        if execute_button:
            st.session_state.exec_button_clicked = True
            all_configs_valid = True
            for i, config in enumerate(st.session_state.regression_configs):
                if not config['y_var'] or not config['x_vars']:
                    st.error(f"Group {i+1}: Both Y variable and at least one X variable must be selected to perform regression analysis.")
                    all_configs_valid = False
                    break
            
            if all_configs_valid:
                with st.spinner("Executing regression analysis..."):
                    for i, config in enumerate(st.session_state.regression_configs):
                        st.session_state.regression_configs[i]['is_executed'] = True
                        
                        # Perform OLS Regression
                        model, vif_data = perform_ols_regression(st.session_state.df, config['y_var'], config['x_vars'])

                        if model:
                            # Extract Summary Stats
                            summary_stats = extract_summary_stats(model)

                            # Generate Summary Tables
                            summary_tables = [
                                model.summary().tables[0].as_html(),  # Model Summary
                                model.summary().tables[1].as_html(),  # Coefficients Table
                                model.summary().tables[2].as_html()   # Residual Analysis
                            ]
                            
                            st.session_state.regression_configs[i]['results'] = {
                                'summary_stats': summary_stats,
                                'summary_tables': summary_tables,
                                'vif_data': vif_data, # Store VIF data
                                'model': model # Store the model object
                            }
                        else:
                            st.session_state.regression_configs[i]['results'] = None

                        st.session_state.selected_group_idx = i
                st.success("Regression analysis completed!")
                st.session_state.next_tab_enabled[2] = True # Enable Batch Results tab
                st.session_state.next_tab_enabled[3] = True # Enable Batch Conclusion tab (since its dependent on batch results)
                st.session_state.next_tab_enabled[4] = True # Enable Forecast tab
                st.session_state.current_tab = 2 # Move to Batch Results tab after execution
