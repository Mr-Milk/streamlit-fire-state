# Streamlit fire state

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mr-milk-streamlit-state-demohome-mqsp3p.streamlitapp.com/)
![pypi version](https://img.shields.io/pypi/v/fire-state?color=black&logo=python&logoColor=white&style=flat)

In a multipage streamlit app, one of the most headache issues 
is that your state is not preserved if you switch between pages.

That's why fire-state is here for you.

## Installation

```shell
pip install fire-state
```

## Quick Start

### Persist state in Form

```python
import streamlit as st
from fire_state import create_store, form_update

# Register state with initiate values in a slot
slot = "home_page"
key1, key2 = create_store(slot, [
    ("state1", 5),
    ("state2", 12),
])

# Now create a form using the generated keys
with st.form("my form"):
    st.slider("State 1", 1, 10, step=1, key=key1)
    st.slider("State 1", 10, 20, step=1, key=key2)
    st.form_submit_button(label="Submit", on_click=form_update, args=(slot,))

```

When you switch between pages, the states are preserved.

### Persist state in any place

You need to control the state by yourself, using the `set_state` function.

```python
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
```

## Advanced Usage

### Persist state after form submission

In this example, we have a form to control 
how the line chart is drawn.

Let's do some setup first

```python
import numpy as np
import pandas as pd
import streamlit as st

np.random.seed(0)

@st.cache
def chart_data(line_count, data_size):
    return pd.DataFrame(
        np.random.randn(data_size, line_count),
        columns=np.random.choice(list('abcdefghijlkmn'), line_count))

```

Now we can use fire state to record the user action.

The idea is that the first time user opens the page, they never click the run button,
so the number of times they click a button is 0. When it no longer is 0, which means user clicked it. 
Therefore, the plot is rendered or updated (if chart data is changed).


```python
from fire_state import create_store, get_state, set_state, form_update

PAGE_SLOT = "Home_Page"
key1, key2, key3 = create_store(PAGE_SLOT, [
    ("line_count", 2),
    ("data_size", 13),
    ("run", 0)
])

with st.form(key="a form"):
    line_count = st.slider("Line Count", 1, 10, step=1, key=key1)
    data_size = st.slider("Data Size", 10, 20, step=1, key=key2)
    run = st.form_submit_button(label="Run", on_click=form_update, args=(PAGE_SLOT,))

prev_run_state = get_state(PAGE_SLOT, 'run')
if (prev_run_state != 0) or run:
    data = chart_data(line_count, data_size)
    st.line_chart(data)
    # increase by 1 every time user click it
    set_state(PAGE_SLOT, ("run", prev_run_state + 1))
```


### Reset the state

Use the `set_store` function to update states in a batch:

```python
import streamlit as st
from fire_state import create_store, \
    get_store, set_store, \
    get_state, set_state

slot = "page"
init_state = [
    ("state1", 1),
    ("state2", 2),
    ("state3", 3),
]
create_store(slot, init_state)

def reset():
    set_store(slot, init_state)

st.button("Reset", on_click=reset)
```

The `set_store` and `get_store` functions allow you to
modify and get your state in a batch.


## The Life Cycle of State

The state persists if you don't close or refresh the page. The state instance
is only destroyed if you stop your app.
