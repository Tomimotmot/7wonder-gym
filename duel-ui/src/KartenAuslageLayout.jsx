import React, { useEffect, useState } from "react";
import "./KartenAuslageLayout.css";

const KartenAuslageLayout = ({ layout, offenLayout }) => {
  const [kartenData, setKartenData] = useState([]);
  const [gezogen, setGezogen] = useState([]);
  const [lastReward, setLastReward] = useState(null);
  const [activePlayer, setActivePlayer] = useState(1);

  const [player1Ressourcen, setPlayer1Ressourcen] = useState([]);
  const [player2Ressourcen, setPlayer2Ressourcen] = useState([]);

  useEffect(() => {
    fetch("/grundspiel_karten_zeitalter_1.json")
      .then((response) => response.json())
      .then((data) => setKartenData(data));
  }, []);

  const handleCardClick = (cardIndex, offen) => {
    if (!offen || gezogen.includes(cardIndex)) return;

    const gezogeneKarte = kartenData[cardIndex];
    setGezogen([...gezogen, cardIndex]);
    setLastReward(`${gezogeneKarte.produziert || "❌ nichts"} (Spieler ${activePlayer})`);

    if (activePlayer === 1) {
      setPlayer1Ressourcen([...player1Ressourcen, gezogeneKarte.produziert]);
      setActivePlayer(2);
    } else {
      setPlayer2Ressourcen([...player2Ressourcen, gezogeneKarte.produziert]);
      setActivePlayer(1);
    }
  };

  return (
    <div className="karten-auslage">
      <h2>Aktiver Spieler: Spieler {activePlayer}</h2>

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
                <div className="kartenname">
                  {card?.name ?? ""}
                </div>
              </div>
            );
          })}
        </div>
      ))}

      {lastReward && (
        <div className="belohnung">Letzter Reward: {lastReward}</div>
      )}

      <div className="spieler-info">
        <h3>Spieler 1 Ressourcen:</h3>
        <p>{player1Ressourcen.filter(Boolean).join(", ") || "–"}</p>
        <h3>Spieler 2 Ressourcen:</h3>
        <p>{player2Ressourcen.filter(Boolean).join(", ") || "–"}</p>
      </div>
    </div>
  );
};

export default KartenAuslageLayout;