# PaloMUD

**PaloMUD** is a **Multi-User Dungeon (MUD)** built in **Python** using the [Evennia](https://www.evennia.com/) framework.
The project serves as a learning playground, exploring the creation of a persistent online world, classic MUD mechanics, and player interaction.

---

**PaloMUD** started as a prototype built "from scratch," handling Telnet sockets manually in Python.
With Evennia, the project now evolves into a more robust and flexible foundation, making it possible to develop:

- Character creation and login
- Exploration of interconnected rooms
- Real-time player-to-player interaction
- Custom systems for combat, economy, and progression
- Extensions with new commands and scripts to enrich the experience

---

## stack
- **Python 3.10+**
- **[Evennia](https://github.com/evennia/evennia)** – framework for creating MUDs, MU*s, and text-based games
- Telnet / Webclient (included with Evennia)
- [Mudlet](https://www.mudlet.org/download/) (for a Graphical User Interface)

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/DvRibeiro/PaloMUD.git
cd PaloMUD
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt

```

### 4. Initialize and start the game

```bash
evennia migrate
evennia start
```

The server will be available via MUD/telnet client to `localhost:4000` and through the **webclient** at `http://localhost:4001`.
We personally created this project to be played on [Mudlet](https://www.mudlet.org/)

---

## Roadmap

- [ ]  Define the world setting and initial lore
- [ ]  Build example maps and rooms
- [ ]  Implement NPCs
- [ ]  Add first custom commands
- [ ]  Document contribution guidelines

---

## References

- [Evennia Documentation](https://www.evennia.com/docs/latest/)
- [Evennia GitHub Repository](https://github.com/evennia/evennia)
- [Mudlet wiki](https://wiki.mudlet.org/w/Main_Page)

---

## License

This project is open-source under the MIT license.

Feel free to study, modify, and contribute.
