import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from statsmodels.stats.outliers_influence import variance_inflation_factor # Import for VIF calculation

@st.cache_data
def perform_ols_regression(df, y_var, x_vars):
    if not y_var or not x_vars:
        return None

    X = df[x_vars]
    X = sm.add_constant(X)  # Add intercept term
    y = df[y_var]

    model = sm.OLS(y, X).fit()
    
    # Calculate VIF
    vif_data = pd.DataFrame()
    vif_data["Variable"] = X.columns
    vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    
    return model, vif_data.to_dict('records') # Return model and VIF data

def extract_summary_stats(model):
    if model is None:
        return None

    summary_data = {}
    # Extract R-squared, Adj. R-squared, F-statistic, Prob (F-statistic)
    summary_data['R-squared'] = model.rsquared
    summary_data['Adj. R-squared'] = model.rsquared_adj
    summary_data['F-statistic'] = model.fvalue
    summary_data['Prob (F-statistic)'] = model.f_pvalue

    # Extract coef and P>|t|
    params_df = model.params.reset_index()
    params_df.columns = ['Variable', 'Coef']
    pvalues_df = model.pvalues.reset_index()
    pvalues_df.columns = ['Variable', 'P>|t|']

    # Merge coef and P>|t| for each variable, excluding 'const'
    coef_pvalue_df = pd.merge(params_df, pvalues_df, on='Variable')
    coef_pvalue_df = coef_pvalue_df[coef_pvalue_df['Variable'] != 'const']

    summary_data['coef_pvalue_df'] = coef_pvalue_df
    
    return summary_data

@st.cache_data
def generate_pearson_correlation(df, selected_vars):
    if not selected_vars or df is None:
        return None, None
    
    corr_matrix = df[selected_vars].corr(method='pearson')

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, ax=ax)
    ax.set_title('Pearson Correlation Matrix')
    return corr_matrix, fig

@st.cache_data
def generate_scatter_plots(df, y_var, x_vars):
    if not y_var or not x_vars or df is None:
        return []
    
    plots = []
    for x_var in x_vars:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(x=df[x_var], y=df[y_var], ax=ax)
        ax.set_title(f'{y_var} vs {x_var} Scatter Plot')
        ax.set_xlabel(x_var)
        ax.set_ylabel(y_var)
        plots.append(fig)
    return plots
