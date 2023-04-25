# Table des matières 
- [Table des matières](#table-des-matières)
- [**Documentation technique par classe, comprenant les principales caractéristiques :**](#documentation-technique-par-classe-comprenant-les-principales-caractéristiques)
  - [**Classe Game**](#classe-game)
    - [**Attributs**](#attributs)
    - [**Méthodes**](#méthodes)
      - [**Fonctions liées aux menus**](#fonctions-liées-aux-menus)
      - [**Gestion des touches dans les paramètres**](#gestion-des-touches-dans-les-paramètres)
      - [**Gestion de la musique**](#gestion-de-la-musique)
      - [**Fonctions liées aux items**](#fonctions-liées-aux-items)
      - [**Fonctions d'UI**](#fonctions-dui)
      - [**Fonctions liées aux switchs**](#fonctions-liées-aux-switchs)
  - [**Classe Entity**](#classe-entity)
    - [**Attributs**](#attributs-1)
    - [**Méthodes**](#méthodes-1)
  - [**Classe Case**](#classe-case)
    - [**Attributs**](#attributs-2)
  - [**Classe Player**](#classe-player)
    - [**Attributs**](#attributs-3)
    - [**Méthodes**](#méthodes-2)
  - [**Classe Trigger**](#classe-trigger)
    - [**Attributs**](#attributs-4)
    - [**Méthodes**](#méthodes-3)
  - [**Classe Level**](#classe-level)
  - [**Classe UI**](#classe-ui)
  - [**Classe Enemy**](#classe-enemy)
  - [**Classe Spike**](#classe-spike)
  - [**Classe Npc**](#classe-npc)
  - [**Classe Inventaire**](#classe-inventaire)
  - [**Classe Item**](#classe-item)
  - [**Classe Lever**](#classe-lever)
  - [**Classe PressurePlate**](#classe-pressureplate)
  - [**Classe Manivelle**](#classe-manivelle)
  - [**Classe Terminal**](#classe-terminal)
  - [**Classe Browser**](#classe-browser)
  - [**Classe API**](#classe-api)
- [**PARTIE WEB**](#partie-web)
  - [**Terminal**](#terminal)
    - [**Attributs**](#attributs-5)
  - [**Méthodes**](#méthodes-4)



# **Documentation technique par classe, comprenant les principales caractéristiques :**

## **Classe Game**

La classe Game est la classe principale du jeu, qui gère l'initialisation du jeu, la boucle de jeu et toutes les interactions entre les différents éléments du jeu.

### **Attributs**

- **screen** : surface Pygame représentant l'écran du jeu
- **clock** : objet Pygame Clock pour gérer la vitesse de rafraîchissement du jeu
- **player** : objet Player représentant le personnage du joueur
- **level** : objet Level représentant le niveau actuel
- **inventarie** : objet Inventory 
- **ui** : objet UI, interface et affichage indépendant du niveau
- **running** : booléen gérant l’exécution de la boucle de jeu principale
- **game\_state** : str gérant le status du jeu
- **is\_in\_a\_note** : un booléen indiquant si le joueur est en train de lire une note
- **settings** : paramètres du jeu actuellement utilisés
- **music\_playing** : musique actuellement jouée dans le jeu

### **Méthodes**

- **\_\_init\_\_** : initialise la classe Game et tous les éléments nécessaires au lancement du jeu
- **run** : démarre la boucle principale du jeu

#### **Fonctions liées aux menus**

- **generate\_menus** : créé les menus du jeu au lancement
- **sauvegarde (name)**  : créé une sauvegarde de la partie en json, nom par défaut « latest »
- **load\_sauvegarde (name)** : charge une sauvegarde enregistrée sous un nom spécifique
- **delete\_sauvegarde (name)** : supprime une sauvegarde enregistrée sous un nom spécifique
- **generate\_world (world, pos)** : Méthode appelée à la création d'un monde, possibilité de spécifier une position du joueur
- **create\_new\_game** : Génère le monde lors du premier chargement (nouvelle partie)
- **change\_level (level)**: Change le monde lors d'un changement de niveau + transition
- **reprendre\_partie** : Fonction liée au bouton "reprendre la partie" du menu de pause
- **save\_npc\_states** : Enregistre les états des pnjs actifs sur le monde quitté par le joueur (et rechargés s'il revient)
- **save\_and\_quit** : Fonction liée au bouton "Sauvegarder et quitter" du menu de pause
- **quit\_game :** Fonction liée au bouton "Quitter" du menu principal  (peut être appelée aussi in game si besoin)

#### **Gestion des touches dans les paramètres**

- **listen\_to\_key :** active le mode détection de touche du jeu : la prochaine touche reçue est prise en compte par les paramètres
- **edit\_key :** Change de manière définitive la touche une fois celle-ci reçue **+** modification du fichier paramètres csv
- **reset\_settings :** Réinitialise les paramètres (copie le fichier default\_settings dans settings)
- **continue\_game :** fonction de "triche" qui permet de revivre après être mort
- **to\_main\_menu :** Retourne au menu principal (sans sauvegarde)
- **retry :** Recommence la partie entièrement

#### **Gestion de la musique**

- **play\_music :** Charge une musique dans le mixer pygame
- **change\_music\_volume :** Change le volume pygame de la musique

#### **Fonctions liées aux items** 

- **read\_note(, note)** : ouvre une note
- **add\_player\_heart(amount=2)** : ajoute un certain montant de vie maximale au joueur
- **heal\_player (amount=2) :** Rajoute de la vie au joueur
- **speed\_player :** Multiplie la vitesse du joueur par un facteur
- **strength\_player :** Multiplie la force du joueur par un facteur
- **invincibility\_player :** Rend le joueur invicible pendant un certain temps

#### **Fonctions d'UI**

- **update\_dialog\_ended(, fin\_dialogue, npc\_name)** : met à jour les éléments du jeu après la fin d'un dialogue

#### **Fonctions liées aux switchs**

- **unlock\_door(, door\_to\_unlock, active, inactive)** : déverrouille une porte en fonction de la position des switchs
- **unlock\_terminal(, term\_to\_unlock, active, inactive)** : déverrouille un terminal en fonction de la position des switchs
- **spawn\_enemy(, x, y, movement\_type, name, speed, damages, health, movement\_condition=True)** : fait apparaître un ennemi sur la carte en fonction de paramètres donnés

## **Classe Entity**

Objet générique représentant une entité, un objet mobile ou immobile, interactif ou n’étant pas lié à la carte. Hérite de la classe pygame.sprite.Sprite

### **Attributs**

- **x** : position x
- **y** : position y
- **groupes** : liste de pygame.sprite.Group auxquels l’entité doit être ajoutée 
- **surface** : pygame.Rect représentant l’image de l’entité
- **rect** : pygame.Rect représentant le rectangle de collisions de l’entité
- **basey** : position y de la base de l’entité (voir explications plus bas)

### **Méthodes**

- **check\_collision(collide\_group, direction, valeur)** : vérifie les collisions entre l’entité et un groupe de sprites selon un déplacement prévue avec un direction et une valeur. Renvoie un booléen.
- **check\_distance\_to (target\_pos, distance\_max) :** Vérifie si la distance entre l'entité et une certaine position est inférieure à une valeur donnée. Renvoie un booléen.

## **Classe Case**

Objet de base Case : sert à contenir une case de la carte. Hérite de pygame.sprite.Sprite

### **Attributs**

- **x (int):** position x 
- **y (int)** : position y
- **groupes (list):** liste de pygame.sprites.Group auxquels ajouter la case
- **texture (pygame.image):** texture de la case (utilisée pour l'affichage dans le cas où l'image n'est pas override)
- **surface (pygame.Surface, optional):** Surface personnalisée pour la case. Par défaut une surface de la taille standard d'une case.
- **basey (int, optional):** Position y de la base de la case pour l'affichage (si =None, utilisation de la base de la surface) . Defaults to None.

## **Classe Player**

Objet principal contrôlable par le joueur, héritant de la classe Entity 

### **Attributs**

- **player\_imgs** : dictionnaire des images du joueur 
- **image** : image actuellement utilisée (mise à jour en fonction de l’action en cours)
- **direction** : direction de déplacement du joueur
- **movement** : pygame.vector2 représentant le mouvement du joueur
- **life :** vie du joueur
- **speed\_multiplier :** multiplicateur de la vitesse de base du joueur
- **strength\_multiplier :** multiplicateur de la force de base du joueur
- **invincibility :** bool si le joueur est invincible pour la gestion des dégats
- **max\_life :** vie maximum atteignable par le joueur
- **attacking :** bool : True si le joueur est actuellement en train d’attaquer
- **weapon :** arme actuellement équipée par le joueur

### **Méthodes**

- **\_\_init\_\_(** **x, y, groupes, collision\_blocks, player\_life, max\_life, weapon=None) :**  arguments lors de l’initialisation du joueur
- **move(keys, settings) :** Déplacement et collisions du personnage principal avec les touches pressées, en fonction des paramètres actuellement utilisés
- **update :** Gère les animations du joueur en fonction de ses déplacements
- **attack :** Gère l'attaque du joueur sur les ennemies

## **Classe Trigger**

Case spéciale contenant une fonction activée lorsque le joueur est dans la surface de la case

### **Attributs**

- **x (int):** position x
- **y (int):** position y 
- **groupes (list**): liste de pygame.sprites.Group auxquels ajouter la case
- **texture (pygame.image):** texture de la case (utilisée pour l'affichage dans le cas où l'image n'est pas override)
- **trigger\_func (func):** fonction appelée lorsque le joueur est dans la zone de la case.
- **surface (pygame.Surface, optional):** Surface personnalisée pour la case. Par défaut une surface de la taille standard d'une case.
- **basey (int, optional):** Position y de la base de la case pour l'affichage (si =None, utilisation de la base de la surface) . Defaults to None.
- **args :** arguments à passer à la fonction appelée
- **activated :** bool représentant le status du trigger (utilisé pour ne pas appeler 2 fois la même fonction

### **Méthodes**

- **\_\_init\_\_(x, y, groupes, texture,trigger\_func,width,height,\*args) :**  initialisation du trigger
- **handle (player,main) :** appelle la fonction du main liée au trigger si le joueur se trouve sur la case

## **Classe Level**

Objet utilisé pour la génération d’un niveau du jeu avec pytmx et pour stocker les différents éléments de la carte.

## **Classe UI**

Class UI : gère tout ce qui est affiché à l'écran et n'est pas directement dans le monde du jeu (overlay, affichage dialogues,...)

## **Classe Enemy**

Objet Enemy héritant de la classe Entité, est hostile au joueur.

## **Classe Spike**

Objet Spike héritant de la classe Entité, est hostile au joueur, se déclenche au passage du joueur sur l’objet.

## **Classe Npc**

Entité spécifiée comme étant un NPC (ou PNJ), capable d'interagir avec le joueur. Hérite de la classe Entity. Peut déclencher un dialogue.

## **Classe Inventaire**

Représente l’inventaire du joueur, gère le stockage des items et l’utilisation de ceux-ci.

## **Classe Item**

Objet item lorsque lâché au sol, peut être ramassé par le joueur si son inventaire n’est pas plein.

Switches :

## **Classe Lever**

Objet levier héritant de la classe Entité, est interactif pour le joueur, appelle une fonction lorsqu’activé.

## **Classe PressurePlate**

Objet plaque de pression héritant de la classe Entité, appelle une fonction lorsqu’activé si le joueur passe au-dessus.

## **Classe Manivelle**

Objet levier héritant de la classe Entité, est interactif pour le joueur, appelle une fonction lorsqu’activé, peut nécessiter une manivelle à placer sur le support avant d’être activable.

## **Classe Terminal**

Objet Terminal interactif par le joueur, créé une instance de Browser si interaction.

## **Classe Browser**

Objet Browser à l’intérieur d’un terminal, ouvre une fenêtre web via librairie pywebview.

## **Classe API**

Classe interagissant avec le code Javascript de la fenêtre pywebview, nécessaire à l’ouverture de la fenêtre et à l’exécution du code, afin de récupérer le statut (réussi ou non) de l’épreuve.

# **PARTIE WEB**

## **Terminal**

Page web interactif avec laquelle l’utilisateur peut interagir en jeu.

### **Attributs**

- **debug:** bool permettant d’accélérer la vitesse d’affichage des éléments web lors du débogage du site.

- **answers:** Tableau contenant les réponses aux énigmes, dans l’ordre des champs de saisie.

- **```<p id="code1\_text"></p>```** : Paragraphe contenant l’énigme. Les zones de saisie sont exprimées par des ```@’``` qui seront remplacé automatiquement lors de l’affichage. Ainsi, le code est très modulable et il suffit de changer le texte de l’énigme et le tableau de ses réponses.

## **Méthodes**

- **(async) typeText(selector, text, whatNext, waitSecondBeforeWhatNext = true, fast\_writing = false) :**  Affiche du texte avec une animation style "écriture progressive" dans le sélecteur indiqué, et exécute à la fin de son affichage une fonction ‘**whatNext’**

- **async typeCursorForMs(selector, cursor, whatNext, count\_total = 5) :** Affiche un curseur qui apparait et disparait  ‘**count\_total’** de fois

- **opacityAnim(idElement) :**  Affiche un élément à l’écran avec une animation type « fade-in »

- **progressBarAnim(selector, whatNext):**  Animation d’une incrémentation d’une barre de progression de 0 à 100% (pour simuler un chargement)

- **(async) eraseText (selector, whatNext) :**  Efface le texte se situant dans le InnerHTML du sélecteur donné, en enlevant les caractère un par un de droite à gauche.

- **(async) progressBarText(selector, whatNext):**  Créé une barre de progression textuelle (dans ce style : [████░░░░░░] 40%) qui s’incrémente de 0 à 100%.

- **button\_login\_clicked() :** Vérifie les informations écrite par l’utilisateur dans les 2 champs de saisies (nom d’utilisateur/mot de passe)

- **close\_terminal() :** Appel l’API python afin de fermer le terminal in-game (sans l’avoir complété)

- **input\_text\_changed() :** Dès que l’utilisateur modifie une de ses réponses, comparent ses saisies à ceux attendues afin de voir s’il a compléter le terminal. Si l’utilisateur l’a complété, alors la fonction fait quitter le terminal à l’aide de l’API python.

- **check\_input() :** Compare une réponse spécifique et renvoie ‘true’ si l’utilisateur a saisi la bonne réponse


Le code d’affichage fonctionne en « file indienne ». Chaque fonction appelé possède un argument ‘whatNext’ qu’il appellera lors de la fin de son exécution. Ainsi, chaque élément apparaisse les uns après les autres pour un effet « terminal »

Voici, dans l’ordre, le chemin d’exécution des fonctions. Le code est simple à comprendre et très facilement modulable pour créé tout type de terminaux.