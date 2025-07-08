import React, { useEffect, useState } from "react";
import "./KartenAuslageLayout.css";

const KartenAuslageLayout = ({ layout }) => {
  const [kartenData, setKartenData] = useState([]);
  const [gezogen, setGezogen] = useState([]);
  const [spieler, setSpieler] = useState(1);
  const [ressourcen, setRessourcen] = useState({ 1: {}, 2: {} });
  const [lastReward, setLastReward] = useState(null);

  useEffect(() => {
    fetch("/grundspiel_karten_zeitalter_1.json")
      .then((res) => res.json())
      .then((data) => setKartenData(data));
  }, []);

  const handleCardClick = (cardIndex, offen) => {
    if (!offen || gezogen.includes(cardIndex)) return;

    const gezogeneKarte = kartenData[cardIndex];
    const produziert = gezogeneKarte?.produziert || "❌ nichts";

    // Update Ressourcen des aktuellen Spielers
    const neuerStand = { ...ressourcen[spieler] };
    if (produziert !== "❌ nichts") {
      neuerStand[produziert] = (neuerStand[produziert] || 0) + 1;
    }

    setRessourcen({
      ...ressourcen,
      [spieler]: neuerStand,
    });

    // Karte als gezogen markieren
    setGezogen([...gezogen, cardIndex]);

    // Letzten Reward anzeigen
    setLastReward(`${produziert} (Spieler ${spieler})`);

    // Spieler wechseln (1 <-> 2)
    setSpieler(spieler === 1 ? 2 : 1);
  };

  const istKarteOffen = (rowIndex, colIndex, cardIndex) => {
    if (gezogen.includes(cardIndex)) return false;
    if (rowIndex === layout.length - 1) return true;

    const untenLinks = layout?.[rowIndex + 1]?.[colIndex];
    const untenRechts = layout?.[rowIndex + 1]?.[colIndex + 1];

    const beideDarunterGezogen =
      (!untenLinks || gezogen.includes(untenLinks)) &&
      (!untenRechts || gezogen.includes(untenRechts));

    return beideDarunterGezogen;
  };

  return (
    <div className="karten-auslage">
      {layout.map((reihe, rowIndex) => (
        <div key={rowIndex} className="reihe">
          {reihe.map((cardIndex, colIndex) => {
            const card = kartenData[cardIndex];
            const offen = istKarteOffen(rowIndex, colIndex, cardIndex);
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
        <div style={{ marginTop: "1rem", fontWeight: "bold", color: "black" }}>
          Letzter Reward: {lastReward}
        </div>
      )}

      <div style={{ marginTop: "1.5rem", textAlign: "left" }}>
        <h3>Spieler 1 Ressourcen:</h3>
        <p>{formatRessourcen(ressourcen[1])}</p>
        <h3>Spieler 2 Ressourcen:</h3>
        <p>{formatRessourcen(ressourcen[2])}</p>
      </div>
    </div>
  );
};

// Hilfsfunktion zur Anzeige der Ressourcen
function formatRessourcen(obj) {
  if (!obj || Object.keys(obj).length === 0) return "–";
  return Object.entries(obj)
    .map(([rohstoff, anzahl]) => `${rohstoff}: ${anzahl}`)
    .join(", ");
}

export default KartenAuslageLayout;