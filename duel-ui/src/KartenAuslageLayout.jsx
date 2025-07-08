import React, { useEffect, useState } from "react";
import "./KartenAuslageLayout.css";

const KartenAuslageLayout = ({ layout }) => {
  const [kartenData, setKartenData] = useState([]);
  const [gezogen, setGezogen] = useState([]);
  const [ressourcenP1, setRessourcenP1] = useState([]);
  const [ressourcenP2, setRessourcenP2] = useState([]);
  const [spieler, setSpieler] = useState(1);
  const [lastReward, setLastReward] = useState(null);

  useEffect(() => {
    fetch("/grundspiel_karten_zeitalter_1.json")
      .then((response) => response.json())
      .then((data) => setKartenData(data));
  }, []);

  const istOffen = (rowIndex, colIndex) => {
    // Wenn es keine Zeile darunter gibt: immer offen
    if (rowIndex === layout.length - 1) return true;

    // Alle Karten darunter müssen gezogen worden sein
    const untereReihe = layout[rowIndex + 1];
    const unterLinks = layout[rowIndex + 1][colIndex] ?? null;
    const unterRechts = layout[rowIndex + 1][colIndex + 1] ?? null;

    return [unterLinks, unterRechts].every((idx) => idx == null || gezogen.includes(idx));
  };

  const handleCardClick = (cardIndex, rowIndex, colIndex) => {
    if (!istOffen(rowIndex, colIndex) || gezogen.includes(cardIndex)) return;

    const gezogeneKarte = kartenData[cardIndex];
    setGezogen((prev) => [...prev, cardIndex]);

    const res = gezogeneKarte?.produziert ?? "❌ nichts";
    setLastReward(`${res} (Spieler ${spieler})`);

    if (spieler === 1) {
      setRessourcenP1((prev) => [...prev, res]);
      setSpieler(2);
    } else {
      setRessourcenP2((prev) => [...prev, res]);
      setSpieler(1);
    }
  };

  return (
    <div className="karten-auslage">
      {layout.map((reihe, rowIndex) => (
        <div key={rowIndex} className="reihe">
          {reihe.map((cardIndex, colIndex) => {
            const card = kartenData[cardIndex];
            const offen = istOffen(rowIndex, colIndex);
            const istGezogen = gezogen.includes(cardIndex);

            return (
              <div
                key={`${rowIndex}-${colIndex}`}
                className={`karte ${offen ? "offen" : "verdeckt"} ${istGezogen ? "gezogen" : ""}`}
                onClick={() => handleCardClick(cardIndex, rowIndex, colIndex)}
              >
                {offen && card?.produziert && (
                  <div className="karte-produziert">{card.produziert.charAt(0)}</div>
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

      <div style={{ marginTop: "1.5rem" }}>
        <h3>Spieler 1 Ressourcen:</h3>
        <div>{ressourcenP1.join(", ") || "–"}</div>
        <h3>Spieler 2 Ressourcen:</h3>
        <div>{ressourcenP2.join(", ") || "–"}</div>
      </div>
    </div>
  );
};

export default KartenAuslageLayout;