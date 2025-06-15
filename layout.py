# === layout.py (Final mit Klickhandling & stabilem Pyramidenlayout – überarbeitet) ===

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
        gap: 8px;
        margin-top: 20px;
    }
    .reihe {
        display: flex;
        gap: 8px;
        justify-content: center;
    }
    .karte {
        border: 1px solid #555;
        border-radius: 8px;
        padding: 6px 4px;
        width: 70px;
        height: 85px;
        text-align: center;
        font-size: 10px;
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
    </style>
    """, unsafe_allow_html=True)

    html = "<div class='pyramide'>"

    for row_index, row in enumerate(st.session_state.auslage):
        html += "<div class='reihe'>"
        for card in row:
            if card["genommen"]:
                html += "<div class='karte verdeckt'></div>"
            elif card["offen"]:
                html += f"""
                <form method='post'>
                    <input type='hidden' name='click' value='{card['id']}'/>
                    <button class='karte offen' type='submit'>
                        <div class='produziert'>{card['effekt']['value']}× {card['effekt']['name']}</div>
                        <div class='kartenname'>{card['name']}</div>
                    </button>
                </form>
                """
            else:
                html += "<div class='karte verdeckt'></div>"
        html += "</div>"
    html += "</div>"

    components.html(html, height=700, scrolling=False)

    # Klick auswerten
    if st.session_state.get("click"):
        clicked_id = int(st.session_state.click)
        for row in st.session_state.auslage:
            for card in row:
                if card["id"] == clicked_id and not card["genommen"] and card["offen"]:
                    st.session_state.ressourcen[st.session_state.spieler][card["effekt"]["name"]] += card["effekt"]["value"]
                    card["genommen"] = True
                    st.session_state.spieler = "Spieler 2" if st.session_state.spieler == "Spieler 1" else "Spieler 1"
                    st.session_state.click = None
                    st.experimental_rerun()
