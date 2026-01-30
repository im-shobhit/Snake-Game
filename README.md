<div align="center">

# 🐍 Classic Snake Game

**A modern, feature-rich implementation of the retro classic using Python & Pygame.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-green?style=for-the-badge&logo=pygame&logoColor=white)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/yourusername/repo)

[View Demo] • [Report Bug] • [Request Feature]

</div>

---

## 📖 About The Project

This is a robust recreation of the classic Snake game. Beyond standard movement, this version introduces quality-of-life features like dynamic window resizing, a persistent high-score system, and adjustable difficulty levels, making it a perfect project for learning game logic in Python.

## ✨ Key Features

* **🎮 Dynamic Resizing:** The game border and playing area adapt automatically when you resize the window.
* **🏆 High Score System:** Your best run is saved locally (`highscore.txt`) and persists across game sessions.
* **⚙️ Difficulty Modes:** Choose your challenge level at the start: **Easy**, **Medium**, or **Hard**.
* **⏱️ Live Timer:** Tracks your survival time during gameplay.
* **⏸️ Pause Functionality:** Need a break? Pause the game instantly without losing progress.

---

## 🕹️ Controls

| Key | Action |
| :---: | :--- |
| **Arrow Keys** | Move the Snake (`↑`, `↓`, `←`, `→`) |
| **`P`** | Pause / Unpause Game |
| **`F`** | Toggle Fullscreen Mode |
| **`C`** | Play Again (at "Game Over" screen) |
| **`Q`** | Quit Game (at "Game Over" screen) |

---

## 🚀 Getting Started

Follow these steps to get a local copy up and running.

### Prerequisites

You need Python installed on your system. This project relies on the **Pygame** library.

### Installation

1. **Clone the repository**
```
git clone [https://github.com/yourusername/snake-game.git](https://github.com/yourusername/snake-game.git)
cd snake-game
```
2. **Install dependencies**
```
pip install pygame
```

3. **Run the game**
```
python snake.py
```
---

### Project Structure
```
snake-game/
├── highscore.txt    # Created automatically to store scores
├── snake.py         # Main game script
├── README.md        # This documentation
└── requirements.txt # Dependencies
```

   ```bash
   git clone [https://github.com/yourusername/snake-game.git](https://github.com/yourusername/snake-game.git)
   cd snake-game
