# Participant Guide: Merge and Conflict Resolution

## Objective

Integrate six branches into your own branch from `origin/master`, resolving
text conflicts and code dependencies until the game runs. Preserve each feature's
behavior. The finished demo on `workshop-solution` is an instructor reference;
`stable-backup` is the original baseline and should remain untouched.

## 1. Create an isolated attempt

After installing dependencies as described in [README.md](README.md):

```sh
git fetch origin
git switch -c workshop/my-attempt origin/master
python tools/check_workshop.py --expect starter
```

Choose a different attempt name if this one already exists. `master` is the
starter; the old documentation's `workshop-main` branch does not exist.

## 2. Merge the six features

Run one command at a time. Resolve and commit each merge before starting the next:

```sh
git merge origin/feature-health-system
git merge origin/feature-armor
git merge origin/feature-weapon-rework
git merge origin/feature-resolution
git merge origin/feature-ray-refactor
git merge origin/feature-init-reorder
```

| Feature | Integration detail to review |
| --- | --- |
| Health | `PLAYER_BASE_HEALTH` must agree between settings and player initialization/recovery |
| Armor | Retain initial armor and absorb incoming damage before reducing health |
| Weapon | Keep `base_damage` and update the NPC damage reference to match |
| Resolution | Keep `BASE_WIDTH`, `BASE_HEIGHT`, and derived rendering constants consistent |
| Raycasting | Keep `perform_ray_cast` and update the call from `update()` |
| Initialization | Resolve the reordered constructors according to their dependencies; initialize `ObjectRenderer` before `Raycasting`, which needs its textures |

Conflicts depend on merge order and Git's merge algorithm. Some files may merge
cleanly but still need an integration correction. In particular, the incoming
initialization reorder places the renderer too late; simply accepting it breaks
the texture dependency.

## 3. Resolve conflicts deliberately

Use `git status` to identify unresolved files. A conflict block contains both
versions separated by `<<<<<<<`, `=======`, and `>>>>>>>`. Keep the combined
behavior rather than choosing an entire side indiscriminately.

For `main.py`, retain the starter's launcher improvements and the enabled flags
from every feature integrated so far. Each historical branch contains an obsolete
`npc_difficulty` flag: remove it when resolving the dictionary. There is no
seventh feature branch to merge.

After removing conflict markers and reconciling the code:

```sh
git diff --check
git add main.py player.py settings.py  # use the actual files you resolved
git commit                         # records this merge resolution
```

Do not set flags for branches you have not integrated. Do not remove combat,
rendering, or constructors just to make the program start. If you want to abandon
an in-progress merge, `git merge --abort` restores the pre-merge state.

## 4. Validate the completed integration

All six flags should be true only after their corresponding changes are retained:

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

```sh
git status
python tools/check_workshop.py --expect solution
python tools/smoke_game.py --frames 120
python main.py
```

The source check confirms syntax and key cross-file names. The runtime check
renders frames, verifies armor absorbs damage, verifies a shot reduces NPC
health by the weapon's base damage, and restarts the game. On a desktop, also
check movement, mouse look, shooting, NPC attacks, and Escape. Headless SDL
instructions are in the README.

## What the exercise teaches

- Remote branches and working on your own integration branch
- Reading and reconciling conflict blocks
- Preserving independent features across overlapping changes
- Detecting semantic errors after Git reports a successful merge
- Verifying a result with both source checks and real runtime behavior

Feature flags are a learning aid, not a secure anti-cheating mechanism. The real
completion criterion is a coherent implementation with all six branches integrated
and the checks passing. `crit_multiplier` is carried by the weapon branch, but
random critical-hit behavior is not implemented or required by this exercise.

## Instructor reference

Use `workshop-solution` to inspect the completed merge history and runnable
integration. Keep feature branches and `stable-backup` unchanged so future
participants can still reproduce the exercise. Start another attempt from
`origin/master` rather than resetting a branch that contains work you want to keep.
