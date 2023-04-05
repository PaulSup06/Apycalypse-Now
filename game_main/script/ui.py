import pygame
from settings import *
from debug import debug

class UI:
    def __init__(self) -> None:
        """Class UI : gère tout ce qui est affiché à l'écran et n'est pas directement dans le monde du jeu (overlay, affichage dialogues,...)
        """
        #chargement des images et textes fixes 
        self.dialog_box = pygame.image.load("..\\textures\\ui\\dialog_box.png").convert_alpha()
        self.hearts = [
            pygame.transform.scale(pygame.image.load("..\\textures\\ui\\heart_full.png"),(32,32)),
            pygame.transform.scale(pygame.image.load("..\\textures\\ui\\heart_half.png"),(32,32)),
            pygame.transform.scale(pygame.image.load("..\\textures\\ui\\heart_empty.png"),(32,32)),
        ]
        self.continue_indic = font2.render("[E] pour continuer...", 1,"white")
        self.screen = pygame.display.get_surface()
        self.current_dialog = None
        self.dialog_counter = 0
        self.ongoin_dialog = False
        
        self.transitions = []

    def load_dialog(self, dialogue_id, npc_name):
        """Affiche un dialogue en bas de l'écran
        Args:
            dialogue_id (int): id du dialogue à afficher
            npc_name (str): nom du npc 
        """

        ''' exemple de structure de donnée des dialogues d'un npc
        {
            "1":{
                    "type": "sans_choix",
                    "goto": "2"
                    "npc_update:("True","...",dialogue suivant)     -->     Change le status du npc 
                },
            "2":{
                    "type": "avec_choix",
                    "choix":[
                        {"index":1,
                        "texte_du_choix": "choix1",
                        "goto_number":"1"
                        },
                        {"index":2,
                        "texte_du_choix": "choix2",
                        "goto_number":"3"
                        }
                    ]
                },
            "3":{
                "type": "sans_choix",
                "goto": "-1"
            }
        }
        '''

        self.current_npc = npc_name
        self.ongoing_dialog = True
        
        self.current_dialog = npc_dialogs[self.current_npc][dialogue_id]
        self.current_dialog_text = self.current_dialog["text"].splitlines()
        self.current_dialog_len = {i:len(self.current_dialog_text[i]) for i in range(len(self.current_dialog_text))}
        
        self.dialog_counter = 0
        self.choix_rendered = []
        
        if self.current_dialog["type"] == "avec_choix":
            self.choix = self.current_dialog["choix"]
            self.nb_choix = len(self.choix)
            if self.nb_choix ==2:
                self.choix_rendered.append(Button(WIDTH//4 - 250,HEIGHT-100,500,50,font1,self.choix[0]["text"],self.select_option,False,button_fillcolors, self.choix[0]["goto"],self.choix[0]["npc_update"]))
                self.choix_rendered.append(Button((WIDTH//4)*3 - 250,HEIGHT-100,500,50,font1,self.choix[1]["text"],self.select_option,False,button_fillcolors,self.choix[1]["goto"],self.choix[1]["npc_update"]))
            elif self.nb_choix ==3:
                self.choix_rendered.append(Button(WIDTH//4 - 175,HEIGHT-100,350,50,font1,self.choix[0]["text"],self.select_option,False,button_fillcolors, self.choix[0]["goto"],self.choix[0]["npc_update"]))
                self.choix_rendered.append(Button((WIDTH//4)*2 - 175,HEIGHT-100,350,50,font1,self.choix[1]["text"],self.select_option,False,button_fillcolors,self.choix[1]["goto"],self.choix[1]["npc_update"]))
                self.choix_rendered.append(Button((WIDTH//4)*3 - 175,HEIGHT-100,350,50,font1,self.choix[2]["text"],self.select_option,False,button_fillcolors,self.choix[2]["goto"],self.choix[2]["npc_update"]))
            elif self.nb_choix ==4:
                self.choix_rendered.append(Button(WIDTH//4 - 250,HEIGHT-110,500,50,font1,self.choix[0]["text"],self.select_option,False,button_fillcolors, self.choix[0]["goto"],self.choix[0]["npc_update"]))
                self.choix_rendered.append(Button((WIDTH//4)*3 - 250,HEIGHT-110,500,50,font1,self.choix[1]["text"],self.select_option,False,button_fillcolors,self.choix[1]["goto"],self.choix[1]["npc_update"]))
                self.choix_rendered.append(Button(WIDTH//4 - 250,HEIGHT-65,500,50,font1,self.choix[2]["text"],self.select_option,False,button_fillcolors, self.choix[2]["goto"],self.choix[2]["npc_update"]))
                self.choix_rendered.append(Button((WIDTH//4)*3 - 250,HEIGHT-65,500,50,font1,self.choix[3]["text"],self.select_option,False,button_fillcolors,self.choix[3]["goto"],self.choix[3]["npc_update"]))
        else:
            self.choix = []
            self.nb_choix = 0    

    def show_ui(self, player):

        #initialisation des variables renvoyées
        npc_update= None
        
        #affichage du dialogue
        #=========================================================================================================================================================
        if self.current_dialog:
            dialog_rendered = []
            
            if self.dialog_counter < sum([len(line) for line in self.current_dialog_text]) and self.dialog_counter != -1:
                self.dialog_counter+=1
                somme=0
                i = 0
                while somme + len(self.current_dialog_text[i])<self.dialog_counter:
                    somme+=len(self.current_dialog_text[i])
                    i+=1

                for j in range(i):
                    dialog_rendered.append(font1.render(self.current_dialog_text[j],1,"white"))
                dialog_rendered.append(font1.render(self.current_dialog_text[i][:self.dialog_counter-somme],1,"white"))
            else:
                self.dialog_counter = -1

            if self.dialog_counter == -1: #dialogue terminé
                self.ongoing_dialog = False
                for line in self.current_dialog_text:
                    dialog_rendered.append(font1.render(line,1,"white"))
            

            # Affiche la bordure du dialogue
            self.screen.blit(self.dialog_box,((self.screen.get_width() - self.dialog_box.get_width())//2, self.screen.get_height() - self.dialog_box.get_height() - 10))

            #calcule la hauteur totale des dialogues pour affichage
            total_height = 0
            max_width = 0
            for element in dialog_rendered:
                total_height += element.get_height() + 10
                if 1 <= self.nb_choix <=3:
                    total_height += 75
                elif 4<= self.nb_choix<=6:
                    total_height += 85
                if max_width<element.get_width():
                    max_width=element.get_width()

            #création d'une surface pygame qui contient tous les dialogues rendus (plus facile à afficher)
            dialog_surf = pygame.Surface((max_width,total_height),pygame.SRCALPHA)

            for h in range(len(dialog_rendered)):
                dialog_surf.blit(dialog_rendered[h], ((dialog_surf.get_width() - dialog_rendered[h].get_width())//2,
                                                      h*(dialog_rendered[h].get_height()+10)))
                
                
            if self.dialog_counter == -1:
                
                for button in self.choix_rendered:
                    npc_update = button.process()
                    self.screen.blit(button.image,(button.x,button.y))
               
                if self.current_dialog["type"] == "sans_choix":
                    #cas où le dialogue est terminé, on rajoute alors une indication de touche au joueur pour continuer
                    self.screen.blit(self.continue_indic, ((self.screen.get_width() - self.dialog_box.get_width())//2 + self.dialog_box.get_width() - self.continue_indic.get_width() - 15, 
                                                        self.screen.get_height() - self.continue_indic.get_height() - 25))
            
            #affichage de la surface à l'écran
            self.screen.blit(dialog_surf,((self.screen.get_width()-dialog_surf.get_width())//2,
                                (self.screen.get_height() - self.dialog_box.get_height() - 10) + 
                                (((self.screen.get_height() - (self.screen.get_height() - self.dialog_box.get_height() - 10)) - total_height)//2)))
                
            
            #=========================================================================================================================================================    

            
    
        #affichage de la vie
        life_surf = pygame.Surface(((player.max_life//2+player.max_life%2) * self.hearts[0].get_width(), self.hearts[0].get_height()),pygame.SRCALPHA)
        for i in range(player.max_life//2+player.max_life%2):
            if player.life//2 >= i+1:
                life_surf.blit(self.hearts[0],(i*self.hearts[0].get_width(),0))
            elif player.life - (i*2) == 1:
                life_surf.blit(self.hearts[1],(i*self.hearts[0].get_width(),0))
            else:
                life_surf.blit(self.hearts[2],(i*self.hearts[0].get_width(),0))
        
        self.screen.blit(life_surf, (15, HEIGHT - life_surf.get_height() - 15))
        #affichage des items
        #affichage de l'inventaire
        # 
        #gestion transitions
        self.handle_transitions()
        return{"npc_update":npc_update}
     
    def finish_dialog(self):
        """Fonction appelée pour accélérer l'affichage du dialogue à l'écran
        Va directement à la fin de la page de dialogue en cours
        """
        self.dialog_counter = -1
    
    def quit_dialog(self,npc_name):
        """Ferme le dialogue en cours et renvoie les modifications à effectuer dans le code
        TODO: Si le dialogue nécessite un choix, aller au dialogue choisi
        
        return : dict
        """
        if self.current_dialog['type']=="sans_choix":
            if self.current_dialog["goto"] == "-1":
                callback_dialog = self.current_dialog
                self.current_dialog = None
                return callback_dialog
                
            else:
                self.load_dialog(self.current_dialog["goto"],npc_name)
                return self.current_dialog

        return {}
     
    def select_option(self,next_dialog,npc_update):
        self.load_dialog(next_dialog,self.current_npc)
        return npc_update       
        
    def add_transition_open(self):
        self.transitions.append(Transition(75,"black_to_white"))

    def add_transition_close(self,function,*args):
        self.transitions.append(Transition(75,"white_to_black",function,*args))

    def handle_transitions(self):
        for transition in self.transitions:
            if transition.handle(self.screen):
                self.transitions.remove(transition)

class Transition:
    def __init__(self, length, type, function=None,*args):
        """Class Transition : permet d'afficher à l'écran une transition en cercles concentriques (ouverture ou fermeture)

        Args:
            length (int): longueur de la transition (en frames)
            type (str): "black_to_white","white_to_black" => type de la transition
            function (func, optional): Fonction à exécuter lors de la fin de la transition (ex : changer de monde). Defaults to None.
        """
        self.length = length
        self.type = type
        self.function = function
        self.args = args
        self.surf = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        self.counter = 0

    def handle(self, screen):
        """Gère la transition

        Args:
            screen (pygame.Surface): surface sur laquelle afficher la transition (écran du jeu)

        Returns:
            Bool: True si la transition est terminée
        """
        if self.type=="black_to_white":
            self.surf.fill('black')
            pygame.draw.circle(self.surf,[0,0,0,0],(WIDTH//2,HEIGHT//2), ((WIDTH)//self.length)*self.counter)
        elif self.type=="white_to_black":
            self.surf.fill("black")
            pygame.draw.circle(self.surf,[0,0,0,0],(WIDTH//2,HEIGHT//2), ((WIDTH)//self.length)*(self.length - self.counter - 1))

        screen.blit(self.surf,(0,0))

        self.counter += 1

        if self.counter > self.length:
            if self.function!=None:
                self.execute_func()
            return True
        
    def execute_func(self):
        """Exécute la fonction attribuée à la transition à la fin de celle-ci
        """
        self.function(*self.args)


class Button:
    def __init__(self, x, y, width, height, font, buttonText='Button', onclickFunction=None, onePress=False,fillColors={'normal': '#ffffff','hover': '#666666','pressed': '#333333','text':(20,20,20),}, *args):
        """Class Button : bouton polyvalent permettant d'exécuter une fonction avec des arguments lorsque pressé

        Args:
            x (int): position x
            y (int): position y 
            width (int): largeur du bouton
            height (int): hauteur du bouton
            font (pygame.font): police d'écriture du texte du bouton
            buttonText (str, optional): texte du bouton. Defaults to 'Button'.
            onclickFunction (func, optional): fonction à exécuter lorsque le bouton est pressé. Defaults to None.
            onePress (bool, optional): si True, la fonction s'exécute en boucle tant que le bouton est enfoncé.
                                       Sinon s'exécute 1 fois et ensuite il faut relacher le clic. Defaults to False.
            fillColors (dict, optional): Couleurs du bouton personnalisables. Defaults to {'normal': '#ffffff','hover': '#666666','pressed': '#333333','text':(20,20,20),}.
            *args : arguments optionnels de la fonction onclickFunction
        """     
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.args = args

        self.fillColors = fillColors

        self.image = pygame.Surface((self.width, self.height)).convert_alpha()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = self.font.render(buttonText, True, self.fillColors["text"])

        self.alreadyPressed = False

    def process(self):
        """Gère l'entièreté du Button (affichage + clic)

        Returns:
            any: return de la fonction onclickFunction
        """
        result = None
        mousePos = pygame.mouse.get_pos()
        
        self.image.fill(self.fillColors['normal'])
        if self.rect.collidepoint(mousePos):
            self.image.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.image.fill(self.fillColors['pressed'])

                if self.onePress:
                    result = self.onclickFunction(*self.args)

                elif not self.alreadyPressed:
                    result = self.onclickFunction(*self.args)
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.image.blit(self.buttonSurf, [
            self.rect.width/2 - self.buttonSurf.get_rect().width/2,
            self.rect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        return result