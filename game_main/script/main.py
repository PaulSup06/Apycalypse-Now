import pygame
import pygame.mixer
import pygame_menu
import pygame_menu.menu
import pygame_menu.widgets
import pygame_menu.themes
from settings import *
from level import Level
from debug import debug
from player import Player
from enemy import Enemy
from ui import *
from inventaire import Inventaire
from datetime import datetime
import sys
import os
import csv
import json

class Game:
    def __init__(self):
        """initialisation générale
        """
        #setup working directory
        os.chdir(os.path.realpath(__file__)[:-7])
        
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.SCALED | pygame.FULLSCREEN)  #initialisation système vidéo pygame      ,pygame.SCALED | pygame.FULLSCREEN
        pygame.display.set_caption(GAME_TITLE) #ajouter titre du jeu ici
        pygame.display.set_icon(pygame.image.load("..\\textures\\test\\rock.png")) #TODO rajouter une petite icone sympa
        self.clock = pygame.time.Clock() #initialisation système de comptage de temps (fps cap) de pygame
        
        #initialisation système audio
        pygame.mixer.init()
        pygame.mixer.set_num_channels(999) # pour pouvoir jouer différent son en simultané 
        self.music_playing=None
        
        self.running = True

        #initialisation de la gestion modifs dynamiques des touches
        self.waiting_for_key = False
        self.editing_key = None
        self.editing_button = None
          
        #génération des interfaces
        self.game_state = "menu"
        self.inventaire = Inventaire(self)  
        self.ui = UI(self)  
        self.menu_pg_pygame = pygame.transform.scale(pygame.image.load("..\\textures\\ui\\menu_bg.png"), (WIDTH,HEIGHT)).convert()
        self.menu_pg_pymenu = pygame_menu.baseimage.BaseImage(
        image_path="..\\textures\\ui\\menu_bg.png",
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
        )
        
        #initialisation des variables se conservant d'un niveau à un autre
        self.settings = get_actual_settings() #décodage du fichier CSV de paramètres du jeu
        self.npc_states = {}
        self.current_life = self.max_life = default_player_life
        self.changing_world = False
        self.player_weapon_name = None
        self.is_in_a_note = False

        # debug
        self.debug_text_showing = False

        self.generate_menus()           

    def generate_menus(self):
        #menus
        self.menu_state = 'main'

        #gestion des thèmes (à déplacer ??)
        theme_main_screen = pygame_menu.themes.THEME_ORANGE.copy()
        theme_main_screen.background_color = self.menu_pg_pymenu
        theme_main_screen.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE
        theme_main_screen.title = False
        theme_main_screen.widget_font_size  = 50
        theme_main_screen.widget_margin = (20,20)

        theme_settings = pygame_menu.themes.THEME_DARK.copy()
        theme_settings.title = True
        theme_settings.widget_font_size  = 30
        theme_settings.widget_font_color = "white"
        theme_settings.widget_margin =  (15,15)
        theme_settings.background_color = (54,79,89,255)
        theme_settings.widget_alignment = pygame_menu.locals.ALIGN_CENTER
        theme_sauvegarde = pygame_menu.themes.THEME_ORANGE.copy()

        self.main_menu = pygame_menu.menu.Menu(GAME_TITLE, WIDTH, HEIGHT, True, theme=theme_main_screen)
        self.settings_menu = pygame_menu.menu.Menu("Paramètres",WIDTH,HEIGHT,True, columns=4, rows=8, theme = theme_settings)
        self.saves_menu = pygame_menu.menu.Menu("Sauvegardes",WIDTH,HEIGHT,True, theme=theme_sauvegarde)
        self.escape_menu = pygame_menu.menu.Menu("Jeu en pause",WIDTH,HEIGHT,True,theme=theme_main_screen)
        
        #menu principal
        #TODO: trouver comment changer la couleur de selection des boutons
        self.main_menu.add.button("Nouvelle partie", self.create_new_game)
        self.main_menu.add.button("Sauvegardes",self.saves_menu)
        self.main_menu.add.button("Paramètres",self.settings_menu)
        self.main_menu.add.button("Quitter", self.quit_game)
        self.main_menu.center_content()
        
        #menu paramètres
        
        #affichage nom des touches 
        for name in settings_fields[:8]:
            self.settings_menu.add.label(settings_name[name])
        #affichage des boutons modif de touches + slider volume en fonction des paramètres enregistrés
        for key, value in self.settings.items():
            if key[0]=="k":
                self.settings_menu.add.button(pygame.key.name(int(value)).upper(),self.listen_to_key,key, button_id=key).add_self_to_kwargs()
            elif key == "volume":
                self.settings_menu.add.range_slider("Volume de la musique : ", int(float(self.settings["volume"])), (0,100),increment=1,rangeslider_id="volume_slider")
                
        self.settings_menu.add.button("Réinitialiser les paramètres",self.reset_settings)
        
        #menu de sauvegardes
        for file in os.listdir("..\\saves\\"):
            if file[-4:] == "json": #Vérifie que le fichier est du bon type 
                row = self.saves_menu.add.frame_h(WIDTH,100,padding=30)
                row._relax = True
                row_label = self.saves_menu.add.label("Sauvegarde du : "+file[:-5],label_id=file+"0")
                row_button1 = self.saves_menu.add.button("Charger",self.load_sauvegarde,file,button_id=file+"1")
                row_button2 = self.saves_menu.add.button("Supprimer",self.delete_sauvegarde,file,button_id=file+"2")
                row.pack(row_label)
                row.pack(row_button1)
                row.pack(row_button2)
                
            else:
                raise Exception("Erreur, fichier sauvegarde corrompu : ",file)
            
        #menu de pause
        self.escape_menu.add.button("Reprendre la partie",self.reprendre_partie)
        self.escape_menu.add.button("Paramètres",self.settings_menu)
        self.escape_menu.add.button("Sauvegarder et quitter",self.save_and_quit,(True))
        self.escape_menu.add.button("Quitter sans sauvegarder",self.save_and_quit,(False))
        self.escape_menu.disable()

        #boutons de fin de partie
        self.death_buttons = [
        Button(WIDTH//2 - 200,HEIGHT//5*2 -50, 400, 100, font1, "Menu principal",self.to_main_menu,True),
        Button(WIDTH//2 - 200,HEIGHT//5*3 -50, 400, 100, font1, "Continuer la partie",self.continue_game,True),
        Button(WIDTH//2 - 200,HEIGHT//5*4 -50, 400, 100, font1, "Recommencer",self.retry,True),
        ]

    def run(self):
        """Boucle de code principale
        """
        while self.running:
            self.screen.fill((0,0,0))

            #EVENT HANDLER PYGAME
            #========================================================================================
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    #TODO éventuellement sauvegarder ici
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if self.is_in_a_note:
                        self.is_in_a_note = False
                    elif self.game_state == "playing":
                        
                        if event.key == int(self.settings["k_attack"]): #TODO ajouter touches dynamiques
                            if not self.ui.current_dialog and not self.inventaire.enabled:
                                self.player.attack(self.level.enemies)
                            elif self.inventaire.enabled:
                                self.inventaire.drop(self.player,self.level.items)
                        elif event.key == int(self.settings["k_interact"]):
                            if self.inventaire.enabled:
                                self.inventaire.use()
                            else:
                                for npc in self.level.npcs:
                                    if npc.check_distance_to((self.player.x,self.player.y),interact_distance):
                                        if not self.ui.current_dialog:
                                            self.ui.load_dialog(*npc.interact())
                                        elif self.ui.ongoing_dialog:
                                            self.ui.finish_dialog()
                                        else:
                                            fin_dialogue = self.ui.quit_dialog(npc.name)
                                            self.update_dialog_ended(fin_dialogue, npc.name)
                                            #handle dialogue ended (fin dialog = dict)
                                            
                                                
                                for terminal in self.level.terminals:
                                    if self.player.check_distance_to(terminal.surface.midbottom,interact_distance) and not terminal.locked and not terminal.using:
                                        renvoi_terminal = terminal.interact()
                                        if renvoi_terminal[0]:
                                            for door in self.level.doors:
                                                if door.id == renvoi_terminal[1]:
                                                    door.unlock()
                                for switch in self.level.switches:
                                    if switch.name == "lever" or switch.name == "manivelle" :
                                        if switch.player_near:
                                            methode_to_call = switch.interact()
                                            if methode_to_call != None:
                                                if methode_to_call == "remove_manivelle_from_player_inventory":
                                                    self.inventaire.remove_item("manivelle")
                                                else:
                                                    methode = getattr(self, methode_to_call)
                                                    methode(switch.action) # action ="left" ou "right"

                        elif event.key == int(self.settings["k_escape"]):
                            self.game_state = "menu"
                            self.escape_menu.enable()
                        
                        elif event.key == int(self.settings["k_inventory"]):
                            #change l'état de l'inventaire
                            self.inventaire.enabled = self.inventaire.enabled == False

                        if self.inventaire.enabled:
                            self.inventaire.move_cursor(event.key,self.settings)

                    if event.key == pygame.K_f: #temporaire pour tests
                        self.play_music("4.wav")
                    if event.key == pygame.K_g: #temporaire pour tests
                        self.play_music("5.wav")
                    if event.key == pygame.K_h: #temporaire pour tests
                        self.play_music("6.wav")
                    if event.key == pygame.K_j: #temporaire pour tests
                        self.play_music("7.wav")
                    if event.key == pygame.K_k: #temporaire pour tests
                        self.play_music("8.wav")
                    elif event.key == pygame.K_y: #temporaire pour tests
                        self.change_level(2)
                    elif event.key==pygame.K_u:
                        self.inventaire.add_item("strength_potion",2)
                        self.inventaire.add_item("note#1", 1)
                        self.inventaire.add_item("invincibility_potion",4)
                        self.inventaire.add_item("manivelle",1)
                        self.inventaire.add_item("speed_potion", 2)

                    elif self.waiting_for_key:
                        self.edit_key(event.key)
                        
                elif event.type==pygame.USEREVENT:
                    #musique fadout terminé 
                    pygame.mixer.music.load(os.path.join(music_folder,self.music_playing))
                    pygame.mixer.music.play(-1)
                #========================================================================================    
                         
            #BOUCLE PRINCIPALE LORS DU JEU        
            if self.game_state == "playing" or self.is_in_a_note:
                if not self.ui.current_dialog and not self.inventaire.enabled:
                    self.player.move(pygame.key.get_pressed(),self.settings)
                self.player.update()
                for enemy in self.level.enemies:
                    damages = enemy.move(self.player)
                    if damages:
                        # un ennemi fait des dégâts au joueur
                        if self.player.invincibility == False:
                            self.player.life -= damages
                            if self.player.life<=0:
                                self.game_state="death"
                for spike in self.level.spikes:
                    damages = spike.check_trigger(self.player)
                    if damages:
                        # un ennemi fait des dégâts au joueur
                        if self.player.invincibility == False:
                            self.player.life -= damages
                            if self.player.life<=0:
                                self.game_state="death"

                self.level.visible_blocks.draw_visible(self.player, self.level.npcs,self.level.enemies, self.level.world_tmx, self.settings)

                for door in self.level.doors:
                    door.update(self.player)
                for term in self.level.terminals:
                    term.handle(self.player, self.screen, self.level.visible_blocks.offset,self.settings)
                for trigger in self.level.trigger_blocks:
                    trigger.handle(self.player, self)
                for switch in self.level.switches:
                    switch.handle(self.player, self.screen, self.level.visible_blocks.offset,self.settings, self.inventaire.have_item("manivelle"))
                    switch.animate()
                for item in self.level.items:
                    if item.handle(self.player, self.level.visible_blocks.offset):
                        self.inventaire.add_item(item.name, item.amount)
                    if item.stack(self.level.items):
                        self.level.items.remove(item)
                if self.inventaire.enabled:
                    self.inventaire.draw_inventory(self.screen, self.settings)
                    
                #hitbox pour débug
                if showing_hitbox:
                    for block in self.level.collision_blocks:
                        pygame.draw.rect(self.screen,'white',pygame.Rect(block.surface.x - self.level.visible_blocks.offset.x,block.surface.y - self.level.visible_blocks.offset.y, block.surface.width, block.surface.height),2)
                    pygame.draw.rect(self.screen,'white',pygame.Rect(self.player.surface.x - self.level.visible_blocks.offset.x,self.player.surface.y - self.level.visible_blocks.offset.y, self.player.surface.width, self.player.surface.height),2)
                    pygame.draw.rect(self.screen,'red',pygame.Rect(self.player.rect.x - self.level.visible_blocks.offset.x,self.player.rect.y - self.level.visible_blocks.offset.y, self.player.rect.width, self.player.rect.height),2)   
                
                # affiche la note par dessus l'écran
                if self.is_in_a_note:
                    self.screen.blit(self.note_img, self.note_rect)
            #UI
            #========================================================================================
                
                ui_return = self.ui.show_ui(self.player)
                if ui_return['npc_update']:
                    for npc in self.level.npcs:
                        if npc.name == self.ui.current_npc:
                            npc.change_state(*ui_return["npc_update"])

            elif self.game_state == "menu":
                
                if self.main_menu.is_enabled():
                    self.main_menu.draw(self.screen)
                    self.main_menu.update(events)
                    
                    slider_vol = self.settings_menu.get_widget("volume_slider").get_value()
                    if self.settings["volume"] != slider_vol:
                        self.change_music_volume(slider_vol)
                
                if self.escape_menu.is_enabled():
                    self.escape_menu.draw(self.screen)
                    self.escape_menu.update(events)
                    slider_vol = self.settings_menu.get_widget("volume_slider").get_value()
                    if self.settings["volume"] != slider_vol:
                        self.change_music_volume(slider_vol)
            
            elif self.game_state == "death":
                self.screen.blit(self.menu_pg_pygame, (0,0))
                game_over_surf = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
                game_over_title = title_font.render("GAME OVER",1,"white")
                game_over_surf.blit(game_over_title,((game_over_surf.get_width()-game_over_title.get_width())//2, 0))
                game_over_text = font1.render("Oh non ! Vous avez été tué ! Vous aurez plus de chance la prochaine fois !",1,"white")
                game_over_surf.blit(game_over_text,((game_over_surf.get_width()-game_over_text.get_width())//2, game_over_title.get_height() + 10))
                game_over_rect = game_over_surf.get_bounding_rect()
                self.screen.blit(game_over_surf, (WIDTH//2 - game_over_rect.width//2 -game_over_rect.x,HEIGHT//5 - game_over_rect.height//2 -game_over_rect.y))
                for button in self.death_buttons:
                    button.process()
                    self.screen.blit(button.image,(button.x,button.y))        

            #========================================================================================
            
            debug(("FPS : " + str(round(self.clock.get_fps(),1)),))

            # message debug
            if self.debug_text_showing:
                pygame.Surface.blit(self.screen, self.debug_text, ((WIDTH/2) - self.debug_text.get_width() / 2, HEIGHT - self.debug_text.get_height() - 10, self.debug_text_rect.width, self.debug_text_rect.height))
                self.debug_text_timer += 1
                if self.debug_text_timer >= FPS * 3:
                    self.debug_text_showing = False
            
            #Update de l'écran et gestion tickrate
            pygame.display.update()
            self.clock.tick(FPS)

    #=====================================================================
    #GESTION DES SAUVEGARDES
    #====================================================================== 
    def sauvegarde(self,file_name="latest.json"):
        """Créé une sauvegarde de la position du joueur sur la carte

        Args:
            file_name (str, optional): Path au fichier dans lequel sera enregistré la position. Defaults to "latest.json".
        """

        pos = {"x":self.player.x,
               "y":self.player.y,
               "life":self.player.life,
               "max_life":self.player.max_life,
               "level":self.level.world_id,
               "weapon":self.player.weapon,
               "inventory":self.inventaire.inventory,
               "npcs":self.npc_states}
        
        file_path = os.path.join("..\\","saves",file_name)
        with open(file_path,'w') as file:
            json.dump(pos, file)

    def load_sauvegarde(self, save_name):
        """Charge une sauvegarde du jeu 
        (même fonction que generate_game mais envoie des paramètres customs)

        Args:
            save_name (str): nom du fichier save à ouvrir
        """
        #gestion du fichier json
        file_path = os.path.join("..\\","saves",save_name)
        with open(file_path,"r") as f:
            params = json.load(f)

        #génération du monde
        self.game_state = "playing"
        self.main_menu.disable()
        
        self.current_life = params["life"]
        self.max_life = params["max_life"]
        
        self.level = Level(self, self.current_life,self.max_life, params["level"],False)

        self.npc_states = params["npcs"]

        self.player = Player(params["x"],params["y"],(self.level.visible_blocks),
                             self.level.collision_blocks,params["life"], params["max_life"],params["weapon"])  
        
        self.level.player = self.player
        self.inventaire = Inventaire(self, params["inventory"])
        self.ui.add_transition_open()
        
    def delete_sauvegarde(self, save_name):
        """Supprime une des sauvegarde

        Args:
            save_name (str): nom de la save à supprimer

        Returns:
            bool: True si la save a bien été supprimée, False si elle n'existe pas
        """
        file_path = os.path.join("..\\","saves",save_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            for i in range(3):
                self.saves_menu.remove_widget(save_name+str(i))
            return True
        else:
            return False


    #=====================================================================
    #FONCTIONS LIEES AUX MENUS ET TRIGGERS
    #======================================================================
    def generate_world(self, current_world=None,pos=None):
        """

        Args:
            current_world (int): Monde à générer
        """
        if pos:
            if type(pos)==tuple:
                if len(pos)==2:
                    try:
                        pos = int(pos[0]), int(pos[1])
                    except Exception as e:
                        print(e,"Mauvaise position donnée... Changement de monde impossible")
                        
        #rend le paramètre optionnel en utilisant la valeur de la classe Game
        self.ui = UI(self)   #reset l'ui lors du chargement (fix bug ui ouvert lors de fermeture d'une précédente page)
        self.changing_world = False 

        if not current_world:
            current_world = self.current_world
            
        self.level = Level(self, self.current_life,self.max_life ,current_world,True)
        self.player = self.level.player
        self.player.weapon = self.player_weapon_name
        
        if pos:
            self.player.x = pos[0]
            self.player.y = pos[1]
        if self.npc_states.get(current_world):
            
            for npc in self.level.npcs:
                npc_status = self.npc_states.get(current_world).get(npc.name)
                if npc_status:
                    npc.change_state(*npc_status)

        
        self.ui.add_transition_open()
    
    def create_new_game(self):
        """Génère le monde lors du premier chargement (nouvelle partie)
        """
        self.game_state = "playing"
        self.main_menu.disable()
        self.inventaire = Inventaire(self)
        #génération du monde
        self.current_world = 1
        self.generate_world(self.current_world)
        self.current_life = self.max_life = default_player_life
            
    def change_level(self, level,pos=None):
        """Change le monde lors d'un changement de niveau + transition

        Args:
            level (int): niveau de destination
        """
        if not self.changing_world:
            self.changing_world = True
            self.save_npc_states(self.current_world)
            self.current_world = level
            self.current_life, self.max_life = self.player.life, self.player.max_life
            self.ui.add_transition_close(self.generate_world,level,pos)

    def reprendre_partie(self):
        """Fonction liée au bouton "reprendre la partie" du menu de pause
        """
        self.escape_menu.disable()
        self.game_state = "playing"
    
    def save_npc_states(self,world):
        """Enregistre les états des pnjs actifs sur le monde quitté par le joueur (et rechargés s'il revient)

        Args:
            world (int): id du monde quitté par le joueur
        """
        for npc in self.level.npcs:
            if not self.npc_states.get(world):
                self.npc_states[world] = {}
            self.npc_states[world][npc.name]=npc.get_state() 
        
    def save_and_quit(self,save=True, name=None):
        """Fonction liée au bouton "Sauvegarder et quitter" du menu de pause

        Args:
            name (str): nom du fichier sauvegarde à générer
        """
        if not name:
            date = datetime.now()
            name = date.strftime("%d %m %Y %Hh %M.json")
        if save:
            self.sauvegarde(name)
        self.escape_menu.disable()
        self.generate_menus()
        self.main_menu.enable()

    def quit_game(self):
        """Fonction liée au bouton "Quitter" du menu principal 
        (peut être appelée aussi in game si besoin)
        """
        self.running = False

    def listen_to_key(self, key, **kwargs):
        """Active le mode détection de touche du jeu : 
        la prochaine touche reçue est prise en compte par les paramètres

        Args:
            key (int): id touche pygame à modifier
            *kwargs['widget'] : bouton correspondant à modifier pendant l'edit de touche
        """
        self.waiting_for_key = True
        self.editing_key = key
        self.editing_button = kwargs['widget']
        self.editing_button.set_title("[Appuyez sur une touche]")

    def edit_key(self,key_pressed):
        """Change de manière définitive la touche une fois celle-ci reçue
        modification du fichier paramètres csv

        Args:
            key_pressed (int): id touche pygame reçue 
        """
        self.waiting_for_key = False
        
            
        self.settings[self.editing_key] = key_pressed
        self.editing_button.set_title(pygame.key.name(key_pressed).upper())
        with open(settings_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=settings_fields)
            writer.writeheader()
            writer.writerow(self.settings)
            
    def reset_settings(self):
        """Réinitialise les paramètres (copie le fichier default_settings dans settings)
        """
        with open(default_settings_path) as f:
            default_settings = f.read()
            with open(settings_path,"w") as s:
                s.write(default_settings)
        self.settings = get_actual_settings()
        self.generate_menus()
                    
    #gestion de la musique
    def play_music(self,file_name):
        """Charge une musique dans le mixer pygame

        Args:
            file_name (str): nom de fichier de la musique à jouer (avec extension)
        """
        
        if file_name == self.music_playing: #musique déjà chargée 
            return False
        else:
            self.music_playing = file_name
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(os.path.join(music_folder,file_name)) 
                #possible de spécifier une extension mais cause problèmes sur anciennes versions de pygame
                pygame.mixer.music.play(-1) #argument -1 = musique en boucle à l'infini
            else:
                pygame.mixer.music.set_endevent(pygame.USEREVENT)
                pygame.mixer.music.fadeout(4000)
        
    def change_music_volume(self, volume):
        """Change le volume pygame de la musique

        Args:
            volume (int): Volume entre 1 et 100
        """
        assert 0<=volume<=100, "Le volume donné n'est pas correct"
        
        self.settings["volume"] = volume
        pygame.mixer.music.set_volume(round(volume/100,2))
        with open(settings_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=settings_fields)
            writer.writeheader()
            writer.writerow(self.settings)   
    
    def to_main_menu(self):
        """Retourne au menu principal (sans sauvegarde)
        """
        self.game_state = 'menu'
        self.main_menu.enable()         
    
    def retry(self):
        """Recommence la partie entièrement
        """
        self.create_new_game()

    def continue_game(self):
        """Fonction de "triche" qui permet de revivre après être mort
        """
        self.player.life = self.player.max_life
        self.current_life = self.max_life = self.player.max_life
        self.game_state = "playing"
    #=================================================================================      


    #=====================================================================
    #FONCTIONS LIEES AUX ITEMS DU JEU
    #=====================================================================
    def heal_player(self, amount=2):
        """Rajoute de la vie au joueur

        Args:
            amount (int, optional): Vie à ajouter. Par défaut 2 soit 1 coeur.

        Returns:
            bool: Capacité du joueur à être soigné
        """
        if self.player.life < self.player.max_life:
            self.player.life += amount #ajoute 1 coeur entier par défaut
            if self.player.life > self.player.max_life:
                self.player.life = self.player.max_life
            self.current_life = self.player.life
            return True
        else:
            return False
    
    def speed_player(self):
        """Multiplie la vitesse du joueur par un facteur

        Returns:
            bool: Capacité du joueur à recevoir l'effet
        """
        self.player.speed_multiplier = speed_potion_multiplier
        self.ui.speed_potion_timer = 0
        return True

        
    def strength_player(self):
        """Multiplie la force du joueur par un facteur

        Returns:
            bool: Capacité du joueur à recevoir l'effet
        """ 
        self.player.strength_multiplier = strength_potion_mutltiplier
        self.ui.strength_potion_timer = 0
        return True

        
    def invincibility_player(self):
        """Rend le joueur invicible pendant un certain temps

        Returns:
            bool: Capacité du joueur à recevoir l'effet
        """ 
        self.player.invincibility = True
        self.ui.invincibility_potion_timer = 0
        return True

        
    def read_note(self, note):
        """Ouvre un note

        Args:
            note (str): nom de la note

        Returns:
            bool: True si note consommée et détruite (toujours False sauf cas particulier)
        """

        self.note_img = pygame.image.load(os.path.join(items_folder,note+".png"))
        self.note_rect = self.note_img.get_rect()
        self.note_rect = pygame.Rect((WIDTH - self.note_rect.width)//2, (HEIGHT - self.note_rect.height)//2,self.note_rect.width, self.note_rect.height)
        self.is_in_a_note = True


        return False
    
    def add_player_heart(self,amount=2):
        """Ajoute de la vie à la vie max du joueur

        Args:
            amount (int, optional): Vie à ajouter. Defaults to 2 soit 1 coeur.
        """
        self.max_life += amount
        self.player.max_life = self.max_life

    #FONCTION D'UI    
    def update_dialog_ended(self,fin_dialogue, npc_name):
        """Fonction appelée à la fin d'un dialogue, peut modifier certaines variables du jeu

        Args:
            fin_dialogue (dict): dictionnaire des actions à effectuer à la fin du dialogue
            npc_name (str): nom du npc à l'origine de la requête
        """
        for npc in  self.level.npcs:
            if npc.name == npc_name:
                current_npc = npc
        if fin_dialogue.get("change_level"):
            self.change_level(fin_dialogue.get("change_level"))
        if fin_dialogue.get("npc_update"):
            current_npc.change_state(*fin_dialogue.get("npc_update"))
        item_dropped = fin_dialogue.get("add_item")
        if item_dropped:
            current_npc.drop_item(item_dropped[0],item_dropped[1],self.level.items)
            
    #=====================================================================
    #FONCTIONS LIEES AUX SWITCHES
    #=====================================================================

    def unlock_door(self, door_to_unlock, active=(), inactive=()):
        """Déverrouille une porte en fonction de la position de switchs donnés

        Args:
            door_to_unlock (str/int): id de la porte à déverrouiller
            active (tuple): id de tous les switchs requis en position "on"
            inactive (tuple): id de tous les switchs requis en position "off"

        Returns:
            bool: True si la porte a bien été ouverte, sinon false
        """
        door_to_unlock = int(door_to_unlock)
        opening = True
        for switch in self.level.switches:
            if switch.id in active and not switch.activated:
                opening = False                
            if switch.id in inactive and switch.activated:
                opening = False
            
        for door in self.level.doors:
            if door.id == door_to_unlock:
                if opening:
                    door.unlock()
                    return True
                else:
                    door.lock()
                    return False

    def unlock_terminal(self, term_to_unlock, active=(), inactive=()):
        """Déverrouille un terminal en fonction de la position de switchs donnés

        Args:
            door_to_unlock (str/int): id du terminal à déverrouiller
            active (tuple): id de tous les switchs requis en position "on"
            inactive (tuple): id de tous les switchs requis en position "off"

        Returns:
            bool: True si la porte a bien été ouverte, sinon false
        """
        
        term_to_unlock = int(term_to_unlock)
        opening = True
        for switch in self.level.switches:
            if switch.id in active and not switch.activated:
                opening = False                
            if switch.id in inactive and switch.activated:
                opening = False
            
        for term in self.level.terminals:
            if term.id == term_to_unlock:
                if opening:
                    term.unlock()
                    return True
                else:
                    term.lock()
                    return False
                
    def spawn_enemy(self,x,y,movement_type,name,speed,damages,health, movement_condition=True):
        """Fait apparaître un ennemi sur la map selon des paramètres donnés

        Args:
            paramètres de l'ennemi à passer via Tiled
        """
        #conversion des paramètres en int (passés en string via Tiled)
        x = int(x)
        y = int(y)
        speed = int(speed)
        damages = int(damages)
        health = int(health)
        Enemy(x,y,None, self.level.enemies,self.level.collision_blocks,self.level.items,self.level.enemy_imgs[name], movement_type,name,speed,damages,health,movement_condition)
    #=====================================================================
    #DEBUG
    #=====================================================================
    def debug_message(self, msg):
        self.debug_text = font2.render(msg, 1,"white")
        self.debug_text_rect = self.debug_text.get_rect()
        self.debug_text_timer = 0
        self.debug_text_showing = True

    def open_castle_door(self):
        pass
    
#===============================================================
#====PROGRAMME PRINCIPAL========================================
#===============================================================

if __name__=='__main__':
    
    game = Game()  
    game.run()