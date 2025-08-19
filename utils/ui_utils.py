import streamlit as st

def get_selected_regression_config(tab_name):
    if not st.session_state.file_uploaded or st.session_state.df is None:
        st.warning(f"Please successfully upload data on the \"Upload Data & Variable Configuration\" page first.")
        return None, None

    if not st.session_state.exec_button_clicked:
        st.warning(f"Please execute regression analysis on the \"Upload Data & Variable Configuration\" page first.")
        return None, None

    available_configs = [config for config in st.session_state.regression_configs if config['is_executed']]

    if not available_configs:
        st.info("No executed regression groups available.")
        return None, None

    st.subheader("Select Group to View")
    config_options = [f"Group {config['id']+1}: Y={config['y_var']} X={config['x_vars']}" for config in available_configs]

    print(f"--- Debug: ui_utils.get_selected_regression_config ---")
    print(f"  Initial st.session_state.selected_group_idx: {st.session_state.selected_group_idx}")
    print(f"  Available configs length: {len(available_configs)}")
    print(f"  Available config options: {config_options}")

    current_selected_idx = st.session_state.selected_group_idx if st.session_state.selected_group_idx < len(available_configs) else 0
    
    # Ensure selected_group_idx is within valid range after filtering available_configs
    if st.session_state.selected_group_idx >= len(available_configs):
        st.session_state.selected_group_idx = 0
        current_selected_idx = 0
    print(f"  Adjusted current_selected_idx: {current_selected_idx}")

    selected_config_idx = st.selectbox(
        "Select Group", # Provide a non-empty label
        range(len(available_configs)), 
        index=current_selected_idx, 
        format_func=lambda x: config_options[x], 
        key=f"select_config_{tab_name.replace(' ', '_').lower()}",
        label_visibility="hidden" # Hide the label visually
    )
    st.session_state.selected_group_idx = selected_config_idx
    print(f"  Selected Group Index after selectbox: {st.session_state.selected_group_idx}")

    current_config = available_configs[selected_config_idx]
    st.subheader(f"Currently Viewing: Group {current_config['id']+1}")
    
    return current_config, available_configs
