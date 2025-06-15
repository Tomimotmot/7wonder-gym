import streamlit as st
from gamelogic import handle_card_click

def render_ressourcen():
    st.markdown("### Ressourcen")
    resourcen = ["Holz", "Lehm", "Stein", "Papyrus", "Glas"]
    table = "<table style='width:100%; text-align:center;'>"
    table += "<tr><th></th>" + "".join(f"<th>{r}</th>" for r in resourcen) + "</tr>"
    for spieler in ["Spieler 1", "Spieler 2"]:
        table += f"<tr><td><b>{spieler}</b></td>"
        for r in resourcen:
            val = st.session_state.ressourcen[spieler][r]
            table += f"<td>{val}</td>"
        table += "</tr>"
    table += "</table>"
    st.markdown(table, unsafe_allow_html=True)

def render_layout():
    st.markdown(f"## 🃏 Zeitalter I – Auslage ({st.session_state.spieler} ist am Zug)")

    for row in st.session_state.auslage:
        # Dynamische Einrückung (Padding) über leere Spalten links/rechts
        total = 6  # maximale Kartenanzahl pro Zeile
        spacer = (total - len(row)) // 2
        cols = st.columns(total)

        for i in range(total):
            with cols[i]:
                if spacer > 0:
                    spacer -= 1
                    st.empty()
                else:
                    if row:
                        card = row.pop(0)
                        if card["genommen"]:
                            st.empty()
                        elif card["offen"]:
                            if st.button(f"{card['effekt']['value']}× {card['effekt']['name']}\n{card['name']}", key=card["id"]):
                                st.session_state.ressourcen[st.session_state.spieler][card["effekt"]["name"]] += card["effekt"]["value"]
                                card["genommen"] = True
                                st.session_state.spieler = "Spieler 2" if st.session_state.spieler == "Spieler 1" else "Spieler 1"
                                st.experimental_rerun()
                        else:
                            st.markdown("<div style='width:70px;height:68px;background-color:#ccc;border-radius:5px;'></div>", unsafe_allow_html=True)

    # POST-Auswertung für Button-Click
    if "click" in st.session_state:
        handle_card_click(int(st.session_state.click))
