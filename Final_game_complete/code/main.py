from os.path import join
from tkinter import W
from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from support import *
from data import Data
from debug import debug  
from ui import UI
from overworld import Overworld
from timer import Timer

class Game:
    def __init__(self):
    #------------------    INITALIZE PYGAME SCREEN              --------------------------------------
        pygame.init()
        self.screen_display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Knight Knight Runner") 

        self.clock = pygame.time.Clock() #normalize the frame rate  through diff ocomputers
        self.import_assets()
    #--------------------------------------------------------

    #-------------------------- Stages -----------------
        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui) #we create data so that we keep all the data and does not change when we change level
        self.tmx_maps = {
            0: load_pygame(join('..', 'data', 'levels', '0.tmx')), 
            1: load_pygame(join('..', 'data', 'levels', '1.tmx')), 
            2: load_pygame(join('..', 'data', 'levels', '2.tmx')),
            3: load_pygame(join('..', 'data', 'levels', '2.tmx'))}
        
        self.tmx_overworld = load_pygame(join('..', 'data', 'overworld', 'overworld.tmx'))
        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
        #self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames)
        #print(join('..', 'data', 'levels', 'omni.tmx'))
    #----------------------------------------------------
        
        self.bg_music.play(-1)
       
        self.game_active = False
        self.game_over_timer = 0

    def switch_stage(self, target, unlock = 0): 
        if target == 'level':
            self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
        else:
            if unlock > 0:
                self.data.unlocked_level = unlock
            else:
                self.data.health -= 1
            self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames,  self.switch_stage)
            #print(target)
            #print(unlock)

    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('..', 'graphics', 'level', 'flag'),
            'saw': import_folder('..', 'graphics', 'enemies', 'saw', 'animation'),
            'floor_spike': import_folder('..', 'graphics', 'enemies', 'floor_spikes'),
            'palms': import_sub_folders('..', 'graphics', 'level', 'palms'),
            'candle': import_folder('..', 'graphics', 'level', 'candle'),
            'window': import_folder('..', 'graphics', 'level', 'window'),
            'big_chain': import_folder('..', 'graphics', 'level', 'big_chains'),
            'small_chain': import_folder('..', 'graphics', 'level', 'small_chains'),
            'candle_light': import_folder('..', 'graphics', 'level', 'candle light'),
            'player': import_sub_folders('..', 'graphics', 'player'),
            'saw': import_folder('..', 'graphics', 'enemies', 'saw', 'animation'),
            'saw_chain': import_image('..', 'graphics', 'enemies', 'saw', 'saw_chain'),
            'helicopter': import_folder('..', 'graphics', 'level', 'helicopter'),
            'boat': import_folder('..', 'graphics', 'objects', 'boat'),
            'spike': import_image('..', 'graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
            'spike_chain': import_image('..', 'graphics', 'enemies', 'spike_ball', 'spiked_chain'),
            'tooth': import_sub_folders('..', 'graphics','enemies', 'tooth'),                                              #'tooth': import_folder('..', 'graphics','enemies', 'tooth', 'run'),
            'shell': import_sub_folders('..', 'graphics','enemies', 'shell'),
            'pearl': import_image('..',  'graphics', 'enemies', 'bullets', 'pearl'),
            'items': import_sub_folders('..', 'graphics', 'items'),
            'particle': import_folder('..', 'graphics', 'effects', 'particle'),
            'water_top': import_folder('..', 'graphics', 'level', 'water', 'top'),
			'water_body': import_image('..', 'graphics', 'level', 'water', 'body'),
			'bg_tiles': import_folder_dict('..', 'graphics', 'level', 'bg', 'tiles'),
			'cloud_small': import_folder('..', 'graphics','level', 'clouds', 'small'),
			'cloud_large': import_image('..', 'graphics','level', 'clouds', 'large_cloud')

        }
        #print(self.level_frames)

        self.font = pygame.font.Font(join('..', 'graphics', 'ui', 'runescape_uf.ttf'), 40)

        self.ui_frames = {
			'heart': import_folder('..', 'graphics', 'ui', 'heart'), 
			'coin':import_image('..', 'graphics', 'ui', 'coin')
        }

        self.overworld_frames = {
        'palms': import_folder('..', 'graphics', 'overworld', 'palm'),
        'water': import_folder('..', 'graphics', 'overworld', 'water'),
        'path': import_folder_dict('..', 'graphics', 'overworld', 'path'),
        'icon': import_sub_folders('..', 'graphics', 'overworld', 'icon')
        }

        self.audio_files = {
            'coin': pygame.mixer.Sound(join('..', 'audio', 'coin.wav')),
            'attack': pygame.mixer.Sound(join('..', 'audio', 'attack.wav')),
            'jump': pygame.mixer.Sound(join('..', 'audio', 'jump.wav')), 
            'damage': pygame.mixer.Sound(join('..', 'audio', 'damage.wav')),
            'pearl': pygame.mixer.Sound(join('..', 'audio', 'pearl.wav')),
        }
        
        self.bg_music = pygame.mixer.Sound(join('..', 'audio', '2021-08-17_-_8_Bit_Nostalgia_-_www.FesliyanStudios.com.mp3'))
        self.bg_music.set_volume(0.5)

    def check_game_over(self):
        game_over = self.font.render('Game Over', False, (255, 255, 255))
        game_over_rect = game_over.get_rect(center = (640 , 360))

        if self.data.health <= 0:
            self.game_over_timer = pygame.time.get_ticks()
            self.screen_display.fill((0, 0, 0))
            self.screen_display.blit(game_over, game_over_rect)
            pygame.display.update()
            
            while pygame.time.get_ticks() - self.game_over_timer < 1000:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
            continue_level = self.font.render('Replay Level', False, (255, 255, 255))
            continue_level_rect = continue_level.get_rect(center = (640 , 260))

            exit_game = self.font.render('Exit Game', False, (255, 255, 255))
            exit_game_rect = exit_game.get_rect(center = (640 , 460))

            self.screen_display.fill((0, 0, 0))
            self.screen_display.blit(continue_level, continue_level_rect)
            self.screen_display.blit(exit_game, exit_game_rect)
            pygame.display.update()

            while True:
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                if continue_level_rect.collidepoint(mouse_pos) and mouse_click[0]:
                    self.game_active = True
                    self.data.health = 5
                    self.switch_stage('level')
                    return

                elif exit_game_rect.collidepoint(mouse_pos) and mouse_click[0]:
                    pygame.quit()
                    sys.exit()                 

    def intro_screen(self): 
        #C:\\Users\\MatyuGuerrero\\Desktop\\Python\\OOP Applications\\i_FinalProject\\graphics\\player\\player_stand.png
        image_path = 'C:\\Users\\MatyuGuerrero\\Desktop\\Python\\OOP Applications\\i_FinalProject\\graphics\\player\\player_stand.png'
        
        try: 
            player_stand = pygame.image.load(image_path).convert_alpha()
            player_stand = pygame.transform.scale(player_stand, (86, 66))
            player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
            player_stand_rect = player_stand.get_rect(center = (640, 360))

            game_name = self.font.render('One Knight', False, (111, 196, 169))
            game_name_rect = game_name.get_rect(center = (640, 260))

            game_message = self.font.render('Press space to run', False,(111,196,169))
            game_message_rect = game_message.get_rect(center = (640, 460))
        except FileNotFoundError:
            print(f"Error: File '{image_path}' not found.")
        
        self.screen_display.fill((94, 129, 162))
        self.screen_display.blit(player_stand, player_stand_rect)  
        self.screen_display.blit(game_name, game_name_rect)
        self.screen_display.blit(game_message, game_message_rect)    

    def run(self):
        running = True 
        while running: #run
        # Handle events
            delta_time = self.clock.tick(60) / 1000
            #print(delta_time)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit() #Forces to leave the loop
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        #print('true')
                        self.game_active = True


            if self.game_active:
                #print('running')
                self.check_game_over()
                self.current_stage.run(delta_time) #Current stage
                self.ui.update(delta_time)
                #debug(self.data.health)
                #debug(self.data.coins)

            else:
                self.intro_screen()


            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()




