import streamlit as st
from gamelogic import handle_card_click

def render_ressourcen():
    st.markdown("### Ressourcen")
    resourcen = ["Holz", "Lehm", "Stein", "Papyrus", "Glas"]
    table = "<table style='width:100%; text-align:center;'>"
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
    st.markdown(f"## 🃏 Zeitalter I – Auslage ({st.session_state.spieler} ist am Zug)")

    st.markdown("""
    <style>
    .pyramide {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 6px;
        margin-top: 20px;
    }
    .reihe {
        display: flex;
        gap: 6px;
        justify-content: center;
    }
    .karte {
        border: 1px solid #555;
        border-radius: 6px;
        padding: 4px;
        width: 70px;
        height: 72px;
        text-align: center;
        font-size: 10px;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background-color: #fff;
        color: #000;
    }
    .verdeckt {
        background-color: #ccc !important;
        color: #ccc !important;
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
    </style>
    """, unsafe_allow_html=True)

    html = "<div class='pyramide'>"

    for row in st.session_state.auslage:
        html += "<div class='reihe'>"
        for card in row:
            if card["genommen"]:
                html += "<div style='width: 70px; height: 72px;'></div>"
            elif card["offen"]:
                html += f'''
                <form method="post">
                    <button name="click" value="{card['id']}" type="submit" class="karte">
                        <div class="produziert">{card["effekt"]["value"]}× {card["effekt"]["name"]}</div>
                        <div class="kartenname">{card["name"]}</div>
                    </button>
                </form>
                '''
            else:
                html += "<div class='karte verdeckt'></div>"
        html += "</div>"
    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    # POST-Auswertung für Button-Click
    if "click" in st.session_state:
        handle_card_click(int(st.session_state.click))
