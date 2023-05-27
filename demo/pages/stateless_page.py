import numpy as np
import pandas as pd
import streamlit as st
from streamlit.runtime.scriptrunner.script_run_context import \
    get_script_run_ctx

np.random.seed(0)
PAGE_SLOT = "Home"

ctx = get_script_run_ctx()
print(ctx.query_string)


@st.cache
def chart_data(line_count, data_size):
    return pd.DataFrame(
        np.random.randn(data_size, line_count),
        columns=np.random.choice(list('abcdefghijlkmn'), line_count))


st.header("Go back to the home page with unchanged state")

st.error("States in this page will not be reserved.")

with st.form(key="a form"):
    line_count = st.slider("Line Count", 1, 10, value=2, step=1, key="line_count")
    data_size = st.slider("Data Size", 10, 20, value=13, step=1, key="data_size")
    run = st.form_submit_button(label="Run")

if run:
    data = chart_data(line_count, data_size)
    st.line_chart(data)
