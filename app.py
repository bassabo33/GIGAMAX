import streamlit as st

st.title("GIGAMAX")

st.write("GitHub → Streamlit Cloud 測試成功！")

start = st.number_input(
    "起始值 X",
    value=50,
    step=1
)

max_steps = st.number_input(
    "最大步數",
    value=12,
    step=1
)

st.write(f"起始值：{start}")
st.write(f"最大步數：{max_steps}")
