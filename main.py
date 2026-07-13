import pygame, sys
from starting_screen import Starting_screen
from menu import Menu
from move_menu import Move_menu
from battle import Battle




class Game:
    def __init__(self):
        loading_screen = Starting_screen(400, 250)
        self.manhinh_khoidong = pygame.sprite.GroupSingle(loading_screen)
        menu_screen = Menu(400,250)
        self.manhinh_menu = pygame.sprite.GroupSingle(menu_screen)
        move_menu = Move_menu(400,250)
        self.move_menu = pygame.sprite.GroupSingle(move_menu)
        battle_screen = Battle(400,250)
        self.manhinh_battle = pygame.sprite.GroupSingle(battle_screen)
        self.menu_music_started = False
        self.battle_music_started = False
        self.cry_done = False

    def run(self, screen):
            if in_menu == 0:
                screen.fill((0, 0, 0))
                self.manhinh_khoidong.draw(screen)
                self.manhinh_khoidong.sprite.draw_button(screen)

            elif in_menu == 1:  
                if not self.cry_done:
                    screen.fill((0, 0, 0))
                    self.manhinh_khoidong.draw(screen)
                    self.manhinh_khoidong.sprite.draw_button(screen)
                    if not pygame.mixer.music.get_busy():  # cry finished
                        self.cry_done = True
                else:  # cry done, show menu
                    self.manhinh_menu.sprite.fade_in()
                    self.manhinh_menu.draw(screen)
                    self.manhinh_menu.sprite.draw_search(screen)
                    self.manhinh_menu.sprite.draw_search_item(screen)
                    self.manhinh_menu.sprite.draw_pokedex(screen)
                    self.manhinh_menu.sprite.draw_pokemon_animation(screen)
                    self.manhinh_menu.sprite.draw_item(screen)

                    if not self.menu_music_started:
                        self.manhinh_menu.sprite.play_music()
                        self.menu_music_started = True
            
            elif in_menu == 2:
                self.move_menu.draw(screen)
                self.move_menu.sprite.fade_in()
                self.move_menu.sprite.draw_screen(screen)

            elif in_menu == 3:
                self.manhinh_battle.draw(screen)
                self.manhinh_battle.sprite.fade_in()
                self.manhinh_battle.sprite.make_landscape(screen)
                self.manhinh_battle.sprite.draw_pokemon(screen)


                if not self.battle_music_started:
                    self.manhinh_battle.sprite.play_music()
                    self.battle_music_started = True



if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 500))
    pygame.display.set_caption("Pokemon Battle")
    clock = pygame.time.Clock()
    game = Game()
    in_menu = 0  # check if the player has pressed "Play"
    pokemon_name = ""
    pokemon_item = ""
    pokemon_ability = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if in_menu == 0: #if player hasnt pressed "Play"
                in_menu = game.manhinh_khoidong.sprite.check_state_button(event)
            elif in_menu == 1:
                game.manhinh_menu.sprite.handle_event(event)
                result = game.manhinh_menu.sprite.check_transfer(event) # check if we pressed the green button in the first menu
                if result is not None:
                    in_menu, pokemon_name, pokemon_item, pokemon_ability = result
                    game.move_menu.sprite.set_pokemon(pokemon_name, pokemon_item, pokemon_ability)
            elif in_menu == 2:
                game.move_menu.sprite.handle_event(event)
                result = game.move_menu.sprite.check_transfer(event)
                if result is not None:
                    in_menu = result
                    game.manhinh_battle.sprite.battle_set_pokemon(pokemon_name.lower(), pokemon_item, pokemon_ability, game.move_menu.sprite.selected_moves, game.move_menu.sprite.selected_nature) #take data for battle
            elif in_menu == 3:
                    game.manhinh_battle.sprite.handle_event(event)
            
        game.run(screen)

        pygame.display.flip()
        clock.tick(60)