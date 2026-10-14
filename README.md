# Git Merge Workshop — Raycasting Game

This repository is a hands-on exercise in **Git branching, merge conflicts, and
reconciling changes across files**. The pygame raycasting game is the teaching
vehicle: participants merge six feature branches and restore a playable game.

**The default `master` branch is intentionally locked.** That is the starting
point of the exercise. To play the completed game instead, use
`workshop-solution`. See [WORKSHOP.md](WORKSHOP.md) for participant instructions.

## Choose your path

| Branch | Purpose |
| --- | --- |
| `master` | Workshop starter, with six required features disabled |
| `feature-*` | Six separate changes that participants must merge and reconcile |
| `workshop-solution` | Completed integration for a runnable demo or instructor reference |
| `stable-backup` | Original baseline game; retained unchanged for reference |

There is no `workshop-main` or `feature-npc-difficulty` branch. The exercise has
six implemented features, not seven. The old orphan `npc_difficulty` flag was an
unintended blocker and is no longer part of the launcher requirement.

## Requirements and setup

- Python 3.10 or later (verified on Python 3.12)
- pygame installed from `requirements.txt`
- A graphical desktop for playing, and an audio device for sound
- Git for the workshop

```sh
git clone https://github.com/LAKWAN194/Merge_Tutorial.git
cd Merge_Tutorial
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows use `python -m venv .venv`, then `.venv\Scripts\Activate.ps1` in
PowerShell. Inside the activated environment, use `python` for all commands below.

## Play the completed demo

```sh
git switch --track origin/workshop-solution
python tools/check_workshop.py --expect solution
python main.py
```

If the local branch already exists, use `git switch workshop-solution`.
Controls: **WASD** to move, **mouse** or **left/right arrows** to look, **left
mouse button** to shoot, and **Escape** to quit. NPCs attack the player; the game
restarts after death. The solution uses a 1280 × 720 window.

The launcher resolves the resource directory relative to `main.py`, so invoking
it by an absolute path also works.

## Start the merge exercise

```sh
git fetch origin
git switch -c workshop/my-attempt origin/master
python tools/check_workshop.py --expect starter
```

Running `python main.py` here produces an explanation listing the features still
missing. Follow [WORKSHOP.md](WORKSHOP.md) to integrate them. Do not copy the
solution or toggle all the flags when practicing: the goal is to understand
and resolve the code changes themselves.

## Verification

The source check needs only Python; it checks syntax and the six feature flags.
For the solution, it also checks key names agree across the health, weapon/NPC,
resolution, and raycasting changes. It does not prove gameplay correctness.

The runtime smoke check needs pygame and exercises real assets, rendering,
updates, armor, weapon damage, and restarting:

```sh
python tools/smoke_game.py --frames 120
```

For automated checks without opening a window or using speakers, on Linux/macOS:

```sh
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python tools/smoke_game.py --frames 120
```

On PowerShell set `$env:SDL_VIDEODRIVER='dummy'` and
`$env:SDL_AUDIODRIVER='dummy'` before running the smoke check. Headless checks
cannot verify how mouse control, audio, or animation feel on a desktop.

## Common problems

- **Starter reports missing merges:** expected until all six features are integrated.
- **Feature branch is not found:** merge `origin/feature-...` after `git fetch origin`.
  Fresh clones do not automatically create local branches for every remote branch.
- **Window or audio initialization fails:** use a desktop/audio device for play,
  or the SDL dummy drivers for automated smoke checks.
- **Merge completes but game crashes:** inspect cross-file renames and constructor
  dependencies; a clean Git status is not proof that the combined code works.

## Project structure

`main.py` runs the game and guards the workshop. `workshop.py` lists its six
features. `player.py`, `weapon.py`, and `npc.py` handle combat; `raycasting.py`,
`object_renderer.py`, and the sprite modules render it. `map.py` and
`pathfinding.py` handle the world, while `resources/` holds images and audio.
`tools/` contains source and runtime checks.
