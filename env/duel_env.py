import os
import pandas as pd
import numpy as np
import random
import logging
from gym import Env, spaces

# Logging konfigurieren (einmalig)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DuelResourceEnv(Env):
    def __init__(self, csv_path=None, verbose=False):
        super().__init__()
        self.verbose = verbose

        # Pfad zur CSV
        if csv_path is None:
            csv_path = os.getenv("DUEL_CSV")
            if csv_path is None:
                base = os.path.dirname(__file__)
                csv_path = os.path.join(base, "..", "data", "grundspiel_karten_zeitalter_1.csv")

        self.card_data = pd.read_csv(csv_path).to_dict("records")
        self.num_cards = len(self.card_data)
        self.structure = [2, 3, 4, 5, 6]
        self.reset()

        self.action_space = spaces.Discrete(self.num_cards)
        self.observation_space = spaces.MultiBinary(self.num_cards)

    def reset(self):
        self.card_indices = list(range(self.num_cards))
        random.shuffle(self.card_indices)
        self.collected_indices = []
        self.done = False
        self.board = []
        idx = 0
        card_layout = []

        for row_index, num in enumerate(self.structure):
            row = []
            for i in range(num):
                card_id = self.card_indices[idx]
                row.append(card_id)
                self.board.append({
                    "id": card_id,
                    "open": row_index % 2 == 0,
                    "covered_by": [],
                    "row": row_index,
                    "column": i
                })
                idx += 1
            card_layout.append(row)

        for i in range(1, len(card_layout)):
            upper = card_layout[i - 1]
            lower = card_layout[i]
            for j, card in enumerate(lower):
                covers = []
                if j < len(upper):
                    covers.append(upper[j])
                if j > 0:
                    covers.append(upper[j - 1])
                for c in covers:
                    for b in self.board:
                        if b["id"] == c:
                            b.setdefault("covers", []).append(card)
                for b in self.board:
                    if b["id"] == card:
                        b["covered_by"] = covers

        if self.verbose:
            logging.info("Spiel zurückgesetzt und Spielfeld aufgebaut.")

        return self._get_obs()

    def _get_obs(self):
        obs = np.zeros(self.num_cards, dtype=int)
        for card in self.board:
            if card["open"] and card["id"] not in self.collected_indices:
                obs[card["id"]] = 1
        return obs

    
    def step(self, action):
        # Gültige Aktionen berechnen
        valid_actions = [
            card["id"]
            for card in self.board
            if card["open"] and card["id"] not in self.collected_indices
        ]

        if self.done:
            if self.verbose:
                logging.warning("Aktion nach Spielende ausgeführt.")
            return self._get_obs(), -1, True, {"valid_actions": valid_actions}

        if action not in valid_actions:
            if self.verbose:
                logging.warning(f"Ungültige Aktion: {action}")
            return self._get_obs(), -1, self.done, {"valid_actions": valid_actions}

        self.collected_indices.append(action)

        # ggf. neue Karten aufdecken
        for b in self.board:
            if action in b.get("covered_by", []):
                b["covered_by"].remove(action)
                if not b["covered_by"]:
                    b["open"] = True

        self.done = len(self.collected_indices) == self.num_cards
        card_data = self.card_data[action]
        reward = 1 if card_data.get("typ") == "Rohstoffgebäude" else 0

        if self.verbose:
            logging.info(f"Zug: {card_data['name']} ({card_data['typ']}) → Reward: {reward}")

        return self._get_obs(), reward, self.done, {
            "karte": card_data["name"],
            "typ": card_data["typ"],
            "valid_actions": valid_actions
        }

    
    def step(self, action):
        if self.done:
            if self.verbose:
                logging.warning("Aktion nach Spielende ausgeführt.")
            return self._get_obs(), -1, True, {}

        card = next((c for c in self.board if c["id"] == action), None)

        if not card or not card["open"] or action in self.collected_indices:
            if self.verbose:
                logging.warning(f"Ungültige Aktion: {action}")
            return self._get_obs(), -1, self.done, {}

        self.collected_indices.append(action)

        for b in self.board:
            if action in b.get("covered_by", []):
                b["covered_by"].remove(action)
                if not b["covered_by"]:
                    b["open"] = True

        self.done = len(self.collected_indices) == self.num_cards
        card_data = self.card_data[action]
        reward = 1 if card_data.get("typ") == "Rohstoffgebäude" else 0

        if self.verbose:
            logging.info(f"Zug: {card_data['name']} ({card_data['typ']}) → Reward: {reward}")

            return self._get_obs(), reward, self.done, {"karte": card_data["name"], "typ": card_data["typ"]}
    
    def render_board(self):
        """Zeigt das aktuelle Zeitalter-I-Spielfeld im Binärstil im Terminal"""
        layout = [[] for _ in self.structure]
        for card in self.board:
            row = card["row"]
            visible = int(card["open"] and card["id"] not in self.collected_indices)
            layout[row].append(visible)

        print("\n🧩 Aktuelles Zeitalter-I-Layout:")
        for row_index, row in enumerate(layout):
            row_str = " ".join(map(str, row))
            print(f"Zeile {row_index}: {row_str}")


    