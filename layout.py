import streamlit as st
import json
from pathlib import Path

def render_layout():
    st.markdown("## 🃏 Zeitalter I – Kartenauslage")

    # Ressourcenübersicht (statisch)
    resourcen = ["Holz", "Lehm", "Stein", "Papyrus", "Glas"]
    spieler_ressourcen = {
        "Spieler 1": {res: 0 for res in resourcen},
        "Spieler 2": {res: 0 for res in resourcen}
    }

    st.markdown("### Ressourcenübersicht")
    res_table = "<table style='width: 100%; text-align: center; border-collapse: collapse;'>"
    res_table += "<tr><th></th>" + "".join(f"<th>{res}</th>" for res in resourcen) + "</tr>"
    for spieler in ["Spieler 1", "Spieler 2"]:
        res_table += f"<tr><td><b>{spieler}</b></td>" + "".join(
            f"<td>{spieler_ressourcen[spieler][res]}</td>" for res in resourcen
        ) + "</tr>"
    res_table += "</table>"
    st.markdown(res_table, unsafe_allow_html=True)

    # Kartenpyramide mit Buttons
    layout_structure = [2, 3, 4, 5, 6]
    sample_cards = load_cards_from_json()
    card_id = 0

    for row_idx, cards_in_row in enumerate(layout_structure):
        cols = st.columns(cards_in_row, gap="small")
        is_open_row = row_idx % 2 == 0
        for col in cols:
            card = sample_cards[card_id % len(sample_cards)]
            if is_open_row:
                if col.button(f"{card['effekt']['value']}× {card['effekt']['name']}\n{card['name']}", key=f"card_{card_id}"):
                    st.success(f"Karte {card['name']} geklickt")
            else:
                col.markdown(
                    "<div style='background-color: #ccc; height: 85px; border-radius: 8px;'></div>",
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
