"""Check workshop source without loading pygame or opening a window."""
import argparse
import ast
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from workshop import FEATURE_BRANCHES


def feature_flags(root):
    tree = ast.parse((root / "main.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "REQUIRED_FEATURES"
            for target in node.targets
        ):
            return ast.literal_eval(node.value)
    raise ValueError("main.py must define REQUIRED_FEATURES")


def check(root, expect):
    for source in root.glob("*.py"):
        ast.parse(source.read_text(), filename=str(source))
    flags = feature_flags(root)
    if any(type(flags.get(name)) is not bool for name in FEATURE_BRANCHES):
        raise ValueError("Each of the six workshop features needs a boolean flag")
    if expect == "starter" and any(flags[name] for name in FEATURE_BRANCHES):
        raise ValueError("Starter must keep the six feature flags disabled")
    if expect == "solution":
        missing = [name for name in FEATURE_BRANCHES if not flags[name]]
        if missing:
            raise ValueError("Features still missing: " + ", ".join(missing))
        player = (root / "player.py").read_text()
        weapon = (root / "weapon.py").read_text()
        npc = (root / "npc.py").read_text()
        settings = (root / "settings.py").read_text()
        rays = (root / "raycasting.py").read_text()
        required = [
            ("PLAYER_BASE_HEALTH" in player and "PLAYER_BASE_HEALTH" in settings, "health rename"),
            ("self.armor" in player and "absorbed" in player, "armor handling"),
            ("self.base_damage" in weapon and "self.game.weapon.base_damage" in npc, "weapon/NPC damage agreement"),
            ("BASE_WIDTH" in settings, "resolution constants"),
            ("def perform_ray_cast(" in rays and "self.perform_ray_cast()" in rays, "raycasting rename"),
        ]
        for valid, label in required:
            if not valid:
                raise ValueError("Missing implementation: " + label)
    print(f"{expect}: Python syntax and workshop structure passed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--expect", choices=["starter", "solution"], default="starter")
    args = parser.parse_args()
    try:
        check(ROOT, args.expect)
    except (ValueError, SyntaxError) as error:
        parser.exit(1, str(error) + "\n")
