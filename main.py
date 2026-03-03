import pygame as pg
import sys
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
    "health_system": False,
    "armor_system": False,
    "weapon_rework": False,
    "npc_difficulty": False,
    "resolution_update": False,
    "ray_refactor": False,
    "init_reorder": False,
}

def check_all_features():
    return all(REQUIRED_FEATURES.values())

class Game: 
    def __init__(self):
        if not check_all_features():
            raise Exception("🚫 Merge all feature branches correctly before running the game.")     
        pg.init()
        self.screen = pg.display.set_mode(RES) # create the game window with the specified resolution
        self.clock = pg.time.Clock() # create a clock object to manage the game's frame rate
        self.delta_time = 1
        pg.mouse.set_visible(False) # hide the mouse cursor
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40) # set a timer to trigger the global event every 40 milliseconds
        self.new_game()
        
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
        
    def update(self):
        self.player.update() # call the update method of the Player instance to update the player's state based on user input and game logic
        self.raycasting.update() # call the update method of the Raycasting instance to update the raycasting state
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip() # update the display to show any changes made to the screen
        self.delta_time = self.clock.tick(FPS)   # Get FPS
        pg.display.set_caption(f'{self.clock.get_fps():.1f}') # display FPS in the window title
        
        
    def draw(self):
        #self.screen.fill('black') # Paint the screen black in each iteration
        #self.map.draw() # call the draw method of the Map instance to render the game map on the screen
        #self.player.draw() # call the draw method of the Player instance to render the player on the screen
        self.object_renderer.draw() # call the draw method of the ObjectRenderer instance to render the game objects on the screen   
        self.weapon.draw()    
    
        
    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
                    
                    
                    
if __name__ == '__main__':
    game = Game()
    game.run()