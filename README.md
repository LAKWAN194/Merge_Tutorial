# 🎮 Raycasting Git Merge Workshop

A Python raycasting game used for practicing **Git branching and merge conflict resolution**.

This project is intentionally structured for a workshop where participants must merge multiple feature branches before the game becomes playable.

---

# 🧰 Requirements

## 🐍 Python

* **Python 3.13.2**
* Must be run inside a **virtual environment**

Check your version:

```bash
python --version
```

Expected:

```
Python 3.13.2
```

---

## 📦 Required Python Packages

* `pygame`

---

## 🔧 Required Tools

* **Git**
* Python 3.13.2

Check Git:

```bash
git --version
```

---

# ⚙️ Setup Instructions

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/LAKWAN194/Merge_Tutorial/
cd Merge_Tutorial
```

---

## 2️⃣ Create Virtual Environment

### Windows (PowerShell)

```bash
python -m venv .venv
.\.venv\Scripts\Activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should now see:

```
(.venv)
```

in your terminal prompt.

---

## 3️⃣ Install Dependencies

```bash
pip install pygame
```

Or if using requirements file:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Game

Once everything is set up:

```bash
python main.py
```

If all feature branches are merged correctly, the game will launch.

If not, you will see:

```
Exception: 🚫 Merge all feature branches correctly before running the game.
```

---

# 🧪 Workshop Mode

This repository contains:

* `stable-backup` → Fully working game (DO NOT TOUCH)
* `workshop-main` → Locked branch (starting point)
* 7 feature branches

Participants must:

1. Merge all feature branches
2. Resolve all conflicts
3. Restore game functionality

---

# 🌿 Feature Branches

* `feature-health-system`
* `feature-armor`
* `feature-weapon-rework`
* `feature-npc-difficulty`
* `feature-resolution`
* `feature-ray-refactor`
* `feature-init-reorder`

---

# 🚀 Merge Instructions (Participants)

Start from:

```bash
git checkout workshop-main
```

Merge branches one by one:

```bash
git merge feature-health-system
git merge feature-armor
git merge feature-weapon-rework
git merge feature-npc-difficulty
git merge feature-resolution
git merge feature-ray-refactor
git merge feature-init-reorder
```

---

# 💥 Resolving Merge Conflicts

When you see something like:

```python
<<<<<<< HEAD
code A
=======
code B
>>>>>>> branch-name
```

You must:

1. Decide what logic to keep
2. Remove the conflict markers
3. Save the file
4. Stage the file:

```bash
git add filename.py
```

5. Complete the merge:

```bash
git commit
```

---

# 🏆 Victory Condition

The game launches successfully:

```bash
python main.py
```

You should be able to:

* Move with WASD
* Look around with mouse
* Shoot
* Take damage from NPCs

If it crashes:

* You missed a conflict
* You lost logic during merge
* A required feature flag is still False

---

# 🛑 Rules for Participants

* ❌ Do NOT edit `stable-backup`
* ❌ Do NOT manually change feature lock flags
* ❌ Do NOT delete functionality to "fix" errors
* ✅ Properly merge and reconcile logic

---

# 🧠 Common Issues

## Virtual environment not activated

Make sure you see:

```
(.venv)
```

before running Python.

---

## pygame not found

Install it:

```bash
pip install pygame
```

---

## Merge not completing

Check:

```bash
git status
```

If you see:

```
Unmerged paths
```

You must:

```bash
git add .
git commit
```

after resolving conflicts.

---

# 📂 Project Structure

* `main.py` → Game entry point
* `player.py` → Player logic
* `npc.py` → NPC behavior
* `weapon.py` → Weapon system
* `raycasting.py` → Rendering engine
* `settings.py` → Game configuration
* `object_handler.py` → Sprite & NPC management
* `stable-backup` → Fully working safe branch
* `workshop-main` → Locked branch for workshop

---

# 🎓 Learning Outcomes

By completing this workshop you will learn:

* Git branching
* Feature workflow
* Merge conflicts
* Conflict markers
* Manual conflict resolution
* Logical reconciliation
* Multi-branch integration

---

# 🏁 End Result

When all conflicts are properly resolved:

🎮 The game runs
🔥 All systems work
✅ All feature flags are enabled
🏆 You win the Git Merge Battle

---
