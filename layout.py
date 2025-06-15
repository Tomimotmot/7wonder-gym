import streamlit as st
import json
from pathlib import Path

def render_layout():
    st.markdown("## 🃏 Zeitalter I – Kartenauslage")

    # Ressourcenübersicht
    resourcen = ["Holz", "Lehm", "Stein", "Papyrus", "Glas"]
    st.markdown("### Ressourcenübersicht")
    res_table = "<table style='width: 100%; text-align: center;'>"
    res_table += "<tr><th></th>" + "".join(f"<th>{r}</th>" for r in resourcen) + "</tr>"
    for sp in ["Spieler 1", "Spieler 2"]:
        res_table += f"<tr><td><b>{sp}</b></td>" + "".join(f"<td>0</td>" for _ in resourcen) + "</tr>"
    res_table += "</table>"
    st.markdown(res_table, unsafe_allow_html=True)

    # Karten laden
    cards = load_cards_from_json()
    layout_structure = [2, 3, 4, 5, 6]
    card_index = 0

    st.markdown("""
    <style>
    .pyramide {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 20px;
        gap: 4px;
    }
    .reihe {
        display: grid;
        grid-template-columns: repeat(11, 1fr);
        gap: 6px;
    }
    .karte {
        width: 64px;
        height: 80px;
        border-radius: 6px;
        font-size: 10px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        text-align: center;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        padding: 4px;
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
    .produziert { font-weight: bold; font-size: 10px; }
    .kartenname { font-size: 9px; font-style: italic; }
    .leer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

    html = "<div class='pyramide'>"
    for i, anzahl in enumerate(layout_structure):
        html += "<div class='reihe'>"
        leer = (11 - anzahl) // 2
        html += "<div class='karte leer'></div>" * leer
        for _ in range(anzahl):
            card = cards[card_index % len(cards)]
            if i % 2 == 0:
                html += f"""
                <div class='karte offen'>
                    <div class='produziert'>{card['effekt']['value']}× {card['effekt']['name']}</div>
                    <div class='kartenname'>{card['name']}</div>
                </div>
                """
            else:
                html += "<div class='karte verdeckt'>???</div>"
            card_index += 1
        html += "<div class='karte leer'></div>" * leer
        html += "</div>"
    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)


def load_cards_from_json():
    path = Path(__file__).parent / "grundspiel_karten_zeitalter_1.json"
    with open(path, encoding="utf-8") as f:
        cards = json.load(f)
    return cards
