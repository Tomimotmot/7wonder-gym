# === layout.py (Pyramidenlayout mit funktionierendem Click-Handling) ===

import streamlit as st
import json
from pathlib import Path
import streamlit.components.v1 as components

def render_layout():
    st.markdown("## 🃏 Zeitalter I – Kartenauslage")

    # === 1. Session-State initialisieren ===
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

    # === 2. Ressourcenübersicht anzeigen ===
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

    # === 3. Kartenlayout & Daten laden ===
    layout_structure = [2, 3, 4, 5, 6]
    sample_cards = load_cards_from_json()
    card_id = 0

    # === 4. Klickverarbeitung ===
    clicked_id = st.experimental_get_query_params().get("click", [None])[0]
    if clicked_id is not None:
        try:
            clicked_id = int(clicked_id)
            if clicked_id not in st.session_state.genommene_karten:
                card = sample_cards[clicked_id % len(sample_cards)]
                st.session_state.ressourcen[st.session_state.spieler][card['effekt']['name']] += card['effekt']['value']
                st.session_state.genommene_karten.add(clicked_id)
                st.session_state.spieler = "Spieler 2" if st.session_state.spieler == "Spieler 1" else "Spieler 1"
            st.experimental_set_query_params()
            st.rerun()
        except Exception as e:
            st.error(f"Fehler beim Klick: {e}")

    # === 5. HTML-Rendern ===
    html = """
    <style>
    .pyramide {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        margin-top: 20px;
    }
    .reihe {
        display: flex;
        justify-content: center;
        gap: 8px;
    }
    .karte {
        width: 80px;
        height: 100px;
        border-radius: 6px;
        padding: 4px;
        font-size: 10px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        text-align: center;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        cursor: pointer;
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
    <script>
    function sendClick(card_id) {
        const url = new URL(window.location);
        url.searchParams.set('click', card_id);
        window.location.href = url.toString();
    }
    </script>
    <div class='pyramide'>
    """

    for row_idx, cards_in_row in enumerate(layout_structure):
        html += "<div class='reihe'>"
        is_open_row = row_idx % 2 == 0

        for _ in range(cards_in_row):
            card = sample_cards[card_id % len(sample_cards)]
            is_taken = card_id in st.session_state.genommene_karten

            if is_taken:
                html += "<div class='karte verdeckt'>✓</div>"
            elif is_open_row:
                html += f"""
                <div class='karte offen' onclick=\"sendClick({card_id})\">
                    <div class='produziert'>{card['effekt']['value']}× {card['effekt']['name']}</div>
                    <div class='kartenname'>{card['name']}</div>
                </div>
                """
            else:
                html += "<div class='karte verdeckt'>???</div>"

            card_id += 1

        html += "</div>"
    html += "</div>"

    components.html(html, height=740, scrolling=False)

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
