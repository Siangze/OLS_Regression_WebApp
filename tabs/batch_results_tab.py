import streamlit as st
import pandas as pd
from utils.ui_utils import get_selected_regression_config

def batch_results_tab():
    st.title("3. Batch Results")

    current_config, available_configs = get_selected_regression_config("Batch Results")

    if current_config is None:
        return

    results = current_config['results']
    if results:
        st.markdown("### Regression Result Summary")
        st.markdown(results['summary_tables'][0], unsafe_allow_html=True) # Model Summary
        st.markdown(results['summary_tables'][1], unsafe_allow_html=True) # Coefficients Table
        st.markdown(results['summary_tables'][2], unsafe_allow_html=True) # Residual Analysis

        st.markdown("### Conclusion")
        summary_stats = results['summary_stats']
        if summary_stats:
            conclusion_data = [
                ['R-squared', f"{summary_stats['R-squared']:.4f}", "**" if summary_stats['R-squared'] > 0.5 else ""],
                ['Adj. R-squared', f"{summary_stats['Adj. R-squared']:.4f}", "**" if summary_stats['Adj. R-squared'] > 0.5 else ""],
                ['F-statistic', f"{summary_stats['F-statistic']:.4f}", ""],
                ['Prob (F-statistic)', f"{summary_stats['Prob (F-statistic)']:.4f}", ""],
            ]
            
            coef_pvalue_df = summary_stats['coef_pvalue_df'].copy()
            coef_pvalue_df['P>|t| Marked'] = coef_pvalue_df.apply(lambda row: f"{row['P>|t|']:.4f}**" if row['P>|t|'] < 0.05 else f"{row['P>|t|']:.4f}", axis=1)
            coef_pvalue_df['Coef Marked'] = coef_pvalue_df['Coef'].apply(lambda x: f"{x:.4f}")

            st.dataframe(pd.DataFrame(conclusion_data, columns=['Statistic', 'Value', 'Judgment: R-squared > 0.5']))

            st.markdown("### Variable Coefficients and Significance")
            st.dataframe(coef_pvalue_df[['Variable', 'Coef Marked', 'P>|t| Marked']])

            # Display VIF results
            if 'vif_data' in results and results['vif_data']:
                st.markdown("### Variance Inflation Factor (VIF)")
                vif_df = pd.DataFrame(results['vif_data'])
                st.dataframe(vif_df[vif_df['Variable'] != 'const']) # Exclude constant for VIF display
        else:
            st.info("No regression results for this group or execution failed.")
