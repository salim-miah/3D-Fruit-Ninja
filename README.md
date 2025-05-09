# 3D Fruit Ninja

Welcome to **3D Fruit Ninja**, a fun and interactive game where you slice fruits with a sword while avoiding bombs! This game is built using **Python** and **OpenGL** to provide a 3D gaming experience.

---

## Game Description

In this game, you play as a ninja who slices fruits flying in the air. Your goal is to score as many points as possible by slicing fruits while avoiding bombs. You can unlock new swords as you progress and switch between them to enhance your gameplay. Be careful not to miss too many fruits or hit bombs, as it will cost you lives!

---

## Features

- **3D Gameplay**: Experience a fully immersive 3D environment.
- **Sword Mechanics**: Swing your sword to slice fruits.
- **Unlockable Swords**: Unlock new swords as you score points.
- **Pause and Restart**: Pause the game or restart it anytime.
- **Japanese-Style Environment**: Enjoy a beautifully designed Japanese-style grid and walls.

---

## Controls

| Key         | Action                                    |
|-------------|-------------------------------------------|
| `W`         | Move forward                              |
| `S`         | Move backward                             |
| `A`         | Rotate player left                        |
| `D`         | Rotate player right                       |
| `E`         | Switch to the next unlocked sword         |
| `P`         | Pause/Resume the game                     |
| `R`         | Restart the game                          |
| Left Click  | Swing the sword                           |
| Right Click | Toggle between first-person and third-person camera |

---

## Sword Unlocking

- **Type 1**: Default sword (available from the start).
- **Type 2**: Unlocked at **100 points**.
- **Type 3**: Unlocked at **500 points**.

---

## Game Rules

1. Slice fruits to earn points:
   - Red fruit: 10 points
   - Green fruit: 20 points
   - Yellow fruit: 50 points
   - Orange fruit: 100 points
2. Avoid bombs! Hitting a bomb will reduce your lives.
3. Missing fruits will also reduce your lives.
4. The game ends when you lose all your lives.

---

## Installation Instructions

1. **Prerequisites**:
   - Python 3.8 or higher
   - `PyOpenGL` library
   - `PyOpenGL_accelerate` (optional for better performance)

2. **Install Dependencies**:
   Run the following command to install the required libraries:
   ```bash
   pip install PyOpenGL PyOpenGL_accelerate

3. **Run the Game**:
   Navigate to the directory containing the `final.py` file and run:
   ```bash
   python final.py
   ```

---

## How to Play

1. Launch the game by running the `final.py` file.
2. Use the controls to move, swing your sword, and interact with the environment.
3. Slice as many fruits as possible while avoiding bombs.
4. Unlock new swords as you score points and switch between them using the `E` key.
5. Pause or restart the game anytime using the `P` and `R` keys, respectively.

---

## Game Environment

- The game features a **Japanese-style environment** with Tatami mat patterns on the grid and Shoji screen-inspired walls.
- The fruits and bombs are rendered in 3D, providing a visually appealing experience.

---

## Known Issues

- The game may run slowly on older systems. Ensure you have the latest version of Python and the required libraries installed.
- If the game crashes, check the console for error messages and ensure all dependencies are installed correctly.

---

## Credits

- **Developers**: Salim Miah, S M Noiem Uddin, Kaiser Fahim
- **Built With**: Python, OpenGL

---

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute the code.

---

Enjoy slicing fruits and becoming the ultimate ninja! 🥷🍉