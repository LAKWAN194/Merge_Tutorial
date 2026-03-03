from importlib.resources import path

import pygame as pg
import math
from settings import *
import os
from collections import deque

class SpriteObject:
    def __init__(self, game,
                 path='resources/sprites/static_sprites/candlebra.png',
                 pos=(10.5, 3.5), scale = 0.7 , shift = 0.27):
        self.game = game
        self.player = game.player

        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()

        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.image_half_width = self.image_width // 2
        self.image_ratio = self.image_width / self.image.get_height()

        self.dx = 0
        self.dy = 0
        self.theta = 0
        self.screen_x = 0

        self.distance = 1
        self.norm_dist = 1
        self.sprite_half_width = 0
        
        self.SPRITE_SCALE = scale
        self.SPRITE_SHIFT = shift

    def get_sprite_projection(self):

        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_height = proj
        proj_width = proj * self.image_ratio

        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_SHIFT
        pos = (self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2  + height_shift)

        self.game.raycasting.objects_to_render.append(
            (self.norm_dist, image, pos)
        )

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y

        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (NUM_RAYS // 2 + delta_rays) * SCALE

        self.distance = math.hypot(dx, dy)
        self.norm_dist = self.distance * math.cos(delta)

        if (
            -self.image_half_width < self.screen_x < WIDTH + self.image_half_width
            and self.norm_dist > 0.5
        ):
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()
        
        
        
class AnimatedSprite(SpriteObject):
    def __init__(self, game, path='resources/sprites/animated_sprites/green_light/0.png', pos=(7.7, 3.5), scale = 0.8 , shift = 0.15, animation_time = 120):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0] + '/'
        self.last_time = pg.time.get_ticks()
        self.images = self.load_images(self.path)
        self.animation_time_previous = pg.time.get_ticks()
        self.animation_trigger = False
        
    def animate(self,images):
        if(self.animation_trigger):
            images.rotate(-1)
            self.image = images[0]
        
    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        
        if time_now - self.animation_time_previous > self.animation_time:
            self.animation_time_previous = time_now
            self.animation_trigger = True

    def load_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images
    
    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)  
