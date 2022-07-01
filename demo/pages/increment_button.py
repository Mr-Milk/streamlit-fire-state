import streamlit as st
from fire_state import create_store, get_state, set_state

slot = "home_page"
create_store(slot, [
    ("state1", 0),
])


def increment():
    prev = get_state(slot, "state1")
    set_state(slot, ("state1", prev + 1))


st.button("+1", on_click=increment)
st.text(f"Value: {get_state(slot, 'state1')}")
