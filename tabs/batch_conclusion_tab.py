import streamlit as st
import pandas as pd

def batch_conclusion_tab():
    st.title("4. Batch Conclusion")

    if not st.session_state.file_uploaded or st.session_state.df is None:
        st.warning("Please successfully upload data on the \"Upload Data & Variable Configuration\" page first.")
        return

    if not st.session_state.exec_button_clicked:
        st.warning("Please execute regression analysis on the \"Upload Data & Variable Configuration\" page first.")
        return

    all_conclusions = []
    for config in st.session_state.regression_configs:
        if config['is_executed'] and config['results']:
            summary_stats = config['results']['summary_stats']
            if summary_stats:
                # Get overall significance based on Prob (F-statistic), R-squared, and individual variable significance
                is_f_significant = summary_stats['Prob (F-statistic)'] < 0.05
                is_r_squared_good = summary_stats['R-squared'] > 0.5 or summary_stats['Adj. R-squared'] > 0.5
                
                # Check if all individual X variables are significant
                all_x_vars_significant = True
                if summary_stats['coef_pvalue_df'] is not None and not summary_stats['coef_pvalue_df'].empty:
                    for _, row in summary_stats['coef_pvalue_df'].iterrows():
                        # Only check significance for actual X variables, not 'const'
                        if row['Variable'] != 'const' and row['P>|t|'] >= 0.05:
                            all_x_vars_significant = False
                            break
                else:
                    # If there are no X variables, or coef_pvalue_df is empty, it can't be all significant
                    all_x_vars_significant = False 

                overall_significance = "Significant" if is_f_significant and is_r_squared_good and all_x_vars_significant else "Not Significant"
                
                # Prepare data for each row in the combined conclusion table
                conclusion_row = {
                    'Group': f"{config['id']+1}",
                    'Y Variable': config['y_var'],
                    'X Variables': ", ".join(config['x_vars']),
                    'R-squared': f"{summary_stats['R-squared']:.4f}",
                    'Adj. R-squared': f"{summary_stats['Adj. R-squared']:.4f}",
                    'F-statistic': f"{summary_stats['F-statistic']:.4f}",
                    'Prob (F-statistic)': f"{summary_stats['Prob (F-statistic)']:.4f}",
                    'Overall Significance': overall_significance
                }
                all_conclusions.append(conclusion_row)
    
    if all_conclusions:
        st.dataframe(pd.DataFrame(all_conclusions))
    else:
        st.info("No batch conclusions available. Please ensure regression analysis has been executed.")
