import pygame
import json
from battle_engine import Battle_Engine
from animation import BattleAnimation
from changing_pokemon import Change_Pokemon
import random

class Battle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # ==========================================
        # 1. CORE ENGINES & DATA LOADING
        # ==========================================
        # import the Battle engine file
        self.engine = Battle_Engine()
        self.animator = BattleAnimation()
        self.change_system = Change_Pokemon()
        

        # read from json file
        with open('pokemon_data.json', 'r') as f: #from moves.json
            pokemon_list = json.load(f)
        self.pokemon_data = {p["name"].lower(): p for p in pokemon_list}


        # ==========================================
        # 2. VISUAL ASSETS & BACKGROUNDS
        # ==========================================
        # create background
        self.image = pygame.image.load('battle_sprite/battle_background.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.image,(int(self.image.get_width()*0.8),int(self.image.get_height()*0.8)))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (x,y))
        self.alpha = 0  # start fully transparent
        self.image.set_alpha(self.alpha)

        # create ground 
        self.ground = pygame.image.load('battle_sprite/battle_ground.png').convert_alpha()
        self.ground= pygame.transform.scale(self.ground,(int(self.ground.get_width()*0.8),int(self.ground.get_height()*0.7)))
        self.ground_x = 700 #intially the land is off screen

        self.ground_player = pygame.image.load('battle_sprite/battle_ground.png').convert_alpha()
        self.ground_player= pygame.transform.scale(self.ground_player,(int(self.ground_player.get_width()*0.8),int(self.ground_player.get_height()*0.7)))
        self.ground_player_x = -100

        self.finished_ground_animation = False


        # ==========================================
        # 3. FONTS & UI LAYOUT ASSETS
        # ==========================================
        # user interface
        self.interface = pygame.image.load('battle_sprite/battle_box.png').convert_alpha()
        self.interface= pygame.transform.scale(self.interface,(int(self.interface.get_width()*1.7),int(self.interface.get_height()*2.2)))
        self.interface_rect = self.interface.get_rect(center=(403,415))

        # font for text
        self.font_pokemon2 = pygame.font.Font('pokemon_pixel_font.ttf', 25)
        self.font_pokemon1 = pygame.font.Font('pokemon_pixel_font.ttf', 35)

        # create hp bar for opponent
        self.hp_bar = pygame.image.load('battle_sprite/hp_bar.png').convert_alpha()
        self.hp_bar = pygame.transform.scale(self.hp_bar,(int(self.hp_bar.get_width()*0.15),int(self.hp_bar.get_height()*0.15)))
        self.hp_bar_rect = self.hp_bar.get_rect(center=(200,80))

        self.duck = pygame.image.load('move_sprites/confusion_status/duck.png').convert_alpha()
        self.duck = pygame.transform.scale(self.duck,(int(self.duck.get_width()*0.4),int(self.duck.get_height()*0.4)))


        # ==========================================
        # 4. MENU HOVER & SELECTION STATES
        # ==========================================
        # variables for hovering
        self.hover = 0
        self.move_surface_rect = pygame.Rect(0, 0, 0, 0)
        self.change_pokemon_surface_rect = pygame.Rect(0, 0, 0, 0)
        self.hovered_move = -1
        self.move_rects = []
        self.sub_pokemon_rect = pygame.Rect()


        # ==========================================
        # 5. GLOBAL BATTLE FLOW & LOGIC FLAGS
        # ==========================================
        # choosing moves
        self.chosen_move = ""
        self.text_index = 0 # text scrolling

        # check if move of my pokemon is done and damage is dealt
        self.move_done = True
        self.move_hit = None  
        self.damage_applied = False 
        self.check_accuracy_yet = False
        self.active_field_trapped = True 


        self.status_done_damage_this_turn = True
        self.status_timer = 0  # timestamp for end of turn delay
        self.turn_done = False
        self.swap_turn_timer_start = 0
        self.go_first_this_turn = None # the pokemon who goes first
        self.present_weather =""
        self.multi_turn_move_charged = 0


        # ==========================================
        # 6. DIALOGUE MESSAGE QUEUE SYSTEM
        # ==========================================
        # message queue 
        self.message_queue = []
        self.current_message = ""
        self.message_timer = None
        self.message_duration = 1500


        # ==========================================
        # 7. ABILITY BOX UI TRIGGERS
        # ==========================================
        # ability box trigger
        self.ability_box = pygame.image.load('battle_sprite/ability_text_box.png').convert_alpha()
        self.ability_box = pygame.transform.scale(self.ability_box,(int(self.ability_box.get_width()*0.3),int(self.ability_box.get_height()*0.4)))
        
        self.ability_box_text = ""
        self.ability_box_showing = False # trigger the ability box when needing

        self.opponent_ability_box_showing = False
        self.opponent_ability_box_text = ""


        # ==========================================
        # 8. PLAYER (POKEMON 1) SPECIFIC BATTLE STATES
        # ==========================================
        self.pokemon1_current_status = ""
        self.hp1_ratio = 1.0  
        self.hp1_display = 1.0
        self.pokemon1_health_decreasing = False
        self.new_hp1_percent_recoil = 0
        self.recoil_pending = False
        self.recoil_decreasing = False
        self.paralysis_checked = False  # check paralyse of pokemon1
        self.pokemon1_heal = False
        self.pokemon1_sleep_counter = 0
        self.animation_status_p1_done = False
        self.pokemon1_confusion = False
        self.sleep_animation_pokemon1_done = True
        self.pokemon1_self_hit = False
        self.being_trapped_p1 = False
        self.trapped_name_p1 = ""
        self.trapped_counter_p1 = 0
        self.seeded_p1 = False
        self.p1_invulnerable = False



        # ==========================================
        # 9. OPPONENT (POKEMON 2) SPECIFIC BATTLE STATES
        # ==========================================
        self.pokemon_list = ["machamp"] #"pidgeot","charizard","venusaur","blastoise","butterfree","raichu",
        self.opponent_name = random.choice(self.pokemon_list)

        # test opponent pokemon, with animation when entering
        front = pygame.image.load(f'pokemon_sprites/{self.opponent_name}/{self.opponent_name}_front.png').convert_alpha()
        front = pygame.transform.scale(front,(int(front.get_width()*0.45),int(front.get_height()*0.45)))

        back = pygame.image.load(f'pokemon_sprites/{self.opponent_name}/{self.opponent_name}_back.png').convert_alpha()
        back = pygame.transform.scale(back,(int(back.get_width()*0.45),int(back.get_height()*0.45)))

        self.opponent_frames = [front, back, front, back, front] # animation sequence
        self.opponent_frame_index = 0 # tracks the current sprite
        self.opponent_last_swap = 0 # record the time of last sprite
        self.opponent_cooldown = 200  # waiting time
        self.cry_done = False # pokemon2 did not cried yet
        
        self.pokemon2_current_status = ""
        self.hp2_ratio = 1.0
        self.pokemon2_previous_hp_percent = 1.0
        self.hp2_raw_display = None  # set to None until battle starts
        self.draining = False # health draning animation
        self.pokemon2_heal = False # self heal

        # --- opponent turn state ---
        self.pokemon2_chosen_move = ""
        self.opponent_turn = False
        self.opponent_move_done = True
        self.opponent_damage_applied = False
        self.opponent_move_hit = None
        self.pokemon2_sleep_counter = 0
        self.animation_status_p2_done = False
        self.pokemon2_confusion = False
        self.sleep_animation_pokemon2_done = True
        self.being_trapped_p2 = False
        self.trapped_name_p2 = ""
        self.trapped_counter_p2 = 0 
        self.seeded_p2 = False
        self.seed_animation_transition = False
        self.p2_invulnerable = False

        # ==========================================
        # 10. WEATHER TURN COUNTS
        # ==========================================
        self.weather_turn = 0
        self.weather_done_damage_this_turn = True
        self.weather_timer = 0
        self.end_turn_weather_animation_done = False

        # ==========================================
        # 11. TRAPPED MOVE
        # ==========================================

        self.trapped_turn_p1 = 0
        self.trapped_turn_p2 = 0
        self.trapped_done_damage_this_turn = True
        self.trapped_timer = 0 
        self.trapped_animation_transition = False

        # ==========================================
        # 12. FAINT
        # ==========================================
        self.pokemon1_fainted = False
        self.pokemon2_fainted = False
        self.victory_music_played = False
        self.battle_over = False
        self.low_health_music = False



    def fade_in(self): 
        
        # transition into the battle page
        if self.alpha < 255:
            self.alpha += 4  # speed of fade, adjust as needed
            self.image.set_alpha(self.alpha)


    def play_music(self):
        pygame.mixer.music.load('battle_music/track_1.mp3') #play_music
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    def make_landscape(self, screen):
        if self.ground_x > 400 and self.ground_player_x < 50:
            self.ground_x -= 3
            self.ground_player_x +=1.8

        self.ground_rect = self.ground.get_rect(center=(self.ground_x, 180))
        self.ground_player_rect = self.ground_player.get_rect(center=(self.ground_player_x, 320))
        screen.blit(self.ground, self.ground_rect)
        screen.blit(self.ground_player, self.ground_player_rect)
        screen.blit(self.interface, self.interface_rect)


    def battle_set_pokemon(self, pokemon_name, pokemon_item, pokemon_ability, moves, nature):
        self.pokemon_name =  pokemon_name
        self.pokemon_item = pokemon_item
        self.pokemon_ability = pokemon_ability
        self.pokemon_moves = moves
        self.pokemon_nature = nature

        # get the combat stats of the pokemon 1
        self.hp1_number = self.pokemon_data[self.pokemon_name]["health"] 
        self.atk_pokemon1 = self.pokemon_data[self.pokemon_name]["attack"] 
        self.def_pokemon1 = self.pokemon_data[self.pokemon_name]["defense"] 
        self.spatk_pokemon1 = self.pokemon_data[self.pokemon_name]["sp_attack"] 
        self.spdef_pokemon1 = self.pokemon_data[self.pokemon_name]["sp_defense"]
        self.speed_pokemon1 = self.pokemon_data[self.pokemon_name]["speed"] 
        self.weight_pokemon1 = self.pokemon_data[self.pokemon_name]["weight_kg"]  
        self.type_pokemon1 = self.pokemon_data[self.pokemon_name]["type"]  
        self.hp1_display = 1.0

        self.check_nature()
        
        # get the combat stats of the pokemon 2
        self.hp2_raw = self.pokemon_data[self.opponent_name]["health"]
        self.atk_pokemon2 = self.pokemon_data[self.opponent_name]["attack"] 
        self.def_pokemon2 = self.pokemon_data[self.opponent_name]["defense"] 
        self.spatk_pokemon2 = self.pokemon_data[self.opponent_name]["sp_attack"] 
        self.spdef_pokemon2 = self.pokemon_data[self.opponent_name]["sp_defense"]
        self.speed_pokemon2 = self.pokemon_data[self.opponent_name]["speed"] 
        self.type_pokemon2 = self.pokemon_data[self.opponent_name]["type"]
        self.weight_pokemon2 = self.pokemon_data[self.opponent_name]["weight_kg"] 
        self.ability_pokemon2 = self.pokemon_data[self.opponent_name]["abilities"][0].lower()

        self.hp2_raw_display = self.hp2_raw # the max health is displayed

        self.engine.get_pokemon1_def_spdef_speed_item_type_ability_turn(self.def_pokemon1,self.spdef_pokemon1, self.speed_pokemon1, self.pokemon_item, self.type_pokemon1, self.pokemon_ability, self.opponent_turn)
        self.engine.get_pokemon1_atk_spatk(self.atk_pokemon1, self.spatk_pokemon1)
        self.engine.get_pokemon2_hp_def_spdef_speed_type_ability(self.hp2_raw, self.def_pokemon2, self.spdef_pokemon2,self.speed_pokemon2, self.type_pokemon2, self.ability_pokemon2)




        #
        black_list = ["bulbasaur", 'squirtle','rattata','raticate','ivysaur','sandshrew', 'nidoqueen','diglett','golduck','golem']
        if self.pokemon_name not in black_list:  #this if statement fix the dimensions of some pokemon
            TARGET_HEIGHT = 120
            self.bottom = 333
        else: 
            if self.pokemon_name == 'ivysaur':
                TARGET_HEIGHT = 140
                self.bottom = 350

            elif self.pokemon_name == 'nidoqueen' or self.pokemon_name =="golduck":
                TARGET_HEIGHT = 190
                self.bottom = 362
            else:
                TARGET_HEIGHT = 90
                self.bottom = 335

        self.pokemon1_sprite = pygame.image.load(f'pokemon_sprites/{self.pokemon_name}/{self.pokemon_name}_battle.png').convert_alpha()
        self.pokemon1_sprite = self.crop_sprite(self.pokemon1_sprite)
        scale = TARGET_HEIGHT / self.pokemon1_sprite.get_height()
        new_width = int(self.pokemon1_sprite.get_width() * scale)
        self.pokemon1_sprite = pygame.transform.scale(self.pokemon1_sprite, (new_width, TARGET_HEIGHT))

        if not self.finished_ground_animation:
            self.ground_x = 700
            self.ground_player_x = -100
            self.opponent_frame_index = 0
            self.opponent_last_swap = 0
            self.finished_ground_animation = True




    def draw_pokemon(self, screen):
        #draw my pokemon
        pokemon_rect = self.pokemon1_sprite.get_rect(centerx=self.ground_player_rect.centerx + 160, bottom= self.bottom)
        if (not self.opponent_turn or self.animator.frame == 0 and self.animator.current_loaded_move not in ("body slam","submission","double-edge","take down")) and not self.pokemon1_fainted and self.engine.charging_move not in ("fly","dig"): # this prevents the tackle not flashing bug when p2 attack p1
            screen.blit(self.pokemon1_sprite, pokemon_rect)

        elif self.pokemon1_fainted:
            if not self.current_message and not self.message_queue:
                self.message_queue.append(f"{self.pokemon_name.capitalize()} lost!")
                self.message_duration = 100000000


        # draw opponent pokemon
        ground_stopped = not (self.ground_x > 400 and self.ground_player_x < 50)

        if ground_stopped and self.opponent_frame_index == 0 and self.opponent_last_swap == 0: # play the pokemon cry when the ground stop moving
            self.opponent_last_swap = pygame.time.get_ticks()  # start the timers 


        if ground_stopped:
            # config for the health bar of pokemon 1
            BAR_X_1 = 50        # left edge of the green/red bars
            BAR_Y_1 = 390         # vertical position
            BAR_WIDTH = 120    # full width at 100% HP
            BAR_HEIGHT = 10     # thickness

            #config for the health bar of pokemon 2
            BAR_X_2 = 90        # left edge of the green/red bars
            BAR_Y_2 = 75         # vertical position


            #pokemon 2

            screen.blit(self.hp_bar,self.hp_bar_rect) # draw hp background after the animation stops
            

            self.pokemon2_name_surface = self.font_pokemon2.render(f"{self.opponent_name.capitalize()}:",True,(0,0,0)) 
            screen.blit(self.hp_bar,self.hp_bar_rect) # draw hp bar after the animation stops
            screen.blit(self.pokemon2_name_surface,(100,45))

            self.engine.check_status_pokemon(screen) # show status for both pokemon
            if self.pokemon2_confusion:
                screen.blit(self.duck,(190,40))



            # health bar for pokemon 2
            pygame.draw.rect(screen, (0, 0, 0), (BAR_X_2 - 2, BAR_Y_2 - 2, BAR_WIDTH + 4, BAR_HEIGHT + 4)) # black border for hp
            pygame.draw.rect(screen, (255, 255, 255), (BAR_X_2, BAR_Y_2, BAR_WIDTH, BAR_HEIGHT)) #red health

            if self.pokemon2_previous_hp_percent > 0.5:
                 pygame.draw.rect(screen, (0, 200, 0), (BAR_X_2, BAR_Y_2, int(BAR_WIDTH * self.pokemon2_previous_hp_percent), BAR_HEIGHT)) # green health
            elif self.pokemon2_previous_hp_percent <= 0.5 and self.pokemon2_previous_hp_percent > 0.25:
                pygame.draw.rect(screen, (218, 165, 32), (BAR_X_2, BAR_Y_2, int(BAR_WIDTH * self.pokemon2_previous_hp_percent), BAR_HEIGHT))
            else:
                 pygame.draw.rect(screen, (255, 0, 0), (BAR_X_2, BAR_Y_2, int(BAR_WIDTH * self.pokemon2_previous_hp_percent), BAR_HEIGHT))

            
            now = pygame.time.get_ticks()
            if now - self.opponent_last_swap >= self.opponent_cooldown:
                if self.opponent_frame_index+2 <= 5:
                    self.opponent_frame_index += 1
                    self.opponent_last_swap = now

            

            sprite = self.opponent_frames[self.opponent_frame_index]
            self.opponent_pokemon_rect = sprite.get_rect(centerx = self.ground_x + 160, bottom = 230)

            if (self.move_done or self.animator.frame == 0 and self.animator.current_loaded_move not in ("body slam","submission","double-edge","take down")) and not self.pokemon2_fainted: # move that move pokemon2 around, which sucks
                screen.blit(sprite, self.opponent_pokemon_rect)

                if not self.cry_done:
                    cry = pygame.mixer.Sound(f'pokemon_audio/{self.opponent_name}.mp3')
                    cry.set_volume(0.6)
                    cry.play()
                    self.cry_done = True

                    if self.pokemon_ability.lower() in ("intimidate","arena trap","cloud nine"):
                        self.ability_box_showing = True
                        self.ability_box_text = self.pokemon_ability.capitalize()
                        self.engine.process_entry_abilities(self.pokemon_ability,self.pokemon_name,"intimidate",self.opponent_name,self.message_queue)


            elif self.pokemon2_fainted:
                if not self.victory_music_played and not self.current_message and not self.message_queue:
                    self.victory_music_played = True
                    pygame.mixer.music.load('battle_music/victory.mp3')
                    pygame.mixer.music.set_volume(0.4)
                    pygame.mixer.music.play(-1)
                    self.message_queue.append(f"{self.pokemon_name.capitalize()} is victorious!")
                    self.message_duration = 100000000
            

        #pokemon 1
            #draw name of pokemon 1
            self.pokemon1_name_surface =  self.font_pokemon1.render(f"{self.pokemon_name.capitalize()}:",True,(0,0,0))
            screen.blit(self.pokemon1_name_surface,(50,350))
        
            #health bar for pokemon 1
            hp1_number_surface  = self.font_pokemon1.render(f"{self.hp1_number} /{self.pokemon_data[self.pokemon_name]["health"]}", True,(0,0,0))
            screen.blit(hp1_number_surface,(180,380))
            pygame.draw.rect(screen, (0, 0, 0), (BAR_X_1 - 2, BAR_Y_1 - 2, BAR_WIDTH + 4, BAR_HEIGHT + 4)) # black border for hp
            pygame.draw.rect(screen, (255, 255, 255), (BAR_X_1, BAR_Y_1, BAR_WIDTH, BAR_HEIGHT)) #white health bavckgorund


            self.hp1_ratio = self.hp1_number / self.pokemon_data[self.pokemon_name]["health"]

            if self.hp1_display > self.hp1_ratio:
                self.hp1_display -= 0.0042
                self.pokemon1_health_decreasing = True
                if self.hp1_display <= self.hp1_ratio:
                    self.hp1_display = self.hp1_ratio
                    self.pokemon1_health_decreasing = False


            if self.hp1_display < self.hp1_ratio:
                self.hp1_display += 0.0042
                if self.hp1_display >= self.hp1_ratio:
                    self.hp1_display = self.hp1_ratio


            if self.hp1_display > 0.5:
                pygame.draw.rect(screen, (0, 200, 0), (BAR_X_1, BAR_Y_1, int(BAR_WIDTH * self.hp1_display), BAR_HEIGHT))
            elif self.hp1_display <= 0.5 and self.hp1_display > 0.25:
                pygame.draw.rect(screen, (218, 165, 32), (BAR_X_1, BAR_Y_1, int(BAR_WIDTH * self.hp1_display), BAR_HEIGHT))
            else:
                
                pygame.draw.rect(screen, (255, 0, 0), (BAR_X_1, BAR_Y_1, int(BAR_WIDTH * self.hp1_display), BAR_HEIGHT))
                if not self.low_health_music:
                    self.low_health_music = True
                    pygame.mixer.music.load('battle_music/low_health.mp3')
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)



            #pokemon 1 item
            item_pokemon1_surface = self.font_pokemon1.render(f"Item: {self.pokemon_item.capitalize()}",True,(0,0,0))
            screen.blit(item_pokemon1_surface, (50,410))

            #pokemon 1 ability
            ability_pokemon1_surface = self.font_pokemon1.render(f"Ability: {self.pokemon_ability.capitalize()}",True,(0,0,0))
            screen.blit(ability_pokemon1_surface,(50, 450))


            if self.hover != 3 and self.hover != 4 and not self.message_queue and not self.current_message:  # check if the moves button has been press

                # draw " what will bulbasaur do":
                question_surface = self.font_pokemon1.render(f"What will {self.pokemon_name.capitalize()} do ?", True,(0,0,0))
                screen.blit(question_surface,(380,350))

                #button move
                self.move_surface = self.font_pokemon1.render("Moves",True,(0,0,0))
                self.move_surface_rect = self.move_surface.get_rect(topleft=(350, 420))
                screen.blit(self.move_surface, self.move_surface_rect)

                #button change pokemon
                self.change_pokemon_surface = self.font_pokemon1.render("Pokemon",True,(0,0,0))
                self.change_pokemon_surface_rect = self.change_pokemon_surface.get_rect(topleft=(590, 420))
                screen.blit(self.change_pokemon_surface, self.change_pokemon_surface_rect)

                if self.hover == 1:
                    pygame.draw.line(screen, (0, 0, 0), (self.move_surface_rect.left, self.move_surface_rect.bottom + 2), (self.move_surface_rect.right, self.move_surface_rect.bottom + 2), 2)

                elif self.hover == 2:
                    pygame.draw.line(screen, (0, 0, 0), ( self.change_pokemon_surface_rect.left, self.change_pokemon_surface_rect.bottom + 2), ( self.change_pokemon_surface_rect.right,  self.change_pokemon_surface_rect.bottom + 2), 2)


            # CHANGE POKEMON MENU
            elif self.hover == 4: # 
                positions = (300, 350)
                sub_pokemon_surface = self.font_pokemon1.render("Charizard", True,(0,0,0))
                self.sub_pokemon_rect  = sub_pokemon_surface.get_rect(topleft = positions)
                if not self.message_queue and not self.current_message:
                    screen.blit(sub_pokemon_surface, self.sub_pokemon_rect)
                    if self.hovered_move == 1:
                        pygame.draw.line(screen, (0, 0, 0), (self.sub_pokemon_rect.left, self.sub_pokemon_rect.bottom + 2), (self.sub_pokemon_rect.right, self.sub_pokemon_rect.bottom + 2), 2)



            # MOVE MENU
            elif self.hover == 3 and not self.chosen_move:
                positions = [(300, 350),(570, 350),(300, 430),(570, 430)]
        
                self.move_rects = []

                if self.engine.charging_move != "": # THIS SHOWS "-" WHEN A CHARGING MOV IS USED
                    for i, move in enumerate(self.pokemon_moves):
                        if move.lower() == self.engine.charging_move:
                            move_surface = self.font_pokemon1.render(move, True, (0, 0, 0))
                        else:
                            move_surface = self.font_pokemon1.render("-", True, (0, 0, 0))
                        move_rect = move_surface.get_rect(topleft=positions[i])
                        self.move_rects.append(move_rect)
                        screen.blit(move_surface, move_rect)
                        if self.hovered_move == i:
                            pygame.draw.line(screen, (0, 0, 0), (move_rect.left, move_rect.bottom + 2), (move_rect.right, move_rect.bottom + 2), 2)

                else:
                    for i, move in enumerate(self.pokemon_moves):
                        move_surface = self.font_pokemon1.render(move, True, (0, 0, 0))
                        move_rect = move_surface.get_rect(topleft=positions[i])
                        self.move_rects.append(move_rect)
                        screen.blit(move_surface, move_rect)
                        if self.hovered_move == i:
                            pygame.draw.line(screen, (0, 0, 0), (move_rect.left, move_rect.bottom + 2), (move_rect.right, move_rect.bottom + 2), 2)


            # POKEMON 1 ATTACK
            elif self.hover == 3 and self.chosen_move and not self.opponent_turn and not self.current_message and not self.message_queue and not self.pokemon1_health_decreasing and not self.move_done and not self.battle_over: 
                # CHECK SLEEP (FIST THING)
                if self.pokemon1_current_status == "sleep" and self.sleep_animation_pokemon1_done:
                    asleep = self.engine.still_asleep()
                    if asleep:
                        self.message_queue.append(f"{self.pokemon_name.capitalize()} is fast asleep!")
                        self.move_hit = None
                        self.sleep_animation_pokemon1_done = False
                    elif not asleep:
                        self.pokemon1_current_status =""
                        self.message_queue.append(f"{self.opponent_name.capitalize()} woke up!")


                if self.pokemon1_confusion:
                    self.message_queue.append(f"{self.pokemon_name.capitalize()} is being confused!")
                    snap_out = random.randint(1,100)
                    self_hit = random.randint(1,100)
                    if snap_out <= 25:   # 30% CHANCE TO SNAP OUT CONFUSION
                        self.message_queue.append(f"{self.pokemon_name.capitalize()} snaps out!")
                        self.pokemon1_confusion = False

                    else:
                        if self_hit <= 50:
                            self.message_queue.append(f"{self.pokemon_name.capitalize()} hit itself!")
                            damage  = round(((10* 40 * ((self.atk_pokemon1 * self.engine.stage_multipliers[self.engine.stages_pokemon1["attack"]])/(self.def_pokemon2 *self.engine.stage_multipliers[self.engine.stages_pokemon2["defense"]])))/50  + 2))
                            self.hp1_ratio = self.pokemon1_previous_hp_percent - damage/ self.pokemon_data[self.pokemon_name]["health"]
                            print(f"mau cua hp1:{self.hp1_ratio}")
                            self.pokemon1_self_hit = True


                #CHECK MULTI TURN MOVE
                self.engine.multi_turn_move()

                if self.engine.charging_move in self.engine.two_turn_move and self.multi_turn_move_charged == 0 and self.pokemon1_current_status != "sleep" and not self.pokemon1_self_hit:
                    if self.engine.charging_move == "razor wind":
                        full_text = f"{self.pokemon_name.capitalize()} whipped up a whirlwind!"

                    elif self.engine.charging_move == "solar beam":
                        full_text = f"{self.pokemon_name.capitalize()} took in the sunlight!"

                    elif self.engine.charging_move == "fly":
                        full_text =  f"{self.pokemon_name.capitalize()} soared up high!"

                    elif self.engine.charging_move == "dig":
                        full_text = f"{self.pokemon_name.capitalize()} dug down!"
                else:
                    if self.pokemon1_current_status != "sleep":
                        full_text = f"{self.pokemon_name.capitalize()} used {self.chosen_move}!"
                    elif self.pokemon1_current_status == "sleep":
                        full_text = ""

                # show the text gradually   
                if self.text_index < len(full_text):
                    self.text_index += 1
                move_chosen_surface = self.font_pokemon1.render(full_text[:self.text_index], True, (0, 0, 0))

                screen.blit(move_chosen_surface, (300, 380))

                #take info of pokemon 1 and 2 for battle engine
                self.engine.get_move(self.chosen_move.lower())
                self.engine.get_pokemon1_def_spdef_speed_item_type_ability_turn(self.def_pokemon1,self.spdef_pokemon1, self.speed_pokemon1, self.pokemon_item, self.type_pokemon1, self.pokemon_ability, self.opponent_turn)

                self.engine.get_pokemon1_atk_spatk(self.atk_pokemon1, self.spatk_pokemon1)

                
                self.engine.get_pokemon2_hp_def_spdef_speed_type_ability(self.hp2_raw, self.def_pokemon2, self.spdef_pokemon2,self.speed_pokemon2, self.type_pokemon2, self.ability_pokemon2)



                if self.text_index == len(full_text):
                        # CHECK STATUS PARALYSIS, FREEZE AND SLEEP
                        if self.pokemon1_current_status == "paralysis" and not self.paralysis_checked and not self.damage_applied:
                            self.paralysis_checked = True
                            if not self.engine.check_paralysis_attack():
                                self.move_hit = None
                                self.damage_applied = True
                                self.move_done = True
                                self.message_queue.append(f"{self.pokemon_name.capitalize()} can't move due to paralysis!")

                        elif self.pokemon1_current_status == "freeze":
                            thaw = self.engine.check_thaw_out()
                            if not thaw and self.engine.pokemon1_move_data["type"] != "Fire" :
                                self.move_hit = None
                                self.damage_applied = True
                                self.move_done = True
                                self.message_queue.append(f"{self.pokemon_name.capitalize()} is frozen solid!")

                            elif not thaw and self.engine.pokemon1_move_data["type"] == "Fire":
                                self.pokemon1_current_status =""
                                self.engine.status_pokemon1 = None

                            elif thaw:
                                self.pokemon1_current_status =""
                                self.message_queue.append(f"{self.pokemon_name.capitalize()} thawed out!")


                        # SHOW THE SLEEP ANIMATION
                        if not self.sleep_animation_pokemon1_done:
                            play = self.animator.play(screen, "status sleep",self.pokemon1_sprite, pokemon_rect,self.opponent_frames[self.opponent_frame_index], self.opponent_pokemon_rect)
                            if play:
                                self.sleep_animation_pokemon1_done = True
                                self.damage_applied = True
                                self.move_done = True


                        #CHECK ACCURACY
                        if self.move_hit is None and not self.move_done and self.pokemon1_current_status !="sleep":
                            self.move_hit = self.engine.check_accuracy()
                            if self.move_hit is None: # FOR CANT MISS MOVE
                                self.move_hit = True

                            if self.multi_turn_move_charged == 0 and self.engine.charging_move != "": # no need to check accuracy in the intermediate turn of the multi move charge
                                self.move_hit = True
                            

                        # CHECK FOR EDGE CASE OF ANIMATION
                        if self.move_hit and not self.damage_applied:
                            if self.chosen_move.lower() in self.engine.status_moves and self.engine.status_moves[self.chosen_move.lower()][1] in ("sleep","poison","bad_poison","paralysis","burn","freeze") and self.pokemon2_current_status !="":
                                self.message_queue.append("But it failed!")

                            if self.chosen_move.lower() == "sandstorm" and self.engine.current_weather == "sandstorm":
                                self.message_queue.append("But it failed!")
                                animation_done = True

                            elif self.chosen_move.lower() == "rain dance" and self.engine.current_weather == "rain dance":
                                self.message_queue.append("But it failed!")
                                animation_done = True

                            elif self.chosen_move.lower() == "sunny day" and self.engine.current_weather == "sunny day":
                                self.message_queue.append("But it failed!")
                                animation_done = True

                            elif self.chosen_move.lower() == "solar beam" and self.engine.current_weather != "sunny day" and self.multi_turn_move_charged == 0:
                                animation_done = True
                            
                            elif self.engine.check_effectiveness() == 0: # dont play the animation when move is unaffected
                                animation_done = True

                            elif self.engine.charging_move in self.engine.two_turn_move and self.multi_turn_move_charged == 0:
                                animation_done = True

                            else:   # PLAY THE ANIMATION
                                animation_done = self.animator.play(screen, self.chosen_move.lower(),self.opponent_frames[self.opponent_frame_index],self.opponent_pokemon_rect, self.pokemon1_sprite, pokemon_rect)
                
                            if animation_done:
                                self.damage_applied = True
                                self.engine.stage_calculation()
                                self.damage, crit, effectiveness = self.engine.damage_calculation()


                                # CHECK FOR MULTI HIT MOVE
                                if self.chosen_move.lower() == "comet punch": # multimove
                                    self.damage = self.damage * len(self.animator.state.get("positions", [1]))
                                    self.message_queue.append(f"Hit {len(self.animator.state.get("positions", [1]))} times!")

                                # DAMAGE BOOST, RECOIL AND ABILITY
                                if not self.engine.check_absorb_move_ability(): 


                                    #WEATHER CHECK
                                    self.engine.check_weather()
                                    if self.present_weather != "" and self.present_weather != self.engine.current_weather:
                                        self.weather_turn = 0 # reset the weather counter if weather changed
                                        self.present_weather = self.engine.current_weather

                                    if self.engine.current_weather == "sandstorm":
                                        if self.weather_turn == 0:
                                            self.present_weather = "sandstorm"
                                            self.weather_turn += 1
                                            self.message_queue.append("A sandstorm brewed!")
                                        self.weather_done_damage_this_turn = False

                                    elif self.engine.current_weather == "rain dance":
                                        if self.weather_turn == 0:
                                            self.present_weather = "rain dance"
                                            self.weather_turn += 1
                                            self.message_queue.append("It started to rain!")
                                        self.weather_done_damage_this_turn = False

                                    elif self.engine.current_weather == "sunny day":
                                        if self.weather_turn == 0:
                                            self.present_weather = "sunny day"
                                            self.weather_turn += 1
                                            self.message_queue.append("The sunlight turn harsh!")
                                        self.weather_done_damage_this_turn = False


                                    # MULTI TURN MOVE CHECK
                                    if self.engine.charging_move != "" and self.multi_turn_move_charged == 0:
                                            self.damage = 0
                                            self.multi_turn_move_charged = 1
                                            self.p1_invulnerable = True

                                    elif self.engine.charging_move != "" and self.multi_turn_move_charged == 1:
                                            self.multi_turn_move_charged = 0
                                            self.engine.charging_move = ""
                                            self.p1_invulnerable = False


                                    # DAMAGE, RECOIL, SECONDARY EFFECT AND HEAL

                                    self.damage = self.engine.apply_damage_boost(self.damage,self.hp1_ratio) # damage boost
                                    self.new_hp1_percent_recoil = self.engine.recoil_damage(self.damage, self.hp1_ratio, self.pokemon_data[self.pokemon_name]["health"])
                                    secondary = self.engine.check_secondary_effect()
                                    self.pokemon1_heal = self.engine.check_heal_move(self.chosen_move.lower()) # check absord health move


                                else:
                                    # CHECK FOR ABSORB MOVE ABILITY
                                    self.opponent_ability_box_text = self.ability_pokemon2.capitalize() # take the foe pokemon ability name
                                    self.opponent_ability_box_showing = True  # show the ability text

                                    if self.ability_pokemon2 in ("lightning rod","flash fire"): 
                                        self.damage = 0
                                        if self.engine.stages_pokemon2["sp_attack"] !=6:
                                            self.message_queue.append(f"{self.opponent_name.capitalize()} has its Sp Atk increased!")

                                    elif self.ability_pokemon2 == "anger point": 
                                        self.message_queue.append(f"{self.opponent_name.capitalize()} has its ATK maxed out!")

                                    elif self.ability_pokemon2 == "damp":
                                        self.damage = 0
                                        self.message_queue.append(f"{self.pokemon_name.capitalize()} cant use {self.chosen_move.capitalize()}!")

                                    elif self.ability_pokemon2 == "water absorb":
                                        self.damage = 0
                                        if self.hp2_ratio <= 0.75:
                                            self.hp2_ratio += 0.25

                                        else:
                                            self.hp2_ratio = 1.0

                                        self.message_queue.append(f"{self.opponent_name.capitalize()} absorbed the water!")

                                    self.new_hp1_percent_recoil = self.hp1_ratio # avoid the recoil bug 
                                    secondary = "" # avoid the secondary bug
                                    

                                print(f"damage gay ra tu p1 len p2:{self.damage}")
                                

                                # CONTACT ABILITY
                                contact_status = self.engine.check_contact_ability()
                                if contact_status: # check if getting contact ability from pokemon 2
                                    self.opponent_ability_box_text = self.ability_pokemon2.capitalize() # take the foe pokemon ability name
                                    self.opponent_ability_box_showing = True  # show the ability text
                                    print(f"{self.engine.status_pokemon1} la hieu ung cua pokemon 1")
                                    if contact_status == "paralysis" and self.pokemon1_current_status == "":
                                        self.pokemon1_current_status = "paralysis"

                                        self.message_queue.append(f"{self.pokemon_name.capitalize()} is paralyzed by contact!")

                                    elif contact_status == "poison" and self.pokemon1_current_status == "":
                                        self.pokemon1_current_status = "poison"
                                        self.message_queue.append(f"{self.pokemon_name.capitalize()} is poisoned by contact!")

                                    elif contact_status == "burn" and self.pokemon1_current_status == "":
                                        self.pokemon1_current_status = "burn"
                                        self.message_queue.append(f"{self.pokemon_name.capitalize()} is burn by contact!")


                                # TOUCH ABILITY
                                touch_status = self.engine.check_touch_ability()
                                if touch_status and self.pokemon2_current_status == "":
                                    self.ability_box_text = self.pokemon_ability.capitalize() # take the foe pokemon ability name
                                    self.ability_box_showing = True 
                                    self.pokemon2_current_status = "poison"
                                    self.message_queue.append(f"{self.opponent_name.capitalize()} is poisoned by contact!")


                                #ACCURACY LOWERED MOVE
                                prevented_stat_lowered = self.engine.prevent_lowered_stat_ability()
                                print(f"hieu ung la{prevented_stat_lowered}")
                                if prevented_stat_lowered:
                                    self.opponent_ability_box_text = self.engine.pokemon2_ability.capitalize()
                                    self.opponent_ability_box_showing = True
                                    if self.engine.pokemon2_ability == "keen eye":
                                        self.message_queue.append(f"{self.opponent_name.capitalize()}'s accuracy cant be lowered!")
                                    elif self.engine.pokemon2_ability == "clear body":
                                        self.message_queue.append(f"{self.opponent_name.capitalize()}'s stats cant be lowered!")



                                self.move_done = True
                                self.move_hit = None

                                if self.chosen_move.lower() in ("take down","submission","double-edge"):
                                    self.recoil_decreasing = True # check if the move need recoil check



                                 # MESSAGE FOR DAMAGE AND CHECKING FOR SECONDARY EFFECTS OF ATTACKS   
                                if self.damage > 0:
                                    # DAMAGE CALCULATION
                                    self.hp2_ratio = self.pokemon2_previous_hp_percent - self.damage / self.pokemon_data[self.opponent_name]["health"]

                                    # CHECK STURDY
                                    if self.pokemon2_previous_hp_percent == 1.0 and self.hp2_ratio <= 0 and self.ability_pokemon2 == "sturdy": # check for ability sturdy
                                        self.opponent_ability_box_text = self.ability_pokemon2.capitalize() # take the foe pokemon ability name
                                        self.opponent_ability_box_showing = True  # show the ability text
                                        self.hp2_raw = 1
                                        self.hp2_ratio = 1 /self.pokemon_data[self.opponent_name]["health"]
                                        self.message_queue.append(f"{self.opponent_name.capitalize()} endured the hit! ")

                                    if crit and not self.opponent_ability_box_showing:
                                        self.message_queue.append("Critical hit!")
                                    elif effectiveness > 1.0 and not self.opponent_ability_box_showing:
                                        self.message_queue.append("It's super effective!")
                                    elif effectiveness < 1.0 and not self.opponent_ability_box_showing:
                                        if self.pokemon_ability.lower() != "tinted lens":
                                            self.message_queue.append("It's not very effective...")
                                    #SECONDARY 
                                    if secondary == "burn"  and self.pokemon2_current_status == "":
                                        self.message_queue.append(f"{self.opponent_name.capitalize()} was burned!")
                                        self.pokemon2_current_status = "burn"
                                        self.status_done_damage_this_turn = False
                                    elif secondary == "paralysis" and self.pokemon2_current_status == "":
                                        self.message_queue.append(f"{self.opponent_name.capitalize()} is paralyzed!")
                                        self.pokemon2_current_status = "paralysis"
                                    elif secondary == "freeze" and self.pokemon2_current_status == "":
                                        self.message_queue.append(f"{self.opponent_name.capitalize()} is frozen!")
                                        self.pokemon2_current_status = "freeze"
                                    elif secondary == "poison" and self.pokemon2_current_status == "":
                                        self.message_queue.append(f"{self.opponent_name.capitalize()} was poisoned!")
                                        self.pokemon2_current_status = "poison"
                                        self.status_done_damage_this_turn = False
                                    elif secondary == "flinch":
                                        self.message_queue.append(f"{self.opponent_name.capitalize()} flinched!")
                                        self.turn_done = True

                                    elif secondary == "confusion":
                                        self.message_queue.append(f"{self.opponent_name.capitalize()} is confused!")
                                        self.pokemon2_confusion = True

                                    elif secondary in ("attack","defense","sp_defense","speed"):
                                        if secondary == "sp_defense":
                                            self.message_queue.append(f"{self.opponent_name.capitalize()}'s Special Defense decreased!") # FIX THE _ ERROR OF SPDEFENSE
                                        else:
                                            self.message_queue.append(f"{self.opponent_name.capitalize()}'s {secondary.capitalize()} decreased!")

                                    if self.pokemon2_current_status == "freeze" and self.engine.pokemon1_move_data["type"] == "Fire" and self.engine.accuracy:
                                        self.pokemon2_current_status = ""
                                        self.engine.status_pokemon2 = None
                                        self.message_queue.append(f"{self.opponent_name.capitalize()} thawed out!")
                                        self.status_done_damage_this_turn = True


                                    # END OF TURN trap DAMAGE MOVE 
                                    if self.chosen_move.lower() in ("fire spin","wrap","bind","clamp"):
                                        self.being_trapped_p2 = True
                                        self.trapped_name_p2  = self.chosen_move.lower()
                                        self.trapped_done_damage_this_turn = False
                                        self.trapped_turn_p2 = random.randint(2,5)
                                        print(f"bi kep trong {self.trapped_turn_p2} luot")
                                        self.message_queue.append(f"{self.opponent_name.capitalize()} is trapped in {self.chosen_move.capitalize()}!")



                                # IF ITS A STATUS OR NON DAMAGING MOVE
                                elif self.damage == 0 and (self.engine.pokemon1_move_data["damage_type"] == "Status") and (self.engine.pokemon1_move_data["name"].lower() not in self.engine.weather_moves) and self.engine.charging_move == "" and self.chosen_move.lower() != "leech seed":  # status move or unaffect, also it cant be leech seed
                                    status = self.engine.status_pokemon2

                                    if self.engine.status_moves[self.chosen_move.lower()][3] == "self": # if its a stat increases
                                        if self.engine.status_moves[self.chosen_move.lower()][2] == 1:
                                            self.message_queue.append(f"{self.pokemon_name.capitalize()}'s {self.engine.status_moves[self.chosen_move.lower()][1].capitalize()} increased!")
                                        elif self.engine.status_moves[self.chosen_move.lower()][2] == 2:
                                            self.message_queue.append(f"{self.pokemon_name.capitalize()}'s {self.engine.status_moves[self.chosen_move.lower()][1].capitalize()} sharply increased!")

                                    if self.engine.status_moves[self.chosen_move.lower()][3] == "opponent" and not prevented_stat_lowered: # if its a stat increases
                                        if self.engine.status_moves[self.chosen_move.lower()][2] == -1:
                                            self.message_queue.append(f"{self.opponent_name.capitalize()}'s {self.engine.status_moves[self.chosen_move.lower()][1].capitalize()} fell!")
                                        elif self.engine.status_moves[self.chosen_move.lower()][2] == -2:
                                             self.message_queue.append(f"{self.opponent_name.capitalize()}'s {self.engine.status_moves[self.chosen_move.lower()][1].capitalize()} harshly fell!")
                                    elif self.engine.status_moves[self.chosen_move.lower()][3] == "opponent" and prevented_stat_lowered:
                                        self.message_queue.append(f"It doesn't affect {self.opponent_name.capitalize()}!")



                                    if self.engine.status_moves[self.chosen_move.lower()][0] == "status" and status is None:
                                        self.message_queue.append(f"It doesn't affect {self.opponent_name.capitalize()}!")

                                    if status == "poison" or status == "bad_poison":
                                        if status == "poison" and self.pokemon2_current_status == "":
                                            self.message_queue.append(f"{self.opponent_name.capitalize()} is poisoned!")
                                        elif status == "bad_poison" and self.pokemon2_current_status == "":
                                            self.message_queue.append(f"{self.opponent_name.capitalize()} is badly poisoned!")

                                        self.pokemon2_current_status = status

                                    elif status == "paralysis" and self.pokemon2_current_status == "":
                                        self.message_queue.append(f"{self.opponent_name.capitalize()} is paralyzed and may not move!")
                                        self.pokemon2_current_status = status

                                    elif status == "sleep" and self.pokemon2_current_status == "":
                                        self.message_queue.append(f"{self.opponent_name.capitalize()} fell asleep!")
                                        self.pokemon2_current_status = status


                                elif self.damage == 0 and self.chosen_move.lower() == "leech seed":
                                    if self.seeded_p2:
                                        self.message_queue.append("But it failed!")
                                    else:
                                        if "Grass" not in self.type_pokemon2:
                                            self.seeded_p2 = True
                                            self.trapped_done_damage_this_turn = False
                                            self.message_queue.append(f"{self.opponent_name.capitalize()} is seeded!")

                                        else:
                                            self.message_queue.append(f"{self.opponent_name.capitalize()} is unaffected!")


                                
                                # THIS IS THE UPDATE TO SHOW THE STATUS ICON 
                                if self.engine.my_pokemon_status is None or self.engine.my_pokemon_status =="" or self.engine.my_pokemon_status == "freeze"  or self.engine.my_pokemon_status == "sleep":
                                    self.engine.my_pokemon_status = self.pokemon1_current_status
                                if self.engine.opponent_pokemon_status is None or self.engine.opponent_pokemon_status == "" or self.engine.opponent_pokemon_status == "freeze"  or self.engine.opponent_pokemon_status == "sleep":
                                    self.engine.opponent_pokemon_status = self.pokemon2_current_status


                                # CHECK FOR DAMAGING STATUS AND END TURN MOVE

                                if self.pokemon2_current_status in ("poison", "bad_poison", "burn") or self.pokemon1_current_status in  ("poison", "bad_poison", "burn"):
                                    self.status_done_damage_this_turn = False

                                if self.being_trapped_p2 or self.being_trapped_p1 or self.seeded_p2 or self.seeded_p1:
                                    self.trapped_done_damage_this_turn = False



                        elif self.move_hit == False:
                            pygame.time.wait(500)
                            if self.chosen_move.lower() in self.engine.status_moves and self.engine.status_moves[self.chosen_move.lower()][1] in ("sleep","poison","bad_poison","paralysis","burn","freeze") and self.pokemon2_current_status !="":
                                self.message_queue.append("But it failed!") #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            else:
                                self.message_queue.append(f"{self.opponent_name.capitalize()} avoided the attack!")
                            self.move_done = True
                            self.damage_applied = True 
                            self.move_hit = None
                            self.multi_turn_move_charged = 0
                            self.engine.charging_move = ""

                            # SHOW THE STATUS ICON AND CHECK OR DAMGAIGNG STATUS

                            if self.engine.my_pokemon_status is None or self.engine.my_pokemon_status =="" or self.engine.my_pokemon_status == "sleep" or self.engine.my_pokemon_status == "freeze":
                                self.engine.my_pokemon_status = self.pokemon1_current_status
                            if self.engine.opponent_pokemon_status is None or self.engine.opponent_pokemon_status == "" or self.engine.opponent_pokemon_status == "sleep" or self.engine.opponent_pokemon_status == "freeze":
                                self.engine.opponent_pokemon_status = self.pokemon2_current_status

                            if self.pokemon2_current_status in ("poison", "bad_poison", "burn") or self.pokemon1_current_status in ("poison", "bad_poison", "burn"):
                                self.status_done_damage_this_turn = False

                            if self.being_trapped_p2 or self.being_trapped_p1 or self.seeded_p1 or self.seeded_p2:
                                self.trapped_done_damage_this_turn = False
                                

                #CHECK WHICH TURN IT IS, AND END IF MY POKEMON MOVE LAST
                if self.go_first_this_turn == "pokemon_2" and self.move_done and self.damage_applied and not self.move_hit:
                    self.turn_done = True
                    print(f"status of p1 my turn(2): {self.engine.status_pokemon1}")
                    print(f"status of p2 my turn(2): {self.engine.status_pokemon2}")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11")


            # RUN THE OPPONENT TURN IF ITS THE OPPONENT TURN
            elif self.hover == 3 and self.chosen_move and self.opponent_turn and not self.battle_over:
                self.run_opponent_turn(screen, pokemon_rect)



            self.update_messages(screen)

            # UPDATE HEALTH OF POKEMON2 
            if self.pokemon2_previous_hp_percent > self.hp2_ratio and self.pokemon2_previous_hp_percent > 0:
                    self.pokemon2_previous_hp_percent -= 0.0042
                    if self.pokemon2_previous_hp_percent <= self.hp2_ratio: # check at the last heal if bigger, let them equal
                        self.pokemon2_previous_hp_percent = self.hp2_ratio 

            elif self.pokemon2_previous_hp_percent < self.hp2_ratio and self.pokemon2_previous_hp_percent <= 1.0:
                self.pokemon2_previous_hp_percent += 0.0042
                if self.pokemon2_previous_hp_percent >= self.hp2_ratio: # check at the last heal if bigger, let them equal
                    self.pokemon2_previous_hp_percent = self.hp2_ratio 

            else:
                # check if pokemon faint
                self.check_fainting() 

                if self.recoil_decreasing and self.chosen_move:
                    self.recoil_decreasing = False

                    if self.new_hp1_percent_recoil < self.hp1_ratio: # this chunk of code check recoil damage
                        old_display = self.hp1_display 
                        recoil_taken = int((self.hp1_ratio - self.new_hp1_percent_recoil) * self.pokemon_data[self.pokemon_name]["health"])
                        self.hp1_number = max(0, self.hp1_number - recoil_taken)
                        self.new_hp1_percent_recoil = self.hp1_ratio
                        self.hp1_display = old_display 
                        if self.chosen_move.lower() in ("take down","submission","double-edge"):
                            self.message_queue.append(f"{self.pokemon_name.capitalize()} is hit by recoil!")

                # IF POKEMON1 USES HEALTH, HEAL
                if self.pokemon1_heal:
                    self.pokemon1_heal = False
                    self.hp1_number = min(self.pokemon_data[self.pokemon_name]["health"] ,self.hp1_number + int(self.damage / 2))
                    self.message_queue.append(f"{self.pokemon_name.capitalize()} regained its health!")

                # CHANGE TURN IF THE TURN ISNT DONE
                if self.chosen_move and self.move_done and self.damage_applied and not self.recoil_decreasing and not self.pokemon1_health_decreasing and not self.current_message and not self.message_queue and not self.turn_done: 
                    if not self.opponent_turn:                                                                                                                                                                              
                        self.opponent_turn = True
                        self.opponent_move_done = False      
                        self.opponent_damage_applied = False 
                        self.swap_turn_timer_start = pygame.time.get_ticks()

                # WHEN BOTH TURN ARE DONE AND ALL THE STATUS AND STUFF ARE DONE
                if self.turn_done and self.status_done_damage_this_turn and self.weather_done_damage_this_turn and not self.pokemon1_health_decreasing: 
                    self.turn_done = False 
                    self.chosen_move = ""
                    self.pokemon2_chosen_move = ""
                    self.hover = 0
                    print(self.engine.stages_pokemon1)
                    print(self.engine.stages_pokemon2)


            # DO THE WEATHER, STATUS
            if self.turn_done:
                if not self.weather_done_damage_this_turn and not self.pokemon1_health_decreasing and self.pokemon2_previous_hp_percent == self.hp2_ratio:
                    if self.weather_timer == 0:
                        self.weather_timer = pygame.time.get_ticks()
                    self.check_weather_damage(screen,pokemon_rect)

                if not self.trapped_done_damage_this_turn and self.weather_done_damage_this_turn and not self.pokemon1_health_decreasing and self.pokemon2_previous_hp_percent == self.hp2_ratio:
                    if self.trapped_timer == 0:
                        self.trapped_timer = pygame.time.get_ticks()

                    self.check_trapped_move(screen, pokemon_rect)

                if not self.status_done_damage_this_turn and self.weather_done_damage_this_turn and self.trapped_done_damage_this_turn and not self.pokemon1_health_decreasing and self.pokemon2_previous_hp_percent == self.hp2_ratio:
                    if self.status_timer == 0:
                        self.status_timer = pygame.time.get_ticks()

                    self.end_turn_status(screen,pokemon_rect) # check the end turn status
                    



    def run_opponent_turn(self, screen, pokemon_rect):
        move_list = ["tackle"]  # hahah
        if self.pokemon2_chosen_move == "":
            self.pokemon2_chosen_move = random.choice(move_list)
   
        swap_turn_timer_stop = pygame.time.get_ticks()

        if swap_turn_timer_stop - self.swap_turn_timer_start > 500 or self.go_first_this_turn == "pokemon_2": 

            # SWAP THE STATS
            self.engine.get_move(self.pokemon2_chosen_move)
            self.engine.get_pokemon1_def_spdef_speed_item_type_ability_turn(self.def_pokemon2, self.spdef_pokemon2, self.speed_pokemon2,"none", self.type_pokemon2, self.ability_pokemon2, self.opponent_turn)
            self.engine.get_pokemon1_atk_spatk(self.atk_pokemon2, self.spatk_pokemon2)
            self.engine.get_pokemon2_hp_def_spdef_speed_type_ability( self.hp1_number, self.def_pokemon1, self.spdef_pokemon1,self.speed_pokemon1, self.type_pokemon1, self.pokemon_ability)
            
            # accuracy check — only once
            if self.opponent_move_hit is None and not self.opponent_move_done:
                stage_2  = self.engine.stages_pokemon2
                self.engine.stages_pokemon2 = self.engine.stages_pokemon1 # swap the stages first
                self.engine.stages_pokemon1 = stage_2

                status_2 = self.engine.status_pokemon2
                self.engine.status_pokemon2 = self.engine.status_pokemon1
                self.engine.status_pokemon1 = status_2

                # CHECK STATUS ,PARALYSIS AND SLEEP AND FROZEN
                if self.pokemon2_current_status == "paralysis" and not self.engine.check_paralysis_attack():
                    print(f"hieu ung cua p2: {self.engine.status_pokemon1}")
                    self.message_queue.append(f"{self.opponent_name.capitalize()} can't move due to paralysis!")
                    self.opponent_damage_applied = True
                    self.opponent_move_done = True
                    self.opponent_move_hit = None
                    self._end_opponent_turn()
                    return
                
                elif self.pokemon2_current_status == "sleep" and self.sleep_animation_pokemon2_done:
                    asleep = self.engine.still_asleep()
                    if asleep:
                        self.message_queue.append(f"{self.opponent_name.capitalize()} is fast asleep!")
                        self.sleep_animation_pokemon2_done = False
                        self.opponent_move_hit = None
                        self.opponent_damage_applied = True
                    elif not asleep:
                        self.pokemon2_current_status =""
                        self.message_queue.append(f"{self.opponent_name.capitalize()} woke up!")
                        

                elif self.pokemon2_current_status == "freeze":
                    thaw_out = self.engine.check_thaw_out()
                    print(f"co hoi out ra la:{thaw_out}")
                    if not thaw_out:
                        print("chua ra")
                        #self.opponent_move_hit = False
                        self.message_queue.append(f"{self.opponent_name.capitalize()} is frozen solid!")
                        self.opponent_damage_applied = True
                        self.opponent_move_done = True
                        self.opponent_move_hit = None
                        self._end_opponent_turn()
                        return
                    elif thaw_out:
                        self.pokemon2_current_status =""
                        self.message_queue.append(f"{self.opponent_name.capitalize()} thawed out!")


                #CHECK CONFUSION
                if self.pokemon2_confusion:
                    self.message_queue.append(f"{self.opponent_name.capitalize()} is being confused!")
                    snap_out = random.randint(1,100)
                    self_hit = random.randint(1,100)
                    if snap_out <= 25:   # 30% CHANCE TO SNAP OUT CONFUSION
                        self.message_queue.append(f"{self.opponent_name.capitalize()} snaps out!")
                        self.pokemon2_confusion = False

                    else:
                        if self_hit <= 50:
                            self.message_queue.append(f"{self.opponent_name.capitalize()} hit itself!")
                            self.opponent_move_hit = None
                            self.opponent_damage_applied = True
                            damage  = round(((10* 40 * ((self.atk_pokemon1 * self.engine.stage_multipliers[self.engine.stages_pokemon1["attack"]])/(self.def_pokemon2 *self.engine.stage_multipliers[self.engine.stages_pokemon2["defense"]])))/50  + 2))
                            self.hp2_ratio = self.pokemon2_previous_hp_percent - damage/ self.pokemon_data[self.opponent_name]["health"]
                            print(f"mau cua hp2:{self.hp2_ratio}")
                            self.opponent_move_done = True
                            self._end_opponent_turn()
                            return
                            
 
                #DRAW ANIMAITON FOR SLEEP
                if not self.sleep_animation_pokemon2_done and not self.message_queue and not self.current_message:
                    play = self.animator.play(screen, "status sleep",self.opponent_frames[self.opponent_frame_index], self.opponent_pokemon_rect,self.pokemon1_sprite, pokemon_rect)
                    if play:
                        self.sleep_animation_pokemon2_done = True
                        self.opponent_move_done = True
                        self._end_opponent_turn()
                        return

                # CHECK ACCURACY (SKIP IF POKEMON IS SLEEPING)
                if not self.opponent_move_hit and self.pokemon2_current_status != "sleep": 
                    self.message_queue.append(f"{self.opponent_name.capitalize()} used {self.pokemon2_chosen_move.capitalize()}!")

                    # CHECK ACCURACY
                    self.opponent_move_hit = self.engine.check_accuracy()
                    if self.opponent_move_hit is None:
                        self.opponent_move_hit = True
                    elif self.opponent_move_hit is not None and self.p1_invulnerable:
                        self.opponent_move_hit = False



            # PLAY ANIMATION
            if self.opponent_move_hit and not self.opponent_damage_applied:
                if self.pokemon2_chosen_move.lower() in self.engine.status_moves and self.engine.status_moves[self.pokemon2_chosen_move.lower()][1] in ("sleep","poison","bad_poison","paralysis","burn","freeze") and self.pokemon1_current_status !="":
                    self.message_queue.append("But it failed!")
                    animation_done = True

                if self.pokemon2_chosen_move.lower() == "sandstorm" and self.engine.current_weather == "sandstorm":
                    self.message_queue.append("But it failed!")
                    animation_done = True

                elif self.pokemon2_chosen_move.lower() == "rain dance" and self.engine.current_weather == "rain dance":
                    self.message_queue.append("But it failed!")
                    animation_done = True

                elif self.pokemon2_chosen_move.lower() == "sunny day" and self.engine.current_weather == "sunny day":
                    self.message_queue.append("But it failed!")
                    animation_done = True

                elif self.engine.check_effectiveness() == 0: # dont play the animation when move is unaffected
                    animation_done = True

                else:
                    animation_done = self.animator.play(screen, self.pokemon2_chosen_move.lower(), self.pokemon1_sprite, pokemon_rect, self.opponent_frames[self.opponent_frame_index], self.opponent_pokemon_rect)

                if animation_done:
                    self.opponent_damage_applied = True
                    self.engine.stage_calculation()
                    damage, crit, effectiveness = self.engine.damage_calculation()

                    # CHECK WEATHER, RECOIL AND SECOANDAY
                    if not self.engine.check_absorb_move_ability():
                        
                        self.engine.check_weather()
                        if self.present_weather != "" and self.present_weather != self.engine.current_weather:
                            self.weather_turn = 0
                            self.present_weather = self.engine.current_weather

                        if self.engine.current_weather == "sandstorm":
                            if self.weather_turn == 0:
                                self.present_weather = "sandstorm"
                                self.weather_turn += 1
                                self.message_queue.append("A sandstorm brewed!")
                            self.weather_done_damage_this_turn = False
                        elif self.engine.current_weather == "rain dance":
                            if self.weather_turn == 0:
                                self.present_weather = "rain dance"
                                self.weather_turn += 1
                                self.message_queue.append("It started to rain!")
                            self.weather_done_damage_this_turn = False
                        elif self.engine.current_weather == "sunny day":
                            if self.weather_turn == 0:
                                self.present_weather = "sunny day"
                                self.weather_turn += 1
                                self.message_queue.append("The sunlight turned harsh!")
                            self.weather_done_damage_this_turn = False


                        # damage boost for opponent low HP abilities
                        damage = self.engine.apply_damage_boost(damage, self.hp2_ratio)

                        # recoil for opponent
                        new_hp2_recoil = self.engine.recoil_damage(damage, self.hp2_ratio, self.pokemon_data[self.opponent_name]["health"])

                        # secondary effect on player
                        secondary = self.engine.check_secondary_effect()

                        # heal move (mega drain heals opponent)
                        opponent_heal = self.engine.check_heal_move(self.pokemon2_chosen_move.lower())


                    else:
                        # CHECK ASBSORB ABILITY
                        self.ability_box_text = self.pokemon_ability.capitalize()
                        self.ability_box_showing = True

                        if self.pokemon_ability.lower() in ("lightning rod", "flash fire"):
                            damage = 0
                            if self.engine.stages_pokemon2["sp_attack"] != 6:
                                self.message_queue.append(f"{self.pokemon_name.capitalize()}'s {self.pokemon_ability.capitalize()} absorbed the move!")
                        elif self.pokemon_ability.lower() == "water absorb":
                            damage = 0
                            if self.hp1_ratio <= 0.75:
                                self.hp1_number = min(self.pokemon_data[self.pokemon_name]["health"], self.hp1_number + int(self.pokemon_data[self.pokemon_name]["health"] * 0.25))
                            else:
                                self.hp1_number = self.pokemon_data[self.pokemon_name]["health"]
                            self.message_queue.append(f"{self.pokemon_name.capitalize()} absorbed the water!")

                        new_hp2_recoil = self.hp2_ratio
                        secondary = ""
                        opponent_heal = False


                    # CONTACT ABILITY
                    contact_status = self.engine.check_contact_ability()
                    if contact_status:
                        self.ability_box_text = self.pokemon_ability.capitalize()
                        self.ability_box_showing = True

                        if contact_status == "paralysis" and self.pokemon2_current_status == "":
                            self.pokemon2_current_status = "paralysis"
                            self.message_queue.append(f"{self.opponent_name.capitalize()} is paralyzed by contact!")

                        elif contact_status == "poison" and self.pokemon2_current_status == "":
                            self.pokemon2_current_status = "poison"
                            self.message_queue.append(f"{self.opponent_name.capitalize()} was poisoned by contact!")
                            self.status_done_damage_this_turn = False

                        elif contact_status == "burn" and self.pokemon2_current_status == "":
                            self.pokemon2_current_status = "burn"
                            self.message_queue.append(f"{self.opponent_name.capitalize()} was burned by contact!")
                            self.status_done_damage_this_turn = False

                        elif contact_status == "sleep" and self.pokemon2_current_status == "":
                            self.pokemon2_current_status = "sleep"
                            self.message_queue.append(f"{self.opponent_name.capitalize()} fell asleep!")
                            

                    #TOUCH ABILITY
                    touch_status = self.engine.check_touch_ability()
                    if touch_status and self.pokemon1_current_status == "":
                        self.opponent_ability_box_text = self.ability_pokemon2.capitalize() # take the foe pokemon ability name
                        self.opponent_ability_box_showing = True 
                        self.pokemon1_current_status = "poison"
                        self.status_done_damage_this_turn = False
                        self.message_queue.append(f"{self.pokemon_name.capitalize()} is poisoned by contact!")


                    #ACCURACY LOWERED MOVE
                    prevented_stat_lowered = self.engine.prevent_lowered_stat_ability()
                    if prevented_stat_lowered:
                        self.ability_box_text = self.engine.pokemon2_ability.capitalize()
                        self.ability_box_showing = True
                        if self.engine.pokemon2_ability == "keen eye":
                            self.message_queue.append(f"{self.pokemon_name.capitalize()}'s accuracy cant be lowered!")
                        elif self.engine.pokemon2_ability == "clear body":
                            self.message_queue.append(f"{self.pokemon_name.capitalize()}'s stats cant be lowered!")


                    print(f"damage gay ra tu p2 len p1: {damage}")

                    # DAMAGE CAL
                    if damage > 0:
                        # update player HP
                        self.hp1_number = max(0, self.hp1_number - damage)

                        # STURDY 
                        if self.hp1_display == 1.0 and self.hp1_number == 0 and self.pokemon_ability== "Sturdy": # check for ability sturdy
                            self.ability_box_text = self.pokemon_ability.capitalize() # take the foe pokemon ability name
                            self.ability_box_showing = True  # show the ability text
                            self.hp1_number = 1
                            self.message_queue.append(f"{self.pokemon_name.capitalize()} endured the hit! ")

                        
                        #self.hp1_display = self.hp1_ratio

                        # SHOW CRIT TEXT
                        if crit and not self.ability_box_showing:
                            self.message_queue.append("Critical hit!")
                        elif effectiveness > 1.0:
                            self.message_queue.append("It's super effective!")
                        elif effectiveness < 1.0:
                            self.message_queue.append("It's not very effective...")

                        elif effectiveness == 0:
                            print("cu dau")
                            self.message_queue.append(f"It doesnt affect {self.pokemon_name.capitalize()}")

                        if secondary == "burn" and self.pokemon1_current_status == "":
                            self.pokemon1_current_status = "burn"
                            self.message_queue.append(f"{self.pokemon_name.capitalize()} was burned!")
                            self.status_done_damage_this_turn = False
                        elif secondary == "paralysis" and self.pokemon1_current_status == "":
                            self.pokemon1_current_status = "paralysis"
                            self.message_queue.append(f"{self.pokemon_name.capitalize()} is paralyzed!")
                        elif secondary == "freeze" and self.pokemon1_current_status == "":
                            self.pokemon1_current_status = "freeze"
                            self.message_queue.append(f"{self.pokemon_name.capitalize()} was frozen!")
                        elif secondary == "poison" and self.pokemon1_current_status == "":
                            self.pokemon1_current_status = "poison"
                            self.message_queue.append(f"{self.pokemon_name.capitalize()} was poisoned!")
                            self.status_done_damage_this_turn = False

                        elif secondary == "flinch" and self.go_first_this_turn == "pokemon_2":
                            self.turn_done = True
                            self.message_queue.append(f"{self.pokemon_name.capitalize()} flinched!")

                        elif secondary == "confusion":
                            self.message_queue.append(f"{self.pokemon_name.capitalize()} is confused!")
                            self.pokemon1_confusion = True

                        elif secondary in ("attack","defense","spdefense","speed"):
                            self.message_queue.append(f"{self.pokemon_name.capitalize()}'s {secondary.capitalize()} decreased!")
                            
                        # thaw player if hit by fire while frozen
                        if self.pokemon1_current_status == "freeze" and self.engine.pokemon1_move_data["type"] == "Fire" and self.engine.accuracy:
                            self.pokemon1_current_status = ""
                            self.engine.status_pokemon2 = None
                            self.message_queue.append(f"{self.pokemon_name.capitalize()} thawed out!")

                        #TRAPPED
                        if self.pokemon2_chosen_move.lower() in ("fire spin","wrap","bind","clamp"):
                            self.being_trapped_p1 = True
                            self.trapped_name_p1  = self.pokemon2_chosen_move.lower()
                            self.trapped_done_damage_this_turn = False
                            self.trapped_turn_p1 = random.randint(2,5)
                            self.message_queue.append(f"{self.pokemon_name.capitalize()} is trapped in {self.pokemon2_chosen_move.capitalize()}!")

                        # RECOIL
                        if new_hp2_recoil < self.hp2_ratio:
                            recoil_taken = int((self.hp2_ratio - new_hp2_recoil) * self.pokemon_data[self.opponent_name]["health"])
                            self.hp2_ratio = new_hp2_recoil
                            self.hp2_raw = max(0, int(self.hp2_ratio * self.pokemon_data[self.opponent_name]["health"]))
                            self.engine.get_pokemon2_current_hp(self.hp2_raw)
                            if self.pokemon2_chosen_move.lower() in ("take down", "submission", "double-edge"):
                                self.message_queue.append(f"{self.opponent_name.capitalize()} is hit by recoil!")

                        # HEAL IF USED HEAL MOVE
                        if opponent_heal:
                            heal_amount = int(damage / 2)
                            self.hp2_ratio = min(1.0, self.hp2_ratio + (heal_amount / self.pokemon_data[self.opponent_name]["health"]))
                            self.message_queue.append(f"{self.opponent_name.capitalize()} regained its health!")




                    elif damage == 0 and self.engine.pokemon1_move_data["damage_type"] == "Status" and self.engine.pokemon1_move_data["name"].lower() not in self.engine.weather_moves and self.pokemon2_chosen_move.lower() != "leech seed":
                        status = self.engine.status_pokemon2

                        if self.engine.status_moves[self.pokemon2_chosen_move.lower()][3] == "self":
                            if self.engine.status_moves[self.pokemon2_chosen_move.lower()][2] == 1:
                                self.message_queue.append(f"{self.opponent_name.capitalize()}'s {self.engine.status_moves[self.pokemon2_chosen_move.lower()][1].capitalize()} increased!")
                            elif self.engine.status_moves[self.engine.pokemon1_move_data["name"].lower()][2] == 2:
                                self.message_queue.append(f"{self.opponent_name.capitalize()}'s {self.engine.status_moves[self.pokemon2_chosen_move.lower()][1].capitalize()} sharply increased!")

                        if self.engine.status_moves[self.pokemon2_chosen_move.lower()][3] == "opponent" and not prevented_stat_lowered: # if its a stat increases
                            if self.engine.status_moves[self.pokemon2_chosen_move.lower()][2] == -1:
                                self.message_queue.append(f"{self.pokemon_name.capitalize()}'s {self.engine.status_moves[self.pokemon2_chosen_move.lower()][1].capitalize()} fell!")
                            elif self.engine.status_moves[self.pokemon2_chosen_move.lower()][2] == -2:
                                    self.message_queue.append(f"{self.pokemon_name.capitalize()}'s {self.engine.status_moves[self.pokemon2_chosen_move.lower()][1].capitalize()} harshly fell!")
                        elif status is None and self.engine.status_moves[self.pokemon2_chosen_move.lower()][3] == "opponent" and prevented_stat_lowered:
                            self.message_queue.append(f"It doesn't affect {self.pokemon_name.capitalize()}!")


                        if self.engine.status_moves[self.pokemon2_chosen_move.lower()][0] == "status" and status is None:
                            self.message_queue.append(f"It doesn't affect {self.pokemon_name.capitalize()}!")

                        if status == "poison" or status == "bad_poison":
                            if status == "poison" and self.pokemon1_current_status == "":
                                self.message_queue.append(f"{self.pokemon_name.capitalize()} is poisoned!")
                            elif status == "bad_poison" and self.pokemon1_current_status == "":
                                self.message_queue.append(f"{self.pokemon_name.capitalize()} is badly poisoned!")
                            self.pokemon1_current_status = status

                        elif status == "paralysis" and self.pokemon1_current_status == "":
                            self.message_queue.append(f"{self.pokemon_name.capitalize()} is paralyzed and may not move!")
                            self.pokemon1_current_status = status

                        elif status == "sleep" and self.pokemon1_current_status =="":
                            self.message_queue.append(f"{self.pokemon_name.capitalize()} fell asleep!")
                            self.pokemon1_current_status = status


                        synchronize = self.engine.ability_synchonize()
                        print(f"synchronize: {synchronize}")
                        if synchronize:
                            self.ability_box_text = self.pokemon_ability.capitalize()
                            self.ability_box_showing = True
                            self.pokemon2_current_status = self.pokemon1_current_status
                            self.message_queue.append(f"{self.opponent_name.capitalize()} is synchronized!")
                            self.status_done_damage_this_turn = False


                    elif damage == 0 and self.pokemon2_chosen_move.lower() == "leech seed":
                        if self.seeded_p1:
                            self.message_queue.append("But it failed!")
                        else:
                            if "Grass" not in self.type_pokemon1:
                                self.seeded_p1 = True
                                self.trapped_done_damage_this_turn = False
                                self.message_queue.append(f"{self.pokemon_name.capitalize()} is seeded!")

                            else:
                                self.message_queue.append(f"{self.pokemon_name.capitalize()} is unaffected!")


                    # SHOW STATUS ICON 
                    if self.engine.my_pokemon_status is None or self.engine.my_pokemon_status =="" or self.engine.my_pokemon_status == "sleep" or self.engine.my_pokemon_status == "freeze":
                        self.engine.my_pokemon_status = self.pokemon1_current_status
                    if self.engine.opponent_pokemon_status is None or self.engine.opponent_pokemon_status == "" or self.engine.opponent_pokemon_status == "sleep" or self.engine.opponent_pokemon_status == "freeze":
                        self.engine.opponent_pokemon_status = self.pokemon2_current_status

                    self.opponent_move_done = True
                    self.opponent_move_hit = None
                    self._end_opponent_turn()


            elif self.opponent_move_hit == False:
                self.message_queue.append(f"{self.pokemon_name.capitalize()} avoided the attack!")

                self.opponent_damage_applied = True
                self.opponent_move_done = True
                self.opponent_move_hit = None

                #SHOW STATUS ICON
                if self.engine.my_pokemon_status is None or self.engine.my_pokemon_status =="" or self.engine.my_pokemon_status == "sleep" or self.engine.my_pokemon_status == "freeze":
                    self.engine.my_pokemon_status = self.pokemon1_current_status
                if self.engine.opponent_pokemon_status is None or self.engine.opponent_pokemon_status == "" or self.engine.opponent_pokemon_status == "sleep" or self.engine.opponent_pokemon_status == "freeze":
                    self.engine.opponent_pokemon_status = self.pokemon2_current_status

                self._end_opponent_turn()



    def _end_opponent_turn(self):
        self.opponent_turn = False
        if self.go_first_this_turn == "pokemon_1" or self.chosen_move == "change": # IF ITS A CHANGE MOVE
            self.turn_done = True # turn is done if both pokemon finish moving, is False if p1 doesnt move yet    
        
        # restore engine to normal player-attacks-opponent orientation
        self.engine.get_pokemon1_atk_spatk(self.atk_pokemon1, self.spatk_pokemon1)
        self.engine.get_pokemon1_def_spdef_speed_item_type_ability_turn(
            self.def_pokemon1, self.spdef_pokemon1, self.speed_pokemon1,
            self.pokemon_item, self.type_pokemon1, self.pokemon_ability
        ,self.opponent_turn)
        self.engine.get_pokemon2_hp_def_spdef_speed_type_ability(
            self.hp2_raw, self.def_pokemon2, self.spdef_pokemon2,
            self.speed_pokemon2, self.type_pokemon2, self.ability_pokemon2
        )

        stage_1  = self.engine.stages_pokemon2
        self.engine.stages_pokemon2 = self.engine.stages_pokemon1 # swap the stages back
        self.engine.stages_pokemon1 = stage_1
       

        status_1 = self.engine.status_pokemon2
        self.engine.status_pokemon2 = self.engine.status_pokemon1 # swap the status too
        self.engine.status_pokemon1 = status_1 


        if self.pokemon2_current_status in ("poison", "bad_poison", "burn") or self.pokemon1_current_status in  ("poison", "bad_poison", "burn"):
            self.status_done_damage_this_turn = False

        if self.being_trapped_p1 or self.being_trapped_p2 or self.seeded_p1 or self.seeded_p2:
            self.trapped_done_damage_this_turn = False


        print(f"status of p1 op turn:{self.engine.status_pokemon1}")
        print(f"status of p2 op turn:{self.engine.status_pokemon2}")
        print(f"status of p1 op turn:{self.engine.my_pokemon_status}")
        print(f"status of p2 op turn:{self.engine.opponent_pokemon_status}")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!")


    def crop_sprite(self, surface):
        bounds = surface.get_bounding_rect()  # finds the non-transparent area
        cropped = pygame.Surface(bounds.size, pygame.SRCALPHA)
        cropped.blit(surface, (0, 0), bounds)
        return cropped
    


    def check_nature(self):

        # Map nature directly to multipliers ordered by: [Atk, Def, SpAtk, SpDef, Spd]
        # Neutral natures defaults to [1.0, 1.0, 1.0, 1.0, 1.0]
        nature_multipliers = {
            # Attack Boosts
            "adamant": [1.1, 1.0, 0.9, 1.0, 1.0],
            "brave":   [1.1, 1.0, 1.0, 1.0, 0.9],
            "lonely":  [1.1, 0.9, 1.0, 1.0, 1.0],
            "naughty": [1.1, 1.0, 1.0, 0.9, 1.0],
            # Defense Boosts
            "bold":    [0.9, 1.1, 1.0, 1.0, 1.0],
            "impish":  [1.0, 1.1, 0.9, 1.0, 1.0],
            "relaxed": [1.0, 1.1, 1.0, 1.0, 0.9],
            "lax":     [1.0, 1.1, 1.0, 0.9, 1.0],
            # Sp. Attack Boosts
            "modest":  [0.9, 1.0, 1.1, 1.0, 1.0],
            "mild":    [1.0, 0.9, 1.1, 1.0, 1.0],
            "quiet":   [1.0, 1.0, 1.1, 1.0, 0.9],
            "rash":    [1.0, 1.0, 1.1, 0.9, 1.0],
            # Sp. Defense Boosts
            "calm":    [0.9, 1.0, 1.0, 1.1, 1.0],
            "careful": [1.0, 1.0, 0.9, 1.1, 1.0],
            "sassy":   [1.0, 1.0, 1.0, 1.1, 0.9],
            "gentle":  [1.0, 0.9, 1.0, 1.1, 1.0],
            # Speed Boosts
            "jolly":   [1.0, 1.0, 0.9, 1.0, 1.1],
            "timid":   [0.9, 1.0, 1.0, 1.0, 1.1],
            "hasty":   [1.0, 0.9, 1.0, 1.0, 1.1],
            "naive":   [1.0, 1.0, 1.0, 0.9, 1.1],
        }

        #  Get multipliers for the nature (defaulting to 1.0 for neutral natures)
        nature = self.pokemon_nature.lower()
        mods = nature_multipliers.get(nature, [1.0, 1.0, 1.0, 1.0, 1.0])

        self.atk_pokemon1   = int(self.atk_pokemon1 * mods[0])
        self.def_pokemon1   = int(self.def_pokemon1 * mods[1])
        self.spatk_pokemon1 = int(self.spatk_pokemon1 * mods[2])
        self.spdef_pokemon1 = int(self.spdef_pokemon1 * mods[3])
        self.speed_pokemon1 = int(self.speed_pokemon1 * mods[4])



    def handle_event(self, event):
        if self.battle_over:
            return
    
        if event.type == pygame.MOUSEMOTION:
            if self.hover == 3:  # don't reset if moves screen is open
                self.hovered_move = -1
                for i, rect in enumerate(self.move_rects):
                    if rect.collidepoint(event.pos):
                        self.hovered_move = i

            elif self.hover  == 4:
                self.hovered_move = -2
                if self.sub_pokemon_rect.collidepoint(event.pos):
                    self.hovered_move = 1


            elif self.hover != 3 and self.hover != 4:
                self.hover = 0
                if self.move_surface_rect.collidepoint(event.pos): 
                    self.hover = 1
                elif self.change_pokemon_surface_rect.collidepoint(event.pos):
                    self.hover = 2




        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.sub_pokemon_rect.collidepoint(event.pos) and self.hover == 4:
                self.message_queue.append("Pokemon has been changed!")
                self.battle_set_pokemon("charizard","Charcoal","Blaze",["Tackle","Scratch","Submission","Fire Blast"],"Hardy")
                self.chosen_move = "change" # THE CHANGE MOVE
                self.engine.charging_move = ""
                self.move_done = True
                self.damage_applied = True
                self.turn_done = False
                self.opponent_turn = False
                self.engine.status_pokemon1 = None
                self.engine.my_pokemon_status = None
                self.engine.stages_pokemon1 = {"attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0, "accuracy": 0, "evasion": 0}
                self.hover = 3

            if self.move_surface_rect.collidepoint(event.pos):
                self.hover = 3 
                self.move_rects = []  # <-- clear so old rects don't fire
                return 
            # CHANGE POKEMON
            elif self.change_pokemon_surface_rect.collidepoint(event.pos) and self.hover != 3:
                self.hover = 4 # go to change pokemon
                self.move_rects = []    

            elif self.hover == 3 and event.button == 3 and not self.chosen_move:  # right click to go back
                self.hover = 0

            elif self.hover == 4 and event.button == 3 and not self.chosen_move:
                self.hover = 0

            for i, rect in enumerate(self.move_rects):
                if rect.collidepoint(event.pos):  # check if the move has been chosen, if yes then get the move name
                    if self.pokemon_moves[i].lower() != self.engine.charging_move and self.engine.charging_move !="":
                        pass
                    else:
                        self.move_done = False
                        self.recoil_decreasing = False
                        self.damage_applied = False
                        self.chosen_move = self.pokemon_moves[i] 
                        self.text_index = 0
                        self.paralysis_checked = False  # add this
                        self.pokemon1_heal = False
                        self.pokemon2_heal = False

                        self.opponent_turn = True if self.engine.move_priority() == "pokemon_2" else False
                        self.opponent_move_done = False      
                        self.opponent_damage_applied = False
                        self.status_done_damage_this_turn = False
                        self.go_first_this_turn = "pokemon_2" if  self.engine.move_priority() == "pokemon_2" else "pokemon_1"
                        print(f"TURN: {self.go_first_this_turn}")
                        self.weather_done_damage_this_turn = True


                    

    
    def update_messages(self, screen):
        if not self.current_message and self.message_queue:
            self.current_message = self.message_queue.pop(0)
            self.message_timer = pygame.time.get_ticks()

        if self.current_message:
            if self.ability_box_showing:
                ability_box_rect = self.ability_box.get_rect(center=(100, 200))
                screen.blit(self.ability_box, ability_box_rect)
                ability_text = self.font_pokemon2.render(self.ability_box_text, True, (0, 0, 0))
                screen.blit(ability_text, (ability_box_rect.x + 10, ability_box_rect.y + 10))

            if self.opponent_ability_box_showing:
                ability_box_rect = self.ability_box.get_rect(center=(710, 70))
                screen.blit(self.ability_box, ability_box_rect)
                ability_text = self.font_pokemon2.render(self.opponent_ability_box_text, True, (0, 0, 0))
                screen.blit(ability_text, (ability_box_rect.x + 10, ability_box_rect.y + 10))
                

            msg_surface = self.font_pokemon1.render(self.current_message, True, (0, 0, 0))
            screen.blit(msg_surface, (300, 350))
            if pygame.time.get_ticks() - self.message_timer >= self.message_duration:
                self.current_message = ""
                self.message_timer = None
                self.ability_box_showing = False
                self.opponent_ability_box_showing = False
                self.ability_box_text = ""
                self.opponent_ability_box_text =""



    def end_turn_status(self,screen, pokemon_rect):
        if (self.pokemon2_current_status != "" or self.pokemon1_current_status !="") and self.status_timer != 0: # if there is a status effect
            if pygame.time.get_ticks() - self.status_timer >= 1300 and not self.message_queue and not self.current_message:

                # play animation for p2 first
                if self.pokemon2_current_status in ("burn", "poison", "bad_poison") and not self.animation_status_p2_done:
                    move_name = "ember" if self.pokemon2_current_status == "burn" else "status poison"
                    animation_done = self.animator.play(screen, move_name,self.opponent_frames[self.opponent_frame_index], self.opponent_pokemon_rect,self.pokemon1_sprite, pokemon_rect)
                    if not animation_done:
                        return
                    self.animation_status_p2_done = True


                # then play animation for p1
                if self.pokemon1_current_status in ("burn", "poison", "bad_poison") and not self.animation_status_p1_done:
                    move_name = "ember" if self.pokemon1_current_status == "burn" else "status poison"
                    animation_done = self.animator.play(screen, move_name,self.pokemon1_sprite, pokemon_rect,self.opponent_frames[self.opponent_frame_index], self.opponent_pokemon_rect)
                    if not animation_done:
                        return
                    self.animation_status_p1_done = True



                # APPLY DAMAGE
                if self.pokemon2_current_status != "":
                    
                    self.hp2_ratio = self.engine.check_end_turn(self.hp2_ratio)
                    self.hp2_raw = int(self.hp2_ratio * self.pokemon_data[self.opponent_name]["health"])
                    self.engine.get_pokemon2_current_hp(self.hp2_raw)

                if self.pokemon1_current_status != "":
                    self.hp1_number = int(self.engine.check_end_turn_pokemon1(self.hp1_ratio) * self.pokemon_data[self.pokemon_name]["health"])



                #STATUS CHECK POKEMON 2
                if self.pokemon2_current_status in ("poison","bad_poison"):

                    self.message_queue.append(f"{self.opponent_name.capitalize()} is hurt by poison!")

                elif self.pokemon2_current_status == "burn":
                    self.message_queue.append(f"{self.opponent_name.capitalize()} is hurt by the burn!")

                #STATUS CHECK POKEMON 1

                if self.pokemon1_current_status in ("poison","bad_poison"):
                    self.message_queue.append(f"{self.pokemon_name.capitalize()} is hurt by poison!")

                elif self.pokemon1_current_status == "burn":
                    self.message_queue.append(f"{self.pokemon_name.capitalize()} is hurt by the burn!")


                self.status_done_damage_this_turn = True
                self.status_timer = 0
                self.animation_status_p2_done = False
                self.animation_status_p1_done = False

        else:
            self.status_done_damage_this_turn = True
            self.status_timer = 0
        
        

    def check_weather_damage(self,screen,pokemon_rect):
        if pygame.time.get_ticks() - self.weather_timer > 1500:
            if not self.end_turn_weather_animation_done:
                if self.engine.current_weather == "sandstorm":
                    animation = self.animator.play(screen, "sandstorm",self.opponent_frames[self.opponent_frame_index],self.opponent_pokemon_rect, self.pokemon1_sprite, pokemon_rect)
                elif self.engine.current_weather == "rain dance":
                    animation = self.animator.play(screen, "rain dance",self.opponent_frames[self.opponent_frame_index],self.opponent_pokemon_rect, self.pokemon1_sprite, pokemon_rect)
                
                elif self.engine.current_weather == "sunny day":
                    animation = self.animator.play(screen, "sunny day",self.opponent_frames[self.opponent_frame_index],self.opponent_pokemon_rect, self.pokemon1_sprite, pokemon_rect)
                

            if animation:
                if self.weather_turn <= 4:
                    self.weather_turn += 1
                    if self.engine.current_weather == "sandstorm":
                        self.message_queue.append("The sandstorm rages!")
                    elif self.engine.current_weather == "rain dance":
                        self.message_queue.append("Rain continues to fall!")
                    elif self.engine.current_weather == "sunny day":
                        self.message_queue.append("The sunlight is strong!")
                                            
                elif self.weather_turn == 5:
                    self.weather_turn = 0
                    if self.engine.current_weather == "sandstorm":
                        self.message_queue.append("The sandstorm subsided!")
                    elif self.engine.current_weather == "rain dance":
                        self.message_queue.append("The rain stopped")
                    elif self.engine.current_weather == "sunny day":
                        self.message_queue.append("The sunlight faded!")
                    
                    self.engine.current_weather = None
                    self.present_weather = ""


                if not self.weather_done_damage_this_turn and self.engine.current_weather == "sandstorm" and self.pokemon_ability.lower() != "cloud nine" and self.ability_pokemon2 != "cloud nine":
                    if "Steel" not in self.type_pokemon1 and "Ground" not in self.type_pokemon1:
                        self.hp1_number-= int(self.pokemon_data[self.pokemon_name]["health"] / 16)
                        self.message_queue.append(f"{self.pokemon_name.capitalize()} is buffed by sandstorm!")

                    if "Steel" not in self.type_pokemon2 and "Ground" not in self.type_pokemon2:
                        self.hp2_ratio -= 0.0625
                        self.message_queue.append(f"{self.opponent_name.capitalize()} is buffed by sandstorm!")

                self.weather_done_damage_this_turn = True
                self.weather_timer = 0
                self.end_turn_weather_animation_done = False # setting to false for the next sandstorm move


    def check_trapped_move(self, screen, pokemon_rect):
        if pygame.time.get_ticks() - self.trapped_timer > 1500 and not self.message_queue and not self.current_message:

            #animation
            if self.being_trapped_p2 and not self.trapped_animation_transition:
                animation_done = self.animator.play(screen, self.trapped_name_p2 ,self.opponent_frames[self.opponent_frame_index], self.opponent_pokemon_rect,self.pokemon1_sprite, pokemon_rect)
                if not animation_done:
                    return
                
            self.trapped_animation_transition = True
            
            if self.being_trapped_p1 and self.trapped_animation_transition: # FINISH P2 ANIMAITON FIRST THEN P1
                animation_done = self.animator.play(screen, self.trapped_name_p1,self.pokemon1_sprite, pokemon_rect,self.opponent_frames[self.opponent_frame_index], self.opponent_pokemon_rect)
                if not animation_done:
                    return
                

            #LEECH SEED ANIMAITON   
            if self.seeded_p2 and not self.seed_animation_transition:
                animation_done = self.animator.play(screen, "mega drain" ,self.opponent_frames[self.opponent_frame_index], self.opponent_pokemon_rect,self.pokemon1_sprite, pokemon_rect)
                if not animation_done:
                    return
            self.seed_animation_transition = True
                
            if self.seeded_p1 and self.seed_animation_transition:
                animation_done = self.animator.play(screen, "mega drain",self.pokemon1_sprite, pokemon_rect,self.opponent_frames[self.opponent_frame_index], self.opponent_pokemon_rect)
                if not animation_done:
                    return
                

            # HEALTH DECREASE   
            if self.being_trapped_p2 and self.trapped_counter_p2 < self.trapped_turn_p2:
                self.message_queue.append(f"{self.opponent_name.capitalize()} is hurted by {self.trapped_name_p2.capitalize()}!")
                self.hp2_ratio -= 0.125
                self.trapped_counter_p2 += 1

            if self.being_trapped_p1 and self.trapped_counter_p1 < self.trapped_turn_p1 :
                self.message_queue.append(f"{self.pokemon_name.capitalize()} is hurted by {self.trapped_name_p1.capitalize()}!")
                self.hp1_number -= int(self.pokemon_data[self.pokemon_name]["health"] / 8)
                self.trapped_counter_p1 += 1


            # HEALTH INCREASE FOR LEECH SEED
            if self.seeded_p2:
                self.hp2_ratio -= 0.125
                self.hp1_number = min(int(self.pokemon_data[self.pokemon_name]["health"]), self.hp1_number + int(self.pokemon_data[self.pokemon_name]["health"]/8))
                self.message_queue.append(f"{self.opponent_name.capitalize()} health is drained!")

            if self.seeded_p1:
                self.hp1_number -= int(self.pokemon_data[self.opponent_name]["health"] / 8)
                self.hp2_ratio = min(1.0, self.hp2_ratio + 0.125)
                self.message_queue.append(f"{self.pokemon_name.capitalize()} health is drained!")

            #RELEASE
            if self.trapped_counter_p2 == self.trapped_turn_p2 and self.being_trapped_p2:
                self.message_queue.append(f"{self.opponent_name.capitalize()} is released!")
                self.being_trapped_p2 = False
                self.trapped_turn_p2 = 0
                self.trapped_counter_p2 = 0
                self.trapped_name_p2 = ""
            
            if self.trapped_counter_p1 == self.trapped_turn_p1 and self.being_trapped_p1:
                self.message_queue.append(f"{self.pokemon_name.capitalize()} is released!")
                self.being_trapped_p1 = False
                self.trapped_turn_p1 = 0
                self.trapped_counter_p1 = 0
                self.trapped_name_p1 = ""
            

            self.trapped_done_damage_this_turn = True
            self.trapped_timer = 0
            self.trapped_animation_transition = False
            self.seed_animation_transition = False



                

    def check_fainting(self):
        # check pokemon 1 health
        if self.hp2_ratio <= 0:
            self.pokemon2_fainted = True
            self.battle_over = True

        if self.hp1_ratio <= 0:
            self.pokemon1_fainted = True
            self.battle_over = True








    