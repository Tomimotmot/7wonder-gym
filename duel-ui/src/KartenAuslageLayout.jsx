import React, { useEffect, useState } from "react";
import "./KartenAuslageLayout.css";

const KartenAuslageLayout = ({ layout, offenLayout }) => {
  const [kartenData, setKartenData] = useState([]);
  const [gezogen, setGezogen] = useState([]);
  const [lastReward, setLastReward] = useState(null);

  useEffect(() => {
    fetch("/grundspiel_karten_zeitalter_1.json")
      .then((response) => response.json())
      .then((data) => setKartenData(data));
  }, []);

  const handleCardClick = (cardIndex, offen) => {
    if (!offen || gezogen.includes(cardIndex)) return;
    const gezogeneKarte = kartenData[cardIndex];
    setGezogen([...gezogen, cardIndex]);
    setLastReward(gezogeneKarte.produziert || "❌ nichts");
    console.log("Gezogen:", gezogeneKarte.name, "→", gezogeneKarte.produziert);
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
                {/* Oben: Anfangsbuchstabe vom "produziert"-Wert */}
                {offen && card?.produziert && (
                  <div className="karte-produziert">
                    {card.produziert.charAt(0)}
                  </div>
                )}

                {/* Unten: Name immer sichtbar */}
                <div className="kartenname">
                  {card?.name ?? ""}
                </div>
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
    </div>
  );
};

export default KartenAuslageLayout;
