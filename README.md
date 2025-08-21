# Regression Analysis and Forecasting Application

# Introduction
This project is an interactive web application developed with Streamlit, designed to help users easily perform regression analysis and data forecasting. It provides an intuitive user interface, allowing users to upload Excel data, configure regression models, view detailed statistical results (including VIF), and conduct forecasts.

# Key Features
Data Upload: Supports uploading Excel (.xlsx) files.

Variable Configuration: Allows users to select a dependent variable (Y) and multiple independent variables (X) to configure different regression groups.

Regression Analysis: Executes Ordinary Least Squares (OLS) multiple linear regression and provides a detailed summary of the results.

VIF Calculation: Automatically calculates Variance Inflation Factor (VIF) to help detect multicollinearity.

Results Presentation: Displays statistical summaries, coefficient tables, residual analysis, and VIF values for each regression model in a tabular format.

Forecasting Capability: Enables numerical forecasting based on the trained models.

# Installation and Running
Before running this application, please ensure you have Python 3.8 or higher installed on your system.

Step 1: Install Dependencies
Open your terminal or command prompt, navigate to the project's root directory, and run the following command to install the necessary Python packages:
    pip install -r requirements.txt
  
If requirements.txt does not exist, you can manually install the following packages:
    pip install streamlit pandas statsmodels numpy matplotlib seaborn
  
Step 2: Run the Application
In the terminal, navigate to the project's root directory, and run the following command to start the Streamlit application:
    streamlit run Streamlit.py
The application will open in your default web browser (usually http://localhost:8501).

# Usage Instructions
Upload Data: On the "Upload Data & Variable Configuration" tab, upload your .xlsx file.

Configure Regression Groups: Select your Y (dependent) variable and one or more X (independent) variables. You can add multiple regression groups by clicking "Add Group".

Execute Regression: Click the "Execute All Regressions" button to run all configured regression models.

View Results: Navigate to the "Batch Results" tab to see detailed statistical results for each regression group, including model summaries, coefficient tables, residual analysis, and VIF values.

Perform Forecast: Navigate to the "Forecast" tab to generate new predictions using the trained models.
