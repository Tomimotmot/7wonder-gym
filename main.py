import streamlit as st
from layout import render_layout

st.set_page_config(page_title="7 Wonders Duel – Zeitalter I", layout="centered")

def main():
    render_layout()

if __name__ == "__main__":
    main()