from settings import * 
from sprites import AnimatedSprite, Heart
from random import randint
from timer import Timer

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font

    #-------------------------------- HEALTH/HEARTS -----------
        self.heart_frames = frames['heart']
        self.heart_surf_width = self.heart_frames[0].get_width()
        self.heart_padding = 6
        #self.create_hearts(5)
    #------------------------------------------------------------
              
    #---------------------------------- COINS --------------- 
        self.coin_amount = 0
        self.coin_timer = Timer(1000)
        self.coin_surf = frames['coin']
    #--------------------------------------------------------

    def display_text(self):
        if self.coin_timer.active:
            text_surf = self.font.render(str(self.coin_amount), False, '#33323d')
            text_rect = text_surf.get_rect(topleft = (16,34))
            self.display_surface.blit(text_surf, text_rect)

            coin_rect = self.coin_surf.get_rect(center = text_rect.bottomleft).move(50,-6)
            self.display_surface.blit(self.coin_surf, coin_rect)

    def create_hearts(self, amount):
        for sprite in self.sprites:
            sprite.kill()

        for heart in range(amount):
            x = 10 + heart * (self.heart_surf_width + self.heart_padding)
            y = 10
            Heart((x,y), self.heart_frames, self.sprites)

    def show_coins(self, amount):
        self.coin_amount = amount
        self.coin_timer.activate()

    def update(self, delta_time):
        self.coin_timer.update()
        self.sprites.update(delta_time)
        self.sprites.draw(self.display_surface)
        self.display_text()