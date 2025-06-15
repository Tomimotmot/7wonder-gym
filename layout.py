import streamlit as st
import streamlit.components.v1 as components

def render_layout():
    st.markdown("## 🃏 Zeitalter I – Kartenauslage")

    layout_structure = [2, 3, 4, 5, 6]
    card_id = 1
    cards_by_row = []

    for row_idx, cards_in_row in enumerate(layout_structure):
        row = []
        is_open_row = row_idx % 2 == 0  # 0, 2, 4 = offen
        for _ in range(cards_in_row):
            row.append({
                "id": card_id,
                "name": f"Karte {card_id}",
                "ressource": "🃏",
                "is_open": is_open_row
            })
            card_id += 1
        cards_by_row.append(row)

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
        padding: 3px;
        min-width: 42px;
        min-height: 50px;
        text-align: center;
        font-size: 10px;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
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
            status = "offen" if card["is_open"] else "verdeckt"
            content = f"<div>{card['ressource']}</div><div>{card['name'] if card['is_open'] else '???'}</div>"
            html += f'<div class="karte {status}">{content}</div>'
        html += '</div>'
    html += '</div>'

    components.html(html, height=520, scrolling=False)