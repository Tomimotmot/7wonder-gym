import streamlit as st
import streamlit.components.v1 as components

def render_layout():
    st.markdown("### 🃏 Zeitalter I – Kartenauslage")

    html = """
    <style>
    .karten-container {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        justify-content: center;
        padding: 10px;
    }

    .karte {
        background-color: #f2f2f2;
        border: 2px solid #888;
        border-radius: 12px;
        padding: 14px;
        min-width: 110px;
        min-height: 90px;
        font-size: 16px;
        text-align: center;
        touch-action: manipulation;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }

    .kartenressource {
        font-size: 24px;
        margin-bottom: 4px;
    }

    .kartenname {
        font-weight: bold;
    }
    </style>

    <div class="karten-container">
        <div class="karte">
            <div class="kartenressource">🪨</div>
            <div class="kartenname">Steinbruch</div>
        </div>
        <div class="karte">
            <div class="kartenressource">🧱</div>
            <div class="kartenname">Lehmgrube</div>
        </div>
        <div class="karte">
            <div class="kartenressource">🌲</div>
            <div class="kartenname">Holzfällerlager</div>
        </div>
        <div class="karte">
            <div class="kartenressource">⛏</div>
            <div class="kartenname">Miene</div>
        </div>
    </div>
    """
    components.html(html, height=300, scrolling=False)