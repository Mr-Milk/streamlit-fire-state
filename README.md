# Streamlit fire state

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mr-milk-streamlit-state-demohome-mqsp3p.streamlitapp.com/)
![pypi version](https://img.shields.io/pypi/v/fire-state?color=black&logo=python&logoColor=white&style=flat)

In multipage streamlit app, one of the most headache issues
is your state will not preserve if you switch between pages.

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

# register your state with initiate values
# the slot is an identifier for your state
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

Great, just create a store and the pass the keys to your form, and you are good to go.

In production, it's recommended that you warp the `create_store` in a `@st.cache`

```python
import streamlit as st
from fire_state import create_store

slot = "page"


@st.cache
def init_state():
    return create_store(slot, [
        ("state1", 5),
        ("state2", 12),
    ])


key1, key2 = init_state()
```

### Persist state after form submission

Now you get the idea of preserving state in form, how to preserve state 
of the action happen after the submission.

For example, you control how your line chart is drawn using a form.

Let's do some set up first

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

This is very similar to the first example, except we add other state
for the run button.

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

The idea is that the first time user open the page, they never click the run button,
so it's value is 0, the number of time they click it. 
When it no longer is 0, that means user clicked it. The plot will always be rendering.


### Working with non-form widget

It's strongly recommended that you work with form for user input.
It batches user events and won't refresh
the page at every `on_change` event.

If you are not working with user input. You need to update the state manually.

```python
from fire_state import create_store, \
    get_store, set_store, \
    get_state, set_state

slot = "page"
create_store(slot, [
    ("state1", 1),
    ("state2", 2),
    ("state3", 3),
    ("state4", 4)
])
```

To change a state value
```python
set_state(slot, ("state2", 3))
```

To read a state value
```python
get_state(slot, "state2") # return 3
```

Or you can change and read in batch
```python
set_store(slot, [
    ("state3", 13),
    ("state4", 14)
])

get_store(slot) # return a dict
```



