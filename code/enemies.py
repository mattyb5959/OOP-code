from settings import *
from random import choice
from timer import Timer
from math import sin

pearl_sprite = pygame.sprite.Group()
class Tooth(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(groups)

    #--------------------------------- images ---------------  
        pos = (pos[0], pos[1] - 22)
        self.frames =  {state: [pygame.transform.scale(frame, (48, 75)) for frame in state_frames] for state, state_frames in frames.items()}
        self.frame_index = 0
        #self.frames, self.frame_index = frames, 0
        self.state = 'run'
        self.image = self.frames[self.state][self.frame_index]
        #self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.z = Z_LAYERS['main']
    #-------------------------------------------------------------
        self.direction = choice((-1,1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]

        self.speed = 200
        self.health = 3
        self.isalive = True

        self.hit_timer = Timer(250)
        self.death_timer = Timer(500)
    
    def hit_by_player(self): 
        if not self.hit_timer.active:
            self.health -= 1
            self.direction *= -1
            self.hit_timer.activate()
            #print(self.health)
            #print('tooth')
            if self.health > 0:
                #print('hit filcker')
                self.flicker()
            elif self.health == 0:
                self.state = 'death'
                self.frame_index = 0
                self.death_timer.activate()
                self.isalive = False
                #self.get_state()
                
    def flicker(self):
        if self.hit_timer.active and sin(pygame.time.get_ticks() * 600) >= 0: #cause sin oscillates between 1 and -1, so when it his 0 and the oteher codition is satisfiied then it will flicker
            flicker_image = self.image.copy()
            
            # Create a surface for the flickering effect
            flicker_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)  # Use SRCALPHA for transparency support
            flicker_surface.fill((255, 0, 0, 128))  # Fill with red color with some transparency
            
            # Apply the flickering effect to the copied image
            flicker_image.blit(flicker_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            # Set the flickered image as the player's image
            self.image = flicker_image

    def animate(self, delta_time):
    #---------------------------------------------- ANIMATE ---------------------------
        self.frame_index += ANIMATION_SPEED * delta_time
        #self.image = self.frames[int(self.frame_index % len(self.frames))]
        #self.image = self.frames[self.state][int(self.frame_index % len(self.frames))]
        #self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image

        #self.get_state()

        if self.state == 'run':
            self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
            self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image
        elif self.state == 'death':
            if self.death_timer.active:
                self.frame_index += ANIMATION_SPEED * delta_time
                if int(self.frame_index) < len(self.frames['death']):
                    self.image = self.frames['death'][int(self.frame_index)]
                    self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image
                else:
                    self.image = self.frames['death'][4]  # Stay in the last frame


        # Check if the current state is in the frames dictionary
    #----------------------------------------------------------------------------------

    def movement(self, delta_time):
        #---------------------------------------------MOVEMENT-----------------------------------
        if self.state != 'death':
            self.rect.x += self.direction * self.speed * delta_time

            #reverse direction when hitting wall or end platform
            floor_rect_right = pygame.Rect(self.rect.bottomright, (1, 1))
            floor_rect_left = pygame.Rect(self.rect.bottomleft, (-1, 1))
            wall_rect = pygame.Rect(self.rect.topleft + vector(-1,0), (self.rect.width + 2, 1)) 

            if (floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0) or (floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0) or (wall_rect.collidelist(self.collision_rects) != -1): 
                self.direction *= -1
        else: 
            self.isalive = False
            #print("dead")
    #------------------------------------------------------------------------------------

    def update(self, delta_time):   
        self.hit_timer.update()
        self.death_timer.update()

        self.animate(delta_time)
        self.movement(delta_time)
        self.flicker()

class Shell(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, reverse, player, create_pearl, shell_sprite):
        super().__init__(groups)
        
        # Resize frames
        self.original_frames = {state: [pygame.transform.scale(frame, (86, 66)) for frame in state_frames] for state, state_frames in frames.items()}
        
        # Make a copy of original frames to apply transformations
        self.frames = self.original_frames.copy()
        
        # Reverse frames if needed
        if reverse:
            self.reverse_frames()
            self.bullet_direction = -1
        else:
            self.bullet_direction = 1

        # Adjust position to move the sprite and hitbox upwards
        pos = (pos[0], pos[1] - 20)  # Adjust as needed
        
        self.frame_index = 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        
        self.old_rect = self.rect.copy()
        self.z = Z_LAYERS['main']
        self.player = player
        
        self.shoot_timer = Timer(3000)
        self.hit_timer = Timer(250)
        self.death_timer = Timer(500)

        self.has_fired = False
        self.create_pearl = create_pearl
        self.shell_sprite = shell_sprite
        
        self.health = 5
        self.isalive = True

    def reverse_frames(self): #new function that so that the shell class is now resized and can handle the new sprites we have inserted.
            self.frames = {key: [pygame.transform.flip(surf, True, False) for surf in surfs] for key, surfs in self.original_frames.items()}

    def state_mangemant(self):
        player_pos, shell_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
        player_near = shell_pos.distance_to(player_pos) < 500
        player_front = shell_pos.x < player_pos.x if self.bullet_direction > 0 else shell_pos.x > player_pos.x
        player_level = abs(shell_pos.y - player_pos.y) < 30
        if self.state != 'death':
            if player_near and player_front and player_level and not self.shoot_timer.active:
                self.state = 'fire'
                self.frame_index = 0
                self.shoot_timer.activate()
                #print('player near')

    def hit_by_pearl(self):
        if not self.hit_timer.active:
            self.health -= 1
            self.hit_timer.activate()
            # Flicker effect
            if self.health > 0:
                #print('hit filcker')
                self.flicker()
            else:
                self.state = 'death'
                self.frame_index = 0
                self.death_timer.activate()
                self.alive = False

    def flicker(self):
        if self.hit_timer.active and sin(pygame.time.get_ticks() * 1000) >= 0: #cause sin oscillates between 1 and -1, so when it his 0 and the oteher codition is satisfiied then it will flicker
            flicker_image = self.image.copy()
            
            # Create a surface for the flickering effect
            flicker_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)  # Use SRCALPHA for transparency support
            flicker_surface.fill((255, 0, 0, 128))  # Fill with red color with some transparency
            
            # Apply the flickering effect to the copied image
            flicker_image.blit(flicker_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            # Set the flickered image as the player's image
            self.image = flicker_image
    
    def animate(self, delta_time):
        #----------------------- ANIMATIONS/ATTACK LOGIC -------------------------------
        if self.state == 'death':
            if self.death_timer.active:
                self.frame_index += ANIMATION_SPEED * delta_time
                if int(self.frame_index) < len(self.frames['death']):
                    self.image = self.frames['death'][int(self.frame_index)]  
                else:
                    self.image = self.frames['death'][4]  # Stay in the last frame
                    self.rect.bottom = pygame.display.get_surface().get_height()
        else:
            self.frame_index += ANIMATION_SPEED * delta_time
            if self.frame_index < len(self.frames[self.state]): #this is explained in 4:48:00
                self.image = self.frames[self.state][int(self.frame_index)]
                #fire
                if self.state == 'fire' and int(self.frame_index) == 3 and not self.has_fired:
                    #print('shoot pearl')
                    self.create_pearl(self.rect.center, self.bullet_direction, self.shell_sprite)
                    self.has_fired = True
            else:
                self.frame_index = 0
                if self.state == 'fire':
                    self.state = 'idle'
                    self.has_fired = False
    #-------------------------------------------------------------------------------

    def update(self, delta_time):
        self.shoot_timer.update()
        self.hit_timer.update()
        self.death_timer.update()
        
        self.state_mangemant()
        self.animate(delta_time)
        self.flicker()

class Pearl(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surf, direction, speed, shell_sprite):
        super().__init__(groups)
        self.pearl = True
        
        # Adjust position to move the sprite and hitbox upwards
        pos = (pos[0] - 5, pos[1] - 20)  # Adjust as needed

        self.image = surf
        self.rect = self.image.get_rect(center = pos + vector(50 * direction, 0))
        self.direction = direction
        self.speed = speed
        self.z = Z_LAYERS['main']

        self.timers = {'pearl_decay': Timer(5000), 'reverse': Timer(250)}
        self.timers['pearl_decay'].activate()

        self.shell_sprite = shell_sprite
        self.add(pearl_sprite) #you need to do this to add the pearl sprit to the group, initalize the pearl sprite so it can interact with the shell
          
    def hit_by_player(self):
        if not self.timers['reverse'].active:
            self.direction *= -1
            self.timers['reverse'].activate()

    def shoot_pearl(self, delta_time):
        self.rect.x += self.direction * self.speed * delta_time
    
    def check_collision(self):
        #print(len(self.shell_sprite.sprites()))
        #print(len(pearl_sprite.sprites()))

        for shell in self.shell_sprite.sprites():  # Use shell_sprite 
            pearls_collided = pygame.sprite.spritecollide(shell, pearl_sprite, True)  # Use pearl_group instead of self.pearl_sprites
            if pearls_collided:
                #print('hit')
                shell.hit_by_pearl()

    def update(self, delta_time):
        for timer in self.timers.values():
            timer.update()       
        
        self.shoot_pearl(delta_time)
        self.check_collision()
        
        if not self.timers['pearl_decay'].active:
            self.kill()
        



