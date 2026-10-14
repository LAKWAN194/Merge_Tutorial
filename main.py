import pygame as pg
import sys
import os
from pathlib import Path
from workshop import FEATURE_BRANCHES
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *

REQUIRED_FEATURES = {
    "health_system": True,
    "armor_system": True,
    "weapon_rework": True,
    "resolution_update": True,
    "ray_refactor": True,
    "init_reorder": True,
}

def check_all_features():
    return all(REQUIRED_FEATURES.get(name, False) for name in FEATURE_BRANCHES)

class Game:
    def __init__(self):
        if not check_all_features():
            missing = [FEATURE_BRANCHES[name] for name in FEATURE_BRANCHES
                       if not REQUIRED_FEATURES.get(name, False)]
            raise RuntimeError("Workshop starter is intentionally locked. Merge: "
                               + ", ".join(missing) + ". See WORKSHOP.md, or use workshop-solution for the demo.")
        os.chdir(Path(__file__).resolve().parent)
        pg.init()
        self.screen = pg.display.set_mode(RES) # create the game window with the specified resolution
        self.clock = pg.time.Clock() # create a clock object to manage the game's frame rate
        self.delta_time = 1000 / FPS
        self.focused = True
        self.mouse_captured = False
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40) # set a timer to trigger the global event every 40 milliseconds
        self.new_game()
        self.set_mouse_capture(True)

    def new_game(self):
        self.map = Map(self) # create a new instance of the Map class, passing the current game instance as an argument.
        self.player = Player(self) # create a new instance of the Player class, passing the current game instance as an argument.
        self.object_renderer = ObjectRenderer(self) # create a new instance of the ObjectRenderer class, passing the current game instance as an argument.
        self.raycasting = Raycasting(self) # create a new instance of the Raycasting class, passing the current game instance as an argument.
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)

        pg.mixer.music.play(-1)
        pg.mouse.get_rel()  # ignore motion while loading assets or restarting

    def update(self):
        self.player.update() # call the update method of the Player instance to update the player's state based on user input and game logic
        self.raycasting.update() # call the update method of the Raycasting instance to update the raycasting state
        self.object_handler.update()
        self.weapon.update()



    def draw(self):
        #self.screen.fill('black') # Paint the screen black in each iteration
        #self.map.draw() # call the draw method of the Map instance to render the game map on the screen
        #self.player.draw() # call the draw method of the Player instance to render the player on the screen
        self.object_renderer.draw() # call the draw method of the ObjectRenderer instance to render the game objects on the screen
        self.weapon.draw()
        if not self.mouse_captured:
            text = pg.font.Font(None, 36).render("Paused — click to resume (Tab releases mouse)", True, "white")
            rect = text.get_rect(center=(HALF_WIDTH, HALF_HEIGHT))
            pg.draw.rect(self.screen, (20, 20, 20), rect.inflate(32, 24))
            self.screen.blit(text, rect)
        pg.display.flip()


    def set_mouse_capture(self, captured):
        self.mouse_captured = captured
        pg.event.set_grab(captured)
        pg.mouse.set_visible(not captured)
        pg.mouse.get_rel()  # discard motion accumulated while paused or changing focus
        if captured and hasattr(self, "object_handler"):
            for sprite in self.object_handler.sprite_list + self.object_handler.npc_list + [self.weapon]:
                if hasattr(sprite, "animation_time_previous"):
                    sprite.animation_time_previous = pg.time.get_ticks()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.set_mouse_capture(False)
                pg.quit()
                sys.exit()
            elif event.type == pg.WINDOWFOCUSLOST:
                self.focused = False
                self.set_mouse_capture(False)
            elif event.type == pg.WINDOWFOCUSGAINED:
                self.focused = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_TAB and self.focused:
                self.set_mouse_capture(not self.mouse_captured)
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.focused and not self.mouse_captured:
                self.set_mouse_capture(True)  # this click resumes without firing
            elif event.type == self.global_event:
                self.global_trigger = True
            elif self.mouse_captured and self.focused:
                self.player.single_fire_event(event)

    def step(self):
        # Sample the current frame before simulation and limit movement after a stall.
        self.delta_time = max(1, min(self.clock.tick(FPS), 50))
        self.check_events()
        if self.mouse_captured and self.focused:
            self.update()
        self.draw()
        pg.display.set_caption(f"Git Merge Workshop — {self.clock.get_fps():.0f} FPS")

    def run(self):
        try:
            while True:
                self.step()
        finally:
            if pg.display.get_init():
                self.set_mouse_capture(False)
            pg.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
