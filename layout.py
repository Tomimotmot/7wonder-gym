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

    # Kartenpyramide mit Button oder grauer Karte
    layout_structure = [2, 3, 4, 5, 6]
    sample_cards = load_cards_from_json()
    card_id = 0

    for row_idx, cards_in_row in enumerate(layout_structure):
        cols = st.columns(cards_in_row, gap="small")
        is_open_row = row_idx % 2 == 0  # Zeilen 0,2,4 offen

        for i in range(cards_in_row):
            card = sample_cards[card_id % len(sample_cards)]
            with cols[i]:
                if is_open_row:
                    st.markdown(
                        f"""
                        <div style='border:1px solid #444; border-radius:8px;
                                    height:90px; display:flex; flex-direction:column;
                                    justify-content:space-between; align-items:center;
                                    padding:4px; background-color:#fff; color:#000;'>
                            <form method="post">
                                <button name="click" value="{card_id}" type="submit" style='all:unset;cursor:pointer;width:100%;text-align:center;'>
                                    <div style='font-size:10px; font-weight:bold;'>{card['effekt']['value']}× {card['effekt']['name']}</div>
                                    <div style='font-size:9px; font-style:italic;'>{card['name']}</div>
                                </button>
                            </form>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        "<div style='height:90px; border:1px solid #444; border-radius:8px; background-color:#bbb;'></div>",
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
