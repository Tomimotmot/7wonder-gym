import React, { useEffect, useState } from "react";
import "./KartenAuslageLayout.css";

const KartenAuslageLayout = ({ layout, offenLayout }) => {
  const [kartenData, setKartenData] = useState([]);
  const [gezogen, setGezogen] = useState([]);
  const [lastReward, setLastReward] = useState(null);
  const [spielerAmZug, setSpielerAmZug] = useState(1);
  const [ressourcenP1, setRessourcenP1] = useState([]);
  const [ressourcenP2, setRessourcenP2] = useState([]);

  useEffect(() => {
    fetch("/grundspiel_karten_zeitalter_1.json")
      .then((response) => response.json())
      .then((data) => setKartenData(data));
  }, []);

  const handleCardClick = (cardIndex, offen) => {
    if (!offen || gezogen.includes(cardIndex)) return;

    const gezogeneKarte = kartenData[cardIndex];
    setGezogen([...gezogen, cardIndex]);

    // Belohnung zuweisen
    const reward = gezogeneKarte.produziert || "❌ nichts";
    setLastReward(`${reward} (Spieler ${spielerAmZug})`);

    if (gezogeneKarte.produziert) {
      if (spielerAmZug === 1) {
        setRessourcenP1((prev) => [...prev, gezogeneKarte.produziert]);
      } else {
        setRessourcenP2((prev) => [...prev, gezogeneKarte.produziert]);
      }
    }

    // Nächster Spieler ist am Zug
    setSpielerAmZug(spielerAmZug === 1 ? 2 : 1);
  };

  return (
    <div className="karten-auslage">
      {layout.map((reihe, rowIndex) => (
        <div key={rowIndex} className="reihe">
          {reihe.map((cardIndex, colIndex) => {
            const card = kartenData[cardIndex];
            const offen = offenLayout?.[rowIndex]?.[colIndex] === 1;
            const istGezogen = gezogen.includes(cardIndex);

            return (
              <div
                key={`${rowIndex}-${colIndex}`}
                className={`karte ${offen ? "offen" : "verdeckt"} ${istGezogen ? "gezogen" : ""}`}
                onClick={() => handleCardClick(cardIndex, offen)}
              >
                {offen && card?.produziert && (
                  <div className="karte-produziert">
                    {card.produziert.charAt(0)}
                  </div>
                )}
                <div className="kartenname">{card?.name ?? ""}</div>
              </div>
            );
          })}
        </div>
      ))}

      {lastReward && (
        <div style={{ marginTop: "1rem", fontWeight: "bold" }}>
          Letzter Reward: {lastReward}
        </div>
      )}

      <div style={{ marginTop: "2rem" }}>
        <h3>Spieler 1 Ressourcen:</h3>
        <p>{ressourcenP1.length > 0 ? ressourcenP1.join(", ") : "–"}</p>

        <h3>Spieler 2 Ressourcen:</h3>
        <p>{ressourcenP2.length > 0 ? ressourcenP2.join(", ") : "–"}</p>
      </div>
    </div>
  );
};

export default KartenAuslageLayout;