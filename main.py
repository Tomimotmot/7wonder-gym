import streamlit as st
from layout import render_layout
from gamelogic import init_game

st.set_page_config(page_title="7 Wonders Duel", layout="centered")

def main():
    init_game()
    render_layout()

if __name__ == "__main__":
    main()
