import streamlit as st
import streamlit.components.v1 as components

def render_layout():
    st.markdown("## 🃏 Zeitalter I – Kartenauslage")

    # Definiere Struktur: 2–3–4–5–6 Karten (oben nach unten)
    layout_structure = [2, 3, 4, 5, 6]
    total_cards = sum(layout_structure)
    card_id = 0
    cards_by_row = []

    # Sichtbarkeitslogik + Kartenaufbau
    for row_idx, cards_in_row in enumerate(layout_structure):
        row = []
        for col in range(cards_in_row):
            is_open = calculate_visibility(row_idx, col, layout_structure)
            row.append({
                "id": card_id,
                "name": f"Karte {card_id + 1}",
                "ressource": "🃏",
                "is_open": is_open
            })
            card_id += 1
        cards_by_row.append(row)

    # HTML/CSS + Kartenanzeige
    html = """
    <style>
    .pyramide {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 6px;
        margin-top: 10px;
    }
    .reihe {
        display: flex;
        gap: 6px;
    }
    .karte {
        background-color: #f0f0f0;
        border: 1px solid #555;
        border-radius: 8px;
        padding: 6px;
        min-width: 60px;
        min-height: 70px;
        text-align: center;
        font-size: 12px;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    .verdeckt {
        background-color: #aaa;
        color: #333;
    }
    </style>
    <div class="pyramide">
    """
    for row in cards_by_row:
        html += '<div class="reihe">'
        for card in row:
            cls = "karte"
            if not card["is_open"]:
                cls += " verdeckt"
                content = "<div>🕳</div><div>???</div>"
            else:
                content = f"<div>{card['ressource']}</div><div>{card['name']}</div>"
            html += f'<div class="{cls}">{content}</div>'
        html += '</div>'
    html += '</div>'

    components.html(html, height=600, scrolling=False)

def calculate_visibility(row_idx, col_idx, layout_structure):
    """
    Sichtbarkeitslogik:
    Eine Karte ist offen, wenn sie keine Karte mehr blockiert – d.h.
    sie liegt in der untersten Reihe oder hat keine Karte mehr direkt darauf.
    """
    if row_idx == len(layout_structure) - 1:
        return True  # Unterste Reihe ist immer offen

    below_count = layout_structure[row_idx + 1]
    offset = (below_count - layout_structure[row_idx]) // 2
    left = col_idx + offset
    right = left + 1
    return right >= below_count  # Wenn rechts kein Blocker mehr da ist