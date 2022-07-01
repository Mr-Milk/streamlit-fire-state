import numpy as np
import pandas as pd
import streamlit as st

from fire_state import create_store, get_store, get_state, set_state, form_update

np.random.seed(0)
PAGE_SLOT = "Home"

key1, key2, _ = create_store(PAGE_SLOT, [
    ("line_count", 2),
    ("data_size", 13),
    ("run", 0)
])


@st.cache
def chart_data(line_count, data_size):
    return pd.DataFrame(
        np.random.randn(data_size, line_count),
        columns=np.random.choice(list('abcdefghijlkmn'), line_count))


st.markdown("# :fire:Streamlit fire state")
st.info("States in this page will be preserved.")

with st.form(key="a form"):
    line_count = st.slider("Line Count", 1, 10, step=1, key=key1)
    data_size = st.slider("Data Size", 10, 20, step=1, key=key2)
    st.markdown("Click the run button to update the value.")
    st.markdown("Each time you click, the count will increase")
    run = st.form_submit_button(label="Run", on_click=form_update, args=(PAGE_SLOT,))

prev_run_state = get_state(PAGE_SLOT, 'run')
if (prev_run_state != 0) or run:
    data = chart_data(line_count, data_size)
    st.line_chart(data)
    set_state(PAGE_SLOT, ("run", prev_run_state + 1))

st.subheader("You current state")
state = get_store(PAGE_SLOT)

st.write(state)
