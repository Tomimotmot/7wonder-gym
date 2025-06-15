import streamlit as st
import json
from pathlib import Path

def render_layout():
    st.markdown("## 🃏 Zeitalter I – Kartenauslage")

    # Session State initialisieren
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

    # Ressourcenübersicht
    resourcen = ["Holz", "Lehm", "Stein", "Papyrus", "Glas"]
    st.markdown(f"### Ressourcenübersicht (aktuell: {st.session_state.spieler})")
    res_table = "<table style='width: 100%; text-align: center; border-collapse: collapse;'>"
    res_table += "<tr><th></th>" + "".join(f"<th>{res}</th>" for res in resourcen) + "</tr>"
    for spieler in ["Spieler 1", "Spieler 2"]:
        res_table += f"<tr><td><b>{spieler}</b></td>" + "".join(
            f"<td>{st.session_state.ressourcen[spieler][res]}</td>" for res in resourcen
        ) + "</tr>"
    res_table += "</table>"
    st.markdown(res_table, unsafe_allow_html=True)

    # Kartenpyramide
    layout_structure = [2, 3, 4, 5, 6]
    sample_cards = load_cards_from_json()
    card_id = 0

    for row_idx, cards_in_row in enumerate(layout_structure):
        cols = st.columns(cards_in_row, gap="small")
        is_open_row = row_idx % 2 == 0

        for col in cols:
            card = sample_cards[card_id % len(sample_cards)]
            is_taken = card_id in st.session_state.genommene_karten

            if is_taken:
                col.markdown(
                    "<div style='background-color: #ddd; height: 100px; border-radius: 6px; text-align: center;'>✓</div>",
                    unsafe_allow_html=True
                )
            elif is_open_row:
                if col.button(f"{card['effekt']['value']}× {card['effekt']['name']}\n{card['name']}", key=f"card_{card_id}"):
                    st.session_state.ressourcen[st.session_state.spieler][card['effekt']['name']] += card['effekt']['value']
                    st.session_state.genommene_karten.add(card_id)
                    st.session_state.spieler = "Spieler 2" if st.session_state.spieler == "Spieler 1" else "Spieler 1"
                    st.rerun()
            else:
                col.markdown(
                    "<div style='background-color: #bbb; height: 100px; border-radius: 6px;'></div>",
                    unsafe_allow_html=True
                )
            card_id += 1

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
