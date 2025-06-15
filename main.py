import streamlit as st
from layout import render_layout

def main():
    st.set_page_config(layout="wide")
    render_layout()

if __name__ == "__main__":
    main()

