import pygame
import json

class Change_Pokemon:
    def __init__(self):

        #GETTING THE INFO FROM THE POKEMON FILE
        with open('pokemon_data.json', 'r') as f: #from moves.json
            pokemon_list = json.load(f)
        self.pokemon_data = {p["name"].lower(): p for p in pokemon_list}

        
        self.sub_pokemon_hp = self.pokemon_data["charizard"]["health"] 
        self.sub_pokemon_atk = self.pokemon_data["charizard"]["attack"] 
        self.sub_pokemon_defense= self.pokemon_data["charizard"]["defense"] 
        self.sub_pokemon_spatk = self.pokemon_data["charizard"]["sp_attack"] 
        self.sub_pokemon_spdefense = self.pokemon_data["charizard"]["sp_defense"]
        self.sub_pokemon_speed = self.pokemon_data["charizard"]["speed"] 
        self.sub_pokemon_weight = self.pokemon_data["charizard"]["weight_kg"]  
        self.sub_pokemon_type = self.pokemon_data["charizard"]["type"]  
        self.sub_pokemon_hp_ratio = 1.0




    def save_pokemon(self,name,atk, spatk, defense, spdefense, speed, type, ability, status_condition):

        self.pokemon_name = name
        self.pokemon_atk = atk
        self.pokemon_spatk = spatk
        self.pokemon_defense = defense
        self.pokemon_spdefense = spdefense
        self.pokemon_speed = speed
        self.pokemon_type = type
        self.pokemon_ability = ability
        self.pokemon_status_condition = status_condition
