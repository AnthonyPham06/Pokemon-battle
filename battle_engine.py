import json
import random 
import pygame
import math

class Battle_Engine:
    def __init__(self):
        with open('moves.json', 'r') as f:
            move_list = json.load(f)
        self.moves = {m["name"].lower(): m for m in move_list}

        self.stages_pokemon1 = {"attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0, "accuracy": 0, "evasion": 0}
        self.stages_pokemon2 = {"attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0, "accuracy": 0, "evasion": 0}


        self.status_pokemon1 = None  # "burn", "poison", "toxic", "paralysis", "sleep", "freeze"  # initally let the status effect == nONE
        self.status_pokemon2 = None


        #move of pokemon 1
        self.pokemon1_move_data = {}
        self.pokemon1_move_name = ""

        self.type_chart = {
        "Normal": {
            "Rock": 0.5, "Ghost": 0.0, "Steel": 0.5},
        "Fire": {
            "Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 2.0, "Bug": 2.0, "Rock": 0.5, "Dragon": 0.5, "Steel": 2.0
        },
        "Water": {
            "Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Ground": 2.0, "Rock": 2.0, "Dragon": 0.5
        },
        "Electric": {
            "Water": 2.0, "Electric": 0.5, "Grass": 0.5, "Ground": 0.0, "Flying": 2.0, "Dragon": 0.5
        },
        "Grass": {
            "Fire": 0.5, "Water": 2.0, "Grass": 0.5, "Poison": 0.5, "Ground": 2.0, "Flying": 0.5, "Bug": 0.5, "Rock": 2.0, "Dragon": 0.5, "Steel": 0.5
        },
        "Ice": {
            "Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 0.5, "Ground": 2.0, "Flying": 2.0, "Dragon": 2.0, "Steel": 0.5
        },
        "Fighting": {
            "Normal": 2.0, "Ice": 2.0, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2.0, "Ghost": 0.0, "Dark": 2.0, "Steel": 2.0, "Fairy": 0.5
        },
        "Poison": {
            "Grass": 2.0, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0.0, "Fairy": 2.0
        },
        "Ground": {
            "Fire": 2.0, "Electric": 2.0, "Grass": 0.5, "Poison": 2.0, "Flying": 0.0, "Bug": 0.5, "Rock": 2.0, "Steel": 2.0
        },
        "Flying": {
            "Electric": 0.5, "Grass": 2.0, "Fighting": 2.0, "Bug": 2.0, "Rock": 0.5, "Steel": 0.5
        },
        "Psychic": {
            "Fighting": 2.0, "Poison": 2.0, "Psychic": 0.5, "Dark": 0.0, "Steel": 0.5
        },
        "Bug": {
            "Fire": 0.5, "Grass": 2.0, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Psychic": 2.0, "Ghost": 0.5, "Dark": 2.0, "Steel": 0.5, "Fairy": 0.5
        },
        "Rock": {
            "Fire": 2.0, "Ice": 2.0, "Fighting": 0.5, "Ground": 0.5, "Flying": 2.0, "Bug": 2.0, "Steel": 0.5
        },
        "Ghost": {
            "Normal": 0.0, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5
        },
        "Dragon": {
            "Dragon": 2.0, "Steel": 0.5, "Fairy": 0.0
        },
        "Dark": {
            "Fighting": 0.5, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5, "Fairy": 0.5
        },
        "Steel": {
            "Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2.0, "Rock": 2.0, "Steel": 0.5, "Fairy": 2.0
        },
        "Fairy": {
            "Fire": 0.5, "Fighting": 2.0, "Poison": 0.5, "Dragon": 2.0, "Dark": 2.0, "Steel": 0.5
        }
        }

        self.stage_multipliers = {
            -6: 0.25, -5: 0.28, -4: 0.33, -3: 0.4,
            -2: 0.5,  -1: 0.67,  0: 1.0,
             1: 1.5,   2: 2.0,   3: 2.5,
             4: 3.0,   5: 3.5,   6: 4.0
        }

        self.status_moves = {
            "swords dance":   ("stages", "attack", +2, "self"),
            "growl":          ("stages", "attack", -1, "opponent"),
            "tail whip":      ("stages", "defense", -1, "opponent"),
            
            # Stat-modifying Status Moves
            "sand attack":    ("stages", "accuracy", -1, "opponent"),
            "leer":           ("stages", "defense", -1, "opponent"),
            "growth":         ("stages", "special", +1, "self"),
            "string shot":    ("stages", "speed", -1, "opponent"),
            "meditate":       ("stages", "attack", +1, "self"),
            "agility":        ("stages", "speed", +2, "self"),
            "screech":        ("stages", "defense", -2, "opponent"),
            "double team":    ("stages", "evasion", +1, "self"),
            "harden":         ("stages", "defense", +1, "self"),
            "minimize":       ("stages", "evasion", +1, "self"),
            "smokescreen":    ("stages", "accuracy", -1, "opponent"),
            "withdraw":       ("stages", "defense", +1, "self"),
            "defense curl":   ("stages", "defense", +1, "self"),
            "barrier":        ("stages", "defense", +2, "self"),
            "amnesia":        ("stages", "special", +2, "self"),
            "kinesis":        ("stages", "accuracy", -1, "opponent"),
            
            # Primary Non-Volatile Status Inflicting Moves
            "sing":           ("status", "sleep", 1, "opponent"),
            "poison powder":  ("status", "poison", 1, "opponent"),
            "stun spore":     ("status", "paralysis", 1, "opponent"),
            "sleep powder":   ("status", "sleep", 1, "opponent"),
            "thunder wave":   ("status", "paralysis", 1, "opponent"),
            "toxic":          ("status", "bad_poison", 1, "opponent"),
            "hypnosis":       ("status", "sleep", 1, "opponent"),
            "glare":          ("status", "paralysis", 1, "opponent"),
            "poison gas":     ("status", "poison", 1, "opponent"),
            "lovely kiss":    ("status", "sleep", 1, "opponent")

        }

        self.weather_moves = ("sandstorm", "sunny day","rain dance")
        self.current_weather = None



        self.condition_moves = {
        "thunder wave": "paralysis",
        "toxic":        "toxic",
        "sleep powder": "sleep",
        
        # Primary Non-Volatile Status Moves
        "sing":          "sleep",
        "poison powder": "poison",
        "stun spore":    "paralysis",
        "hypnosis":      "sleep",
        "glare":         "paralysis",
        "poison gas":    "poison",
        "lovely kiss":   "sleep",
        
        # Volatile / Confusion Status Moves
        "supersonic":    "confusion",
        "confuse ray":   "confusion"
        }

        self.secondary_effects = {
    "poison sting": ("poison",    10),
    "fire punch":   ("burn",      10),  # 10% chance
    "ice punch":    ("freeze",    10),
    "thunder punch":("paralysis", 10),
    "ember":        ("burn",      10),
    "flamethrower": ("burn",      30),
    "fire blast":   ("burn",      30),
    "thunderbolt":  ("paralysis", 10),
    "thunder":      ("paralysis", 10),
    "ice beam":     ("freeze",    10),
    "blizzard":     ("freeze",    10),
    "body slam":    ("paralysis", 10),
    "stomp":        ("flinch",    30),
    "headbutt":     ("flinch",    30),
    "bite":         ("flinch",    30),
    "low kick":     ("flinch",    30),
    "bone club":    ("flinch",    10),
    "rolling kick": ("flinch",    30),
    "psybeam":      ("confusion", 10),
    "confusion":    ("confusion", 10),
    "acid":         ("defense", 10),
    "aurora beam":  ("attack", 10),
    "bubble beam":  ("speed", 10),
    "psychic":      ("sp_defense",10),
    }
        
        self.flat_damage_move = ["super fang","dragon rage","sonic boom","seismic toss"]


        self.high_crit_moves = ("karate chop", "razor wind","slash","sky attack")

        self.two_turn_move = ("razor wind", "fly", "solar beam", "dig", "skull bash", "sky attack", "thrash")

        self.charging_move = ""

        self.multi_hit_move = ("double slap", "double kick", "comet punch", "fury attack", "fury swipes", "pin missile", "twineedle", "bone rush", "bullet seed","bonemerang")




        # status image
        self.poison_image = pygame.image.load('status_sprite/poison.png').convert_alpha()
        self.poison_image = pygame.transform.scale(self.poison_image,(int(self.poison_image.get_width()*0.2),int(self.poison_image.get_height()*0.2)))

        self.burn_image = pygame.image.load('status_sprite/burn.png').convert_alpha()
        self.burn_image_image = pygame.transform.scale(self.burn_image,(int(self.burn_image.get_width()*0.2),int(self.burn_image.get_height()*0.2)))

        self.paralysis_image = pygame.image.load('status_sprite/paralyze.png').convert_alpha()
        self.paralysis_image = pygame.transform.scale(self.paralysis_image,(int(self.paralysis_image.get_width()*0.2),int(self.paralysis_image.get_height()*0.2)))

        self.burn_image = pygame.image.load('status_sprite/burn.png').convert_alpha()
        self.burn_image = pygame.transform.scale(self.burn_image,(int(self.burn_image.get_width()*0.2),int(self.burn_image.get_height()*0.2)))

        self.freeze_image = pygame.image.load('status_sprite/frozen.png').convert_alpha()
        self.freeze_image = pygame.transform.scale(self.freeze_image,(int(self.freeze_image.get_width()*0.2),int(self.freeze_image.get_height()*0.2)))

        self.sleep_image = pygame.image.load('status_sprite/sleep.png').convert_alpha()
        self.sleep_image = pygame.transform.scale(self.sleep_image,(int(self.sleep_image.get_width()*0.2),int(self.sleep_image.get_height()*0.2)))

        self.accuracy = True

        # check for arena trap
        self.active_field_trapped = False

        #toxic counter 
        self.toxic_counter = 1

        # anger point check
        self.crit_for_anger_point = False


        # check for unaware 
        self.unaware = 1

        # sleep and sleep counter
        self.pokemon1_sleep_counter = 0
        self.pokemon2_sleep_counter = 0
        self.sleep_turn = 0

        # weather multiplier
        self.weather_damage_multiplier = 1

        # turn
        self.opponent_turn = None

        # already got status
        self.my_pokemon_status = None
        self.opponent_pokemon_status = None

        # check entry pokemon showing
        self.p1_showing = False
        self.p2_showing = False

        # light screen, reflect, aurora veil check
        self.p1_screen = False
        self.p2_screen = False
        self.turn_screen_p1 = 0
        self.turn_screen_p2 = 0
        self.p1_screen_name = ""
        self.p2_screen_name = ""

    # get move for pokemon 1
    def get_move(self, move):
        self.pokemon1_move_name = move
        self.pokemon1_move_data = self.moves[move.lower()]

    def get_pokemon1_atk_spatk(self, attack, spatk):
        self.pokemon1_atk = attack*1.5 if self.pokemon1_ability =="hustle" else attack
        self.pokemon1_spatk = spatk

    def get_pokemon1_def_spdef_speed_item_type_ability_turn(self, defense, spdefense, speed, item, type, ability, turn):
        self.pokemon1_defense = defense
        self.pokemon1_spdefense = spdefense
        self.pokemon1_speed = speed
        self.pokemon1_item = item
        self.pokemon1_type = type
        self.pokemon1_ability = ability.lower()
        self.opponent_turn = turn

        if "Rock" in self.pokemon1_type and self.current_weather == "sandstorm":
            self.pokemon1_spdefense *= 1.5 


    # get stat for pokemon 2

    def get_pokemon2_hp_def_spdef_speed_type_ability(self,hp, defense, spdefense, speed,type, ability):
        self.pokemon2_hp = hp
        self.pokemon2_defense = defense
        self.pokemon2_spdefense = spdefense
        self.pokemon2_speed = speed
        self.pokemon2_type = type
        self.pokemon2_ability = ability.lower()


        if self.current_weather == "sandstorm":
            if "Rock" in self.pokemon1_type and (self.pokemon1_ability == "cloud nine" or self.pokemon2_ability == "cloud nine"):
                self.pokemon1_spdefense /= 1.5

            if "Rock" in self.pokemon2_type and self.pokemon1_ability != "cloud nine" or self.pokemon2_ability != "cloud nine":
                self.pokemon2_spdefense *= 1.5

            
        

    def get_pokemon2_current_hp(self,hp):
        self.pokemon2_hp = hp 


    def damage_calculation(self, is_opponent_turn):
        effectiveness = self.check_effectiveness()
        print(self.pokemon1_move_name)

        if self.pokemon1_move_name in self.flat_damage_move and self.accuracy: # check for flat damage move
                    if self.pokemon1_move_name == "super fang":
                        return int(self.pokemon2_hp/2),False,1
                    elif self.pokemon1_move_name == "sonic boom":
                        return 20, False, 1
                    elif self.pokemon1_move_name == "dragon rage":
                        return 40, False, 1
                    elif self.pokemon1_move_name == "seismic toss":
                        return 50,False, 1

        if self.pokemon1_move_data["damage_type"] == "Physical":
                    
            crit = self.crit_chance()

            if self.pokemon1_ability == "technician" and self.pokemon1_move_data["damage"] <= 60:
                self.pokemon1_move_data["damage"] = int(self.pokemon1_move_data["damage"]*1.5)
                print(f"technician activated, damage is now {self.pokemon1_move_data['damage']}")


            self.weather_multiplier() # check weather multiplier
            print(f"{self.weather_damage_multiplier} damage thoi tiet" )

            if crit: 
                if self.pokemon2_ability == "anger point" and self.pokemon1_move_data["name"] not in self.multi_hit_move: # if crit is true 
                    self.crit_for_anger_point = True # this variables serves as a check for anger point ability

                if self.pokemon1_ability == "sniper": # check for ability Sniper
                    multiplier = 3
                else:
                    multiplier = 1.5


                damage = round(((10* self.pokemon1_move_data["damage"] * self.weather_damage_multiplier * ((self.pokemon1_atk * max(self.stage_multipliers[self.stages_pokemon1["attack"]],1.0))/(self.pokemon2_defense *min(self.stage_multipliers[self.stages_pokemon2["defense"]],1.0))))/50  + 2)*multiplier*effectiveness*self.STAB())

            else:
                damage = round(((10* self.pokemon1_move_data["damage"] * self.weather_damage_multiplier * ((self.pokemon1_atk * self.stage_multipliers[self.stages_pokemon1["attack"]])/(self.pokemon2_defense *self.stage_multipliers[self.stages_pokemon2["defense"]])))/50  + 2)*effectiveness*self.STAB())


            if self.check_effectiveness() > 1 and self.pokemon2_ability == "filter":# check for ability filter
                damage *= 0.75     


            if self.check_effectiveness() < 1 and self.check_effectiveness() > 0:
                if self.pokemon1_ability == "tinted lens":  # tinted lens ability
                    damage = damage * (1/self.check_effectiveness())
                else:
                    print("its not very effective")

            elif self.check_effectiveness() > 1:
                print("its super effective")

            
            elif self.check_effectiveness() == 0:
                print("it doesnt affect")


            if self.accuracy:
                    
                random_roll = random.randint(85,100)    # random roll for damage
                damage = (damage * random_roll)/100
                if self.status_pokemon1 =="burn" or (is_opponent_turn and self.p1_screen_name == "reflect") or (not is_opponent_turn and self.p2_screen_name == "reflect"): # cut the damage in half if burned
                    print("burn or reflect is up, damage is halved")
                    return int(damage/2), crit, effectiveness
                
                print(f"thong so la:{damage},{crit},{effectiveness}")
                return int(damage),crit, effectiveness
            
            else:
                print("you missed")
                return 0, False, 1.0

        elif self.pokemon1_move_data["damage_type"] == "Special":
            crit = self.crit_chance()

            if self.pokemon1_ability == "technician" and self.pokemon1_move_data["damage"] <= 60:
                self.pokemon1_move_data["damage"] = int(self.pokemon1_move_data["damage"]*1.5)

            self.weather_multiplier() # check weather damage mul
            print(f"{self.weather_damage_multiplier} damage thoi tiet" )

            if crit: # if crit is true 
                if self.pokemon2_ability == "anger point":
                    self.crit_for_anger_point = True # this variables serves as a check for anger point ability

                if self.pokemon1_ability == "sniper": # check for ability Sniper
                    multiplier = 3
                else:
                    multiplier = 1.5

                
                damage = round(((10* self.pokemon1_move_data["damage"]* self.weather_damage_multiplier * ((self.pokemon1_spatk * max(self.stage_multipliers[self.stages_pokemon1["sp_attack"]],1.0))/(self.pokemon2_spdefense *min(self.stage_multipliers[self.stages_pokemon2["sp_defense"]],1.0))))/50  + 2)*multiplier* self.STAB())

            else:
                damage = round(((10* self.pokemon1_move_data["damage"] * self.weather_damage_multiplier * ((self.pokemon1_spatk * self.stage_multipliers[self.stages_pokemon1["sp_attack"]])/(self.pokemon2_spdefense * self.stage_multipliers[self.stages_pokemon2["sp_defense"]])))/50  + 2)*effectiveness*self.STAB())


            if self.check_effectiveness() > 1 and self.pokemon2_ability == "filter":# check for ability filter
                damage *= 0.75

            if self.check_effectiveness() < 1 and self.check_effectiveness() > 0:
                if self.pokemon1_ability == "tinted lens":  # tinted lens ability
                    damage = damage * (1/self.check_effectiveness())
                else:
                    print("its not very effective")


            if self.accuracy:
                random_roll_special = random.randint(85,100)
                damage = int((damage*random_roll_special)/100)

                print(f"dang dung {self.p2_screen_name}")
                print(f"luot cua thang lon: {is_opponent_turn}")

                if (is_opponent_turn and self.p1_screen_name == "light screen") or (not is_opponent_turn and self.p2_screen_name == "light screen"): # cut the damage in half if burned
                    print("light screen is up, damage is halved")
                    return int(damage/2), crit, effectiveness
                
                return damage, crit, effectiveness
            else:
                return 0, False, 1.0
            
        return 0, False, 1.0
    

    
    def stage_calculation(self, is_opponent_turn, message_queue):
        # only run if the move is a status move, not damaging move, or if the move is a weather move
        if self.pokemon1_move_data["damage_type"] != "Status" or self.pokemon1_move_data["name"] in self.weather_moves:
            return 0
        

        # check if the move is light screen or reflect, and print a message if it is
        if self.pokemon1_move_data["name"].lower() == "light screen" or self.pokemon1_move_data["name"].lower() == "reflect":

            if (not is_opponent_turn and self.p1_screen) or (is_opponent_turn and self.p2_screen): # if the screen is already up
                message_queue.append(f"But it failed!")
                return 0
                                     
            if not is_opponent_turn and not self.p1_screen: # not have light screen or reflect yet
                self.p1_screen = True
                message_queue.append(f"A magic barrier formed on your side!")
                self.p1_screen_name = self.pokemon1_move_data["name"].lower()

            elif is_opponent_turn and not self.p2_screen: # not have light screen or reflect yet
                self.p2_screen = True
                message_queue.append(f"A magic barrier formed on the opponent's side!")
                self.p2_screen_name = self.pokemon1_move_data["name"].lower()



        # get the move name in lowercase so it matches the status_moves dictionary keys
        move_key = self.pokemon1_move_name.lower()

        # check if the move is actually in the status_moves dictionary
        if move_key not in self.status_moves:
            return 0

        # unpack the move data from the status_moves dictionary
        effect_type = self.status_moves[move_key][0]   # "stages" or "status"
        stat = self.status_moves[move_key][1]           # which stat is affected
        amount = self.status_moves[move_key][2]         # how much it changes
        target = self.status_moves[move_key][3]         # "self" or "opponent"

        # ---- STAGE CHANGES ----
        if effect_type == "stages":

        # self-targeting moves (buffs on pokemon 1)
            if target == "self":

                if move_key =="growth":  # if its growth
                    if self.current_weather == "sunny day" and self.pokemon1_ability != "cloud nine" and self.pokemon2_ability != "cloud nine":
                            amount *= 2

                    if self.stages_pokemon1["sp_attack"] + amount > 6 or self.stages_pokemon1["attack"]+amount > 6:
                        print("spatk and atk cant go any higher!")

                    else:
                        self.stages_pokemon1["sp_attack"] += amount
                        self.stages_pokemon1["attack"] += amount
                        print(self.stages_pokemon1)

                elif move_key == "amnesia":
                    if self.stages_pokemon1["sp_defense"] + amount >6:
                        print("sp defense cant go any higher")
                    else:
                        self.stages_pokemon1["sp_defense"] += amount
                        print(self.stages_pokemon1)

                else:
                    if self.stages_pokemon1[stat] + amount > 6:
                        print(f"{stat} cant go any higher")

                    else:
                        self.stages_pokemon1[stat] += amount
                        print(self.stages_pokemon1)

        # opponent-targeting moves (debuffs on pokemon 2)
            elif target == "opponent":
                if self.pokemon1_move_data["name"].lower() in ("sand attack","kinesis","smokescreen") and self.pokemon2_ability == "keen eye":
                    pass

                elif self.pokemon2_ability == "clear body":
                    pass
                
            # check if the stage would go below the -6 floor
                elif self.stages_pokemon2[stat] + amount < -6:
                    print(f"{stat} cant go any lower!")

            # if within floor, apply the stage change
                else:
                    self.stages_pokemon2[stat] += amount
                    print(f"Pokemon 2 {stat} is now stage {self.stages_pokemon2[stat]}")


    # ---- STATUS CONDITIONS ----
        elif effect_type == "status":
            
            if target == "opponent":
                if self.status_pokemon2 is None:
                    if self.accuracy:
                        if (stat == "paralysis" and "Electric" in self.pokemon2_type) or self.pokemon2_ability == "limber":
                            pass

                        elif (stat == "poison" or stat == "bad_poison") and "Poison" in self.pokemon2_type:
                            pass

                        else:
                            self.status_pokemon2 = stat
                            print(f"Pokemon 2 is now {stat}!")

                    else:
                        print("you missed")

                else:
                    print("Pokemon 2 already has a status condition!")

            elif target == "self":
                if self.status_pokemon1 is None:
                    self.status_pokemon1 = stat
                    print(f"Pokemon 1 is now {stat}!")

                else:
                    print("Pokemon 1 already has a status condition!")


        
    def check_accuracy(self):
        if self.pokemon1_move_data["accuracy"] is not None:
            check_sure_hit = self.pokemon1_move_data["accuracy"]
        else:
            print("cant miss")
            self.accuracy = True
            return 
        
        chance = random.randint(0,100)
        print(f"co hoi trc la:{chance}")

        if self.stages_pokemon2["evasion"] != 0 and self.pokemon1_ability != "keen eye": # if increased evasion, the foe pokemon can dodge. Keen eye ability can bypass this
            chance = int(chance * ((3+self.stages_pokemon2["evasion"])/3))

        

        chance = int(0.7*chance) if self.pokemon1_ability =="compound eyes" else chance # check for Compound Eyes
        chance = int(1.2* chance) if self.pokemon1_ability == "hustle" else chance # check for hustle ability
        chance = int(1.2 * chance) if (self.pokemon2_ability == "sand veil" and self.current_weather == "sandstorm" and self.pokemon1_ability != "cloud nine") else chance # check sand veil
        chance = int(1.2* chance) if (self.pokemon1_move_data["name"].lower() == "thunder" and self.current_weather == "sunny day" and self.pokemon1_ability != "cloud nine") else chance


        chance = -1 if (self.pokemon1_ability == "no guard" or self.pokemon2_ability == "no guard") else chance
        chance = -1 if (self.pokemon1_move_data["name"].lower() == "thunder" and self.current_weather == "rain dance" and self.pokemon1_ability != "cloud nine") else chance


        print(f"co hoi sau la {chance}")

        if chance == -1:
            self.accuracy = True
            return
        

        if chance <= int(check_sure_hit): # the lower the chance the higher the hit ratio
            self.accuracy = True
            return True
        else:
            self.accuracy = False
            return False
        

    def crit_chance(self):
        crit = random.randint(0,100)
        low_crit = 4
        medium_crit = 12
        high_crit = 50

        if self.pokemon2_ability == "battle armor": # ability battle armor prevent crit
            return False
        
        if self.pokemon1_item == "scope-lens":   # if the held item is scope lens
            if self.pokemon1_move_name.lower() in self.high_crit_moves and crit <= high_crit:
                return True
            elif  self.pokemon1_move_name.lower() not in self.high_crit_moves and crit < medium_crit:  
                return True
            return False
                
        elif self.pokemon1_item != "scope-lens": # if the held item is not scope lens
            if self.pokemon1_move_name.lower() in self.high_crit_moves and crit < medium_crit:
                return True
            elif self.pokemon1_move_name.lower() not in self.high_crit_moves and crit < low_crit:
                return True
            
            return False
        

    def check_status_pokemon(self, screen):
        # blit the effects to the right pokemon
        if self.my_pokemon_status is not None or self.my_pokemon_status == "":
            if self.my_pokemon_status == "poison" or self.my_pokemon_status == "bad_poison":
                screen.blit(self.poison_image, (190,355))
            elif self.my_pokemon_status == "paralysis":
                screen.blit(self.paralysis_image, (190,355))
            elif self.my_pokemon_status == "burn":
                screen.blit(self.burn_image,(190,355))
            elif self.my_pokemon_status == "freeze":
                screen.blit(self.freeze_image,(190,355))
            elif self.my_pokemon_status == "sleep":
                screen.blit(self.sleep_image,(190,355))



        if self.opponent_pokemon_status is not None or self.opponent_pokemon_status == "" :
            if self.opponent_pokemon_status == "poison" or self.opponent_pokemon_status == "bad_poison":
                screen.blit(self.poison_image, (240,70))
            elif self.opponent_pokemon_status == "paralysis":
                screen.blit(self.paralysis_image, (240,70))
            elif self.opponent_pokemon_status == "burn":
                screen.blit(self.burn_image,(240,70))
            elif self.opponent_pokemon_status == "freeze":
                screen.blit(self.freeze_image,(240,70))
            elif self.opponent_pokemon_status == "sleep":
                screen.blit(self.sleep_image,(240,70))


    def still_asleep(self):
        if self.status_pokemon1 == "sleep" and self.pokemon1_sleep_counter == 0:
            chance = random.randint(1,4)
            chance = math.floor(chance/2) if self.pokemon1_ability == "early bird" else chance # check for ability early bird
            self.sleep_turn = chance
            print(f"ngu {chance} luot")

        if self.pokemon1_sleep_counter < self.sleep_turn:
            self.pokemon1_sleep_counter += 1
            print(f"dang ngu luot {self.pokemon1_sleep_counter}")
            return True
        
        else:
            self.status_pokemon1 = None
            self.pokemon1_sleep_counter = 0
            self.sleep_turn = 0
            return False




    def check_effectiveness(self):
        multiplier = 1.0
        move_type = self.pokemon1_move_data["type"]
        for defender_type in self.pokemon2_type:
            try:
                multiplier *= self.type_chart[move_type][defender_type]
            except KeyError:
                pass
        return multiplier
        

    def STAB(self):
        if self.pokemon1_move_data["type"] in self.pokemon1_type: # if move is same type as pokemon
            return 1.5
        else:
            return 1
        

    def check_end_turn(self, health_percent):
        if self.pokemon2_ability == "magic guard":
            return health_percent
        
        else:
            if self.status_pokemon2 == "poison":
                health_percent -= 0.12
                return health_percent
            elif self.status_pokemon2 == "bad_poison":
                health_percent -= 0.06*self.toxic_counter
                self.toxic_counter += 1
                return health_percent
            elif self.status_pokemon2 =="burn":
                health_percent -= 0.06

        return health_percent
    

    def check_end_turn_pokemon1(self, health_percent):

        if self.pokemon1_ability == "magic guard":
            return health_percent
        
        else:
            if self.status_pokemon1 == "poison":
                health_percent -= 0.12
                return health_percent
            elif self.status_pokemon1 == "bad_poison":
                health_percent -= 0.06*self.toxic_counter
                self.toxic_counter +=1
                return health_percent
            elif self.status_pokemon1 =="burn":
                health_percent -= 0.06


        return health_percent


    def check_secondary_effect(self):
        move_key = self.pokemon1_move_name
        if move_key not in self.secondary_effects or self.pokemon1_ability =="sheer force": # check for ability sheer force
            return None
        status, chance = self.secondary_effects[move_key]
        if random.randint(1, 100) <= chance:
            if self.status_pokemon2 is None or status in ("flinch","confusion","attack","defense","sp_defense","speed"): # EVEN IF POKEMON HAS NON VOLATILE EFFECTS, IT CAN STILL BE CONFUSE AND FLINCH
                if status == "burn" and "Fire" in self.pokemon2_type:
                    return None
                elif (status == "paralyze" and "Electric" in self.pokemon2_type) or self.pokemon2_ability == "limber":
                    return None
                elif status == "poison" and "Poison" in self.pokemon2_type:
                    return None
                elif status == "flinch" or status =="confusion":
                    return status
                
                elif status in ("attack","defense","sp_defense","speed"):
                    if self.stages_pokemon2[status] < 6:
                        self.stages_pokemon2[status] -= 1  # DECREASE STATS
                    return status
                
                else:
                    self.status_pokemon2 = status
                    return status
        return None
    

    

    def process_entry_abilities(self, pokemon_1_ability, pokemon_1_name, pokemon_2_ability, pokemon_2_name, message_queue):
        p1_ability = pokemon_1_ability.lower().strip()
        p2_ability = pokemon_2_ability.lower().strip()
        self.p1_showing = False
        self.p2_showing = False

        if (p1_ability == "intimidate" or p2_ability == "intimidate"):
            if p1_ability == "intimidate" and p2_ability not in ("clear body", "hyper cutter", "white smoke"):
                self.stages_pokemon2["attack"] = max(-6, self.stages_pokemon2["attack"] - 1)
                message_queue.append(f"{pokemon_1_name.capitalize()}'s Intimidate cut the foe's Attack!")
                self.p1_showing = True

            if p2_ability == "intimidate" and p1_ability not in ("clear body", "hyper cutter", "white smoke"):
                self.stages_pokemon1["attack"] = max(-6, self.stages_pokemon1["attack"] - 1)
                message_queue.append(f"Foe {pokemon_2_name.capitalize()}'s Intimidate cut {pokemon_1_name.capitalize()}'s Attack!")
                self.p2_showing = True

        if (p1_ability == "arena trap" or p2_ability == "arena trap"):
            if p1_ability == "arena trap" and p2_ability != "levitate" and "Ghost" not in self.pokemon2_type and "Flying" not in self.pokemon2_type:
                self.active_field_trapped = True
                message_queue.append(f"{pokemon_2_name.capitalize()} is trapped!")  
                self.p1_showing = True

            if p2_ability == "arena trap" and p1_ability != "levitate" and "Ghost" not in self.pokemon1_type and "Flying" not in self.pokemon1_type:
                self.active_field_trapped = True
                message_queue.append(f"{pokemon_1_name.capitalize()} is trapped!")
                self.p2_showing = True
                
        if (p1_ability == "cloud nine" or p2_ability == "cloud nine"):
            if p1_ability == "cloud nine":
                self.p1_showing = True
            if p2_ability == "cloud nine":
                self.p2_showing = True
            message_queue.append("The effects of weather are negated!")


        return self.p1_showing, self.p2_showing



    def apply_damage_boost(self, damage,hp_ratio): # for normal damage boost
        if self.pokemon1_ability == "overgrow" and self.pokemon1_move_data["type"] == "Grass" and hp_ratio <=0.33:
            return int(damage*1.5)
        elif self.pokemon1_ability == "torrent" and self.pokemon1_move_data["type"] == "Water" and hp_ratio <=0.33:
            return int(damage*1.5)
        elif self.pokemon1_ability == "blaze" and self.pokemon1_move_data["type"] == "Fire" and hp_ratio <=0.33:
            return int(damage*1.5)
        elif self.pokemon1_ability == "swarm" and self.pokemon1_move_data["type"] == "Bug" and hp_ratio <=0.33:
            return int(damage*1.5)
        elif self.pokemon1_ability == "sheer force":
            return int(damage*1.3)
        return damage
    

    def recoil_damage(self, damage, hp_ratio, total_health):
        if self.pokemon1_move_name in ("take down","double-edge","submission") and self.pokemon1_ability != "rock head":
            return hp_ratio - (damage/4)/total_health  
        return hp_ratio 



    def check_absorb_move_ability(self):
        move_type = self.pokemon1_move_data["type"].lower()

        if self.pokemon2_ability == "lightning rod" and move_type =="electric" and self.accuracy: # if the move hit a lightning rod pokmeon
            if self.stages_pokemon2["sp_attack"] !=6:
                self.stages_pokemon2["sp_attack"] +=1
            return True
        
        elif self.pokemon2_ability == "water absorb" and move_type =="water" and self.accuracy: # if the move hit a lightning rod pokmemon

            return True # make this heals the user of teh ability
        
        elif self.pokemon2_ability == "flash fire" and move_type =="fire" and self.accuracy: # if the move hit a lightning rod pokmemon
            if self.stages_pokemon2["sp_attack"] !=6:
                self.stages_pokemon2["sp_attack"] +=1
            return True # make this increase the fire move atk of the pokemon by 50%
        
        elif self.pokemon2_ability == "anger point" and self.crit_for_anger_point and self.accuracy: # if the move hit a lightning rod pokmemon
            self.stages_pokemon2["attack"] = 6 # max out atk
            self.crit_for_anger_point = False
            return True
        
        elif self.pokemon2_ability == "damp" and self.pokemon1_move_data["name"] == "Explosion" and self.accuracy: # treat damp as an abosrb ability
            return True
        
        elif self.pokemon2_ability == "levitate" and move_type == "ground" and self.accuracy:
            return True
        
        return False
    

    
    def check_contact_ability(self):

        chance = random.randint(0,100) # chance of getting the status effect
        if self.pokemon2_ability == "static" and self.pokemon1_move_data["contact"] and chance <= 100 and self.status_pokemon1 is None and "Electric" not in self.pokemon1_type and self.charging_move == "" and self.pokemon1_ability != "limber": # if my pokemon touch a pokemonn with static
            self.status_pokemon1 = "paralysis"
            return "paralysis"
        
        elif self.pokemon2_ability == "poison point" and self.pokemon1_move_data["contact"] and chance <= 20 and self.status_pokemon1 is None and "Poison" not in self.pokemon1_type and self.charging_move == "": # if my pokemon touch a pokemonn with poison
            self.status_pokemon1 = "poison"
            return "poison"

        
        elif self.pokemon2_ability == "flame body" and self.pokemon1_move_data["contact"] and chance <= 30 and self.status_pokemon1 is None and "Fire" not in self.pokemon1_type and self.charging_move == "": # if my pokemon touch a pokemon with flame body
            self.status_pokemon1 = "burn"
            return "burn"
        
        elif self.pokemon2_ability == "effect spore" and self.pokemon1_move_data["contact"] and chance <= 30 and self.status_pokemon1 is None and self.charging_move == "": # if my pokemon touch a pokemonn with effect spore
            effect = ["paralysis","poison","sleep"] # sleep later
            random_effect = random.choice(effect)
            self.status_pokemon1 = random_effect
            return random_effect
        
        return False
        
    
    def prevent_lowered_stat_ability(self):

        if self.pokemon1_move_data["name"].lower() in ("sand attack","kinesis","smokescreen") and self.pokemon2_ability == "keen eye":
            return True
        elif self.pokemon1_move_data["name"].lower() in self.status_moves:
            if self.status_moves[self.pokemon1_move_data["name"].lower()][0] == "stages" and self.status_moves[self.pokemon1_move_data["name"].lower()][3] == "opponent" and self.pokemon2_ability == "clear body":
                return True
        
        return False
    
    def check_touch_ability(self):
        chance = random.randint(0,100)
        if self.pokemon1_ability == "poison touch" and self.pokemon1_move_data["contact"] and chance <= 30 and self.status_pokemon2 is None and "Poison" not in self.pokemon2_type: # if my pokemon touch a pokemonn with poison
            self.status_pokemon2 = "poison"
            return "poison"
        return False
        


    def check_paralysis_attack(self):
        attack = random.randint(1,100)
        if self.status_pokemon1 == "paralysis" and attack > 75:
            return False
        return True

    
    def check_thaw_out(self):
        chance = random.randint(1,100)
        if self.status_pokemon1 == "freeze" and chance <= 20:
            self.status_pokemon1 = None
            return True
        return False



    def check_heal_move(self,move):
        if move == "mega drain":
            return True
        return False
    

    def check_weather(self):
        if self.pokemon1_move_data["name"].lower() == "sandstorm":
            self.current_weather = "sandstorm"
            return "sandstorm"
        
        elif self.pokemon1_move_data["name"].lower() == "rain dance":
            self.current_weather = "rain dance"
            return "rain dance"
        
        elif self.pokemon1_move_data["name"].lower() == "sunny day":
            self.current_weather = "sunny day"
            return "sunny day"

        return False
    


    def weather_multiplier(self):
        if self.pokemon1_ability != "cloud nine" and self.pokemon2_ability != "cloud nine":
            if self.current_weather == "rain dance":
                if self.pokemon1_move_data["type"].lower() == "water":
                    self.weather_damage_multiplier = 1.5

                elif self.pokemon1_move_data["type"].lower() == "fire":
                    self.weather_damage_multiplier = 0.5

            elif self.current_weather == "sunny day":
                if self.pokemon1_move_data["type"].lower() == "water":
                    self.weather_damage_multiplier = 0.5

                elif self.pokemon1_move_data["type"].lower() == "fire":
                    self.weather_damage_multiplier = 1.5

            else:
                self.weather_damage_multiplier = 1
            return self.weather_damage_multiplier
        
        self.weather_damage_multiplier = 1
        return self.weather_damage_multiplier



    def move_priority(self):

        mul2, mul1 = 1,1

        if self.status_pokemon1 == "paralysis":
            mul1 *= 0.25
        if self.status_pokemon2 == "paralysis":
            mul2 *= 0.25

        if self.pokemon1_ability != "cloud nine" and self.pokemon2_ability !="cloud nine":
            if self.current_weather == "sandstorm":

                if self.pokemon1_ability == "sand rush":
                    mul1 *= 2
                if self.pokemon2_ability == "sand rush":
                    mul2 *= 2

            elif self.current_weather == "rain dance":
                if self.pokemon1_ability == "swift swim":
                    mul1 *= 2
                if self.pokemon2_ability == "swift swim":
                    mul2 *= 2

            elif self.current_weather == "sunny day":
                if self.pokemon1_ability == "chlorophyll":
                    mul1 *= 2
                if self.pokemon2_ability == "chlorophyll":
                    mul2 *= 2

        if self.pokemon2_speed * self.stage_multipliers[self.stages_pokemon2["speed"]] *mul2 > self.pokemon1_speed*self.stage_multipliers[self.stages_pokemon1["speed"]] * mul1:
            return "pokemon_2"                          
        else:
            return "pokemon_1"
        


    def multi_turn_move(self):
        if not self.pokemon1_move_data:
            return
        if self.pokemon1_move_data["name"].lower() in self.two_turn_move:
            if self.pokemon1_move_data["name"].lower() == "solar beam" and self.current_weather == "sunny day": # no charge in suuny day for solar beam
                pass
            else:
                self.charging_move = self.pokemon1_move_data["name"].lower()

        

    # SPECIAL ABILITY, ABILITY THAT HAS BIZZARE EFFECTS
    def ability_synchonize(self):
        immune = {"paralysis": "Electric", "poison": "Poison", "bad_poison": "Poison", "burn": "Fire"}
        if self.pokemon1_ability == "synchronize" and self.status_pokemon1 is not None and self.status_pokemon1 not in ("freeze", "sleep"):
            if self.status_pokemon2 is None: # if p1 has a negative status, inflict it to p2
                if immune.get(self.status_pokemon1) in self.pokemon2_type:
                    return False
                
                self.status_pokemon2 = self.status_pokemon1
                return True
 


        elif self.pokemon2_ability == "synchronize" and self.status_pokemon2 and self.status_pokemon2 not in ("freeze", "sleep"):
            if not self.status_pokemon1: # if p2 has a negative status, inflict it to p1 
                if immune.get(self.status_pokemon2) in self.pokemon1_type:
                    return False
                
                self.status_pokemon1 = self.status_pokemon2
                return True

        else:
            return False



    

            



