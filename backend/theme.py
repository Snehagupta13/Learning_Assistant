import streamlit as st

def apply_theme():
    """Sidebar toggle for Light/Dark mode with CSS injection."""
    mode = st.sidebar.radio("🌗 Theme", ["Light", "Dark"], index=0)

    if mode == "Dark":
        st.markdown(
            """
            <style>
            body, .stApp {
                background-color: #0E1117;
                color: #FAFAFA;
            }
            .stMarkdown, .stTextInput, .stSelectbox, .stRadio, .stButton button {
                color: #FAFAFA !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:  # Light
        st.markdown(
            """
            <style>
            body, .stApp {
                background-color: #FFFFFF;
                color: #000000;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    return mode
