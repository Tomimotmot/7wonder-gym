# === layout.py (Pyramidenlayout im echten Spielstil, statisch) ===

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

    # Kartenpyramide mit echtem Versatz-Layout (Zeilen mit Einrückung)
    layout_structure = [2, 3, 4, 5, 6]
    sample_cards = load_cards_from_json()
    card_id = 0

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
        justify-content: center;
        gap: 6px;
    }
    .reihe:nth-child(1) { margin-left: 90px; }
    .reihe:nth-child(2) { margin-left: 65px; }
    .reihe:nth-child(3) { margin-left: 40px; }
    .reihe:nth-child(4) { margin-left: 20px; }
    .reihe:nth-child(5) { margin-left: 0px; }

    .karte {
        width: 60px;
        height: 75px;
        border-radius: 6px;
        padding: 4px;
        font-size: 10px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        text-align: center;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    .offen {
        background-color: #fff;
        color: #000;
        border: 1px solid #444;
    }
    .verdeckt {
        background-color: #bbb;
        color: #bbb;
        border: 1px solid #888;
    }
    .produziert {
        font-weight: bold;
        font-size: 10px;
    }
    .kartenname {
        font-size: 9px;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

    html = "<div class='pyramide'>"
    for row_idx, cards_in_row in enumerate(layout_structure):
        html += "<div class='reihe'>"
        is_open_row = row_idx % 2 == 0
        for _ in range(cards_in_row):
            card = sample_cards[card_id % len(sample_cards)]
            if is_open_row:
                html += f"""
                <div class='karte offen'>
                    <div class='produziert'>{card['effekt']['value']}× {card['effekt']['name']}</div>
                    <div class='kartenname'>{card['name']}</div>
                </div>
                """
            else:
                html += "<div class='karte verdeckt'>???</div>"
            card_id += 1
        html += "</div>"
    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)



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
