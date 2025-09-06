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
            /* Force text inside widgets to white */
            .stMarkdown, .stTextInput label, .stSelectbox label, .stRadio label,
            .stCheckbox label, .stMultiSelect label, .stTextArea label {
                color: #FAFAFA !important;
            }
            /* Text inside input boxes */
            input, textarea, select {
                background-color: #1E1E1E !important;
                color: #FAFAFA !important;
            }
            /* Buttons */
            .stButton button {
                background-color: #262730 !important;
                color: #FAFAFA !important;
                border: 1px solid #FAFAFA !important;
            }
            .stButton button:hover {
                background-color: #333333 !important;
                color: #FFFFFF !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:  # Light mode
        st.markdown(
            """
            <style>
            body, .stApp {
                background-color: #FFFFFF;
                color: #000000;
            }
            /* Reset widget styling */
            input, textarea, select {
                background-color: #FFFFFF !important;
                color: #000000 !important;
            }
            .stButton button {
                background-color: #F0F0F0 !important;
                color: #000000 !important;
                border: 1px solid #000000 !important;
            }
            .stButton button:hover {
                background-color: #E0E0E0 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    return mode
