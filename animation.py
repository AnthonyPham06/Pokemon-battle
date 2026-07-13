import pygame
from battle_engine import Battle_Engine
import random
import math

class BattleAnimation:
    def __init__(self):
        self.Engine = Battle_Engine()
        self.move_name = ""
        self.current_loaded_move = None
        self.frame = 0
        self.hit_sound = pygame.mixer.Sound('battle_music/tackle.mp3')
        self.hit_played = False
        self.dark_overlay = pygame.Surface((800, 500))
        self.state = {}

        self.move_registry = {
            "tackle":        (None,               self.anim_tackle),
            "swords dance":  (self._load_sword,   self.sword_dance),
            "poison powder": (self._load_poison,  self.anim_poison),
            "earthquake":    (self._load_eq,      self.anim_earthquake),
            "toxic":         (self._load_toxic,   self.anim_toxic),
            "scratch":       (self._load_scratch, self.anim_scratch),
            "hydro pump":    (self._load_hydro,   self.anim_hydro_pump),
            "fire punch":    (self._load_punch,   self.punch),
            "ice punch":     (self._load_punch,   self.punch),
            "mega punch":    (self._load_punch,   self.punch),
            "thunder punch": (self._load_punch,   self.punch),
            "karate chop":   (self._load_karate_chop, self.karate_chop),
            "take down":     (self._load_take_down, self.anim_take_down),
            "submission": (self._load_submission, self.anim_submission),
            "mega kick": (self._load_mega_kick, self.anim_mega_kick),
            "strength": (self._load_strength, self.anim_strength),
            "low kick": (self._load_low_kick, self.anim_low_kick),
            "fire blast": (self._load_fire_blast, self.anim_fire_blast),
            "bite": (self._load_bite, self.anim_bite),
            "double-edge": (self._load_take_down, self.anim_take_down), 
            "poison sting": (self._load_poison_sting, self.anim_poison_sting),
            "wing attack": (self._load_wing_attack, self.anim_wing_attack),
            "gust": (self._load_gust, self.anim_gust),
            "comet punch": (self._load_comet_punch, self.anim_comet_punch),
            "double team": (self._load_double_team, self.anim_double_team),
            "thunderbolt": (self._load_thunderbolt, self.anim_thunderbolt),
            "ember": (self._load_ember, self.anim_ember),
            "mega drain": (self._load_mega_drain, self.anim_mega_drain),
            "agility": (self._load_double_team, self.anim_double_team),
            "body slam": (self._load_body_slam, self.anim_body_slam),
            "sandstorm": (self._load_sandstorm, self.anim_sandstorm),   
            "slash": (self._load_slash, self.anim_slash),
            "hyper beam": (self._load_hyper_beam, self.anim_hyper_beam),
            "rain dance": (self._load_rain_dance, self.anim_rain_dance),
            "thunder": (self._load_thunder, self.anim_thunder),
            "sunny day": (self._load_sunny_day, self.anim_sunny_day),
            "solar beam": (self._load_solar_beam, self.anim_solar_beam),
            "growth": (self._load_growth, self.anim_growth),
            "swift":         (self._load_swift,   self.anim_swift),
            "flamethrower": (self._load_flamethrower, self.anim_flamethrower),
            "stun spore": (self._load_stun_spore, self.anim_stun_spore),
            "razor wind": (self._load_razor_wind, self.anim_razor_wind),
            "sand attack": (self._load_sand_attack, self.anim_sand_attack),
            "status poison": (self._load_status_poison, self.anim_status_poison),
            "sleep powder": (self._load_sleep_powder, self.anim_sleep_powder),
            "ice beam": (self._load_ice_beam, self.anim_ice_beam),
            "status sleep": (self._load_status_sleep, self.anim_status_sleep),
            "surf": (self._load_surf, self.anim_surf),
            "amnesia": (self._load_amnesia, self.anim_amnesia),
            "screech": (self._load_screech, self.anim_screech),
            "psybeam": (self._load_psybeam, self.anim_psybeam),
            "harden": (self._load_harden, self.anim_harden),
            "glare": (self._load_glare, self.anim_glare),
            "acid": (self._load_acid, self.anim_acid),
            "psychic": (self._load_psychic, self.anim_psychic),
            "fire spin": (self._load_fire_spin, self.anim_fire_spin),
            "wrap": (self._load_wrap, self.anim_wrap),
            "leech seed": (self._load_leech_seed, self.anim_leech_seed),
            "dig": (self._load_dig, self.anim_dig),
            "fly": (self._load_fly, self.anim_fly),

        }

    # ------------------------------------------------------------------ #
    #  LOAD FUNCTIONS                                                      #
    # ------------------------------------------------------------------ #

    def _load_sword(self, name):
        img = pygame.image.load('move_sprites/sword_dance/sword_dance.png').convert_alpha()
        img = pygame.transform.scale(img, (int(img.get_width()*0.5), int(img.get_height()*0.5)))
        self.state["sound"] = pygame.mixer.Sound('move_sprites/sword_dance/sword_dance.mp3')
        self.state["img"]   = img
        self.state["rect"]  = img.get_rect(center=(210, 260))
        self.state["start"] = None

    def _load_poison(self, name):
        frames = [pygame.image.load(f'move_sprites/poison_powder/poison_powder_{i}.png').convert_alpha() for i in range(1, 4)]
        frames = [pygame.transform.scale(f, (60, 60)) for f in frames]
        self.state["sound"]  = pygame.mixer.Sound('move_sprites/poison_powder/poison_powder.mp3')
        self.state["frames"] = frames
        self.state["index"]  = 0
        self.state["timer"]  = 0
        self.state["speed"]  = 600

    def _load_status_poison(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/poison_status/poison_status.mp3')
        self.state["start"] = None

    def _load_eq(self, name): #earthquake
        self.state["sound"]    = pygame.mixer.Sound('move_sprites/earthquake/earthquake.mp3')
        self.state["start"]    = None
        self.state["duration"] = 3000

    def _load_toxic(self, name):
        puddle = pygame.image.load('move_sprites/toxic/toxic_2.png').convert_alpha()
        puddle = pygame.transform.scale(puddle, (50, 30))
        bubble = pygame.image.load('move_sprites/toxic/toxic_1.png').convert_alpha()
        bubble = pygame.transform.scale(bubble, (30, 30))
        self.state["sound"]  = pygame.mixer.Sound('move_sprites/toxic/toxic.mp3')
        self.state["puddle"] = puddle
        self.state["bubble"] = bubble
        self.state["start"]  = None

    def _load_scratch(self, name):
        img1 = pygame.image.load('move_sprites/scratch/scratch_1.png').convert_alpha()
        img2 = pygame.image.load('move_sprites/scratch/scratch_2.png').convert_alpha()
        self.state["sound"] = pygame.mixer.Sound('move_sprites/scratch/scratch.mp3')
        self.state["img1"]  = img1
        self.state["img2"]  = img2
        self.state["start"] = None

    def _load_hydro(self, name):
        img = pygame.image.load('move_sprites/hydro_pump/hydro_pump.png').convert_alpha()
        img = pygame.transform.scale(img, (60, 60))
        self.state["sound"] = pygame.mixer.Sound('move_sprites/hydro_pump/hydro_pump.mp3')
        self.state["img"]   = img
        self.state["start"] = None

    def _load_punch(self, name):
        punch_type = name.replace(" ", "_")
        words = name.split(" ")
        scale_fist, scale_effect = 0.6, 0.6
        if words[0] == "mega":
            scale_fist, scale_effect = 1.2, 1.2
        elif words[0] == "thunder":
            scale_fist, scale_effect = 0.6, 0.5
        fist   = pygame.image.load(f'move_sprites/{punch_type}/{punch_type}_1.png').convert_alpha()
        effect = pygame.image.load(f'move_sprites/{punch_type}/{punch_type}_2.png').convert_alpha()
        self.state["sound"]  = pygame.mixer.Sound(f'move_sprites/{punch_type}/{punch_type}.mp3')
        self.state["fist"]   = pygame.transform.scale(fist,   (int(fist.get_width()*scale_fist),     int(fist.get_height()*scale_fist)))
        self.state["effect"] = pygame.transform.scale(effect, (int(effect.get_width()*scale_effect), int(effect.get_height()*scale_effect)))
        self.state["start"]  = None

    
    def _load_karate_chop(self,name):
        img = pygame.image.load('move_sprites/karate_chop/karate_chop.png').convert_alpha()
        img = pygame.transform.scale(img,(int(img.get_width()*0.5), int(img.get_height()*0.5)))
        self.state["sound"] = pygame.mixer.Sound('move_sprites/karate_chop/karate_chop.mp3')
        self.state["img"]  = img
        self.state["start"] = None

    def _load_take_down(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/take_down/take_down.mp3')
        self.state["start"] = None
        self.state["origin_x"] = None

    def _load_submission(self, name):
        img = pygame.image.load('move_sprites/submission/submission.png').convert_alpha()
        self.state["sound"] = pygame.mixer.Sound('move_sprites/submission/submission.mp3')
        self.state["img"]   = pygame.transform.scale(img,(int(img.get_width()*0.5), int(img.get_height()*0.5)))
        self.state["start"] = None
        self.state["angle"] = 0

    def _load_mega_kick(self, name):
        img = pygame.image.load('move_sprites/mega_kick/mega_kick.png').convert_alpha()
        self.state["sound"]  = pygame.mixer.Sound('move_sprites/mega_kick/mega_kick.mp3')
        self.state["img"]    = pygame.transform.scale(img,(int(img.get_width()*0.8), int(img.get_height()*0.8)))
        self.state["start"]  = None

    def _load_strength(self, name):
        img = pygame.image.load('move_sprites/strength/strength.png').convert_alpha()
        self.state["sound"] = pygame.mixer.Sound('move_sprites/strength/strength.mp3')
        self.state["img"]   = img
        self.state["start"] = None


    def _load_low_kick(self, name):
        img = pygame.image.load('move_sprites/low_kick/low_kick.png').convert_alpha()
        self.state["sound"] = pygame.mixer.Sound('move_sprites/low_kick/low_kick.mp3')
        self.state["img"]   = pygame.transform.scale(img,(int(img.get_width()*0.4), int(img.get_height()*0.4)))
        self.state["start"] = None

    def _load_fire_blast(self, name):
        img = pygame.image.load('move_sprites/fire_blast/fire_blast.png').convert_alpha()
        img = pygame.transform.scale(img, (int(img.get_width()*0.5), int(img.get_height()*0.5)))
        self.state["sound"] = pygame.mixer.Sound('move_sprites/fire_blast/fire_blast.mp3')
        self.state["img"]   = img
        self.state["start"] = None
        self.state["scale"] = 1.0

    def _load_bite(self, name):
        img1 = pygame.image.load('move_sprites/bite/bite_1.png').convert_alpha()
        img2 = pygame.image.load('move_sprites/bite/bite_2.png').convert_alpha()
        self.state["sound"] = pygame.mixer.Sound('move_sprites/bite/bite.mp3')
        self.state["img1"]  = pygame.transform.scale(img1, (int(img1.get_width()*0.5), int(img1.get_height()*0.5)))
        self.state["img2"]  = pygame.transform.scale(img2, (int(img2.get_width()*0.5), int(img2.get_height()*0.5)))
        self.state["start"] = None

    def _load_poison_sting(self, name):
        img = pygame.image.load('move_sprites/poison_sting/poison_sting.png').convert_alpha()
        self.state["sound"] = pygame.mixer.Sound('move_sprites/poison_sting/poison_sting.mp3')
        self.state["img"]   = pygame.transform.rotate(img, 120)
        self.state["start"] = None

    def _load_wing_attack(self, name):
        img = pygame.image.load('move_sprites/wing_attack/wing_attack.png').convert_alpha()
        self.state["sound"]   = pygame.mixer.Sound('move_sprites/wing_attack/wing_attack.mp3')
        self.state["img"]     = pygame.transform.scale(img, (int(img.get_width()*0.5), int(img.get_height()*0.5)))
        self.state["start"]   = None

    def _load_gust(self, name):
        img = pygame.image.load('move_sprites/gust/gust.png').convert_alpha()
        self.state["sound"] = pygame.mixer.Sound('move_sprites/gust/gust.mp3')
        self.state["img"]   = pygame.transform.scale(img, (int(img.get_width()*0.7), int(img.get_height()*0.7)))
        self.state["start"] = None
        self.state["angle"] = 0


    def _load_comet_punch(self, name):
        img = pygame.image.load('move_sprites/comet_punch/comet_punch.png').convert_alpha()
        self.state["sound"] = pygame.mixer.Sound('move_sprites/comet_punch/comet_punch.mp3')
        self.state["img"]   = pygame.transform.scale(img, (int(img.get_width()*0.5), int(img.get_height()*0.5)))
        self.state["start"] = None
        self.state["hit_count"] = 0
        self.state["next_hit_time"] = 0
        self.state["positions"] = []
        self.state["flash_until"] = 0

    def _load_double_team(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/double_team/double_team.mp3')
        self.state["start"] = None
        self.state["offset"] = 0
        self.state["direction"] = 1

    def _load_thunderbolt(self, name):
        effect = pygame.image.load('move_sprites/thunder_punch/thunder_punch_2.png').convert_alpha()
        self.state["sound"]  = pygame.mixer.Sound('move_sprites/thunderbolt/thunderbolt.mp3')
        self.state["effect"] = pygame.transform.scale(effect, (int(effect.get_width()*0.3), int(effect.get_height()*0.3)))
        self.state["start"]  = None
        self.state["hit_count"] = 0

    def _load_ember(self, name):
        img = pygame.image.load('move_sprites/fire_blast/fire_blast.png').convert_alpha()
        self.state["sound"] = pygame.mixer.Sound('move_sprites/ember/ember.mp3')
        self.state["img"]   = pygame.transform.scale(img, (int(img.get_width()*0.5), int(img.get_height()*0.5)))
        self.state["start"] = None

    def _load_mega_drain(self, name):
        img = pygame.image.load('move_sprites/mega_drain/mega_drain.png').convert_alpha()
        self.state["sound"] = pygame.mixer.Sound('move_sprites/mega_drain/mega_drain.mp3')
        self.state["img"]   = pygame.transform.scale(img, (int(img.get_width()*0.2), int(img.get_height()*0.2)))
        self.state["start"] = None
        self.state["particles"] = []

    def _load_body_slam(self, name):
        img = pygame.image.load('move_sprites/body_slam/body_slam.png').convert_alpha()
        self.state["sound"] = pygame.mixer.Sound('move_sprites/body_slam/body_slam.mp3')
        self.state["img"]   = pygame.transform.scale(img, (int(img.get_width()*0.5), int(img.get_height()*0.5)))
        self.state["start"] = None

    def _load_sandstorm(self, name):
        img = pygame.image.load('battle_sprite/sandstorm_background.png').convert_alpha()
        self.state["img"] = pygame.transform.scale(img, (800, 500))
        self.state["sound"] = pygame.mixer.Sound('move_sprites/sandstorm/sandstorm.mp3')
        self.state["start"] = None
        self.state["particles"] = []
        self.state["spawn_timer"] = 0


    def _load_slash(self, name):
        img1 = pygame.image.load('move_sprites/slash/slash_1.png').convert_alpha()
        img2 = pygame.image.load('move_sprites/slash/slash_2.png').convert_alpha()
        img3 = pygame.image.load('move_sprites/slash/slash_3.png').convert_alpha()
        self.state["sound"] = pygame.mixer.Sound('move_sprites/slash/slash.mp3')
        self.state["frames"] = [img1, img2, img3]
        self.state["start"] = None


    def _load_hyper_beam(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/hyper_beam/hyper_beam.mp3')
        self.state["start"] = None
        self.state["particles"] = []
        self.state["spawn_timer"] = 0


    def _load_rain_dance(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/rain_dance/rain_dance.mp3')
        self.state["start"] = None
        self.state["particles"] = []
        self.state["spawn_timer"] = 0
        self.state["overlay"] = pygame.Surface((800, 330))
        self.state["overlay"].fill((20, 60, 120))   


    def _load_thunder(self, name):
        bg = pygame.image.load('move_sprites/thunder/thunder_1.png').convert_alpha()
        self.state["bg"] = pygame.transform.scale(bg, (800, 400))
        strike = pygame.image.load('move_sprites/thunder/thunder_2.png').convert_alpha()
        self.state["strike"] = pygame.transform.scale(strike, (int(strike.get_width()*0.5), int(strike.get_height()*0.5)))
        self.state["big_strike"] = pygame.transform.scale(strike, (int(strike.get_width()*0.8), int(strike.get_height()*0.8)))
        self.state["sound"] = pygame.mixer.Sound('move_sprites/thunder/thunder.mp3')
        self.state["start"] = None

    def _load_sunny_day(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/sunny_day/sunny_day.mp3')
        self.state["start"] = None
        self.state["overlay"] = pygame.Surface((800, 330))
        self.state["overlay"].fill((255, 170, 30))


    def _load_solar_beam(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/solar_beam/solar_beam.mp3')
        self.state["start"] = None
        self.state["particles"] = []
        self.state["spawn_timer"] = 0

    def _load_growth(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/growth/growth.mp3')
        self.state["start"] = None


    def _load_swift(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/swift/swift.mp3')
        self.state["start"] = None


    def _load_flamethrower(self, name):
        img = pygame.image.load('move_sprites/fire_blast/fire_blast.png').convert_alpha()
        self.state["img"]         = pygame.transform.scale(img, (int(img.get_width()*0.35), int(img.get_height()*0.35)))
        self.state["sound"]       = pygame.mixer.Sound('move_sprites/flamethrower/flamethrower.mp3')
        self.state["start"]       = None
        self.state["particles"]   = []
        self.state["spawn_timer"] = 0

    def _load_stun_spore(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/stun_spore/stun_spore.mp3')
        self.state["start"] = None
        self.state["particles"] = []
        self.state["spawn_timer"] = 0

    def _load_razor_wind(self, name):
        img = pygame.image.load('move_sprites/razor_wind/razor_wind.png').convert_alpha()
        self.state["sound"] = pygame.mixer.Sound('move_sprites/slash/slash.mp3')
        self.state["img"] = pygame.transform.scale(img, (int(img.get_width() * 0.6), int(img.get_height() * 0.6)))
        self.state["start"] = None
        self.state["phase"] = "travel"  # "travel" then "flash"


    def _load_sand_attack(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/sand_attack/sand_attack.mp3')
        self.state["start"] = None
        self.state["particles"] = []
        self.state["spawn_timer"] = 0
        self.state["spawning_done"] = False

    def _load_sleep_powder(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/sleep_powder/sleep_powder.mp3')
        self.state["start"] = None
        self.state["particles"] = []
        self.state["spawn_timer"] = 0
    
    def _load_ice_beam(self, name):
        img = pygame.image.load('move_sprites/ice_beam/ice_beam.png').convert_alpha()
        self.state["sound"] = pygame.mixer.Sound('move_sprites/ice_beam/ice_beam.mp3')
        self.state["img"] = pygame.transform.scale(img, (int(img.get_width()*0.5), int(img.get_height()*0.5)))
        self.state["start"] = None
        self.state["particles"] = []
        self.state["spawn_timer"] = 0

    def _load_status_sleep(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/status_sleep/sleep.mp3')
        self.state["start"] = None
        self.state["particles"] = []
        self.state["spawn_timer"] = 0
        self.state["sound_played"] = False

    def _load_surf(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/surf/surf.mp3')
        self.state["start"] = None
        self.state["wave_y"] = 520  # start below screen

    def _load_amnesia(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/amnesia/amnesia.mp3')
        self.state["start"] = None
        self.state["angle"] = 0

    def _load_screech(self, name):
        img = pygame.image.load('move_sprites/screech/screech.png').convert_alpha()
        self.state["img"] = pygame.transform.scale(img, (int(img.get_width()*0.5), int(img.get_height()*0.5)))
        self.state["sound"] = pygame.mixer.Sound('move_sprites/screech/screech.mp3')
        self.state["start"] = None

    def _load_psybeam(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/psybeam/psybeam.mp3')
        self.state["start"] = None
        self.state["particles"] = []
        self.state["spawn_timer"] = 0

    def _load_harden(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/harden/harden.mp3')
        self.state["start"] = None

    def _load_glare(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/glare/glare.mp3')
        self.state["start"] = None
        self.state["particles"] = []
        self.state["spawn_timer"] = 0

    def _load_acid(self, name):
        img = pygame.image.load('move_sprites/acid/acid.png').convert_alpha()
        img = pygame.transform.scale(img, (int(img.get_width()*0.4), int(img.get_height()*0.4)))
        self.state["sound"] = pygame.mixer.Sound('move_sprites/acid/acid.mp3')
        self.state["img"] = img
        self.state["start"] = None
        self.state["particles"] = []
        self.state["spawn_timer"] = 0

    def _load_psychic(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/psychic/psychic.mp3')
        self.state["start"] = None

    def _load_fire_spin(self, name):
        img = pygame.image.load('move_sprites/fire_spin/fire_spin.png').convert_alpha()
        img = pygame.transform.scale(img, (int(img.get_width()*0.35), int(img.get_height()*0.35)))
        self.state["sound"] = pygame.mixer.Sound('move_sprites/fire_spin/fire_spin.mp3')
        self.state["img"] = img
        self.state["start"] = None

    def _load_wrap(self, name):
        frames = [pygame.image.load(f'move_sprites/wrap/wrap_{i}.png').convert_alpha() for i in range(1, 5)]
        frames = [pygame.transform.scale(f, (int(f.get_width()*0.5), int(f.get_height()*0.5))) for f in frames]
        self.state["sound"] = pygame.mixer.Sound('move_sprites/wrap/wrap.mp3')
        self.state["frames"] = frames
        self.state["start"] = None

    def _load_leech_seed(self, name):
        seed = pygame.image.load('move_sprites/leech_seed/seed.png').convert_alpha()
        seed = pygame.transform.scale(seed, (int(seed.get_width()*0.6), int(seed.get_height()*0.6)))
        sprout1 = pygame.image.load('move_sprites/leech_seed/sprout_1.png').convert_alpha()
        sprout2 = pygame.image.load('move_sprites/leech_seed/sprout_2.png').convert_alpha()
        sprout1 = pygame.transform.scale(sprout1, (int(sprout1.get_width()*0.7), int(sprout1.get_height()*0.7)))
        sprout2 = pygame.transform.scale(sprout2, (int(sprout2.get_width()*0.7), int(sprout2.get_height()*0.7)))

        self.state["sound"] = pygame.mixer.Sound('move_sprites/leech_seed/leech_seed.mp3')
        self.state["seed"] = seed
        self.state["sprouts"] = [sprout1, sprout2]
        self.state["start"] = None

    def _load_dig(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/earthquake/earthquake.mp3')
        self.state["start"] = None

    def _load_fly(self, name):
        self.state["sound"] = pygame.mixer.Sound('move_sprites/fly/fly.mp3')
        self.state["start"] = None


    


    # ------------------------------------------------------------------ #
    #  LOAD / PLAY DISPATCH                                                #
    # ------------------------------------------------------------------ #

    def load_move(self, move_name):
        clean_name = move_name.lower().strip()
        if self.current_loaded_move == clean_name:
            return
        self.current_loaded_move = clean_name
        self.state = {}
        load_fn, _ = self.move_registry.get(clean_name, (None, None)) # _ mean dont care about this value
        if load_fn:
            load_fn(clean_name)

    def play(self, screen, move_name, opponent_sprite, opponent_rect, my_sprite, my_rect):
        self.load_move(move_name)
        clean = move_name.lower().strip()
        _, play_fn = self.move_registry.get(clean, (None, None))
        if play_fn:
            return play_fn(move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect)
        return True

    # ------------------------------------------------------------------ #
    #  SHARED HELPERS                                                      #
    # ------------------------------------------------------------------ #

    def flash(self, screen, opponent_sprite, opponent_rect, frame, total_flashes=3):
        cycle = frame % 10
        if cycle < 5:
            screen.blit(opponent_sprite, opponent_rect)
        return frame >= total_flashes * 10

    def _flash_phase(self, screen, opponent_sprite, opponent_rect):
        if not self.hit_played:
            self.hit_sound.play()
            self.hit_played = True
        done = self.flash(screen, opponent_sprite, opponent_rect, self.frame)
        self.frame += 1
        if done:
            self.frame = 0
            self.hit_played = False
            self.current_loaded_move = None
        return done
    
    def _start_animation(self, reset_frame=False):
        now = pygame.time.get_ticks()
        s = self.state

        if s["start"] is None:
            s["start"] = now
            s["sound"].play()

            if reset_frame:
                self.frame = 0

        return now - s["start"]
    

    # ------------------------------------------------------------------ #
    #  ANIMATION METHODS                                                   #
    # ------------------------------------------------------------------ #

    def anim_tackle(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        return self._flash_phase(screen, opponent_sprite, opponent_rect)
    

    def sword_dance(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        rect = s["img"].get_rect(center=(my_rect.centerx, my_rect.centery - 30))

        s["img"].set_alpha(min(255, int((elapsed / 100) * 255)))
        screen.blit(s["img"],rect)
        if elapsed >= 1000:
            s["img"].set_alpha(255)
            self.current_loaded_move = None
            return True
        return False

    def anim_poison(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        now = pygame.time.get_ticks()
        s = self.state
        self.frame = 0
        if s["index"] == 0 and s["timer"] == 0:
            s["sound"].play()
            s["timer"] = now
        rect = s["frames"][s["index"]].get_rect(center=opponent_rect.center)
        screen.blit(s["frames"][s["index"]], rect)
        if now - s["timer"] >= s["speed"]:
            s["index"] += 1
            s["timer"] = now
        if s["index"] >= len(s["frames"]):
            s["index"] = 0
            s["timer"] = 0
            self.current_loaded_move = None
            return True
        return False
    

    def anim_status_poison(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        tinted = opponent_sprite.copy()
        overlay = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)

        if elapsed < 600:
            alpha = int((elapsed / 600) * 180)
        elif elapsed < 1200:
            alpha = int((1 - (elapsed - 600) / 600) * 180)
        elif elapsed < 1800:
            alpha = int((elapsed - 1200) / 600 * 180)
        elif elapsed < 2400:
            alpha = int((1 - (elapsed - 1800) / 600) * 180)
        else:
            self.current_loaded_move = None
            return True

        overlay.fill((148, 0, 211, alpha))
        tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(tinted, opponent_rect)

        return False

    def punch(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        if move_name == "mega punch":
            if elapsed < 1000:
                self.dark_overlay.fill((0, 0, 0))
                self.dark_overlay.set_alpha(min(180, int((elapsed / 600) * 180)))
                screen.blit(self.dark_overlay, (0, 0))
                if elapsed >= 700:

                    fist_rect = s["fist"].get_rect(center=opponent_rect.center)
                    screen.blit(s["fist"], fist_rect)

                return False
            flash_elapsed = elapsed - 1000
            self.dark_overlay.fill((0, 0, 0))
            self.dark_overlay.set_alpha(max(0, 180 - int((flash_elapsed / 400) * 180)))
            screen.blit(self.dark_overlay, (0, 0))

        elif move_name == "thunder punch":
            if elapsed < 1200:
                self.dark_overlay.fill((0, 0, 0))
                self.dark_overlay.set_alpha(min(160, int((elapsed / 600) * 160)))
                screen.blit(self.dark_overlay, (0, 0))
                
                if elapsed >= 300:
                    fist_rect = s["fist"].get_rect(center=opponent_rect.center)
                    screen.blit(s["fist"], fist_rect)
                if elapsed >= 600:
                    sx, sy = random.randint(-4, 4), random.randint(-4, 4)
                    cx, cy = opponent_rect.centerx, opponent_rect.centery - 50
                    screen.blit(s["effect"], (cx - 30 + sx, cy - 80 + sy))
                    screen.blit(s["effect"], (cx + sx,      cy - 40 + sy))
                    screen.blit(s["effect"], (cx - 20 + sx, cy + sy))

                return False
            flash_elapsed = elapsed - 1200
            self.dark_overlay.fill((0, 0, 0))
            self.dark_overlay.set_alpha(max(0, 160 - int((flash_elapsed / 400) * 160)))
            screen.blit(self.dark_overlay, (0, 0))

        else:
            if elapsed < 1000:
                cx, cy = opponent_rect.centerx, opponent_rect.centery - 50
                if move_name == "fire punch":
                    screen.blit(s["effect"], (cx - 40, cy))
                elif move_name == "ice punch":
                    screen.blit(s["effect"], (cx - 50, cy))
                    screen.blit(s["effect"], (cx + 50, cy + 20))
                    screen.blit(s["effect"], (cx - 40, cy + 75))
                    screen.blit(s["effect"], (cx, cy - 30))
                    screen.blit(s["effect"], (cx - 10, cy + 10))
                if elapsed >= 400:
                    fist_rect = s["fist"].get_rect(center=opponent_rect.center)
                    screen.blit(s["fist"], fist_rect)
                return False

        done = self._flash_phase(screen, opponent_sprite, opponent_rect)
        if done:
            s["start"] = None
        return done

    def anim_earthquake(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        s = self.state
        elapsed = self._start_animation()

        progress = elapsed / s["duration"]
        intensity = int((progress * 2 if progress < 0.5 else (1 - progress) * 2) * 18)
        shaken_rect = opponent_rect.move(random.randint(-intensity, intensity), random.randint(-intensity // 2, intensity // 2))
        screen.blit(opponent_sprite, shaken_rect)
        if elapsed >= s["duration"]:
            self.current_loaded_move = None
            return True
        return False

    def anim_toxic(self, move_name, screen, opponent_sprite, opponent_rect,my_sprite,my_rect):
        now = pygame.time.get_ticks()
        s = self.state
        if s["start"] is None:
            s["start"] = now
            s["sound"].play()
            s["puddle_positions"] = [
                (opponent_rect.left - 10,    opponent_rect.bottom - 20),
                (opponent_rect.centerx - 10, opponent_rect.bottom - 15),
                (opponent_rect.right - 20,   opponent_rect.bottom - 25),
            ]
        elapsed = now - s["start"]

        for pos in s["puddle_positions"]:
            screen.blit(s["puddle"], pos)

        for i, pos in enumerate(s["puddle_positions"]):
            bubble_elapsed = elapsed - i * 200
            if bubble_elapsed > 0:
                rise = int((bubble_elapsed / 800) * 80)
                bubble_y = pos[1] - rise
                if bubble_y > opponent_rect.top - 20:
                    screen.blit(s["bubble"], (pos[0] + random.randint(-2, 2), bubble_y))

        tinted = opponent_sprite.copy()
        overlay = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
        overlay.fill((148, 0, 211, 120))
        tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        if elapsed > 3100:
            shaken_rect = opponent_rect.move(random.randint(-4, 4), random.randint(-3, 3))
            screen.blit(tinted, shaken_rect)
        else:
            screen.blit(tinted, opponent_rect)

        if elapsed >= 5000:
            self.current_loaded_move = None
            return True
        return False

    def anim_scratch(self, move_name, screen, opponent_sprite, opponent_rect,my_sprite,my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        if elapsed < 400:
            screen.blit(opponent_sprite, opponent_rect)
            screen.blit(s["img1"], (opponent_rect.centerx - 20, opponent_rect.top))
            return False
        elif elapsed < 800:
            screen.blit(opponent_sprite, opponent_rect)
            screen.blit(s["img2"], (opponent_rect.centerx - 20, opponent_rect.top))
            return False
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done

    def anim_hydro_pump(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        start_x, start_y = my_rect.centerx, my_rect.centery
        end_x, end_y = opponent_rect.centerx, opponent_rect.centery

        if elapsed < 1200:
            screen.blit(opponent_sprite, opponent_rect)
            progress = min(1.0, elapsed / 800)
            for i in range(20):
                dp = progress - (i * 0.12)
                if dp <= 0:
                    continue
                if dp >= 1.0:  # ADD THIS - drop has hit raichu, don't draw it
                    continue
                dp = min(1.0, dp)
                x = int(start_x + (end_x - start_x) * dp)
                y = int(start_y + (end_y - start_y) * dp)
                screen.blit(s["img"], (x - 20, y - 20)) #offset
            return False
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        
    def karate_chop(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        now = pygame.time.get_ticks()
        state = self.state
        if state["start"] is None:
            state["start"] = now
            state["sound"].play()
            state["y"] = opponent_rect.top
            self.frame = 0
        elapsed = now - state["start"]
        if elapsed < 100:
            screen.blit(state["img"], (opponent_rect.centerx - 40, state["y"]))
        elif elapsed < 1200:
            screen.blit(state["img"], (opponent_rect.centerx - 40, state["y"]))
            if state["y"] > opponent_rect.bottom - 40:
                pass
            else:
                state["y"] += 4  # move down fast
            return False
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                state["start"] = None
            return done
        
    def anim_take_down(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        now = pygame.time.get_ticks()
        s = self.state
        if s["start"] is None:
            s["start"] = now
            s["sound"].play()
            s["origin_x"] = opponent_rect.x
            self.frame = 0
        elapsed = now - s["start"]

        if elapsed < 600:
            # slide right over 300ms, then back over the next 300ms
            if elapsed < 300:
                offset = int((elapsed / 300) * 60)
            else:
                offset = int(((600 - elapsed) / 300) * 60)
            shifted_rect = opponent_rect.move(offset, 0)
            screen.blit(opponent_sprite, shifted_rect)
            return False
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        
    def anim_submission(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        if elapsed < 1200:
            s["angle"] = (s["angle"] + 15) % 360
            radius = 30
            vec = pygame.math.Vector2(radius, 0).rotate(s["angle"])
            cx = opponent_rect.centerx + int(vec.x)
            cy = opponent_rect.centery + int(vec.y)
            orbiting_rect = opponent_sprite.get_rect(center=(cx, cy))
            screen.blit(opponent_sprite, orbiting_rect)

            if (elapsed // 200) % 2 == 0:
                img_rect = s["img"].get_rect(center=(cx, cy))
                screen.blit(s["img"], img_rect)
            return False
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done

    def anim_mega_kick(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        if elapsed < 1400:
            # darken screen
            alpha = min(180, int((elapsed / 600) * 180))
            self.dark_overlay.fill((0, 0, 0))
            self.dark_overlay.set_alpha(alpha)
            screen.blit(self.dark_overlay, (0, 0))

            # blit mega kick image with shake after 500ms
            if elapsed >= 500:
                sx = random.randint(-5, 5)
                sy = random.randint(-5, 5)
                img_rect = s["img"].get_rect(center=(opponent_rect.centerx + sx, opponent_rect.centery + sy))
                screen.blit(s["img"], img_rect)
            return False
        else:
            # fade dark overlay out during flash
            flash_elapsed = elapsed - 1400
            fade_alpha = max(0, 180 - int((flash_elapsed / 400) * 180))
            self.dark_overlay.fill((0, 0, 0))
            self.dark_overlay.set_alpha(fade_alpha)
            screen.blit(self.dark_overlay, (0, 0))

            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        

    def anim_strength(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        if elapsed < 1400:
            screen.blit(opponent_sprite, opponent_rect)
            # show impact at 200ms, 600ms, 1000ms for 150ms each
            if 600 <= elapsed < 850 or 950 <= elapsed < 1100 or 1200 <= elapsed < 1350:
                img_rect = s["img"].get_rect(center=opponent_rect.center)
                screen.blit(s["img"], img_rect)
            return False
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        
    def anim_low_kick(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        now = pygame.time.get_ticks()
        s = self.state
        if s["start"] is None:
            s["start"] = now
            s["sound"].play()
            self.frame = 0
        elapsed = now - s["start"]

        if elapsed < 600:
            screen.blit(opponent_sprite, opponent_rect)
            progress = elapsed / 700 
            x = int(opponent_rect.left + progress * opponent_rect.width)
            y = opponent_rect.bottom - s["img"].get_height()
            screen.blit(s["img"], (x, y))
            return False
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        
    def anim_fire_blast(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        # phase 1: 0-1000ms, fire images orbit in a small circle around raichu
        if elapsed < 1000:
            screen.blit(opponent_sprite, opponent_rect)
            angle_offset = (elapsed / 1000) * 360
            num_particles = 8
            radius = 90
            for i in range(num_particles):
                angle = angle_offset + (i * 360 / num_particles)
                vec = pygame.math.Vector2(radius, 0).rotate(angle)
                cx = opponent_rect.centerx + int(vec.x)
                cy = opponent_rect.centery + int(vec.y)
                img_rect = s["img"].get_rect(center=(cx, cy))
                screen.blit(s["img"], img_rect)
            return False

        # phase 2: 1000-1500ms, raichu shrinks
        elif elapsed < 1500:
            progress = (elapsed - 1000) / 500
            screen.blit(opponent_sprite, opponent_rect)
            radius = int(90 * (1.0 - progress))  # shrink from 90 to 0
            num_particles = 8
            angle_offset = (elapsed / 1000) * 360
            for i in range(num_particles):
                angle = angle_offset + (i * 360 / num_particles)
                vec = pygame.math.Vector2(radius, 0).rotate(angle)
                cx = opponent_rect.centerx + int(vec.x)
                cy = opponent_rect.centery + int(vec.y)
                img_rect = s["img"].get_rect(center=(cx, cy))
                screen.blit(s["img"], img_rect)
            return False

        # phase 3: 1500-2500ms, 3 lines of fire blast at 120 degrees from each other
        elif elapsed < 2500:
            progress = (elapsed - 1500) / 1000
            max_reach = 180
            num_per_line = 6
            for line in range(3):
                angle = line * 120
                for j in range(num_per_line):
                    frac = j / num_per_line
                    if frac > progress:
                        break
                    dist = int(frac * max_reach)
                    vec = pygame.math.Vector2(dist, 0).rotate(angle)
                    cx = opponent_rect.centerx + int(vec.x)
                    cy = opponent_rect.centery + int(vec.y)
                    img_rect = s["img"].get_rect(center=(cx, cy))
                    screen.blit(s["img"], img_rect)
            return False

        # phase 4: flash
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
                s["scale"] = 1.0
            return done
        

    def anim_bite(self, move_name, screen, opponent_sprite, opponent_rect,my_sprite,my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        if elapsed < 900:
            screen.blit(opponent_sprite, opponent_rect)
            progress = min(1.0, elapsed / 300)
            # img1 comes from above, img2 comes from below
            offset = int((1.0 - progress) * 60)
            img1_rect = s["img1"].get_rect(midbottom=(opponent_rect.centerx, opponent_rect.centery - offset))
            img2_rect = s["img2"].get_rect(midtop=(opponent_rect.centerx, opponent_rect.centery + offset))
            screen.blit(s["img1"], img1_rect)
            screen.blit(s["img2"], img2_rect)
            return False
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        
    def anim_poison_sting(self, move_name, screen, opponent_sprite, opponent_rect,my_sprite,my_rect):
        s = self.state
        elapsed = self._start_animation(True)
        
        start_x, start_y = my_rect.centerx, my_rect.centery
        end_x, end_y = opponent_rect.centerx, opponent_rect.centery

        if elapsed < 600:
            screen.blit(opponent_sprite, opponent_rect)
            progress = elapsed / 600
            if progress < 1.0:
                x = int(start_x + (end_x - start_x) * progress)
                y = int(start_y + (end_y - start_y) * progress)
                img_rect = s["img"].get_rect(center=(x, y))
                screen.blit(s["img"], img_rect)
            return False
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        
    def anim_wing_attack(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        start_x, start_y = my_rect.centerx, my_rect.centery
        end_x, end_y = opponent_rect.centerx, opponent_rect.centery

        if elapsed < 600:
            screen.blit(opponent_sprite, opponent_rect)
            progress = elapsed / 600
            if progress < 1.0:
                x = int(start_x + (end_x - start_x) * progress)
                y = int(start_y + (end_y - start_y) * progress)
                img_rect = s["img"].get_rect(center=(x, y))
                screen.blit(s["img"], img_rect)
            return False
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        
    def anim_gust(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        if elapsed < 1000:
            s["angle"] = (elapsed / 1000) * 360
            radius = 70
            vec = pygame.math.Vector2(radius, 0).rotate(s["angle"])
            cx = opponent_rect.centerx + int(vec.x)
            cy = opponent_rect.centery + int(vec.y)
            screen.blit(opponent_sprite, opponent_rect)
            img_rect = s["img"].get_rect(center=(cx, cy))
            screen.blit(s["img"], img_rect)
            return False
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        

    def anim_comet_punch(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        now = pygame.time.get_ticks()
        s = self.state
        if s["start"] is None:
            s["start"] = now
            self.frame = 0
            num_hits = random.randint(2, 5)
            s["positions"] = [(opponent_rect.centerx, opponent_rect.centery) for _ in range(num_hits)]
            s["hit_count"] = 0
            s["next_hit_time"] = now + 150
            s["showing_until"] = 0
            s["current_pos"] = None


        if s["current_pos"] is not None and now < s["showing_until"]:
            cx, cy = s["current_pos"]
            img_rect = s["img"].get_rect(center=(cx, cy))
            screen.blit(s["img"], img_rect)
            return False

        if s["hit_count"] < len(s["positions"]) and now >= s["next_hit_time"]:
            cx, cy = s["positions"][s["hit_count"]]
            s["current_pos"] = (cx, cy)
            s["showing_until"] = now + 1000
            img_rect = s["img"].get_rect(center=(cx, cy))
            screen.blit(s["img"], img_rect)
            s["sound"].play()
            s["hit_count"] += 1
            s["next_hit_time"] = now + 1200
            return False

        if s["hit_count"] >= len(s["positions"]) and now >= s["next_hit_time"]:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done

        return False
    
    def anim_double_team(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        if elapsed < 2000:
            speed = 20
            s["offset"] += speed * s["direction"]
            if s["offset"] > 80 or s["offset"] < -80:
                s["direction"] *= -1

            # draw faded ghost copies on left and right
            ghost = my_sprite.copy()
            ghost.set_alpha(120)
            left_rect = my_rect.move(-abs(s["offset"]), 0)
            right_rect = my_rect.move(abs(s["offset"]), 0)
            screen.blit(ghost, left_rect)
            screen.blit(my_sprite, my_rect)
            screen.blit(ghost, right_rect)
            return False
        else:
            screen.blit(my_sprite, my_rect)
            self.current_loaded_move = None
            return True
        
    def anim_thunderbolt(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        num_hits = 3
        hit_interval = 300  # ms between each hit
        phase_end = num_hits * hit_interval  # 900ms

        if elapsed < phase_end:
            current_hit = elapsed // hit_interval
            hit_elapsed = elapsed % hit_interval
            if hit_elapsed < 150:  # show effect for first 150ms of each hit window
                offsets = [(-10, -10), (10, 5), (-5, 10)]
                ox, oy = offsets[min(current_hit, len(offsets)-1)]
                img_rect = s["effect"].get_rect(center=(opponent_rect.centerx + ox, opponent_rect.centery + oy))
                screen.blit(s["effect"], img_rect)
            return False
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        
    
    def anim_ember(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite,my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        if elapsed < 600:
            progress = elapsed / 600
            x = int(opponent_rect.left + progress * opponent_rect.width)
            y = opponent_rect.bottom - s["img"].get_height()
            img_rect = s["img"].get_rect(center=(x, y))
            screen.blit(s["img"], img_rect)  
            return False
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        

    def anim_mega_drain(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        # spawn particles continuously for first 1200ms
        if elapsed < 1200:
            screen.blit(opponent_sprite, opponent_rect)

            # spawn a new particle every ~40ms (roughly 1-2 per frame)
            if random.randint(0, 2) == 0:
                sx = opponent_rect.centerx + random.randint(-30, 30)
                sy = opponent_rect.centery + random.randint(-30, 30)
                s["particles"].append({
                    "x": float(sx),
                    "y": float(sy),
                    "tx": my_rect.centerx + random.randint(-20, 20),
                    "ty": my_rect.centery + random.randint(-20, 20),
                    "progress": 0.0,
                    "speed": random.uniform(0.01, 0.025)
                })

            # update and draw all particles
            alive = []
            for p in s["particles"]:
                p["progress"] = min(1.0, p["progress"] + p["speed"])
                x = int(p["x"] + (p["tx"] - p["x"]) * p["progress"])
                y = int(p["y"] + (p["ty"] - p["y"]) * p["progress"])
                img_rect = s["img"].get_rect(center=(x, y))
                screen.blit(s["img"], img_rect)
                if p["progress"] < 1.0:
                    alive.append(p)
            s["particles"] = alive
            return False

        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
                s["particles"] = []
            return done
        

    def anim_body_slam(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        # phase 1: 0-400ms — squeeze the opponent sprite vertically
        if elapsed < 400:
            progress = elapsed / 400  # 0.0 → 1.0
            squeeze = 1.0 - (0.6 * progress)  # scale y from 1.0 down to 0.4
            squeezed_w = opponent_sprite.get_width()
            squeezed_h = max(1, int(opponent_sprite.get_height() * squeeze))
            squeezed = pygame.transform.scale(opponent_sprite, (squeezed_w, squeezed_h))
            # pin to the bottom of original rect so it squishes downward
            squeezed_rect = squeezed.get_rect(midbottom=opponent_rect.midbottom)
            screen.blit(squeezed, squeezed_rect)
            return False

        # phase 2: 400-700ms — slam impact image blits over the opponent
        elif elapsed < 700:
            screen.blit(opponent_sprite, opponent_rect)
            img_rect = s["img"].get_rect(center=opponent_rect.center)
            screen.blit(s["img"], img_rect)
            return False

        # phase 3: flash like normal
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        
        
    def anim_sandstorm(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation()
        now = pygame.time.get_ticks()

        s["img"].set_alpha(max(0, int(200 * (1.0 - elapsed / 3000))))
        screen.blit(s["img"], (0, -160))

        if now - s["spawn_timer"] >= 60:
            s["spawn_timer"] = now
            for _ in range(random.randint(2, 4)):
                s["particles"].append({"x": float(random.randint(-50, 0)), "y": float(random.randint(0, 300)),
                                    "speed": random.uniform(8, 18), "length": random.randint(20, 70),
                                    "thickness": random.randint(1, 3)})

        alive = []
        for p in s["particles"]:
            p["x"] += p["speed"]
            if p["x"] < 850:
                pygame.draw.line(screen, (210, 180, 100),
                                (int(p["x"]), int(p["y"])), (int(p["x"]) - p["length"], int(p["y"])), p["thickness"])
                alive.append(p)
        s["particles"] = alive

        if elapsed >= 3000:
            self.current_loaded_move = None
            return True
        return False
    

    def anim_slash(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        elapsed = self._start_animation(True)
        
        # Draw current frame

        if elapsed > 150 and elapsed < 350:
            frame_rect =  self.state["frames"][0].get_rect(center=opponent_rect.center)
            screen.blit(self.state["frames"][0], frame_rect)

        elif elapsed > 350 and elapsed < 550:
            frame_rect =  self.state["frames"][1].get_rect(center=opponent_rect.center)
            screen.blit(self.state["frames"][1], frame_rect)

        elif elapsed > 550 and elapsed < 750:
            frame_rect =  self.state["frames"][2].get_rect(center=opponent_rect.center)
            screen.blit(self.state["frames"][2], frame_rect)

        
        # After all 3 frames, do flash
        if elapsed > 850:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                self.current_loaded_move = None
                self.state["start"] = None
            return done
        
        return False
    

    def anim_hyper_beam(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation()
        now = pygame.time.get_ticks()

        BLACKOUT     = 800
        BEAM_END     = 3000
        FADE_END     = 3400

        # Darken
        if elapsed < BLACKOUT:
            self.dark_overlay.fill((0, 0, 0))
            self.dark_overlay.set_alpha(int(elapsed / BLACKOUT * 240))
            screen.blit(self.dark_overlay, (0, 0))
            screen.blit(opponent_sprite, opponent_rect)
            screen.blit(my_sprite, my_rect)
            return False

        # Beam
        if elapsed < BEAM_END:
            self.dark_overlay.fill((0, 0, 0))
            self.dark_overlay.set_alpha(230)
            screen.blit(self.dark_overlay, (0, 0))
            screen.blit(my_sprite, my_rect)

            if now - s["spawn_timer"] >= 20:
                s["spawn_timer"] = now
                for _ in range(random.randint(3, 6)):
                    s["particles"].append({
                        "t": 0.0,
                        "speed": random.uniform(0.012, 0.022),
                        "dx": random.randint(-14, 14),
                        "dy": random.randint(-14, 14),
                        "color": random.choice([(255,255,120),(255,180,60),(200,120,255),(120,200,255),(255,255,255)]),
                        "width": random.randint(2, 6),
                    })

            sx, sy = my_rect.centerx, my_rect.centery
            ex, ey = opponent_rect.centerx, opponent_rect.centery

            alive = []
            for p in s["particles"]:
                p["t"] = min(1.0, p["t"] + p["speed"])
                x  = int(sx + (ex - sx) * p["t"] + p["dx"])
                y  = int(sy + (ey - sy) * p["t"] + p["dy"])
                x0 = int(sx + (ex - sx) * max(0, p["t"] - 0.04) + p["dx"])
                y0 = int(sy + (ey - sy) * max(0, p["t"] - 0.04) + p["dy"])
                pygame.draw.line(screen, p["color"], (x0, y0), (x, y), p["width"])
                if p["t"] < 1.0:
                    alive.append(p)
            s["particles"] = alive

            pygame.draw.line(screen, (255, 255, 255), (sx, sy), (ex, ey), 4 + random.randint(-1, 1))
            pygame.draw.line(screen, (255, 240, 100), (sx, sy), (ex, ey), 2)

            beam_elapsed = elapsed - BLACKOUT
            if beam_elapsed > 400:
                r = int(8 + 10 * abs(math.sin(beam_elapsed / 120)))
                pygame.draw.circle(screen, (255, 255, 200), opponent_rect.center, r)
                pygame.draw.circle(screen, (255, 180,  60), opponent_rect.center, r + 6, 2)

            return False

        # Fade out darkness
        if elapsed < FADE_END:
            self.dark_overlay.fill((0, 0, 0))
            self.dark_overlay.set_alpha(int(230 * (1 - (elapsed - BEAM_END) / (FADE_END - BEAM_END))))
            screen.blit(self.dark_overlay, (0, 0))
            return False

        # Flash
        done = self._flash_phase(screen, opponent_sprite, opponent_rect)
        if done:
            s["start"] = None
            s["particles"] = []
        return done
    

    def anim_rain_dance(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation()
        now = pygame.time.get_ticks()

        DARKEN = 500
        RAIN   = 2000
        FADE   = 2500

        if elapsed < DARKEN:
            s["overlay"].set_alpha(int(elapsed / DARKEN * 140))
            screen.blit(s["overlay"], (0, 0))
            return False

        if elapsed < RAIN:
            s["overlay"].set_alpha(140)
            screen.blit(s["overlay"], (0, 0))

            if now - s["spawn_timer"] >= 40:
                s["spawn_timer"] = now
                for _ in range(random.randint(3, 6)):
                    s["particles"].append({
                        "x":         float(random.randint(0, 800)),
                        "y":         float(random.randint(-20, 0)),
                        "speed_x":   random.uniform(3, 6),
                        "speed_y":   random.uniform(10, 18),
                        "length":    random.randint(10, 25),
                        "thickness": random.randint(1, 2),
                    })

            alive = []
            for p in s["particles"]:
                p["x"] += p["speed_x"]
                p["y"] += p["speed_y"]
                if p["y"] < 330:
                    color = (random.randint(80, 120), random.randint(140, 180), random.randint(210, 255))
                    x2 = int(p["x"] - p["length"] * (p["speed_x"] / p["speed_y"]))
                    y2 = int(p["y"] - p["length"])
                    pygame.draw.line(screen, color, (int(p["x"]), int(p["y"])), (x2, y2), p["thickness"])
                    alive.append(p)
            s["particles"] = alive
            return False

        if elapsed < FADE:
            s["overlay"].set_alpha(int(140 * (1 - (elapsed - RAIN) / (FADE - RAIN))))
            screen.blit(s["overlay"], (0, 0))
            return False

        if elapsed >= 3000:
            self.current_loaded_move = None
            return True
        

    def anim_thunder(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        BG_END      = 600
        STRIKE1_END = 1100
        STRIKE2_END = 1600
        BIG_END     = 2400

        if elapsed < BG_END:
            alpha = int(250 * (elapsed / BG_END))
            s["bg"].set_alpha(alpha)
            screen.blit(s["bg"], (0, -70))
            screen.blit(opponent_sprite, opponent_rect)
            return False

        # background stays for all remaining phases
        s["bg"].set_alpha(250)
        screen.blit(s["bg"], (0, -70))
        screen.blit(opponent_sprite, opponent_rect)

        if elapsed < STRIKE1_END:
            img_rect = s["strike"].get_rect(midbottom=(opponent_rect.left - 10, opponent_rect.bottom))
            screen.blit(s["strike"], img_rect)
            return False

        if elapsed < STRIKE2_END:
            img_rect = s["strike"].get_rect(midbottom=(opponent_rect.right + 10, opponent_rect.bottom))
            screen.blit(s["strike"], img_rect)
            return False

        if elapsed < BIG_END:
            img_rect = s["big_strike"].get_rect(midbottom=(opponent_rect.centerx, opponent_rect.bottom))
            screen.blit(s["big_strike"], img_rect)
            return False

        done = self._flash_phase(screen, opponent_sprite, opponent_rect)
        if done:
            s["start"] = None
        return done
    
    def anim_sunny_day(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation()

        FLASH_END = 1000
        FADE_END  = 2000

        # phase 1: fade in yellow
        if elapsed < FLASH_END:
            alpha = int(140 * (elapsed / FLASH_END))
            s["overlay"].set_alpha(alpha)
            screen.blit(s["overlay"], (0, 0), (0, 0, 800, 330))
            return False

        # phase 2: fade out
        if elapsed < FADE_END:
            alpha = int(140 * (1.0 - (elapsed - FLASH_END) / (FADE_END - FLASH_END)))
            s["overlay"].set_alpha(alpha)
            screen.blit(s["overlay"], (0, 0), (0, 0, 800, 330))
            return False

        self.current_loaded_move = None
        return True
    

    def anim_solar_beam(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation()
        now = pygame.time.get_ticks()

        BLACKOUT = 800
        BEAM_END = 3000
        FADE_END = 3400

        if elapsed < BLACKOUT:
            self.dark_overlay.fill((0, 0, 0))
            self.dark_overlay.set_alpha(int(elapsed / BLACKOUT * 240))
            screen.blit(self.dark_overlay, (0, 0))
            screen.blit(opponent_sprite, opponent_rect)
            screen.blit(my_sprite, my_rect)
            return False

        if elapsed < BEAM_END:
            self.dark_overlay.fill((0, 0, 0))
            self.dark_overlay.set_alpha(230)
            screen.blit(self.dark_overlay, (0, 0))
            screen.blit(my_sprite, my_rect)

            if now - s["spawn_timer"] >= 20:
                s["spawn_timer"] = now
                for _ in range(random.randint(3, 6)):
                    s["particles"].append({
                        "t": 0.0,
                        "speed": random.uniform(0.012, 0.022),
                        "dx": random.randint(-14, 14),
                        "dy": random.randint(-14, 14),
                        "color": random.choice([(255,220,50),(200,255,80),(255,255,100),(100,220,50),(180,255,60)]),
                        "radius": random.randint(4, 10),
                    })

            sx, sy = my_rect.centerx, my_rect.centery
            ex, ey = opponent_rect.centerx, opponent_rect.centery

            alive = []
            for p in s["particles"]:
                p["t"] = min(1.0, p["t"] + p["speed"])
                x = int(sx + (ex - sx) * p["t"] + p["dx"])
                y = int(sy + (ey - sy) * p["t"] + p["dy"])
                pygame.draw.circle(screen, p["color"], (x, y), p["radius"])
                if p["t"] < 1.0:
                    alive.append(p)
            s["particles"] = alive

            beam_elapsed = elapsed - BLACKOUT
            if beam_elapsed > 400:
                r = int(8 + 10 * abs(math.sin(beam_elapsed / 120)))
                pygame.draw.circle(screen, (200, 255, 80), opponent_rect.center, r)
                pygame.draw.circle(screen, (255, 220, 50), opponent_rect.center, r + 6, 2)

            return False

        if elapsed < FADE_END:
            self.dark_overlay.fill((0, 0, 0))
            self.dark_overlay.set_alpha(int(230 * (1 - (elapsed - BEAM_END) / (FADE_END - BEAM_END))))
            screen.blit(self.dark_overlay, (0, 0))
            return False

        done = self._flash_phase(screen, opponent_sprite, opponent_rect)
        if done:
            s["start"] = None
            s["particles"] = []
        return done
    
    def anim_growth(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        if elapsed < 600:
            # grow
            scale = 1.0 + 0.12 * (elapsed / 600)
        elif elapsed < 1000:
            # shrink back
            scale = 1.12 - 0.12 * ((elapsed - 600) / 400)
        else:
            self.current_loaded_move = None
            return True

        new_w = int(my_sprite.get_width() * scale)
        new_h = int(my_sprite.get_height() * scale)
        scaled = pygame.transform.scale(my_sprite, (new_w, new_h))
        scaled_rect = scaled.get_rect(center=my_rect.center)
        screen.blit(scaled, scaled_rect)
        return False
    

    def anim_swift(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        # Fast shooting phase (600ms total duration)
        if elapsed < 600:
            screen.blit(opponent_sprite, opponent_rect)
            
            # Deterministic loop generating separate, straight parallel star lines on the fly
            for i in range(6):
                star_elapsed = elapsed - (i * 45)  # Staggered launch times
                if star_elapsed <= 0:
                    continue
                
                t = star_elapsed / 350.0  # Time to travel from user to opponent
                if t >= 1.0:
                    continue

                ox = int((i - 2.5) * 22)
                oy = int(((i * 2) % 5 - 2) * 18)

                # Calculate linear path from attacker to target with the offset
                cx = int(my_rect.centerx + ox + (opponent_rect.centerx - my_rect.centerx) * t)
                cy = int(my_rect.centery + oy + (opponent_rect.centery - my_rect.centery) * t)
                
                pts = [
                    (cx, cy - 11), (cx + 4, cy - 4), (cx + 11, cy), (cx + 4, cy + 4),
                    (cx, cy + 11), (cx - 4, cy + 4), (cx - 11, cy), (cx - 4, cy - 4)
                ]
                pygame.draw.polygon(screen, (246, 190, 0), pts)
                pygame.draw.polygon(screen, (255, 255, 255), pts, 1)
            return False

        # Execute final flash phase sequence on hit
        done = self._flash_phase(screen, opponent_sprite, opponent_rect)
        if done:
            s["start"] = None
        return done
    

    def anim_flamethrower(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        DURATION = 3000
        if elapsed < DURATION:
            screen.blit(opponent_sprite, opponent_rect)
            sx, sy = my_rect.centerx, my_rect.centery
            ex, ey = opponent_rect.centerx, opponent_rect.centery
            now = pygame.time.get_ticks()

            if now - s.get("spawn_timer", 0) >= 40:
                s["spawn_timer"] = now
                s.setdefault("particles", []).append({
                    "t": 0.0,
                    "speed": random.uniform(0.014, 0.022),
                    "dy": random.uniform(-18, 18),
                })

            alive = []
            for p in s.get("particles", []):
                p["t"] = min(1.0, p["t"] + p["speed"])
                x = int(sx + (ex - sx) * p["t"])
                y = int(sy + (ey - sy) * p["t"] + math.sin(p["t"] * math.pi * 3) * p["dy"])
                screen.blit(s["img"], s["img"].get_rect(center=(x, y)))
                if p["t"] < 1.0:
                    alive.append(p)
            s["particles"] = alive
            return False

        done = self._flash_phase(screen, opponent_sprite, opponent_rect)
        if done:
            s["start"] = None
            s["particles"] = []
        return done
    

    def anim_stun_spore(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation()
        now = pygame.time.get_ticks()

        screen.blit(opponent_sprite, opponent_rect)

        if now - s["spawn_timer"] >= 80:
            s["spawn_timer"] = now
            for _ in range(random.randint(2, 4)):
                s["particles"].append({
                    "x": float(opponent_rect.centerx + random.randint(-30, 30)),
                    "y": float(opponent_rect.top + random.randint(0, 20)),
                    "speed_y": random.uniform(1.5, 3.5),
                    "drift_x": random.uniform(-0.8, 0.8),
                    "size": random.randint(3, 7),
                    "alpha": 255,
                })

        alive = []
        for p in s["particles"]:
            p["y"] += p["speed_y"]
            p["x"] += p["drift_x"]
            p["alpha"] = max(0, p["alpha"] - 3)
            color = (255, random.randint(200, 230), 0)
            pygame.draw.circle(screen, color, (int(p["x"]), int(p["y"])), p["size"])
            if p["y"] < opponent_rect.bottom + 40 and p["alpha"] > 0:
                alive.append(p)
        s["particles"] = alive

        if elapsed >= 2000:
            self.current_loaded_move = None
            return True
        return False
    

    def anim_razor_wind(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        if s["phase"] == "travel":
            screen.blit(opponent_sprite, opponent_rect)

            travel_duration = 800
            offsets = [0, -25, 25]  # 3 copies, vertically spread

            for offset in offsets:
                progress = min(1.0, elapsed / travel_duration)
                x = int(my_rect.centerx + (opponent_rect.centerx - my_rect.centerx) * progress)
                y = int(my_rect.centery + (opponent_rect.centery - my_rect.centery) * progress) + offset
                img_rect = s["img"].get_rect(center=(x, y))
                screen.blit(s["img"], img_rect)

            if elapsed >= travel_duration:
                s["phase"] = "flash"
                s["start"] = None  # reset so _flash_phase works fresh
            return False

        else:  # flash phase
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["phase"] = "travel"
            return done
        

    def anim_sand_attack(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation()
        now = pygame.time.get_ticks()

        screen.blit(opponent_sprite, opponent_rect)

        # spawn particles for first 600ms only
        if elapsed < 600 and not s["spawning_done"]:
            if now - s["spawn_timer"] >= 80:
                s["spawn_timer"] = now
                for _ in range(random.randint(2, 3)):
                    s["particles"].append({
                        "x": float(my_rect.centerx),
                        "y": float(my_rect.centery),
                        "tx": float(opponent_rect.centerx + random.randint(-25, 25)),
                        "ty": float(opponent_rect.centery + random.randint(-10, 20)),
                        "progress": 0.0,
                        "speed": random.uniform(0.018, 0.03),
                        "size": random.randint(3, 6),
                    })
        elif elapsed >= 600:
            s["spawning_done"] = True

        alive = []
        for p in s["particles"]:
            p["progress"] = min(1.0, p["progress"] + p["speed"])
            x = int(p["x"] + (p["tx"] - p["x"]) * p["progress"])
            y = int(p["y"] + (p["ty"] - p["y"]) * p["progress"])
            shade = random.randint(180, 210)
            pygame.draw.circle(screen, (shade, 160, 80), (x, y), p["size"])
            if p["progress"] < 1.0:
                alive.append(p)
        s["particles"] = alive

        if elapsed >= 1200 and not s["particles"]:
            self.current_loaded_move = None
            return True
        return False
    
    def anim_sleep_powder(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation()
        now = pygame.time.get_ticks()

        screen.blit(opponent_sprite, opponent_rect)

        if now - s["spawn_timer"] >= 70:
            s["spawn_timer"] = now
            for _ in range(random.randint(2, 4)):
                s["particles"].append({
                    "x": float(opponent_rect.centerx + random.randint(-30, 30)),
                    "y": float(opponent_rect.top + random.randint(-10, 10)),
                    "speed_y": random.uniform(1.5, 3.5),
                    "speed_x": random.uniform(-1.0, 1.0),
                    "size": random.randint(4, 9),
                    "alpha": 255,
                })

        alive = []
        for p in s["particles"]:
            p["y"] += p["speed_y"]
            p["x"] += p["speed_x"]
            p["alpha"] = max(0, p["alpha"] - 3)
            surf = pygame.Surface((p["size"] * 2, p["size"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (50, 220, 50, p["alpha"]), (p["size"], p["size"]), p["size"])
            screen.blit(surf, (int(p["x"]) - p["size"], int(p["y"]) - p["size"]))
            if p["alpha"] > 0 and p["y"] < opponent_rect.bottom + 30:
                alive.append(p)
        s["particles"] = alive

        if elapsed >= 2000:
            self.current_loaded_move = None
            return True
        return False
    

    def anim_ice_beam(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)
        now = pygame.time.get_ticks()

        BEAM_END = 800
        ICE_END  = 1400

        # phase 1: draw the beam from my pokemon to opponent
        if elapsed < BEAM_END:
            screen.blit(opponent_sprite, opponent_rect)

            if now - s["spawn_timer"] >= 20:
                s["spawn_timer"] = now
                for _ in range(random.randint(2, 4)):
                    s["particles"].append({
                        "t": 0.0,
                        "speed": random.uniform(0.015, 0.025),
                        "dx": random.randint(-8, 8),
                        "dy": random.randint(-8, 8),
                        "size": random.randint(3, 7),
                    })

            sx, sy = my_rect.centerx, my_rect.centery
            ex, ey = opponent_rect.centerx, opponent_rect.centery

            alive = []
            for p in s["particles"]:
                p["t"] = min(1.0, p["t"] + p["speed"])
                x = int(sx + (ex - sx) * p["t"] + p["dx"])
                y = int(sy + (ey - sy) * p["t"] + p["dy"])
                x0 = int(sx + (ex - sx) * max(0, p["t"] - 0.05) + p["dx"])
                y0 = int(sy + (ey - sy) * max(0, p["t"] - 0.05) + p["dy"])
                color = random.choice([(180, 230, 255), (140, 210, 255), (255, 255, 255), (100, 180, 255)])
                pygame.draw.line(screen, color, (x0, y0), (x, y), p["size"])
                if p["t"] < 1.0:
                    alive.append(p)
            s["particles"] = alive

            # core beam line
            pygame.draw.line(screen, (200, 240, 255), (sx, sy), (ex, ey), 4 + random.randint(-1, 1))
            pygame.draw.line(screen, (255, 255, 255), (sx, sy), (ex, ey), 2)

            return False

        # phase 2: show ice particle image around opponent
        elif elapsed < ICE_END:
            screen.blit(opponent_sprite, opponent_rect)
            positions = [
                (opponent_rect.left - 10,  opponent_rect.top - 2),
                (opponent_rect.right - 5, opponent_rect.top - 5),
                (opponent_rect.left - 7,  opponent_rect.bottom - 13),
                (opponent_rect.right - 6, opponent_rect.bottom - 10),
                (opponent_rect.centerx - 14, opponent_rect.top - 18),
            ]
            for pos in positions:
                screen.blit(s["img"], pos)
            return False

        # phase 3: flash
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
                s["particles"] = []
            return done
        

    def anim_status_sleep(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation()
        now = pygame.time.get_ticks()

        if not s["sound_played"]:
            s["sound"].play()
            s["sound_played"] = True

        screen.blit(opponent_sprite, opponent_rect)

        font = pygame.font.Font('pokemon_pixel_font.ttf', 35)

        if now - s["spawn_timer"] >= 400:
            s["spawn_timer"] = now
            s["particles"].append({
                "x": float(opponent_rect.centerx + random.randint(-10, 10)),
                "y": float(opponent_rect.top),
                "speed_x": random.uniform(-0.8, 0.8),
                "speed_y": random.uniform(-1.5, -0.8),
                "alpha": 255,
                "size": random.randint(18, 28),
            })

        alive = []
        for p in s["particles"]:
            p["x"] += p["speed_x"]
            p["y"] += p["speed_y"]
            p["alpha"] = max(0, p["alpha"] - 2)
            surf = font.render("Z", True, (48,50,52))
            surf = pygame.transform.scale(surf, (p["size"], p["size"]))
            surf.set_alpha(p["alpha"])
            screen.blit(surf, (int(p["x"]), int(p["y"])))
            if p["alpha"] > 0:
                alive.append(p)
        s["particles"] = alive

        if elapsed >= 2500:
            s["sound_played"] = False
            self.current_loaded_move = None
            return True
        return False
    
    def anim_surf(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        RISE_END = 1200

        if elapsed < RISE_END:
            # move wave up from bottom of screen to top
            progress = elapsed / RISE_END  # 0.0 -> 1.0
            wave_y = int(300 - progress * 560)  # 520 down to -40

            # draw multiple sine-wave lines to make a wave shape
            for row in range(30):
                y = wave_y + row
                points = []
                for x in range(0, 801, 4):
                    offset = int(12 * math.sin((x / 60) + (elapsed / 120)))
                    points.append((x, y + offset + row * 2))
                if len(points) >= 2:
                    alpha = min(220, row * 10)
                    color = (
                        int(30 + (1 - progress) * 40),
                        int(100 + (1 - progress) * 60),
                        int(200 + (1 - progress) * 55)
                    )
                    pygame.draw.lines(screen, color, False, points, 2)

            screen.blit(opponent_sprite, opponent_rect)
            return False

        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        

    def anim_amnesia(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        if elapsed < 1500:
            screen.blit(my_sprite, my_rect)

            font = pygame.font.Font('pokemon_pixel_font.ttf', 80)
            question = font.render("?", True, (180, 100, 255))

            swing = math.sin(elapsed / 100) * 20
            scale = 1.0 + 0.1 * math.sin(elapsed / 150)
            scaled = pygame.transform.rotozoom(question, swing, scale)

            rect = scaled.get_rect(center=(my_rect.centerx, my_rect.top - 20))
            screen.blit(scaled, rect)
            return False

        else:
            self.current_loaded_move = None
            return True
        

    def anim_screech(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        start_x, start_y = my_rect.centerx, my_rect.centery
        end_x, end_y = opponent_rect.centerx, opponent_rect.centery

        if elapsed < 600:
            progress = elapsed / 600
            x = int(start_x + (end_x - start_x) * progress)
            y = int(start_y + (end_y - start_y) * progress)
            img_rect = s["img"].get_rect(center=(x, y))
            screen.blit(s["img"], img_rect)
            return False
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        
    def anim_psybeam(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)
        now = pygame.time.get_ticks()

        BEAM_DURATION = 700

        if elapsed < BEAM_DURATION:
            screen.blit(opponent_sprite, opponent_rect)

            # spawn new particles along the beam
            if now - s["spawn_timer"] >= 15:
                s["spawn_timer"] = now
                s["particles"].append({
                    "t": 0.0,
                    "speed": random.uniform(0.05, 0.08),
                    "phase": random.uniform(0, math.pi * 2),
                    "color": random.choice([(255, 100, 220), (180, 80, 255), (255, 150, 240)])
                })

            start_x, start_y = my_rect.centerx, my_rect.centery
            end_x, end_y = opponent_rect.centerx, opponent_rect.centery

            # find the perpendicular direction so the particles can wobble side to side
            dx = end_x - start_x
            dy = end_y - start_y
            length = math.hypot(dx, dy)
            if length == 0:
                length = 1
            perp_x = -dy / length
            perp_y = dx / length

            # update and draw every particle currently alive
            alive = []
            for p in s["particles"]:
                p["t"] = min(1.0, p["t"] + p["speed"])
                base_x = start_x + dx * p["t"]
                base_y = start_y + dy * p["t"]
                wobble = math.sin(p["t"] * math.pi * 4 + p["phase"]) * 12
                x = int(base_x + perp_x * wobble)
                y = int(base_y + perp_y * wobble)
                pygame.draw.circle(screen, p["color"], (x, y), 5)
                if p["t"] < 1.0:
                    alive.append(p)
            s["particles"] = alive

            return False

        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
                s["particles"] = []
            return done
        

    def anim_harden(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        screen.blit(my_sprite, my_rect)

        if elapsed < 800:
            progress = elapsed / 800
            flash_alpha = int(160 * abs(math.sin(progress * math.pi * 3)))

            tinted = my_sprite.copy()
            overlay = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
            overlay.fill((200, 200, 200, flash_alpha))
            tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

            screen.blit(tinted, my_rect)
            return False
        else:
            self.current_loaded_move = None
            return True
        

    def anim_glare(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)
        now = pygame.time.get_ticks()

        SPARK_END = 700
        TINT_END  = 1300

        eye_x = opponent_rect.centerx
        eye_y = opponent_rect.centery - int(opponent_rect.height * 0.15)

        # phase 1: spark at opponent's eyes
        if elapsed < SPARK_END:
            screen.blit(opponent_sprite, opponent_rect)

            if now - s["spawn_timer"] >= 40:
                s["spawn_timer"] = now
                for _ in range(2):
                    s["particles"].append({
                        "x": eye_x + random.randint(-10, 10),
                        "y": eye_y + random.randint(-6, 6),
                        "life": 200
                    })

            alive = []
            for p in s["particles"]:
                p["life"] -= 16
                if p["life"] > 0:
                    jitter_x = p["x"] + random.randint(-5, 5)
                    jitter_y = p["y"] + random.randint(-5, 5)
                    pygame.draw.line(screen, (255, 255, 100), (p["x"], p["y"]), (jitter_x, jitter_y), 2)
                    alive.append(p)
            s["particles"] = alive
            return False

        # phase 2: opponent tinted
        if elapsed < TINT_END:
            tinted = opponent_sprite.copy()
            overlay = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
            overlay.fill((255, 230, 50, 100))
            tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(tinted, opponent_rect)
            return False

        self.current_loaded_move = None
        s["start"] = None
        s["particles"] = []
        return True
    
    def anim_acid(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)
        now = pygame.time.get_ticks()

        SPRAY_END = 900

        if elapsed < SPRAY_END:
            screen.blit(opponent_sprite, opponent_rect)

            if now - s["spawn_timer"] >= 60:
                s["spawn_timer"] = now
                s["particles"].append({
                    "x": float(my_rect.centerx + random.randint(-15, 15)),
                    "y": float(my_rect.centery + random.randint(-15, 15)),
                    "tx": opponent_rect.centerx + random.randint(-25, 25),
                    "ty": opponent_rect.centery + random.randint(-25, 25),
                    "progress": 0.0,
                    "speed": random.uniform(0.02, 0.035)
                })

            alive = []
            for p in s["particles"]:
                p["progress"] = min(1.0, p["progress"] + p["speed"])
                x = int(p["x"] + (p["tx"] - p["x"]) * p["progress"])
                y = int(p["y"] + (p["ty"] - p["y"]) * p["progress"])
                img_rect = s["img"].get_rect(center=(x, y))
                screen.blit(s["img"], img_rect)
                if p["progress"] < 1.0:
                    alive.append(p)
            s["particles"] = alive
            return False

        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
                s["particles"] = []
            return done
        
    def anim_psychic(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        RING_END = 900

        if elapsed < RING_END:
            screen.blit(opponent_sprite, opponent_rect)

            progress = elapsed / RING_END
            num_rings = 4
            for i in range(num_rings):
                ring_progress = (progress - i * 0.15) % 1.0
                if ring_progress <= 0:
                    continue
                radius = int(80 * (1.0 - ring_progress))
                alpha = int(255 * ring_progress)
                ring_color = (200, 50, 200)

                ring_surface = pygame.Surface((radius*2+4, radius*2+4), pygame.SRCALPHA)
                pygame.draw.circle(ring_surface, (*ring_color, alpha), (radius+2, radius+2), radius, 6)
                ring_rect = ring_surface.get_rect(center=opponent_rect.center)
                screen.blit(ring_surface, ring_rect)
            return False

        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        
    def anim_fire_spin(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        SPIN_END = 1200

        if elapsed < SPIN_END:
            screen.blit(opponent_sprite, opponent_rect)

            progress = elapsed / SPIN_END
            num_particles = 6
            radius = int(80 * (1.0 - progress * 0.5))  # tightens as it spins
            angle_offset = elapsed * 0.6  # spin speed

            for i in range(num_particles):
                angle = angle_offset + (i * 360 / num_particles)
                vec = pygame.math.Vector2(radius, 0).rotate(angle)
                cx = opponent_rect.centerx + int(vec.x)
                cy = opponent_rect.centery + int(vec.y * 0.6)  # flatten vertically for a spin look
                img_rect = s["img"].get_rect(center=(cx, cy))
                screen.blit(s["img"], img_rect)
            return False

        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        

    def anim_wrap(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        FRAME_TIME = 200  # ms per frame
        WRAP_END = FRAME_TIME * len(s["frames"])  # 800ms total

        if elapsed < WRAP_END:
            screen.blit(opponent_sprite, opponent_rect)

            frame_index = min(int(elapsed / FRAME_TIME), len(s["frames"]) - 1)
            img_rect = s["frames"][frame_index].get_rect(center=opponent_rect.center)
            screen.blit(s["frames"][frame_index], img_rect)
            return False

        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        
    def anim_leech_seed(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        THROW_END   = 500
        SPROUT1_END = 800
        SPROUT2_END = 1100

        start_x, start_y = my_rect.centerx, my_rect.centery
        end_x, end_y = opponent_rect.centerx, opponent_rect.bottom - 10

        screen.blit(opponent_sprite, opponent_rect)

        if elapsed < THROW_END:
            progress = elapsed / THROW_END
            x = int(start_x + (end_x - start_x) * progress)
            y = int(start_y + (end_y - start_y) * progress)
            img_rect = s["seed"].get_rect(center=(x, y))
            screen.blit(s["seed"], img_rect)
            return False

        elif elapsed < SPROUT1_END:
            img_rect = s["sprouts"][0].get_rect(midbottom=(end_x, end_y + 10))
            screen.blit(s["sprouts"][0], img_rect)
            return False

        elif elapsed < SPROUT2_END:
            img_rect = s["sprouts"][1].get_rect(midbottom=(end_x, end_y + 10))
            screen.blit(s["sprouts"][1], img_rect)
            return False

        else:
            self.current_loaded_move = None
            s["start"] = None
            return True
        

    def anim_dig(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        TRAVEL_DURATION = 1000
        ERUPTION_DURATION = 800

        
        if elapsed < TRAVEL_DURATION + ERUPTION_DURATION:
            screen.blit(opponent_sprite, opponent_rect)

        #TRAVEL PHASE
        if elapsed < TRAVEL_DURATION:
            progress = elapsed / TRAVEL_DURATION
            start_x, start_y = my_rect.centerx, my_rect.bottom - 10
            end_x, end_y = opponent_rect.centerx, opponent_rect.bottom - 10
            
            # Interpolate coordinates along the screen ground coordinate line
            current_x = int(start_x + (end_x - start_x) * progress)
            current_y = int(start_y + (end_y - start_y) * progress)

            # Main traveling dirt mound layers
            pygame.draw.ellipse(screen, (101, 67, 33), (current_x - 35, current_y - 15, 70, 30))
            pygame.draw.ellipse(screen, (139, 69, 19), (current_x - 22, current_y - 18, 44, 24))

            # Flicker minor dirt debris elements near the moving mound
            random.seed(elapsed // 40)
            for _ in range(6):
                offset_x = random.randint(-18, 18)
                offset_y = random.randint(-12, 6)
                size = random.randint(3, 6)
                pygame.draw.circle(screen, (80, 50, 20), (current_x + offset_x, current_y + offset_y), size)

            return False

        # ERRUPTION PHASE
        elif elapsed < TRAVEL_DURATION + ERUPTION_DURATION:
            eruption_elapsed = elapsed - TRAVEL_DURATION
            progress = eruption_elapsed / ERUPTION_DURATION
            
            base_x = opponent_rect.centerx
            base_y = opponent_rect.bottom - 10

            # Growing shockwave ring on the floor base
            ring_radius = int(progress * 60)
            if ring_radius > 5:
                pygame.draw.ellipse(screen, (139, 69, 19), (base_x - ring_radius, base_y - int(ring_radius / 2), ring_radius * 2, ring_radius), 2)

            # Erupting dirt debris elements shooting upward (deterministic seed)
            random.seed(42)
            for i in range(14):
                angle = random.uniform(math.pi, 2 * math.pi)  # Upward semicircle arc arc
                speed = random.uniform(120, 280)
                dist = speed * progress
                
                # Apply gravity effect pulling particles back down over time
                gravity = 250 * (progress ** 2)
                
                px = int(base_x + math.cos(angle) * dist)
                py = int(base_y + math.sin(angle) * dist + gravity)
                
                size = random.randint(4, 11)
                color = random.choice([(101, 67, 33), (139, 69, 19), (80, 50, 20)])
                pygame.draw.circle(screen, color, (px, py), size)

            return False

       # FLASH
        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done
        

    def anim_fly(self, move_name, screen, opponent_sprite, opponent_rect, my_sprite, my_rect):
        s = self.state
        elapsed = self._start_animation(True)

        DESCENT_DURATION = 500

        if elapsed < DESCENT_DURATION:
            screen.blit(opponent_sprite, opponent_rect)

        # ------------------------------------------------------------------ #
        #  1. DESCENT PHASE: Dive bomb from the top onto the opponent        #
        # ------------------------------------------------------------------ #
        if elapsed < DESCENT_DURATION:
            progress = elapsed / DESCENT_DURATION

            # Ground shadow grows rapidly beneath the opponent target
            shadow_w = int(opponent_rect.width * (progress * 1.3))
            shadow_h = int(14 * (progress * 1.3))
            pygame.draw.ellipse(screen, (20, 20, 20), (opponent_rect.centerx - shadow_w//2, opponent_rect.bottom - 6, shadow_w, shadow_h))

            # Dive straight down onto opponent coordinates
            start_y = -50
            end_y = opponent_rect.centery
            current_y = int(start_y + (end_y - start_y) * progress)

            # Wind streaks
            random.seed(elapsed // 30)
            for _ in range(4):
                line_x = opponent_rect.centerx + random.randint(-30, 30)
                line_y = current_y + random.randint(-40, 10)
                length = random.randint(20, 50)
                pygame.draw.line(screen, (240, 240, 255), (line_x, line_y), (line_x, line_y + length), 2)

            # Draw attacking dark blue circle silhouette
            pygame.draw.circle(screen, (16, 44, 87), (opponent_rect.centerx, current_y), 24)
            return False

        else:
            done = self._flash_phase(screen, opponent_sprite, opponent_rect)
            if done:
                s["start"] = None
            return done