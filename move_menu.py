import pygame
import json
from menu import Menu

class Move_menu(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()

        #create background
        self.image = pygame.image.load('menu_screen.jpg').convert_alpha()
        self.original_image = pygame.transform.scale(self.image,(int(self.image.get_width()*0.25),int(self.image.get_height()*0.25)))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (x,y))
        self.alpha = 0  # start fully transparent
        self.image.set_alpha(self.alpha)


        # create backing arrow
        self.back_arrow = pygame.image.load('menu_sprites/back_arrow.png').convert_alpha()
        self.back_arrow = pygame.transform.scale(self.back_arrow,(int(self.back_arrow.get_width()*0.2),int(self.back_arrow.get_height()*0.2)))
        self.back_arrow_rect = self.back_arrow.get_rect(center =(20,40))


        # create the ui for the menu
        self.move_table = pygame.image.load('menu_sprites/move_box.png').convert_alpha()
        self.move_table = pygame.transform.scale(self.move_table,(int(self.move_table.get_width()*1.7),int(self.move_table.get_height()*10)))
        self.move_table_rect = self.move_table.get_rect(center =(400,200))

        #font
        self.pokemon_name_font = pygame.font.Font('pokemon_pixel_font.ttf', 35) #font for pokemon name
        self.pokemon_ability_font = pygame.font.Font('pokemon_pixel_font.ttf', 35)
        self.pokemon_item_font = pygame.font.Font('pokemon_pixel_font.ttf', 35)
        self.nature_and_move_description_font = pygame.font.Font('pokemon_pixel_font.ttf', 26)

        # ui
        self.ui_pokemon = pygame.image.load('menu_sprites/move_menu_ui.png').convert_alpha()
        self.ui_pokemon = pygame.transform.scale(self.ui_pokemon,(int(self.ui_pokemon.get_width()*0.57),int(self.ui_pokemon.get_height()*0.62)))
        self.ui_pokemon_rect = self.ui_pokemon.get_rect(center =(417,250))


        #pokemon name and rotating variables
        self.pokemon_name = ""
        self.last_time = 0
        self.sprite_turn = 0

        # read the move lsit
        with open('moves.json', 'r') as f: #from moves.json
            move_list = json.load(f)
        self.move_name = {p["name"].lower(): p for p in move_list} 
        
        #read learnable move
        with open('pokemon_data.json', 'r') as f: # see the learnable list
            self.pokemon_data = {p["name"]: p for p in json.load(f)}

        #read nature
        with open('pokemon_nature.json', 'r') as f:
            nature_list = json.load(f)
            self.pokemon_nature =  {p["nature"]: p for p in nature_list}
            self.pokemon_nature_description = {p["nature"]: p["description"] for p in nature_list}
            
        # nature search variables
        self.nature_rect = pygame.Rect(400, 35, 150, 40)  # adjust position to fit your UI
        self.nature_text = ""
        self.nature_active = False
        self.nature_results = []
        self.nature_selected = False
        self.selected_nature = ""
        self.selected_nature_description = ""


        # draw move search
        self.move_search_rects = [
        pygame.Rect(400, 150, 200, 40),
        pygame.Rect(400, 205, 200, 40),
        pygame.Rect(400, 250, 200, 40),
        pygame.Rect(400, 300, 200, 40)
        ]
        self.move_searches = ["", "", "", ""]
        self.move_active = [False, False, False, False]
        self.move_results = [[], [], [], []]
        self.move_selected = [False, False, False, False]
        self.selected_moves = ["", "", "", ""]
        self.hovered_move = -1 # check if the mouse is place at the block


        #move damage type
        self.physical_attack_icon = pygame.image.load('move_sprites/physical.png').convert_alpha()
        self.physical_attack_icon = pygame.transform.scale(self.physical_attack_icon,(int(self.physical_attack_icon.get_width()*0.1),int(self.physical_attack_icon.get_height()*0.1)))

        self.special_attack_icon = pygame.image.load('move_sprites/special.png').convert_alpha()
        self.special_attack_icon = pygame.transform.scale(self.special_attack_icon,(int(self.special_attack_icon.get_width()*0.085),int(self.special_attack_icon.get_height()*0.085)))

        self.status_icon = pygame.image.load('move_sprites/status.png').convert_alpha()
        self.status_icon = pygame.transform.scale(self.status_icon,(int(self.status_icon.get_width()*0.11),int(self.status_icon.get_height()*0.11)))

        # enter battle arrow
        self.battle_arrow = pygame.image.load('menu_sprites/enter_arrow.png').convert_alpha()
        self.battle_arrow = pygame.transform.scale(self.battle_arrow,(int(self.battle_arrow.get_width()*0.2),int(self.battle_arrow.get_height()*0.2)))
        self.battle_arrow_rect = self.battle_arrow.get_rect(center =(20,90))



        
    def check_transfer(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_arrow_rect.collidepoint(event.pos):
                return 1
            elif self.battle_arrow_rect.collidepoint(event.pos) and all(self.move_selected) and self.nature_selected: # this check if the battle arrow is clicked, then proceed to battle
                return 3
        
        return None
    
    
    def set_pokemon(self, name,item_name,ability_name):
        if name != self.pokemon_name: # this special line solve the charmander fly bug
            self.move_searches = ["", "", "", ""]
            self.move_active = [False, False, False, False]
            self.move_results = [[], [], [], []]
            self.move_selected = [False, False, False, False]
            self.selected_moves = ["", "", "", ""]
            self.nature_text = ""
            self.nature_active = False
            self.nature_results = []
            self.nature_selected = False
            self.selected_nature = ""
            self.selected_nature_description = ""
            self.alpha = 0
            self.image.set_alpha(0)
        self.pokemon_name = name
        self.pokemon_item = item_name
        self.pokemon_ability = ability_name
        self.move_suitable = self.pokemon_data[self.pokemon_name]["Learnable"]

    
    def fade_in(self): # transition into the menu page
        if self.alpha < 255:
            self.alpha += 4  # speed of fade, adjust as needed
            self.image.set_alpha(self.alpha)


    def draw_screen(self,screen):
        screen.blit(self.move_table,self.move_table_rect)
        screen.blit(self.back_arrow,self.back_arrow_rect)

        if all(self.move_selected) and self.nature_selected: # show arrow only when all the actions are done
            screen.blit(self.battle_arrow,self.battle_arrow_rect)

        screen.blit(self.ui_pokemon,self.ui_pokemon_rect)
        self.write_pokemon_name(screen)
        self.write_pokemon_ability(screen)
        self.write_and_draw_item(screen)
        self.draw_pokemon(screen)
        self.draw_move_search(screen)
        self.draw_nature_search(screen)
        self.show_move_description(screen)


    def write_pokemon_name(self,screen):
        text_surface = self.pokemon_name_font.render(self.pokemon_name, True, (0, 0, 0)) 
        screen.blit(text_surface,(120,10))


    def write_pokemon_ability(self,screen):
        ability_surface = self.pokemon_ability_font.render(self.pokemon_ability, True, (0,0,0))
        screen.blit(ability_surface,(57,60))


    def write_and_draw_item(self, screen):
        item_sprite = pygame.image.load(f'held_items/{self.pokemon_item}.png').convert_alpha()
        item_sprite = pygame.transform.scale(item_sprite,(int(item_sprite.get_width()*0.5),int(item_sprite.get_height()*0.5)))
        item_sprite_rect = item_sprite.get_rect(center =(90,405))
        screen.blit(item_sprite,item_sprite_rect)
        item_text_surface = self.pokemon_item_font.render(self.pokemon_item, True,(0,0,0))
        screen.blit(item_text_surface,(140,405))

    
    def draw_pokemon(self, screen):

        self.pokemon_front = pygame.image.load(f'pokemon_sprites/{self.pokemon_name}/{self.pokemon_name}_front.png').convert_alpha()
        self.pokemon_front = pygame.transform.scale(self.pokemon_front,(int(self.pokemon_front.get_width()*0.6),int(self.pokemon_front.get_height()*0.6)))
        self.pokemon_front_rect = self.pokemon_front.get_rect(center=(200,250))

        self.pokemon_back = pygame.image.load(f'pokemon_sprites/{self.pokemon_name}/{self.pokemon_name}_back.png').convert_alpha()
        self.pokemon_back = pygame.transform.scale(self.pokemon_back,(int(self.pokemon_back.get_width()*0.6),int(self.pokemon_back.get_height()*0.6)))
        self.pokemon_back_rect = self.pokemon_back.get_rect(center=(200,250))

        current_time =pygame.time.get_ticks()
        if current_time - self.last_time >= 333:
            self.sprite_turn = 1 - self.sprite_turn
            self.last_time = current_time

        if self.sprite_turn == 0:
            screen.blit(self.pokemon_front, self.pokemon_front_rect)
        else:
            screen.blit(self.pokemon_back, self.pokemon_back_rect)

    

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.nature_active = self.nature_rect.collidepoint(event.pos)

            for i, nature_name in enumerate(self.nature_results[:3]):
                result_rect = pygame.Rect(self.nature_rect.x, self.nature_rect.bottom + i * 35, self.nature_rect.width, 30)
                if result_rect.collidepoint(event.pos):
                    self.nature_text = nature_name
                    self.nature_results = []
                    self.nature_active = False
                    self.nature_selected = True
                    self.selected_nature = nature_name
                    self.selected_nature_description = self.pokemon_nature_description[nature_name]

        if event.type == pygame.KEYDOWN and self.nature_active:
            if event.key == pygame.K_BACKSPACE:
                self.nature_text = self.nature_text[:-1]
                self.nature_selected = False
            else:
                self.nature_text += event.unicode

            if self.nature_text:
                self.nature_results = []
                for name in self.pokemon_nature:
                    if self.nature_text.lower() in name.lower():
                        self.nature_results.append(name)
            else:
                self.nature_results = []


        for i in range(4):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.move_active[i] = self.move_search_rects[i].collidepoint(event.pos)  
                for j, move_name in enumerate(self.move_results[i][:3]):
                    result_rect = pygame.Rect(self.move_search_rects[i].x, self.move_search_rects[i].bottom + j * 35, self.move_search_rects[i].width, 30)
                    if result_rect.collidepoint(event.pos):
                        self.move_searches[i] = move_name
                        self.move_results[i] = []
                        self.move_active[i] = False
                        self.move_selected[i] = True
                        self.selected_moves[i] = move_name

            if event.type == pygame.KEYDOWN and self.move_active[i]:
                if event.key == pygame.K_BACKSPACE:
                    self.move_searches[i] = self.move_searches[i][:-1]
                    self.move_selected[i] = False
                    self.selected_moves[i] = ""

                else:
                    self.move_searches[i] += event.unicode

                if self.move_searches[i]:
                    self.move_results[i] = []
                    for name in self.move_suitable:
                        if (self.move_searches[i].lower() in name.lower()) and name not in self.selected_moves:
                            self.move_results[i].append(name)
                else:
                    self.move_results[i] = []


            if event.type == pygame.MOUSEMOTION:
                self.hovered_move = -1
                for i in range(4):
                    if self.move_search_rects[i].collidepoint(event.pos) and self.selected_moves[i] != "":
                        self.hovered_move = i

                    

    def draw_nature_search(self, screen): # draw the search for nature

    # show cursor if active
        if self.nature_active:
            display_text = self.nature_text + "|"

        elif self.nature_text == "":
            display_text = "Enter nature"

        else:
            display_text = self.nature_text

        text_surface = self.pokemon_name_font.render(display_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.nature_rect.x , self.nature_rect.y ))

        

    # draw dropdown results
        if self.nature_results:
            for i, name in enumerate(self.nature_results[:2]):
                result_rect = pygame.Rect(self.nature_rect.x, self.nature_rect.bottom + i * 35, 300, 35)
                pygame.draw.rect(screen, (0, 0, 0), result_rect)
                pygame.draw.rect(screen, (255, 255, 255), result_rect, 1)
                name_surface = self.pokemon_name_font.render(name, True, (255, 255, 255))
                screen.blit(name_surface, (result_rect.x + 8, result_rect.y + 5))

        if self.nature_selected:
            description_surface = self.nature_and_move_description_font.render(self.selected_nature_description, True, (0, 0, 0))
            screen.blit(description_surface, (590,35))



    def draw_move_search(self, screen):
        for i in range(4):
            if self.move_active[i]:
                display_text = self.move_searches[i] + "|"
            elif self.move_searches[i] == "":
                display_text = "Enter move"
            else:
                display_text = self.move_searches[i]

            text_surface = self.pokemon_name_font.render(display_text, True, (255, 255, 255))
            screen.blit(text_surface, (self.move_search_rects[i].x, self.move_search_rects[i].y))

        for i in range(4):
            if self.move_results[i]:
                for j, move_name in enumerate(self.move_results[i][:3]):
                    result_rect = pygame.Rect(self.move_search_rects[i].x, self.move_search_rects[i].bottom + j * 35, 300, 35)
                    pygame.draw.rect(screen, (0, 0, 0), result_rect)
                    pygame.draw.rect(screen, (255, 255, 255), result_rect, 1)
                    name_surface = self.pokemon_name_font.render(move_name, True, (255, 255, 255))
                    screen.blit(name_surface, (result_rect.x + 8, result_rect.y + 5))

            if self.move_selected[i] and self.selected_moves[i]:
                move = self.move_name[self.selected_moves[i].lower()]
                if move["damage_type"] == "Physical":
                    self.physical_attack_icon_rect = self.physical_attack_icon.get_rect(center=(650,170+i*50)) # draw the phy attack icon
                    screen.blit(self.physical_attack_icon,self.physical_attack_icon_rect)
                elif move["damage_type"] == "Special":
                    self.special_attack_icon_rect = self.special_attack_icon.get_rect(center=(650,170+i*50)) # draw the phy attack icon
                    screen.blit(self.special_attack_icon,self.special_attack_icon_rect)
                else:
                    self.status_icon_rect = self.status_icon.get_rect(center=(650,170+i*50))
                    screen.blit(self.status_icon, self.status_icon_rect)

    
    def show_move_description(self, screen):
        if self.hovered_move == -1:
            return
        i = self.hovered_move
        if self.move_selected[i]:
            move = self.move_name[self.selected_moves[i].lower()]
            if move["damage"] is not None:
                damage = str(move["damage"])
            else: 
                damage = "-"
            type_surface = pygame.image.load(f'typing/{move["type"]}.png').convert_alpha()
            type_surface = pygame.transform.scale(type_surface,(int(type_surface.get_width()*0.8),int(type_surface.get_height()*0.8)))
            type_surface_rect = type_surface.get_rect(center=(450, 370))
            damage_surface = self.pokemon_ability_font.render(f'DMG: {damage}', True, (0, 0, 0))
            description_surface =self.nature_and_move_description_font.render(move["description"], True, (0, 0, 0))

            if move["accuracy"] is not None:
                accuracy = str(move["accuracy"]) + "%"
            else:
                accuracy = "-"   # this prevents accuracy from showing None
            accuracy_surface = self.pokemon_ability_font.render(f'ACC: {accuracy}', True,(0,0,0))
            screen.blit(accuracy_surface,(670,360))
            screen.blit(type_surface, type_surface_rect)
            screen.blit(damage_surface, (570, 360))
            screen.blit(description_surface, (390, 410))





