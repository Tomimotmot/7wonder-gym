// src/KartenAuslageLayout.jsx
import React, { useEffect, useState } from "react";
import "./KartenAuslageLayout.css";

const KartenAuslageLayout = ({ layout, offenLayout }) => {
  const [kartenData, setKartenData] = useState([]);

  useEffect(() => {
    fetch("/grundspiel_karten_zeitalter_1.json")
      .then((response) => response.json())
      .then((data) => setKartenData(data));
  }, []);

  return (
    <div className="karten-auslage">
      {layout.map((reihe, rowIndex) => (
        <div key={rowIndex} className="reihe">
          {reihe.map((cardIndex, colIndex) => {
            const card = kartenData[cardIndex];
            const offen = offenLayout?.[rowIndex]?.[colIndex] === 1;

            return (
              <div
                key={`${rowIndex}-${colIndex}`}
                className={`karte ${offen ? "offen" : "verdeckt"}`}
              >
                {/* Oben: Anfangsbuchstabe vom "produziert"-Wert */}
                <div className="karte-produziert">
                  {offen && card?.produziert ? card.produziert.charAt(0) : ""}
                </div>

                {/* Unten: Name immer sichtbar */}
                <div className="kartenname">
                  {card?.name ?? ""}
                </div>
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
};

export default KartenAuslageLayout;
