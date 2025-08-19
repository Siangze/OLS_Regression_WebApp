import streamlit as st
import pandas as pd
import statsmodels.api as sm

st.title("OLS Regression Analysis")

# 使用者輸入 Excel 路徑
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name="Sheet1", header=0)
        st.success("Data loaded successfully!")
        st.dataframe(df)

        # 選擇 Y 和 X 變數
        columns = df.columns.tolist()
        y_var = st.selectbox("Choose Y variable", columns)
        x_vars = st.multiselect("Choose X variables", [col for col in columns if col != y_var])

        if y_var and x_vars:
            # 準備資料
            X = df[x_vars]
            X = sm.add_constant(X)  # 加入截距項
            y = df[y_var]

            # 執行 OLS
            model = sm.OLS(y, X).fit()
            st.subheader("Regression Result Summary")

            # 結果
            summary_tables = model.summary().tables
            st.markdown(summary_tables[0].as_html(), unsafe_allow_html=True) # 模型摘要
            st.markdown(summary_tables[1].as_html(), unsafe_allow_html=True) # 係數表
            
            additional_statistics = st.checkbox("Additional Statistics", value=True)
            if additional_statistics:
                st.markdown(summary_tables[2].as_html(), unsafe_allow_html=True) # 殘差分析

    except Exception as e:
        st.error(f"Error: {e}")