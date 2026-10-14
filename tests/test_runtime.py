import math
import unittest
from collections import deque
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pygame as pg
from main import Game
from player import Player
from sprite_object import AnimatedSprite
from npc import NPC
from weapon import Weapon


class InputTests(unittest.TestCase):
    def game(self):
        game = Game.__new__(Game)
        game.focused = True
        game.mouse_captured = True
        game.global_event = pg.USEREVENT
        game.player = SimpleNamespace(single_fire_event=Mock())
        return game

    def dispatch(self, game, *events):
        with patch('main.pg.event.get', return_value=list(events)), \
             patch('main.pg.event.set_grab') as grab, \
             patch('main.pg.mouse.set_visible') as visible, \
             patch('main.pg.mouse.get_rel', return_value=(200, 0)):
            game.check_events()
            return grab, visible

    def test_focus_loss_pauses_and_resume_click_does_not_fire(self):
        game = self.game()
        grab, visible = self.dispatch(game, pg.event.Event(pg.WINDOWFOCUSLOST))
        self.assertFalse(game.focused)
        self.assertFalse(game.mouse_captured)
        grab.assert_called_once_with(False)
        visible.assert_called_once_with(True)
        self.dispatch(game, pg.event.Event(pg.WINDOWFOCUSGAINED))
        self.assertFalse(game.mouse_captured)
        self.dispatch(game, pg.event.Event(pg.MOUSEBUTTONDOWN, button=1))
        self.assertTrue(game.mouse_captured)
        game.player.single_fire_event.assert_not_called()
        self.dispatch(game, pg.event.Event(pg.MOUSEBUTTONDOWN, button=1))
        game.player.single_fire_event.assert_called_once()

    def test_tab_releases_and_recaptures(self):
        game = self.game()
        self.dispatch(game, pg.event.Event(pg.KEYDOWN, key=pg.K_TAB))
        self.assertFalse(game.mouse_captured)
        self.dispatch(game, pg.event.Event(pg.KEYDOWN, key=pg.K_TAB))
        self.assertTrue(game.mouse_captured)

    def test_mouse_sensitivity_is_independent_of_frame_time(self):
        angles = []
        for elapsed in [8, 32]:
            player = Player.__new__(Player)
            player.game = SimpleNamespace(delta_time=elapsed)
            player.angle = 0
            with patch('player.pg.mouse.get_rel', return_value=(100, 0)):
                player.mouse_coordinates()
            angles.append(player.angle)
        self.assertAlmostEqual(angles[0], angles[1])
        self.assertAlmostEqual(angles[0], .2)

    def test_step_caps_stalls_and_draws_after_simulation(self):
        game = self.game()
        calls = []
        game.clock = SimpleNamespace(tick=lambda fps: 500, get_fps=lambda: 60)
        game.check_events = lambda: calls.append('events')
        game.update = lambda: calls.append('update')
        game.draw = lambda: calls.append('draw')
        with patch('main.pg.display.set_caption'):
            game.step()
            self.assertEqual(calls, ['events', 'update', 'draw'])
            self.assertEqual(game.delta_time, 50)
            calls.clear()
            game.mouse_captured = False
            game.step()
            self.assertEqual(calls, ['events', 'draw'])

    def test_display_is_presented_after_drawing(self):
        game = self.game()
        calls = []
        game.object_renderer = SimpleNamespace(draw=lambda: calls.append('world'))
        game.weapon = SimpleNamespace(draw=lambda: calls.append('weapon'))
        with patch('main.pg.display.flip', side_effect=lambda: calls.append('present')):
            game.draw()
        self.assertEqual(calls, ['world', 'weapon', 'present'])


class AnimationTests(unittest.TestCase):
    def test_frame_files_play_in_natural_order(self):
        sprite = AnimatedSprite.__new__(AnimatedSprite)
        filenames = ['10.png', '2.png', '0.png', '1.png']
        with patch('sprite_object.os.listdir', return_value=filenames), \
             patch('sprite_object.os.path.isfile', return_value=True), \
             patch('sprite_object.pg.image.load', side_effect=lambda name: SimpleNamespace(convert_alpha=lambda: name)):
            images = sprite.load_images('frames')
        self.assertEqual(list(images), ['frames/0.png', 'frames/1.png', 'frames/2.png', 'frames/10.png'])

    def test_state_switch_uses_new_animation_immediately(self):
        sprite = AnimatedSprite.__new__(AnimatedSprite)
        sprite.animation_trigger = False
        sprite.image = 'idle'
        sprite.animate(deque(['attack0', 'attack1']))
        self.assertEqual(sprite.image, 'attack0')

    def test_death_starts_at_first_frame_and_holds_last(self):
        npc = NPC.__new__(NPC)
        npc.alive = False
        npc.death_animation_started = False
        npc.animation_trigger = True
        npc.frame_counter = 0
        npc.death_images = deque(['death0', 'death1', 'death2'])
        with patch('npc.pg.time.get_ticks', return_value=100):
            npc.animate_death()
            self.assertEqual(npc.image, 'death0')
            for _ in range(8):
                npc.animate_death()
        self.assertEqual(npc.image, 'death2')
        self.assertEqual(npc.frame_counter, 2)

    def test_shotgun_completes_sequence_and_returns_to_rest(self):
        weapon = Weapon.__new__(Weapon)
        weapon.game = SimpleNamespace(player=SimpleNamespace(shot=True))
        weapon.images = deque(['rest', 'fire1', 'fire2'])
        weapon.num_images = 3
        weapon.frame_counter = 0
        weapon.reloading = True
        weapon.animation_trigger = True
        shown = []
        for _ in range(3):
            weapon.animate_shot()
            shown.append(weapon.images[0])
        self.assertEqual(shown, ['fire1', 'fire2', 'rest'])
        self.assertFalse(weapon.reloading)


if __name__ == '__main__':
    unittest.main()
