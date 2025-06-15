# === layout.py (Pyramiden-Layout final mit Klick-Handling) ===

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
    st.markdown(f"## 🃏 Zeitalter I – Auslage ({st.session_state.spieler} ist am Zug)")

    # CSS + Layout-Template
    st.markdown("""
    <style>
    .pyramide {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        margin-top: 20px;
    }
    .reihe {
        display: flex;
        gap: 8px;
        justify-content: center;
    }
    .karte {
        width: 70px;
        height: 90px;
        border-radius: 6px;
        border: 1px solid #555;
        padding: 6px 4px;
        font-size: 11px;
        text-align: center;
        background-color: #fff;
        color: #000;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.25);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .verdeckt {
        background-color: #bbb !important;
        color: #bbb !important;
    }
    .produziert { font-weight: bold; font-size: 11px; padding-bottom: 2px; }
    .kartenname { font-size: 10px; font-style: italic; padding-top: 2px; }
    form { margin: 0; }
    button.karte {
        all: unset;
        width: 70px;
        height: 90px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border-radius: 6px;
        border: 1px solid #555;
        padding: 6px 4px;
        background-color: #fff;
        color: #000;
        text-align: center;
        font-size: 11px;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

    # HTML-Rendering vorbereiten
    html = "<div class='pyramide'>"
    for row in st.session_state.auslage:
        html += "<div class='reihe'>"
        for card in row:
            if card["genommen"]:
                html += "<div class='karte verdeckt'></div>"
            elif card["offen"]:
                html += f'''
                <form method="post">
                    <button name="click" value="{card['id']}" type="submit" class="karte">
                        <div class="produziert">{card['effekt']['value']}× {card['effekt']['name']}</div>
                        <div class="kartenname">{card['name']}</div>
                    </button>
                </form>
                '''
            else:
                html += "<div class='karte verdeckt'></div>"
        html += "</div>"
    html += "</div>"

    components.html(html, height=600, scrolling=False)

    # Klick-Verarbeitung via Session State (kein query param)
    if "_clicked" not in st.session_state:
        st.session_state._clicked = None

    if st.session_state._clicked:
        clicked_id = int(st.session_state._clicked)
        for row in st.session_state.auslage:
            for card in row:
                if card["id"] == clicked_id and not card["genommen"] and card["offen"]:
                    effekt = card["effekt"]
                    st.session_state.ressourcen[st.session_state.spieler][effekt["name"]] += effekt["value"]
                    card["genommen"] = True
                    st.session_state.spieler = "Spieler 2" if st.session_state.spieler == "Spieler 1" else "Spieler 1"
                    st.session_state._clicked = None
                    st.experimental_rerun()

    # POST-Klick-Auswertung (über hidden input abgefangen)
    if st.requested_url_query_params.get("click"):
        st.session_state._clicked = st.requested_url_query_params.get("click")[0]
        st.experimental_set_query_params()  # reset params