import streamlit as st

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

    html = """
    <style>
    .pyramide { display: flex; flex-direction: column; align-items: center; gap: 4px; margin-top: 10px; }
    .reihe { display: flex; gap: 4px; }
    .karte {
        border: 1px solid #555;
        border-radius: 6px;
        padding: 4px 4px;
        min-width: 60px;
        min-height: 68px;
        text-align: center;
        font-size: 10px;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .produziert { font-size: 10px; font-weight: bold; padding-bottom: 2px; }
    .kartenname { font-size: 9px; font-style: italic; padding-top: 2px; }
    .offen { background-color: #fff; color: #000; }
    .verdeckt { background-color: #ccc; color: #ccc; }
    </style>
    """
    st.markdown(html, unsafe_allow_html=True)

    for row in st.session_state.auslage:
        cols = st.columns(len(row), gap="small")
        for col, card in zip(cols, row):
            with col:
                if card["genommen"]:
                    st.empty()
                elif card["offen"]:
                    if st.button(f"{card['effekt']['value']}× {card['effekt']['name']}\n{card['name']}", key=card["id"]):
                        st.session_state.ressourcen[st.session_state.spieler][card["effekt"]["name"]] += card["effekt"]["value"]
                        card["genommen"] = True
                        st.session_state.spieler = "Spieler 2" if st.session_state.spieler == "Spieler 1" else "Spieler 1"
                        st.experimental_rerun()
                else:
                    st.markdown('<div class="karte verdeckt"></div>', unsafe_allow_html=True)
