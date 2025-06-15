import streamlit as st
import streamlit.components.v1 as components
import json
from pathlib import Path

def render_layout():
    st.markdown("## 🃏 Zeitalter I – Kartenauslage")

    layout_structure = [2, 3, 4, 5, 6]
    sample_cards = load_cards_from_json()
    cards_by_row = []
    card_id = 0

    for row_idx, cards_in_row in enumerate(layout_structure):
        row = []
        is_open_row = row_idx % 2 == 0  # Offen in Reihe 0, 2, 4
        for _ in range(cards_in_row):
            card = sample_cards[card_id % len(sample_cards)]
            effekt_text = f'{card["effekt"]["value"]}× {card["effekt"]["name"]}'
            row.append({
                "name": card["name"],
                "effekt": effekt_text,
                "offen": is_open_row
            })
            card_id += 1
        cards_by_row.append(row)

    # HTML & CSS
    html = """
    <style>
    .pyramide {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 3px;
        margin-top: 10px;
    }
    .reihe {
        display: flex;
        gap: 3px;
    }
    .karte {
        border: 1px solid #555;
        border-radius: 5px;
        padding: 4px 3px;
        min-width: 60px;
        min-height: 70px;
        text-align: center;
        font-size: 10.5px;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
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
        color: #333;
    }
    </style>
    <div class="pyramide">
    """

    for row in cards_by_row:
        html += '<div class="reihe">'
        for card in row:
            status = "offen" if card["offen"] else "verdeckt"
            if card["offen"]:
                content = f'<div class="produziert">{card["effekt"]}</div><div class="kartenname">{card["name"]}</div>'
            else:
                content = '<div class="produziert">???</div><div class="kartenname">???</div>'
            html += f'<div class="karte {status}">{content}</div>'
        html += '</div>'
    html += '</div>'

    components.html(html, height=520, scrolling=False)


def load_cards_from_json():
    path = Path(__file__).parent / "zeitalter1_offiziell.json"
    with open(path, encoding="utf-8") as f:
        cards = json.load(f)

    for i, card in enumerate(cards):
        if "name" not in card or "effekt" not in card:
            raise ValueError(f"Karte {i+1} fehlt 'name' oder 'effekt'")
        if "name" not in card["effekt"] or "value" not in card["effekt"]:
            raise ValueError(f"Karte {i+1} hat unvollständigen Effekt")

    return cards