# Pokemon Pygame Battle Engine

Whats sup! This is a passion project built to recreate the classic, turn-based Pokémon battle mechanics using Python and Pygame. Instead of just hardcoding a basic fight screen, I built a dedicated battle engine from scratch that handles everything behind the scenes,inspired from GEN 1 pokemon Red
and Blue. Hope you guys enjoy it!!!!

##  What it does

* **Turn Logic:** Resolves actions properly by factoring in move selection, and speed priority.
* ** Battle Math:** Features a custom damage engine built around the Gen 1 formulas (yes, including STAB, type effectiveness, and critical hits).
* **Status Effects:** Fully tracks and applies active conditions like Paralysis, Burn, Poison, and Sleep during turns.
* **Pygame Interface:** Includes health bars that shift colors dynamically, animated text boxes, and responsive UI menus.

---

## How the code is organized

```text
├── assets/
│   ├── sprites/          # Front/back Pokémon graphics
│   └── fonts/            # Retro gaming fonts
├── data/
│   ├── pokemon.json      # Base stats, types, and learnsets
│   └── moves.json        # Move power, accuracy, and typing
├── src/
│   ├── engine.py         # The core battle state machine
│   ├── formulas.py       # Damage, stat modifiers, and RNG calculation
│   ├── entities.py       # Pokémon and Trainer classes
│   └── interface.py      # Health bars, menus, and sprite animations
└── main.py               # Game bootstrapper and main loop
