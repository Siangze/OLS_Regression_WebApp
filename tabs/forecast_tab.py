import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
from utils.ui_utils import get_selected_regression_config
from utils.regression_utils import perform_ols_regression


def forecast_tab():
    st.title("5. Forecast")

    # --- 基本檢查 ---
    if not (st.session_state.file_uploaded and st.session_state.df is not None):
        st.warning("Please upload data first.")
        return
    if not st.session_state.exec_button_clicked:
        st.warning("Please execute regression analysis first.")
        return

    current_config, _ = get_selected_regression_config("Forecast")
    if not current_config or not current_config['is_executed'] or not current_config['results']:
        st.info("Please execute regression analysis on the \"Upload Data & Variable Configuration\" page first.")
        return

    results = current_config['results']
    model = results.get('model')

    if model:
        st.markdown("### Regression Model Formula")
        summary_stats = results['summary_stats']
        if summary_stats:
            coef_df = summary_stats['coef_pvalue_df']

            formula = []
            if 'const' in model.params: # Access const directly from model.params
                formula.append(f"{model.params['const']:.4f}")

            for _, row in coef_df.iterrows():
                formula.append(f"{row['Coef']:.4f} * {row['Variable']}")
            
            st.write(f"**Y = { ' + '.join(formula)}**")

        st.markdown("### Forecast Input")

    # --- Forecast Input ---
    st.sidebar.subheader("Forecast Configuration")
    df_columns = st.session_state.df.columns.tolist()
    ts_col = st.sidebar.selectbox("Select Year/Time Column", ["None"] + df_columns, index=0)
    ts_col = None if ts_col == "None" else ts_col
    st.session_state.time_series_column = ts_col

    numeric_x_vars = [col for col in current_config['x_vars'] if col in st.session_state.numeric_columns]
    base_cols = [ts_col] if ts_col else ["Year"]
    expected_cols = base_cols + numeric_x_vars

    if st.session_state.forecast_input_df.empty or list(st.session_state.forecast_input_df.columns) != expected_cols:
        st.session_state.forecast_input_df = pd.DataFrame({c: [] for c in expected_cols})

    edited_df = st.sidebar.data_editor(st.session_state.forecast_input_df, num_rows="dynamic")
    if not st.session_state.forecast_input_df.equals(edited_df):
        st.session_state.forecast_input_df = edited_df
        st.rerun()

    if st.sidebar.button("Execute Forecast"):
        if st.session_state.forecast_input_df.empty:
            st.error("Please add at least one row.")
            return
        Xf = st.session_state.forecast_input_df[numeric_x_vars].apply(pd.to_numeric, errors="coerce")
        if Xf.isnull().any().any():
            st.error("Non-numeric values found in forecast input.")
            return
        Xf = sm.add_constant(Xf, has_constant="add")
        st.session_state.forecast_results = pd.DataFrame({
            base_cols[0]: st.session_state.forecast_input_df[base_cols[0]],
            "Predicted Y (Forecast)": model.predict(Xf)
        })
        st.subheader("Forecasted Y Values")
        st.dataframe(st.session_state.forecast_results)

    # --- Plot ---
    if ts_col and model is not None:
        df_actual = st.session_state.df.copy()
        Xa = df_actual[current_config['x_vars']].apply(pd.to_numeric, errors="coerce").dropna()
        Xa = sm.add_constant(Xa, has_constant="add")
        df_actual = df_actual.loc[Xa.index].copy()
        df_actual["Actual Y"] = df_actual[current_config['y_var']]
        df_actual["Predicted Y (Actual Data)"] = model.predict(Xa)

        plot_df = df_actual[[ts_col, "Actual Y", "Predicted Y (Actual Data)"]]

        # --- 繪製 Actual 與 Predicted ---
        fig = px.line(
            plot_df,
            x=ts_col,
            y=["Actual Y", "Predicted Y (Actual Data)"],
            title="Actual vs. Predicted Y Trend"
        )

        # --- 再單獨加 Forecast 線 (紅色虛線 + 接點) ---
        if st.session_state.forecast_results is not None:
            fr = st.session_state.forecast_results.copy().sort_values(ts_col)

            # 找出 Predicted 線的最後一個點
            last_pred_point = plot_df[[ts_col, "Predicted Y (Actual Data)"]].dropna().iloc[-1]

            # 在 Forecast DataFrame 開頭插入這個點
            fr_with_anchor = pd.concat([
                pd.DataFrame({
                    ts_col: [last_pred_point[ts_col]],
                    "Predicted Y (Forecast)": [last_pred_point["Predicted Y (Actual Data)"]]
                }),
                fr
            ], ignore_index=True)

            # 畫紅色虛線（避免 legend 重複）
            fig.add_trace(
                go.Scatter(
                    x=fr_with_anchor[ts_col],
                    y=fr_with_anchor["Predicted Y (Forecast)"],
                    mode="lines",
                    name="Forecast",  # ✅ 統一名稱
                    line=dict(color="red", dash="dot"),
                    showlegend=True,
                    legendgroup="forecast"  # ✅ 避免重複
                )
            )

        st.plotly_chart(fig, use_container_width=True)
