from os.path import join
from settings import *
from level import Level
from pytmx.util_pygame import load_pygame



class Game:
    def __init__(self):
    #------------------    INITALIZE PYGAME SCREEN              --------------------------------------
        pygame.init()
        self.screen_display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Knight Knight Runner") 
    #--------------------------------------------------------

    #-------------------------- Stages -----------------
        self.tmx_maps = {0: load_pygame(join('..', 'data', 'levels', 'omni.tmx'))}
        
        print(join('..', 'data', 'levels', 'omni.tmx'))
        self.current_stage = Level(self.tmx_maps[0])
    #----------------------------------------------------

    def run(self):
        running = True 
        while running: #run
        # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit() #Forces to leave the loop

            self.current_stage.run() #Current stage

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()




