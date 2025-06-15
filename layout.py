# layout.py – Pyramidenlayout mit klickbaren Karten per st.form_submit_button (stabil)

import streamlit as st
import json
from pathlib import Path

def render_layout():
    st.markdown("## 🃏 Zeitalter I – Kartenauslage")

    # 1. Session-Init
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

    if "klick_id" not in st.session_state:
        st.session_state.klick_id = -1

    # 2. Klick-Auswertung (falls vorhanden)
    if st.session_state.klick_id != -1:
        card_id = st.session_state.klick_id
        cards = load_cards_from_json()
        if card_id not in st.session_state.genommene_karten:
            effekt = cards[card_id % len(cards)]["effekt"]
            st.session_state.ressourcen[st.session_state.spieler][effekt["name"]] += effekt["value"]
            st.session_state.genommene_karten.add(card_id)
            st.session_state.spieler = "Spieler 2" if st.session_state.spieler == "Spieler 1" else "Spieler 1"
        st.session_state.klick_id = -1
        st.rerun()

    # 3. Ressourcenanzeige
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

    # 4. Pyramidenstruktur 2–3–4–5–6 (abwechselnd offen/verdeckt)
    layout_structure = [(2, True), (3, False), (4, True), (5, False), (6, True)]
    cards = load_cards_from_json()
    card_id = 0

    st.markdown("""
    <style>
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
    }
    .offen { background: #fff; color: #000; border: 1px solid #444; }
    .verdeckt { background: #bbb; color: #bbb; border: 1px solid #999; }
    .produziert { font-weight: bold; font-size: 10px; }
    .kartenname { font-style: italic; font-size: 9px; }
    </style>
    """, unsafe_allow_html=True)

    with st.form("pyramidenform"):
        for n, is_open in layout_structure:
            cols = st.columns(n)
            for i in range(n):
                card = cards[card_id % len(cards)]
                taken = card_id in st.session_state.genommene_karten

                with cols[i]:
                    if taken:
                        st.markdown(f"<div class='karte verdeckt'>✓</div>", unsafe_allow_html=True)
                    elif is_open:
                        btn = st.form_submit_button(f"{card['effekt']['value']}× {card['effekt']['name']}\n{card['name']}", key=f"card_{card_id}")
                        if btn:
                            st.session_state.klick_id = card_id
                    else:
                        st.markdown("<div class='karte verdeckt'>???</div>", unsafe_allow_html=True)

                card_id += 1

        # Dummy-Button erforderlich für Streamlit-Formularsystem
        st.form_submit_button("Bestätigen")

def load_cards_from_json():
    path = Path(__file__).parent / "grundspiel_karten_zeitalter_1.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)
