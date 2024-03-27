import pygame
import sys

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 64
        self.vel = 5
        self.is_jumping = False
        self.jump_count = 10
        # Adding hitbox
        self.is_double_press = False
        self.last_down_press_time = 0# Initialize prev_key_time
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

 

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def move(self, keys_pressed, platforms):
        
        # Check if the player is on the ground (i.e., colliding with a platform)
        on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.y < platform.rect.y + platform.rect.height:
                on_ground = True
                break

        # Apply gravity if not jumping and not on the ground
        if not self.is_jumping and not on_ground:
            self.y += self.vel


        if keys_pressed[pygame.K_LEFT]  or keys_pressed[pygame.K_a] and self.x > 0:
            self.x -= self.vel
        
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d] and self.x < 800 - self.width:  # Assuming screen width is 800
            self.x += self.vel
        
        if not self.is_jumping:
            if keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
                self.is_jumping = True
        else:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count ** 2) * 0.3 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10
        

        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_down_press_time < 200:  # Time threshold for double press (200 milliseconds)
                self.is_double_press = True
            self.last_down_press_time = current_time
        else:
            self.is_double_press = False



        if self.is_double_press:
            platform_below = False
            for platform in platforms:
                if self.rect.colliderect(platform.rect) and self.y < platform.rect.y + platform.rect.height:
                    platform_below = True
                    break
            if not platform_below:
                self.y += self.vel * 2  # Adjust the speed as needed

        # Update hitbox position
        self.rect.topleft = (self.x, self.y)

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (100, 100, 100)  # Default color, you can customize it

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    player = Player(100, 400)
    platforms = [Platform(300, 500, 200, 20), Platform(200, 400, 200, 20)]  # Example platforms
    ground = Platform(0, 550, 800, 50)

    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys_pressed = pygame.key.get_pressed()
        player.move(keys_pressed, [ground] + platforms)  

        # Check collision between player and platforms
        # Check collision between player and platforms
        for platform in platforms:
            if player.rect.colliderect(platform.rect) and player.y < platform.rect.y + platform.rect.height:
                player.is_jumping = False
                player.jump_count = 10
                player.y = platform.rect.y - player.height
        
        player.draw(screen)


        # Draw ground platform
        ground.draw(screen)

        # Draw other platforms
        for platform in platforms:
            platform.draw(screen)

        pygame.display.flip()
        clock.tick(60)
if __name__ == "__main__":
    main()