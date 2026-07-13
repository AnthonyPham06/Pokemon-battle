import pygame
import json

class Menu(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        pygame.mixer.init()
        self.image = pygame.image.load('menu_screen.jpg').convert_alpha()
        self.original_image = pygame.transform.scale(self.image,(int(self.image.get_width()*0.25),int(self.image.get_height()*0.25)))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (x,y))
        self.alpha = 0  # start fully transparent
        self.image.set_alpha(self.alpha)

        #pokemon filter box
        self.font = pygame.font.Font('pokemon_pixel_font.ttf', 22)
        self.search_rect = pygame.Rect(10, 20, 150, 40)
        self.search_text = ""
        self.active = False
        self.results = []
        self.selected = False
        
        # search item box
        self.search_item_rect = pygame.Rect(170, 20, 150, 40)
        self.search_item_text = ""
        self.search_item_active = False
        self.search_item_selected = False


        # take data of pokemon from json file
        with open('pokemon_data.json', 'r') as f:
            pokemon_list = json.load(f)
        self.pokemon_data = {p["name"].lower(): p for p in pokemon_list}    # take pokemon name
        self.pokemon_description = {p["name"]: p["description"] for p in pokemon_list} # take pokemon description
        self.pokemon_ability = {p["name"]: p["abilities"][0] for p in pokemon_list}
        self.pokemon_ability_description = {p["name"]: p["ability_descriptions"][p["abilities"][0]] for p in pokemon_list} # take ability description
        self.typing = {p["name"]: p["type"] for p in pokemon_list}  # take type from json
        self.ability_surface = None 

        self.hp = {p["name"]: p["health"] for p in pokemon_list} # take hp
        self.atk = {p["name"]: p["attack"] for p in pokemon_list} # take atk
        self.defend = {p["name"]: p["defense"] for p in pokemon_list} #take def
        self.spatk = {p["name"]: p["sp_attack"] for p in pokemon_list} #take spatk
        self.spdef = {p["name"]: p["sp_defense"] for p in pokemon_list} #take spdef
        self.speed = {p["name"]: p["speed"] for p in pokemon_list} # take speed
        self.weight = {p["name"]: p["weight_kg"] for p in pokemon_list} # weight


        # take data of items
        with open('item_list.json', 'r') as f:
            item_list = json.load(f)
            self.item_id = {p["id"]: p for p in item_list} 
            self.item_name = {p["name"]: p for p in item_list} 
            self.item_results = []

        # load pokedex sprite and animation
        self.pokedex = pygame.image.load('pokedex.jpg').convert_alpha()
        self.pokedex = pygame.transform.scale(self.pokedex,(int(self.pokedex.get_width()*0.6),int(self.pokedex.get_height()*0.65)))
        self.pokedex_rect = self.pokedex.get_rect(center=(600, 325))
        self.last_time = 0
        self.sprite_turn = 0
        self.cooldown = 333
        self.idle = ""
        

        #load text box
        self.text_box = pygame.image.load('menu_sprites/text_box.png').convert_alpha()
        self.text_box = pygame.transform.scale(self.text_box,(int(self.text_box.get_width()*0.417),int(self.text_box.get_height()*0.65)))
        self.text_box_rect = self.text_box.get_rect(center=(605, 430))

        #load ability box
        self.ability_box = pygame.image.load('menu_sprites/ability_box.png').convert_alpha()
        self.ability_box = pygame.transform.scale(self.ability_box,(int(self.ability_box.get_width()*0.41),int(self.ability_box.get_height()*0.55)))
        self.ability_box_rect = self.ability_box.get_rect(center=(190, 265))

        #load stat box
        self.stat_box = pygame.image.load('menu_sprites/stat_box.png').convert_alpha()
        self.stat_box = pygame.transform.scale(self.stat_box,(int(self.stat_box.get_width()*0.4),int(self.stat_box.get_height()*2.5)))
        self.stat_box_rect = self.stat_box.get_rect(center=(96, 405))

        #item_box
        self.item_box = pygame.image.load('menu_sprites/item_box.png').convert_alpha()
        self.item_box = pygame.transform.scale(self.item_box,(int(self.item_box.get_width()*0.4),int(self.item_box.get_height()*2.6)))
        self.item_box_rect = self.item_box.get_rect(center=(286, 410))


        # font for description
        self.font = pygame.font.Font('pokemon_pixel_font.ttf', 22)
        self.text_surface = None

        self.description_font = pygame.font.Font('pokemon_pixel_font.ttf', 26) # also use for stats
        self.ability_font = pygame.font.Font('pokemon_pixel_font.ttf', 30)
        self.ability_description_font = pygame.font.Font('pokemon_pixel_font.ttf', 19)
        self.ability_description =""
        self.description_lines = []


        #enter_arrow for transitioning
        self.enter_arrow = pygame.image.load('menu_sprites/enter_arrow.png').convert_alpha()
        self.enter_arrow = pygame.transform.scale(self.enter_arrow,(int(self.enter_arrow.get_width()*0.3),int(self.enter_arrow.get_height()*0.3)))
        self.enter_arrow_rect = self.enter_arrow.get_rect(center =(40,190))
        


    def fade_in(self): # transition into the menu page
        if self.alpha < 255:
            self.alpha += 4  # speed of fade, adjust as needed
            self.image.set_alpha(self.alpha)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.search_rect.collidepoint(event.pos)  # check if the search or item bar is pressed in
            self.search_item_active = self.search_item_rect.collidepoint(event.pos)

            for i, name in enumerate(self.results[:3]):
                result_rect = pygame.Rect(self.search_rect.x, self.search_rect.bottom + i * 35, self.search_rect.width, 30)
                if result_rect.collidepoint(event.pos):
                    self.search_text = name  # fill bar with clicked name
                    self.results = []        # clear dropdown
                    self.active = False # deactivate box
                    self.selected = True 
                    if self.selected == True:
                        self.idle = self.search_text
                        # load the pokemon
                        self.front_sprite = pygame.image.load(f'pokemon_sprites/{self.idle}/{self.idle}_front.png').convert_alpha() # we first upload 2 images of bulbasaur, this should be changed later
                        self.back_sprite = pygame.image.load(f'pokemon_sprites/{self.idle}/{self.idle}_back.png').convert_alpha() 

                        #load the typing image here
                        if len(self.typing[self.idle]) == 1: #single type
                            self.first_type = pygame.image.load(f'typing/{self.typing[self.idle][0]}.png').convert_alpha()
                            self.first_type_sprite = pygame.transform.scale(self.first_type,(int(self.first_type.get_width()*0.65),int(self.first_type.get_height()*0.65)))
                            self.first_type_sprite_rect = self.first_type_sprite.get_rect(center=(720,110))

                        elif len(self.typing[self.idle]) == 2: #double type
                            self.first_type = pygame.image.load(f'typing/{self.typing[self.idle][0]}.png').convert_alpha()
                            self.second_type = pygame.image.load(f'typing/{self.typing[self.idle][1]}.png').convert_alpha()
                            self.first_type_sprite = pygame.transform.scale(self.first_type,(int(self.first_type.get_width()*0.65),int(self.first_type.get_height()*0.65)))
                            self.second_type_sprite = pygame.transform.scale(self.second_type,(int(self.second_type.get_width()*0.65),int(self.second_type.get_height()*0.65)))
                            self.first_type_sprite_rect = self.first_type_sprite.get_rect(center=(720,110))
                            self.second_type_sprite_rect = self.second_type_sprite.get_rect(center=(720,140))
                        



                        self.front_sprite = pygame.transform.scale(self.front_sprite,(int(self.front_sprite.get_width()*0.65),int(self.front_sprite.get_height()*0.65)))
                        self.back_sprite = pygame.transform.scale(self.back_sprite,(int(self.back_sprite.get_width()*0.65),int(self.back_sprite.get_height()*0.65)))

                        self.front_sprite_rect = self.front_sprite.get_rect(center=(600, 250))  # bound the image to rect
                        self.back_sprite_rect = self.back_sprite.get_rect(center=(600, 250)) 

                        cry = pygame.mixer.Sound(f'pokemon_audio/{self.search_text}.mp3')
                        cry.set_volume(0.6)
                        cry.play()

                        # inside handle_event, after self.idle = self.search_text
                        self.hp_surface = self.ability_font.render('HP: ' + str(self.hp[self.idle]), True, (0, 0, 0))
                        self.atk_surface = self.ability_font.render('ATK: ' + str(self.atk[self.idle]), True, (0, 0, 0))
                        self.defend_surface = self.ability_font.render('DEF: ' + str(self.defend[self.idle]), True, (0, 0, 0))
                        self.spatk_surface = self.ability_font.render('SPATK: ' + str(self.spatk[self.idle]), True, (0, 0, 0))
                        self.spdef_surface = self.ability_font.render('SPDEF: ' + str(self.spdef[self.idle]), True, (0, 0, 0))
                        self.speed_surface = self.ability_font.render('SPEED: ' + str(self.speed[self.idle]), True, (0, 0, 0))
                        self.weight_surface = self.ability_font.render('WEIGHT: ' + str(self.weight[self.idle]), True, (0, 0, 0))
                        self.ability_surface = self.ability_font.render(self.pokemon_ability[self.idle], True, (0, 0, 0))
                        self.ability_description_surface = self.ability_description_font.render(self.pokemon_ability_description[self.idle], True, (0, 0, 0))

                        # Write the description for pokemon
                        description = self.pokemon_description[name]
                        words = description.split() 
                        lines = []
                        current_line = ""

                        for word in words:
                            test_line = current_line + word + " "
                            if self.description_font.size(test_line)[0] < self.text_box_rect.width - 40:  # use description_font here
                                current_line = test_line
                            else:
                                lines.append(current_line)
                                current_line = word + " "
                        lines.append(current_line)
                        self.description_lines = lines

            # check if item result was clicked
            for i, item_name in enumerate(self.item_results[:3]):
                item_result_rect = pygame.Rect(self.search_item_rect.x, self.search_item_rect.bottom + i * 35, self.search_item_rect.width, 30)
                if item_result_rect.collidepoint(event.pos):
                    self.search_item_text = item_name # filled the item bar with clicked name
                    self.item_results = []
                    self.search_item_active = False
                    self.search_item_selected = True
                    self.item_sprite = pygame.image.load(f'held_items/{self.search_item_text}.png').convert_alpha()
                    self.item_sprite = pygame.transform.scale(self.item_sprite,(int(self.item_sprite.get_width()*0.5),int(self.item_sprite.get_height()*0.5)))

                    self.item_sprite_rect = self.item_sprite.get_rect(center=(285,350))


                     


        if event.type == pygame.KEYDOWN and self.active: #input text for first box
            self.selected = False
            if event.key == pygame.K_BACKSPACE:
                self.search_text = self.search_text[:-1]
            else:
                self.search_text += event.unicode

            # filter as you type
            if self.search_text:
                self.results = []
                for p in self.pokemon_data.values():
                    pokemon_name = p["name"].lower()            #Basically, this whole block of code finds the pokemon with the recent typing
                    search = self.search_text.lower()
                    if search in pokemon_name:
                        self.results.append(p["name"])
            else:
                self.results = []

        if event.type == pygame.KEYDOWN and self.search_item_active:
            self.search_item_selected = False
            if event.key == pygame.K_BACKSPACE:
                self.search_item_text = self.search_item_text[:-1]
            else:
                self.search_item_text += event.unicode

            if self.search_item_text:
                self.item_results = []
                for item in self.item_name.values():
                    if self.search_item_text.lower() in item["name"].lower():
                        self.item_results.append(item["name"])
            else:
                self.item_results = []
         

    def draw_search(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.search_rect)  # solid black fill
        pygame.draw.rect(screen, (255, 255, 255), self.search_rect, 2)  # white border
        if self.active:
            display_text = self.search_text + "|" # if the cursor is active
        else:
            display_text = self.search_text # if the cursor is not active

        text_surface = self.font.render(display_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.search_rect.x + 8, self.search_rect.y + 8))

        

        if self.search_text:
            if self.results:
                #recommend pokemon
                for i, name in enumerate(self.results[:3]):  
                    result_rect = pygame.Rect(self.search_rect.x, self.search_rect.bottom + i * 35, self.search_rect.width, 30)
                    pygame.draw.rect(screen, (0, 0, 0), result_rect)
                    pygame.draw.rect(screen, (255, 255, 255), result_rect, 1)
                    name_surface = self.font.render(name, True, (255, 255, 255))
                    screen.blit(name_surface, (result_rect.x + 8, result_rect.y + 8))
            elif not self.selected:
                # invalid pokemon
                invalid_rect = pygame.Rect(self.search_rect.x, self.search_rect.bottom, self.search_rect.width, 30)
                pygame.draw.rect(screen, (0, 0, 0), invalid_rect)
                pygame.draw.rect(screen, (255, 0, 0), invalid_rect, 1)  # red border for invalid
                invalid_surface = self.font.render("Invalid Pokemon", True, (255, 0, 0))
                screen.blit(invalid_surface, (invalid_rect.x + 8, invalid_rect.y + 8))


    def draw_search_item(self,screen):
        pygame.draw.rect(screen, (0, 0, 0), self.search_item_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.search_item_rect, 2)
        if self.search_item_active:
            display_text = self.search_item_text + "|" # if the cursor is active
        else:
            display_text = self.search_item_text # if the cursor is not active

        text_surface = self.font.render(display_text, True, (255, 255, 255))     
        screen.blit(text_surface, (self.search_item_rect.x + 8, self.search_item_rect.y + 8)) 

        if self.search_item_text and self.item_results: #this chunk prints 3 items if the item is in the list
            for i, item_name in enumerate(self.item_results[:3]):
                item_result_rect = pygame.Rect(self.search_item_rect.x, self.search_item_rect.bottom + i * 35, self.search_item_rect.width, 30)
                pygame.draw.rect(screen, (0, 0, 0), item_result_rect)
                pygame.draw.rect(screen, (255, 255, 255), item_result_rect, 1)
                name_surface = self.font.render(item_name, True, (255, 255, 255))
                screen.blit(name_surface, (item_result_rect.x + 8, item_result_rect.y + 8))

        elif not self.search_item_selected and self.search_item_text != "": # this chunk prints invalid item if the item is not in the list
            invalid_rect = pygame.Rect(self.search_item_rect.x, self.search_item_rect.bottom, self.search_item_rect.width, 30)
            pygame.draw.rect(screen, (0, 0, 0), invalid_rect)
            pygame.draw.rect(screen, (255, 0, 0), invalid_rect, 1)  # red border for invalid
            invalid_surface = self.font.render("Invalid item", True, (255, 0, 0))
            screen.blit(invalid_surface, (invalid_rect.x + 8, invalid_rect.y + 8))



    def draw_pokemon_animation(self,screen):
        #if not self.selected:  # don't draw if nothing selected
            #return
        if self.idle == "":
            return 
        else:
            current_time =pygame.time.get_ticks()
            if current_time - self.last_time >= self.cooldown:
                self.sprite_turn = 1 - self.sprite_turn
                self.last_time = current_time

            if self.sprite_turn == 0:
                screen.blit(self.front_sprite, self.front_sprite_rect)
            else:
                screen.blit(self.back_sprite, self.back_sprite_rect)


    def draw_item(self,screen):
        if not self.search_item_selected:  # don't draw if nothing selected
            return
        else:
            screen.blit(self.item_sprite, self.item_sprite_rect)



    def draw_pokedex(self, screen):
        screen.blit(self.pokedex, self.pokedex_rect)
        if self.selected and self.search_item_selected:
            screen.blit(self.enter_arrow,self.enter_arrow_rect)
        screen.blit(self.text_box, self.text_box_rect)
        screen.blit(self.ability_box, self.ability_box_rect)
        screen.blit(self.stat_box, self.stat_box_rect)
        screen.blit(self.item_box,self.item_box_rect)
        if self.search_item_selected:
            item_name_surface = self.ability_font.render(self.search_item_text, True, (0, 0, 0))
            screen.blit(item_name_surface, (self.item_box_rect.x + 40, self.item_box_rect.y + 70))

            item_effect_surface = self.ability_description_font.render(self.item_name[self.search_item_text]["effect"], True, (0, 0, 0))
            screen.blit(item_effect_surface, (self.item_box_rect.x + 10, self.item_box_rect.y + 100))

        if self.idle =="":  # only draw text when pokemon is selected
            return
        
    
        ability_surface = self.ability_font.render(self.pokemon_ability[self.idle], True, (0, 0, 0))
        screen.blit(ability_surface, (self.ability_box_rect.x + 20, self.ability_box_rect.y + 10)) # write ability name into the screen

        ability_description_surface = self.ability_description_font.render(self.pokemon_ability_description[self.idle], True, (0, 0, 0))
        screen.blit(ability_description_surface, (self.ability_box_rect.x + 20, self.ability_box_rect.y + 50)) #write ability description into the screen

        if len(self.typing[self.idle]) == 1:
            screen.blit(self.first_type_sprite,self.first_type_sprite_rect)  
        elif len(self.typing[self.idle]) == 2:                                         #all of this chunk draw type into the screen
            screen.blit(self.first_type_sprite,self.first_type_sprite_rect)
            screen.blit(self.second_type_sprite,self.second_type_sprite_rect)

        screen.blit(self.hp_surface, (self.stat_box_rect.x + 20, self.stat_box_rect.y + 20))   

        screen.blit(self.atk_surface, (self.stat_box_rect.x + 20, self.stat_box_rect.y + 43))

        screen.blit(self.defend_surface, (self.stat_box_rect.x + 20, self.stat_box_rect.y + 66))

        screen.blit(self.spatk_surface, (self.stat_box_rect.x + 20, self.stat_box_rect.y + 89))

        screen.blit(self.spdef_surface, (self.stat_box_rect.x + 20, self.stat_box_rect.y + 112))

        screen.blit(self.speed_surface, (self.stat_box_rect.x + 20, self.stat_box_rect.y + 135))


        screen.blit(self.weight_surface, (self.stat_box_rect.x + 20, self.stat_box_rect.y + 158))

    
        for i, line in enumerate(self.description_lines):
            text_surface = self.description_font.render(line, True, (0, 0, 0))
            x = self.text_box_rect.x + 20
            y = self.text_box_rect.y + 10 + i * 18
            screen.blit(text_surface, (x, y))


    def play_music(self):
        pygame.mixer.music.load('menu_music.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)


    def check_transfer(self,event):     #check if the button is clicked, if clicked, transfer to move menu
        if event.type == pygame.MOUSEBUTTONDOWN and self.enter_arrow_rect.collidepoint(event.pos) and self.idle != "" and self.search_item_text:
            return 2, self.idle, self.search_item_text, self.pokemon_ability[self.idle]
        else:
            return None

    

    