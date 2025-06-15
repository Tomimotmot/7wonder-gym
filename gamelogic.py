import streamlit as st
import json
from pathlib import Path

def load_cards_from_json():
    path = Path(__file__).parent / "grundspiel_karten_zeitalter_1.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def init_game():
    if "spieler" not in st.session_state:
        st.session_state.spieler = "Spieler 1"
    if "ressourcen" not in st.session_state:
        resourcen = ["Holz", "Lehm", "Stein", "Papyrus", "Glas"]
        st.session_state.ressourcen = {
            "Spieler 1": {r: 0 for r in resourcen},
            "Spieler 2": {r: 0 for r in resourcen}
        }
    if "auslage" not in st.session_state:
        structure = [2, 3, 4, 5, 6]
        cards = load_cards_from_json()
        auslage = []
        index = 0
        for row_idx, count in enumerate(structure):
            row = []
            is_open = row_idx % 2 == 0
            for _ in range(count):
                card = cards[index]
                row.append({
                    "id": index,
                    "name": card["name"],
                    "effekt": card["effekt"],
                    "offen": is_open,
                    "genommen": False
                })
                index += 1
            auslage.append(row)
        st.session_state.auslage = auslage

def handle_card_click(card_id):
    for row in st.session_state.auslage:
        for card in row:
            if card["id"] == card_id and not card["genommen"] and card["offen"]:
                effekt = card["effekt"]
                st.session_state.ressourcen[st.session_state.spieler][effekt["name"]] += effekt["value"]
                card["genommen"] = True
                st.session_state.spieler = "Spieler 2" if st.session_state.spieler == "Spieler 1" else "Spieler 1"
                st.experimental_rerun()
