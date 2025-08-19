import streamlit as st

st.title("Hello Streamlit 👋")
st.write("這是一個最小展示用的範例。")

name = st.text_input("請輸入你的名字：")
if name:
    st.success(f"你好，{name}！")