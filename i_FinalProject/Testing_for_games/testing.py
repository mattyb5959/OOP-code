import pygame
import sys  
from random import randint, choice
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))





def main():
    #------------------    INITALIZE PYGAME SCREEN              --------------------------------------

    pygame.init() #initalize pygame
    WIDTH, HEIGHT = 800, 600 #screen size width and height
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Create teh screen
    pygame.display.set_caption("Knight Knight Runner") 

    #--------------------------------------------------------

    #-------------------------     START PROGRAM STUFF  -------------
    clock = pygame.time.Clock()
    test_font = pygame.font.Font('font/Pixeltype.ttf', 50) #Change this 
    game_active = False
    start_time = 0
    score = 0
    #bg_music = pygame.mixer.Sound('audio/music.wav')
    #bg_music.play(loops = -1)
    #------------------------------------------------------------  

    #---------------------------- ADD SPRITES AND STUFF HERE -----------------

    sky_surface = pygame.image.load('graphics/Sky.png').convert()
    ground_surface = pygame.image.load('graphics/ground.png').convert()

    #------------------------------------------------------------

    #----------------------    MAIN GAME LOOP         ---------------------------------

    running = True #clears up any confusion about what true does
    while running: #run
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False #Forces to leave the loop


        # Draw everything to the screen
        screen.fill((0, 0, 0))  # Fill the screen with black
        
        #Add Drawings below

        pygame.display.flip()  # Update the display

    pygame.quit()
    sys.exit()
    #--------------------------------------------------------   


if __name__ == "__main__":
    main()
