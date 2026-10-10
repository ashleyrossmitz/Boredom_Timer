<div align="center">

# Boredom Timer ⏱

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

</div>

> Boredom timer — counts how long you were bored and saves the statistics.

## 📖 About the project
Boredom timer is a console application that measures how much time
you were bored and lets you rate the "boredom difficulty" on a scale of 1–5.
The statistics are saved to JSON and available for viewing.

## 🚀 Launch

```bash
python Boredom_Timer.py
```

## 🎮 Usage
1. Run the program.
2. Select 1 to start the timer.
3. Press Enter to start.
4. Be bored.
5. Press Enter to stop.
6. Rate the difficulty (1–5).
7. Session is saved automatically.

## Requirements

- Python 3.10+

## 📁 Project structure

```
Boredom_Timer/
├── Boredom_Timer.py     # main code
├── stats.json           # session database (created automatically)
├── .gitignore           # what not to push to Git
└── README.md            # this file
```

## 🛠 Technologies
Python 3.10+

Standard libraries: time, datetime, json, os, collections

## 🗺 Plans
- [ ] Migrate from JSON to SQLite
- [ ] Add Flask web interface
- [ ] Add AI analysis of sessions

## 📄 License

MIT