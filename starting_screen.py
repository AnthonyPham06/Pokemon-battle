import pygame, sys


class Starting_screen(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        pygame.mixer.init()
        pygame.mixer.music.load('starting_music.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, start =22.0)

        
        self.image = pygame.image.load('Starting_screen.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.image,(int(self.image.get_width()*0.66),int(self.image.get_height()*0.595)))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (x,y))

        self.starting_button = pygame.image.load('starting_button.png').convert_alpha()
        self.starting_button = pygame.transform.scale(self.starting_button,(int(self.starting_button.get_width()*0.25),int(self.starting_button.get_height()*0.25)))
        self.starting_button_rect = self.starting_button.get_rect(center=(400, 330))

        self.exit_button = pygame.image.load('exit_button.png').convert_alpha()
        self.exit_button = pygame.transform.scale(self.exit_button,(int(self.exit_button.get_width()*0.19),int(self.starting_button.get_height()*0.87)))
        self.exit_button_rect = self.exit_button.get_rect(center=(400, 410))

    def draw_button(self, screen):
        screen.blit(self.starting_button, self.starting_button_rect)
        screen.blit(self.exit_button, self.exit_button_rect)

    def check_state_button(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.starting_button_rect.collidepoint(event.pos):
                pygame.mixer.music.load('raquaza_cry.mp3')
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(0, start=1.4, fade_ms=2)
                return 1
            
            elif self.exit_button_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
        return 0
    

    

    def play_music(self):
        pass
