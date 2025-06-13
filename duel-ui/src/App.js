// src/App.js
import React from 'react';
import KartenAuslageLayout from './KartenAuslageLayout';

const kartenIndexLayout = [
  [0, 1],
  [2, 3, 4],
  [5, 6, 7, 8],
  [9, 10, 11, 12, 13],
  [14, 15, 16, 17, 18, 19],
];

const offenLayout = [
  [1, 1],
  [0, 0, 0],
  [1, 1, 1, 1],
  [0, 0, 0, 0, 0],
  [1, 1, 1, 1, 1, 1],
];

function App() {
  return (
    <div className="App">
      <h2>Zeitalter I</h2>
      <KartenAuslageLayout layout={kartenIndexLayout} offenLayout={offenLayout} />
    </div>
  );
}

export default App;
