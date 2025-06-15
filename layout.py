# layout.py — stabiles Pyramidenlayout mit Click-Handling über versteckte Form

import streamlit as st
import json
from pathlib import Path

def render_layout():
    st.markdown("## 🃏 Zeitalter I – Kartenauslage")

    # 1. Session-Initialisierung
    if "spieler" not in st.session_state:
        st.session_state.spieler = "Spieler 1"

    if "ressourcen" not in st.session_state:
        res = ["Holz", "Lehm", "Stein", "Papyrus", "Glas"]
        st.session_state.ressourcen = {
            "Spieler 1": {r: 0 for r in res},
            "Spieler 2": {r: 0 for r in res},
        }

    if "genommene_karten" not in st.session_state:
        st.session_state.genommene_karten = set()

    # 2. Klick-Auswertung (über Form)
    if "klick_id" in st.session_state and st.session_state.klick_id != -1:
        cid = st.session_state.klick_id
        cards = load_cards_from_json()
        if cid not in st.session_state.genommene_karten:
            effekt = cards[cid % len(cards)]["effekt"]
            st.session_state.ressourcen[st.session_state.spieler][effekt["name"]] += effekt["value"]
            st.session_state.genommene_karten.add(cid)
            st.session_state.spieler = "Spieler 2" if st.session_state.spieler == "Spieler 1" else "Spieler 1"
        st.session_state.klick_id = -1
        st.experimental_rerun()

    # 3. Ressourcen-Tabelle
    resourcen = ["Holz", "Lehm", "Stein", "Papyrus", "Glas"]
    st.markdown(f"### Ressourcenübersicht ({st.session_state.spieler} ist am Zug)")
    st.markdown("<style>th, td {padding: 4px 8px;}</style>", unsafe_allow_html=True)
    table = "<table style='width:100%; text-align:center;'><tr><th></th>"
    table += "".join(f"<th>{r}</th>" for r in resourcen) + "</tr>"
    for sp in ["Spieler 1", "Spieler 2"]:
        table += f"<tr><td><b>{sp}</b></td>" + "".join(
            f"<td>{st.session_state.ressourcen[sp][r]}</td>" for r in resourcen
        ) + "</tr>"
    table += "</table>"
    st.markdown(table, unsafe_allow_html=True)

    # 4. Kartenaufbau
    cards = load_cards_from_json()
    layout_structure = [(2, True), (3, False), (4, True), (5, False), (6, True)]
    card_id = 0

    # 5. HTML + Form
    st.markdown("""
    <style>
    .pyramide { display: flex; flex-direction: column; align-items: center; gap: 10px; margin-top: 20px; }
    .reihe { display: flex; gap: 8px; justify-content: center; }
    .karte {
        width: 80px; height: 100px; border-radius: 6px;
        display: flex; flex-direction: column; justify-content: space-between;
        text-align: center; font-size: 10px; cursor: pointer;
        padding: 4px; box-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    .offen { background: #fff; border: 1px solid #444; color: #000; }
    .verdeckt { background: #bbb; border: 1px solid #999; color: #bbb; }
    .produziert { font-weight: bold; font-size: 10px; }
    .kartenname { font-style: italic; font-size: 9px; }
    </style>
    """, unsafe_allow_html=True)

    with st.form("kartenform"):
        for anzahl, offen in layout_structure:
            st.markdown("<div class='reihe'>", unsafe_allow_html=True)
            cols = st.columns(anzahl)
            for i in range(anzahl):
                card = cards[card_id % len(cards)]
                genommen = card_id in st.session_state.genommene_karten
                if genommen:
                    with cols[i]:
                        st.markdown("<div class='karte verdeckt'>✓</div>", unsafe_allow_html=True)
                elif offen:
                    with cols[i]:
                        if st.form_submit_button(f"{card['effekt']['value']}× {card['effekt']['name']}\n{card['name']}", key=f"klick_{card_id}"):
                            st.session_state.klick_id = card_id
                else:
                    with cols[i]:
                        st.markdown("<div class='karte verdeckt'>???</div>", unsafe_allow_html=True)
                card_id += 1
            st.markdown("</div>", unsafe_allow_html=True)

        # Submit-Button nur nötig, wenn keine Karte geklickt wird
        st.form_submit_button("🕹️ Weiter", use_container_width=True)

def load_cards_from_json():
    path = Path(__file__).parent / "grundspiel_karten_zeitalter_1.json"
    with open(path, encoding="utf-8") as f:
        cards = json.load(f)

    for i, card in enumerate(cards):
        if "name" not in card or "effekt" not in card:
            raise ValueError(f"Karte {i+1} fehlt 'name' oder 'effekt'")
        if "name" not in card["effekt"] or "value" not in card["effekt"]:
            raise ValueError(f"Karte {i+1} hat unvollständigen Effekt")

    return cards
