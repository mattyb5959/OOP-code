from settings import *
from os.path import join
from timer import Timer
from math import sin
from enemies import Tooth


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, semi_collision_sprites, frames, data, attack_sound, jump_sound):
        #general setup
        super().__init__(groups)
        self.z = Z_LAYERS['main']
        
        self.data = data
    #--------------------------------- images ---------------
        self.frames =  {state: [pygame.transform.scale(frame, (86, 66)) for frame in state_frames] for state, state_frames in frames.items()} #so we can resize it
        self.frame_index = 0
        self.state, self.facing_right = 'idle', True
        self.image = self.frames[self.state][self.frame_index] 
        
        #self.image = pygame.draw.rect(self.rect, (0, 0, 0), )
    #-------------------------------------------------------------
        
    #--------------------------------- rectangles ---------------
        self.rect = self.image.get_rect(topleft = pos) #this is the players hitbox
        hitbox_width = self.rect.width - 50 # Adjust as needed
        hitbox_height = self.rect.height - 55  # Adjust as needed
        self.hitbox_rect = self.rect.inflate(-hitbox_width, -hitbox_height)
        self.old_rect = self.hitbox_rect.copy()

        #self.hitbox_rect = self.rect.inflate(-76, -36)
        #self.old_rect = self.hitbox_rect.copy()
    #-------------------------------------------------------------

    #--------------------------------- movement----------------------------------------
        self.direction = vector()
        self.speed = 200
        self.gravity = 1300
        self.jump = False
        self.jump_height = 900
        self.attacking = False
    #----------------------------------------------------------------------------------
    
    #--------------------------------- Collisons----------------------------------------
        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        self.platform = None
    #-----------------------------------------------------------------------------------

        #self.display_surface = pygame.display.get_surface()
    
    #--------------------------------- Timer ----------------------------------------
        self.timers = {
            'wall jump': Timer(400),
            'wall slide block': Timer(250),
            'platform skip': Timer(100),
            'attack block': Timer(500),
            'hit timer': Timer(800)
        }

    #--------------------------------------------------------------------------------

    #--------------------------------- Audio ----------------------------------------
        self.attack_sound = attack_sound
        self.attack_sound.set_volume(0.5)
        self.jump_sound = jump_sound
        self.jump_sound.set_volume(0.5)
    #--------------------------------------------------------------------------------

    def player_input(self):
        key_pressed = pygame.key.get_pressed() 
        input_vector = vector(0,0) #new vector with no values, every frame input vector starts 0,0
        #However when a player presses a button then the player will move and right but if they presse both it wont move

        if key_pressed[pygame.K_SPACE] or key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
            #print('up')
            self.jump = True
            self.timers['wall jump'].activate()

        if not self.timers['wall jump'].active:
            if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
            #print('down')
                self.timers['platform skip'].activate()

            if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
                #print('left')
                input_vector.x -= 1
                self.facing_right = False

            if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
                #print('right')
                input_vector.x += 1
                self.facing_right = True
            
            if key_pressed[pygame.K_q] or key_pressed[pygame.K_j]:
                self.attack()
    
            
            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x #normalize will make the length of vector ALWAYS = 1 that way we ensure that the vector ONLY sets the directio

    def attack(self):
        if not self.timers['attack block'].active:
            self.attacking = True
            self.frame_index = 0
            self.timers['attack block'].activate()
            self.attack_sound.play()

 # Call hit_by_player method of tooth sprite  
    def move(self, delta_time):
        
        self.old_rect = self.hitbox_rect.copy()
    #--------------------------------- Horizontal ----------------------------------------    
        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        self.collision('horizontal')
    #-------------------------------------------------------------------------------------
    
    #--------------------------------- Vertical----------------------------------------
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
            self.direction.y = 0
            self.hitbox_rect.y += self.gravity / 10 * delta_time
        
        else:
            self.direction.y += self.gravity / 2 * delta_time
            self.hitbox_rect.y += self.direction.y  * delta_time #so that the gravity increases with time
            self.direction.y += self.gravity / 2 * delta_time
        
            #The code below does not work because it is not frame rate dependent. It may look like it with delta time
        #However if the frame rate changes you would get different behavior.
        #self.rect.y += self.gravity * delta_time
        #self.rect.y += self.direction.y #so that the gravity increases with time

    #-----------------------------------------------------------------------------------

        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.timers['wall slide block'].activate()
                self.hitbox_rect.bottom -= 1 
                self.jump_sound.play()
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
                self.timers['wall jump'].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1
                self.jump_sound.play()
            self.jump = False
        #print(self.direction.y) #The gravity should not be increaseing while on a platform
        
        self.collision('vertical')
        self.semi_collision()
        self.rect.center = self.hitbox_rect.center

    def platform_move(self, delta_time):
        #print(self.platform)
        if self.platform:
            #print('standing on platfrom')
            #self.hitbox_rect.topleft += self.platform.direction * self.platform.speed * delta_time      #Uncomment this if bug testing fails - Seperate platforms vertical and horizontal change how it interacts with vertical
            #self.old_rect.topleft += self.platform.direction * self.platform.speed * delta_time
                

            # Check if the player is within the platform's hitbox vertically
            if self.platform.rect.top <= self.hitbox_rect.centery <= self.platform.rect.bottom:                                                 #Vertical Moving platform
                # Update the player's position to move with the platform
                self.hitbox_rect.bottom += self.platform.direction.y * self.platform.speed * delta_time

            # Check if the player is within the platform's hitbox horizontally
            else:                                                                                                                               #Horizontal Movement
                # Update the player's position to move with the platform
                self.hitbox_rect.right += self.platform.direction.x * self.platform.speed * delta_time

            #print('standing on playform', self.hitbox_rect.topleft)

        else:
            pass
            #print('not on platform')

        #print('working?')

    def check_contact(self):
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2))
        right_rect = pygame.Rect(self.hitbox_rect.topright + vector(0, self.hitbox_rect.height/4), (2, self.hitbox_rect.height / 2))
        #pygame.draw.rect(self.display_surface, 'black', right_rect)                                                                                #<- explain this 
        left_rect = pygame.Rect(self.hitbox_rect.topleft + vector(-2, self.hitbox_rect.height/4), (2, self.hitbox_rect.height / 2))
       
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        semi_collide_rect = [sprite.rect for sprite in self.semi_collision_sprites]
        #pygame.rect(Left, Top, Width, Height)
        #with did two tupoles (left, top) and (right, bottom)
        #feet_position = self.hitbox_rect.bottomleft

        #check rects
        #pygame.draw.rect(self.display_surface, 'orange', floor_rect)
        #pygame.draw.rect(self.display_surface, 'orange', right_rect)
        #pygame.draw.rect(self.display_surface, 'orange', left_rect)

        
        #collisions
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 or floor_rect.collidelist(semi_collide_rect) >= 0 and self.direction.y >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False 
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False
        #print(self.on_surface)

        #if not any(self.on_surface.values()):
            #self.platform = None
        
        on_platform = False
        self.platform = None
        sprites = self.collision_sprites.sprites() + self.semi_collision_sprites.sprites()
        #print([sprite for sprite in sprites if hasattr(sprite, 'moving')])
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            #print("Sprite attributes:", dir(sprite))
            if sprite.rect.colliderect(floor_rect):
                on_platform = True
                self.platform = sprite
                #print('floor')
            #else:
                #print('yes')
                #self.on_surface['floor'] = True
                #print(sprite)
                #print(self.platform)

        self.on_surface['floor'] = on_platform or floor_rect.collidelist(collide_rects) >= 0 or floor_rect.collidelist(semi_collide_rect) >= 0
        self.on_surface['right'] = right_rect.collidelist(collide_rects) >= 0
        self.on_surface['left'] = left_rect.collidelist(collide_rects) >= 0

        if not self.on_surface['floor']:
            self.platform = None
                   
    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect): #checks overlap with the player
                if axis == 'horizontal':
                        #print('overlap')
                #----------------- Does it come from left? ---------------------
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right):
                        self.hitbox_rect.left = sprite.rect.right
                #---------------------------------------------------------------
                #----------------- Does it come from right? ---------------------
                    if self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left):
                        self.hitbox_rect.right = sprite.rect.left
                #---------------------------------------------------------------
                

                else: # vert
                #----------------- Does it come from above? ---------------------
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
                        self.hitbox_rect.top = sprite.rect.bottom 
                        if hasattr(sprite, 'moving'):
                            self.hitbox_rect.top += 10
                #---------------------------------------------------------------
                #----------------- Does it come from below? ---------------------
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top
                #--------------------------------------------------------------

                self.direction.y = 0 

    def semi_collision(self):
        if not self.timers['platform skip'].active:
            for sprite in self.semi_collision_sprites:
                if sprite.rect.colliderect(self.hitbox_rect):
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:
                        self.hitbox_rect.bottom = sprite.rect.top
                        if self.direction.y > 0:
                            self.direction.y = 0

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def animate(self, delta_time):
        self.frame_index += ANIMATION_SPEED * delta_time
        
        if self.state == 'attack' and self.frame_index >= len(self.frames[self.state]):
            self.state = 'idle'
        
        #print(f' frame index = {self.frame_index} state = {self.state}, dt = {delta_time} image = {self.image}')
       
        #print(self.frames)

        # resized_frames = {}
        # for state, frames in self.frames.items():
        #     resized_frames[state] = [pygame.transform.scale(frame, (110, 96)) for frame in frames]

        # self.image = resized_frames[self.state][int(self.frame_index % len(resized_frames[self.state]))]
        # self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)

        # if self.attacking and self.frame_index > len(self.frames[self.state]):
        #     self.attacking = False

        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)

        if self.attacking and self.frame_index > len(self.frames[self.state]):
            self.attacking = False

        debuging = int(self.frame_index % len(self.frames[self.state]))
        change_time_to_frame_number_by_mod = len(self.frames[self.state])
        #print(f'state = {self.state}, self.frame_index = {self.frame_index}, time to num mod = {change_time_to_frame_number_by_mod}, image = {debuging}')

    def get_state(self):
        if self.on_surface['floor']:
            if self.attacking:
                self.state = 'attack'
            else:
                self.state = 'idle' if self.direction.x == 0 else 'run'
        else:
            if self.attacking:
                self.state = 'air_attack'
            else:
                if any((self.on_surface['left'], self.on_surface['right'])):
                    self.state = 'wall'
                else: 
                    self.state = 'jump' if self.direction.y < 0 else 'fall'

    def get_damage(self):
        if not self.timers['hit timer'].active:
            #print('player was damaged')
            self.data.health -= 1
            self.timers['hit timer'].activate()

    def flicker(self):
        if self.timers['hit timer'].active and sin(pygame.time.get_ticks() * 600) >= 0: #cause sin oscillates between 1 and -1, so when it his 0 and the oteher codition is satisfiied then it will flicker
            white_mask = pygame.mask.from_surface(self.image)
            white_surf = white_mask.to_surface()
            white_surf.set_colorkey('black')
            self.image = white_surf

    def update(self, delta_time):
        self.old_rect = self.hitbox_rect.copy()
        self.update_timers()
        
        self.player_input()
        self.move(delta_time)
        self.platform_move(delta_time)
        self.check_contact()

        self.get_state()
        self.animate(delta_time)

        self.flicker()
        #print(self.on_surface)
        #print('updating?')
        #print(self.timers['wall jump'].active)
        #print(self.timers['wall slide block'].active)

        #-------------------------TESTING------------------------------------------




