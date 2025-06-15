# === layout.py (Statisch, sauberes Pyramidenlayout ohne Interaktion, optimiert) ===

import streamlit as st
import streamlit.components.v1 as components

def render_ressourcen():
    st.markdown("### Ressourcen")
    resourcen = ["Holz", "Lehm", "Stein", "Papyrus", "Glas"]
    table = "<table style='width:100%; text-align:center; border-collapse: collapse;'>"
    table += "<tr><th></th>" + "".join(f"<th>{r}</th>" for r in resourcen) + "</tr>"
    for spieler in ["Spieler 1", "Spieler 2"]:
        table += f"<tr><td><b>{spieler}</b></td>"
        for r in resourcen:
            val = st.session_state.ressourcen[spieler][r]
            table += f"<td>{val}</td>"
        table += "</tr>"
    table += "</table>"
    st.markdown(table, unsafe_allow_html=True)

def render_layout():
    st.markdown(f"## 🃏 Zeitalter I – Kartenauslage ({st.session_state.spieler} ist am Zug)")

    # CSS für Pyramidenlayout und Karten
    st.markdown("""
    <style>
    .pyramide {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        margin-top: 20px;
    }
    .reihe {
        display: flex;
        gap: 10px;
        justify-content: center;
    }
    .karte {
        border: 1px solid #444;
        border-radius: 8px;
        padding: 6px 4px;
        width: 75px;
        height: 90px;
        text-align: center;
        font-size: 10px;
        box-shadow: 2px 2px 3px rgba(0,0,0,0.2);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .produziert {
        font-size: 10px;
        font-weight: bold;
        padding-bottom: 2px;
    }
    .kartenname {
        font-size: 9px;
        font-style: italic;
        padding-top: 2px;
    }
    .offen {
        background-color: #fff;
        color: #000;
    }
    .verdeckt {
        background-color: #bbb;
        color: #bbb;
    }
    </style>
    """, unsafe_allow_html=True)

    # Kartenanzeige in HTML
    html = "<div class='pyramide'>"
    for row in st.session_state.auslage:
        html += "<div class='reihe'>"
        for card in row:
            if card["genommen"]:
                html += "<div class='karte verdeckt'></div>"
            elif card["offen"]:
                html += f"""
                <div class='karte offen'>
                    <div class='produziert'>{card['effekt']['value']}× {card['effekt']['name']}</div>
                    <div class='kartenname'>{card['name']}</div>
                </div>
                """
            else:
                html += "<div class='karte verdeckt'></div>"
        html += "</div>"
    html += "</div>"

    components.html(html, height=740, scrolling=False)
