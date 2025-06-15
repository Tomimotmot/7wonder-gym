# === layout.py (Pyramiden-Layout final mit Klick-Handling, wie Screenshot) ===

import streamlit as st
import streamlit.components.v1 as components

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
    st.markdown(f"## 🃏 Zeitalter I – Kartenauslage ({st.session_state.spieler} ist am Zug)")

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
        padding: 4px 3px;
        width: 70px;
        height: 76px;
        text-align: center;
        font-size: 10.5px;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.15);
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
    form { margin: 0; }
    button.karte { all: unset; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

    html = "<div class='pyramide'>"

    for row in st.session_state.auslage:
        html += "<div class='reihe'>"
        for card in row:
            if card["genommen"]:
                html += "<div class='karte verdeckt'></div>"
            elif card["offen"]:
                html += f'''
                <form method="post">
                    <button name="click" value="{card['id']}" type="submit" class="karte offen">
                        <div class="produziert">{card["effekt"]["value"]}× {card["effekt"]["name"]}</div>
                        <div class="kartenname">{card["name"]}</div>
                    </button>
                </form>
                '''
            else:
                html += "<div class='karte verdeckt'></div>"
        html += "</div>"
    html += "</div>"

    components.html(html, height=660, scrolling=False)

    # Klickhandling über session_state
    if st.session_state.get("click"):
        clicked_id = int(st.session_state.click)
        for row in st.session_state.auslage:
            for card in row:
                if card["id"] == clicked_id and not card["genommen"] and card["offen"]:
                    effekt = card["effekt"]
                    st.session_state.ressourcen[st.session_state.spieler][effekt["name"]] += effekt["value"]
                    card["genommen"] = True
                    st.session_state.spieler = "Spieler 2" if st.session_state.spieler == "Spieler 1" else "Spieler 1"
                    st.session_state.click = None
                    st.experimental_rerun()

    # Klick-Input setzen (muss im Hauptskript abgefangen und in session_state.click gespeichert werden)
    if "click" not in st.session_state:
        st.session_state.click = None
