# 🧨 Git Workshop – Merge & Conflict Resolution Guide

## 🎯 Objective

Your mission:

Merge 6 feature branches into master and restore the game to a playable state.

The game will NOT run until:
- All branches are merged
- All merge conflicts are resolved properly
- `REQUIRED_FEATURES` contains **7 True values**

---

# 🛑 RULES

- ❌ Do NOT checkout `stable-backup`
- ❌ Do NOT manually set all REQUIRED_FEATURES to True
- ❌ Do NOT delete feature logic to “make it run”
- ✅ You MUST resolve conflicts properly
- ✅ The game must run successfully at the end

---

# 🧭 STEP 1 — Switch to Main Workshop Branch

```bash
git checkout master
```

Confirm:

```bash
git branch
```

You should see:

```
* master
  stable-backup
  feature-health-system
  feature-armor
  feature-weapon-rework
  feature-resolution
  feature-ray-refactor
  feature-init-reorder
```

---

# 🚀 STEP 2 — Merge Branches One by One

We will merge in this order:

1. feature-health-system
2. feature-armor
3. feature-weapon-rework
4. feature-resolution
5. feature-ray-refactor
6. feature-init-reorder

---

## ✅ Merge 1

```bash
git merge feature-health-system
```

If no conflicts:

```bash
git status
```

Then continue.

---

## 🔥 Merge 2 (First Conflict Expected)

```bash
git merge feature-armor
```

You will likely see:

```
CONFLICT (content): Merge conflict in main.py
```

---

# 🧨 How to Resolve a Merge Conflict

Open the conflicted file.

You will see something like:

```python
<<<<<<< HEAD
    "health_system": True,
    "armor_system": False,
=======
    "health_system": False,
    "armor_system": True,
>>>>>>> feature-armor
```

### What This Means

- `HEAD` = current branch (master)
- `feature-armor` = incoming branch

---

## ✅ Correct Resolution

You must combine BOTH changes:

```python
    "health_system": True,
    "armor_system": True,
```

### 🔥 REMOVE THESE LINES COMPLETELY:

```
<<<<<<< HEAD
=======
>>>>>>> feature-armor
```

Save the file.

---

## Finish the Merge

```bash
git add main.py
git commit
```

---

# 🧨 Repeat For Each Branch

---

## Merge 3

```bash
git merge feature-weapon-rework
```

Possible conflict in:
- npc.py
- weapon.py
- main.py

### If conflict in weapon damage:

You may see:

```python
<<<<<<< HEAD
self.damage = 50
=======
self.base_damage = 40
self.crit_multiplier = 2
>>>>>>> feature-weapon-rework
```

### Correct resolution:

Keep the rework version:

```python
self.base_damage = 40
self.crit_multiplier = 2
```

And ensure npc.py references:

```python
self.game.weapon.base_damage
```

NOT `.damage`.

---

After fixing:

```bash
git add .
git commit
```

---

## Merge 4

```bash
git merge feature-resolution
```

Conflict likely in `settings.py`.

You may see:

```python
<<<<<<< HEAD
RES = WIDTH, HEIGHT = 1600, 900
=======
BASE_WIDTH, BASE_HEIGHT = 1280, 720
RES = WIDTH, HEIGHT = BASE_WIDTH, BASE_HEIGHT
>>>>>>> feature-resolution
```

Keep the new structure:

```python
BASE_WIDTH, BASE_HEIGHT = 1280, 720
RES = WIDTH, HEIGHT = BASE_WIDTH, BASE_HEIGHT
```

Remove conflict markers.

Then:

```bash
git add settings.py
git commit
```

---

## Merge 5

```bash
git merge feature-ray-refactor
```

Conflict likely in:

- raycasting.py

You may see:

```python
<<<<<<< HEAD
def ray_cast(self):
=======
def perform_ray_cast(self):
>>>>>>> feature-ray-refactor
```

Keep the renamed version:

```python
def perform_ray_cast(self):
```

Then ensure update() calls:

```python
self.perform_ray_cast()
```

NOT:

```python
self.ray_cast()
```

Save.

```bash
git add raycasting.py
git commit
```

---

## Merge 6

```bash
git merge feature-init-reorder
```

Resolve any conflicts in:

- main.py

Ensure:
- ObjectRenderer is initialized BEFORE Raycasting (important for textures)
- No constructor logic is removed

After resolving:

```bash
git add .
git commit
```

---

# 🧪 FINAL CHECK

Check REQUIRED_FEATURES in main.py:

It MUST look like:

```python
REQUIRED_FEATURES = {
    "health_system": True,
    "armor_system": True,
    "weapon_rework": True,
    "resolution_update": True,
    "ray_refactor": True,
    "init_reorder": True,
}
```

---

# 🧠 Verify No Conflict Markers Exist

Search entire project for:

```
<<<<<<<
=======
>>>>>>>
```

In VS Code:
- Ctrl + Shift + F
- Search `<<<<<<<`

There must be ZERO results.

---

# 🎮 Run The Game

```bash
python main.py
```

If everything is correct:

✅ Game launches  
✅ Player moves  
✅ NPCs attack  
✅ No crash  

---

# 🚨 If The Game Still Crashes

Run:

```bash
git status
```

Make sure:
- No unmerged files remain
- All conflicts were committed

Common mistakes:
- Leftover conflict markers
- Missing method rename
- Incorrect attribute name
- Forgot to update constructor calls

---

# 🏁 Victory Condition

When the game runs successfully, you have:

- Merged 6 branches
- Resolved multiple conflicts
- Reconciled logic properly
- Completed the Git merge challenge

---

# 🧨 Emergency Reset (Instructor Only)

To restore working version:

```bash
git checkout stable-backup
```

---

# 🏆 Congratulations


You have survived the Git Merge Tutorial.
