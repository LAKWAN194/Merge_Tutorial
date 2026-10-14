"""Run the completed game briefly, with optional SDL dummy video/audio drivers."""
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.check_workshop import check


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames", type=int, default=120)
    args = parser.parse_args()
    if args.frames < 1:
        parser.error("--frames must be positive")
    check(ROOT, "solution")
    import pygame as pg
    from main import Game
    game = Game()
    try:
        for _ in range(args.frames):
            game.check_events()
            game.update()
            game.draw()
        original_health = game.player.health
        game.player.get_damage(10)
        assert game.player.armor == 40 and game.player.health == original_health
        game.player.get_damage(50)
        assert game.player.armor == 0 and game.player.health == original_health - 10
        npc = game.object_handler.npc_list[0]
        npc.ray_cast_value = True
        npc.screen_x = game.screen.get_width() // 2
        npc.sprite_half_width = 20
        npc.distance = 1
        game.player.shot = True
        health = npc.health
        npc.check_hit_in_npc()
        assert npc.health == health - game.weapon.base_damage
        game.new_game()
        game.update()
        game.draw()
        assert game.player.armor == 50
        print(f"Game passed {args.frames} frames, armor, weapon damage, and restart checks")
    finally:
        pg.quit()


if __name__ == "__main__":
    main()
