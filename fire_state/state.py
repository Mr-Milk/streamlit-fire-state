from typing import List, Tuple, Any

import streamlit as st

# Try the different possible import paths for get_script_run_ctx
try:
    # Streamlit 1.x and above (latest versions)
    from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
except (ImportError, ModuleNotFoundError):
    try:
        # Streamlit 0.x to 1.x (older versions)
        from streamlit.scriptrunner.script_run_context import get_script_run_ctx
    except (ImportError, ModuleNotFoundError):
        try:
            # Some Streamlit beta or intermediate versions
            from streamlit.runtime.scriptrunner_utils.script_run_context import get_script_run_ctx
        except (ImportError, ModuleNotFoundError):
            # If the function doesn't exist at all in the current version, define a fallback function.
            def get_script_run_ctx(suppress_warning: bool = False):
                """
                Fallback function if get_script_run_ctx is not available.
                Returns None, assuming no context is available.
                """
                if not suppress_warning:
                    print("Warning: ScriptRunContext not available in this Streamlit version.")
                return None


class Storage:

    def __init__(self):
        self._store = dict()
        self._slot_keys = dict()
        self._slot_sessions = dict()

    def _get_write_slot(self, slot, check=True):
        if slot not in self._store.keys():
            if check:
                msg = f"Slot {slot} not found"
                raise KeyError(msg)
            else:
                self._store[slot] = dict()
        return self._store[slot]

    def _store_keys(self, slot):
        return set(self._store[slot].keys())

    def update_slot_session(self, slot, session_id):
        """Return True the slot is going to be updated, Return False the slot is going to be created"""
        prev_id = self._slot_sessions.get(slot)
        self._slot_sessions[slot] = session_id
        # user session is changed
        if (prev_id is None) or (prev_id != session_id):
            return True
        else:
            return False

    def create(self, slot, items):
        write_obj = self._get_write_slot(slot, check=False)
        obj_keys = set(write_obj.keys())

        register_keys = []
        origin_keys = []
        for k, v in items:
            register_key = f"__{slot}-{k}__"
            if k not in obj_keys:
                write_obj[k] = v
                st.session_state[register_key] = v
            else:
                st.session_state[register_key] = write_obj[k]
            register_keys.append(register_key)
            origin_keys.append(k)

        self._slot_keys[slot] = dict(zip(origin_keys, register_keys))
        return register_keys

    def update(self, slot, items):
        write_obj = self._get_write_slot(slot, check=True)
        store_keys = self._store_keys(slot)

        for k, v in items:
            if k not in store_keys:
                raise KeyError(f"Cannot find `{k}` in your slot `{slot}`")
            write_obj[k] = v

    def get(self, slot):
        return self._store[slot]

    def get_keys(self, slot):
        return self._slot_keys[slot]


store = Storage()


def _get_session_id():
    return get_script_run_ctx().session_id


def create_store(slot: str, states: List) -> List[str]:
    """Create a storage, specific your initial value here

    Only the first time to call this function will write entry to the store,
    Following calls will have no effects.

    Return you with a list of keys to use in form

    For performance concert, wrap it in @st.cache

    Parameters
    ----------
    slot: str
        The identifier to store your states

    states: list of tuple,
        (state name, state value), the state name must be str
        eg. [('state1', 1), ('state2', 2)]

    Returns
    -------
    list of str
        A list of keys to use in form to preserve state

    """
    session_id = _get_session_id()
    updated = store.update_slot_session(slot, session_id)
    keys = store.create(slot, states)
    if updated:
        set_store(slot, states)
    return keys


def set_store(slot, states):
    """Update the storage object explicitly"""
    # update the storage object
    store.update(slot, states)

    # update the st.session_state
    slot_keys = store.get_keys(slot)
    for k, v in states:
        st.session_state[slot_keys[k]] = v


def get_store(slot):
    return store.get(slot)


def set_state(slot: str, state: Tuple):
    set_store(slot, [state])


def get_state(slot: str, state: str) -> Any:
    """To get a state value

    Parameters
    ----------
    slot: str
    state: str

    """
    return store.get(slot)[state]


def form_update(slot):
    """Update the form value after user click on the form button"""
    # update from the st.session_state
    slot_keys = store.get_keys(slot)
    persist_states = [(orig, st.session_state[reg]) for orig, reg in slot_keys.items()]
    store.update(slot, persist_states)
