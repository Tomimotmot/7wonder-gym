# layout.py – Direkt klickbare Karten ohne Extra-Button (Pyramide 2–3–4–5–6)

import streamlit as st
import json
from pathlib import Path
import streamlit.components.v1 as components

def render_layout():
    st.markdown("## 🃏 Zeitalter I – Kartenauslage")

    # 1. Session-State Setup
    if "spieler" not in st.session_state:
        st.session_state.spieler = "Spieler 1"

    if "ressourcen" not in st.session_state:
        r = ["Holz", "Lehm", "Stein", "Papyrus", "Glas"]
        st.session_state.ressourcen = {
            "Spieler 1": {x: 0 for x in r},
            "Spieler 2": {x: 0 for x in r},
        }

    if "genommene_karten" not in st.session_state:
        st.session_state.genommene_karten = set()

    # 2. Ressourcenanzeige
    st.markdown(f"### Ressourcenübersicht ({st.session_state.spieler} ist am Zug)")
    res = ["Holz", "Lehm", "Stein", "Papyrus", "Glas"]
    table = "<table style='width:100%; text-align:center;'><tr><th></th>"
    table += "".join(f"<th>{r}</th>" for r in res) + "</tr>"
    for sp in ["Spieler 1", "Spieler 2"]:
        table += f"<tr><td><b>{sp}</b></td>" + "".join(
            f"<td>{st.session_state.ressourcen[sp][r]}</td>" for r in res
        ) + "</tr>"
    table += "</table>"
    st.markdown(table, unsafe_allow_html=True)

    # 3. Kartenstruktur vorbereiten
    layout_structure = [(2, True), (3, False), (4, True), (5, False), (6, True)]
    cards = load_cards_from_json()
    card_id = 0

    # 4. HTML + CSS + JS
    html = """
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
        justify-content: center;
        gap: 10px;
    }
    .karte {
        width: 84px; height: 105px;
        border-radius: 6px;
        font-size: 10px;
        padding: 6px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        text-align: center;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        cursor: pointer;
    }
    .offen { background: #fff; color: #000; border: 1px solid #444; }
    .verdeckt { background: #bbb; color: #bbb; border: 1px solid #999; }
    .produziert { font-weight: bold; font-size: 10px; }
    .kartenname { font-style: italic; font-size: 9px; }
    </style>
    <script>
    function sendClick(card_id) {
        const url = new URL(window.location.href);
        url.searchParams.set('click', card_id);
        window.location.href = url.toString();
    }
    </script>
    <div class='pyramide'>
    """

    for n, is_open in layout_structure:
        html += "<div class='reihe'>"
        for i in range(n):
            card = cards[card_id % len(cards)]
            taken = card_id in st.session_state.genommene_karten

            if taken:
                html += "<div class='karte verdeckt'>✓</div>"
            elif is_open:
                html += f"""
                <div class='karte offen' onclick="sendClick({card_id})">
                    <div class='produziert'>{card['effekt']['value']}× {card['effekt']['name']}</div>
                    <div class='kartenname'>{card['name']}</div>
                </div>
                """
            else:
                html += "<div class='karte verdeckt'>???</div>"

            card_id += 1
        html += "</div>"
    html += "</div>"

    components.html(html, height=740, scrolling=False)

    # 5. Klick-Verarbeitung über Query-Parameter
    params = st.query_params
    if "click" in params:
        try:
            clicked = int(params["click"])
            if clicked not in st.session_state.genommene_karten:
                eff = cards[clicked % len(cards)]["effekt"]
                st.session_state.ressourcen[st.session_state.spieler][eff["name"]] += eff["value"]
                st.session_state.genommene_karten.add(clicked)
                st.session_state.spieler = "Spieler 2" if st.session_state.spieler == "Spieler 1" else "Spieler 1"
            st.query_params.clear()
            st.rerun()
        except Exception as e:
            st.error(f"Fehler bei Klick: {e}")

def load_cards_from_json():
    path = Path(__file__).parent / "grundspiel_karten_zeitalter_1.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)
