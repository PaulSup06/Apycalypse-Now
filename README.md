## TODO :
#### Se reporter à la Roadmap ouverte dans l'onglet "Issues", le Readme étant destiné à ne plus contenir ces sections
- [x] Ajout des animations
- [x] Ajout d'un menu au lancement du jeu
- [x] Menu choix des touches (codage des touches dynamique)
- [ ] Joueur:
    - [x] animations
    - [x] attaques (base + animation)
    - [ ] armes et attaques fonctionnelles 
    - [ ] inventaire ? (optionnel)
- [ ] UI:
    - [ ] vie/armure/items
    - [x] Menu de dialogues
- [ ] Textures :
    - [ ] Joueur (animations)
    - [x] Monde 
    - [ ] Mobs
    - [ ] Armes (optionnel textures sur le joueur)
- [ ] Entités (mobs et interactions joueur):
    - [x] Mobs agressifs de base (déplacements en ligne)
    - [ ] Mobs agressifs intelligents (pathfinding)
    - [ ] Mobs tir à distance ?
    - [ ] Autres personnages interactifs (menu ? + dialogues + cinématiques ? + quêtes ?)
- [x] Génération du/des mondes :
    - [x] décodage de pytmx et génération map
    - [x] ajout "hauteur" d'objet pour l'affichage
    - [ ] ajout items/mobs dynamiquement (modification de la map ?) (optionnel)
- [x] Ajout énigmes via pages Internet
- [x] Sauvegarde de la position du joueur/son monde actuel (à la fermeture du jeu !!! à ajouter)
    - [x] décodage JSON et choix de la sauvegarde utilisée
- [x] IMPORTANT Optimiser le code/jeu pour maintenir les 60 fps au mieux sur toutes les machines (ex : pc du lycée), sinon passer à 30fps


## MISC :
- Police d'écriture des menus pygame : https://dennisbusch-de.itch.io/0xdbs-terminal-chonker-8x8-1bpp-bitmap-font
- Ressources en ligne d'asset :
    ##### [itch.io](https://itch.io/c/133871/tiled-resources)
    ##### [opengameart](https://opengameart.org/)
    ##### [hamsterrpublic tilemaps](https://rpg.hamsterrepublic.com/ohrrpgce/Free_Tilemaps)
    ##### [hamsterrpublic animations](https://rpg.hamsterrepublic.com/ohrrpgce/Free_Animations)
    ##### [Spriter ressource (ressources de jeux rétro console)](https://www.spriters-resource.com/snes/bszelda/?source=genre)
    
  ### MUSIQUE :
    ##### [Dystopian pack (banger absolu allez écouter)](https://timbeek.itch.io/dystopian)
    ##### [Synthwave Pink Bloom pack (idem)](https://davidkbd.itch.io/pink-bloom-synthwave-music-pack)
    
 ### EFFET AUDIO:
    ##### [freesound.org](freesound.org)


# REQUIS POUR L'INSTALLATION
### Python 3.8 ou plus récent
### Windows 10/11
### game folder

## Modules python :
-pygame (2.3.0 ou +) installée depuis la version site python.org, car nous avons eu des problèmes avec la version Microsoft Store

-pywebview (4.0.2 ou +)
!!! SPECIFIQUE REQUIS:
    - .NET Framework 4.6.2 ou +
    - Edge Runtime installed (https://developer.microsoft.com/en-us/microsoft-edge/webview2/)
    - wheel library for python (before install)

-pygame_menu (4.4.0 ou +)
-pytmx (3.31 ou +)



# NOTICE UTILISATION TILED
GENERALITES :
-Le fond du jeu est une image .png exportée de Tiled (nom de type : "numero_level.png"), tout ce qui y touche est regroupé par convention dans un dossier de layers visibles mais pas utilisés par le programme directement
-Le layer 'ground props' correspond à tous les éléments de décors qui ne sont pas directement le fond de carte, tout ce qui est en l'air notamment. TOUS les éléments doivent disposer d'une classe "hx" où x est la hauteur de la tile,(par convention du haut de celle-ci) par rapport au sol, en nombre de tiles.
Ex : un pot de fleur de 2 tiles de haut comporte une première tile "h1" posée sur le sol (haut de la tile à 1 du sol) et une deuxième tile "h2" au dessus de celle-ci. 

Pour le joueur:
    Celui-ci se trouve dans le layer d'objets 'entitees', sans paramètres. Image sans importance. NOM DE L'OBJET = player

Pour les spikes/...:
    Idem joueur, indiquer le nom de l'objet systématiquement, l'image n'est pas nécéssairement utilisée (à vérif coté code)

Pour les NPC:
    Ils sont également dans le layer 'entitees', l'IMAGE EST IMPORTANTE et ont plusieurs propriétées:
        -npc_name -> (string) nom du npc utilisé pour les dialogues (voir structure de dialogues)
        -first_dialog -> (string) premier dialogue appelé (le plus souvent 1 sauf si particulier au monde)
        -indicator -> (string) en-tête par défaut du NPC
        -talkable -> (bool) case à cocher si le npc est interactif (possibilité de ne pas le faire parler au joueur) ATTENTION Le cas échéant, lui donner quand même les autres paramètres

Pour les triggers :
    Utiliser un layer d'objet "triggers", contenant au choix des rectangles ou des objets avec image classiques (image non utilisée)
    Ceux-ci doivent posséder OBLIGATOIREMENT les propriétés:
        -function -> (string) nom de la fonction dans le main, sans les parenthèses
        -args -> (string) arguments de la fonction (voir en dessous)
ATTENTION pour utiliser les triggers avec des arguments, il faut respecter la syntaxe :
    Dans le cas d'un paramètre simple, pas de souci: param / (param)
    Dans le cas de paramètres multiples : param1,param2 / (param1,param2)
    Dans le cas de paramètres imbriqués (ex : la position du joueur au spawn, qui est une tuple (x,y) ): (param1),(param2,param3)
    ATTENTION AUX ESPACES ! PAS D'ESPACE ENTRE LES ARGUMENTS/PARENTHESES/VIRGULES

Pour les blocks de collison :
    Utiliser un layer d'objet "collision", contenant au choix des rectangles ou des objets avec image classiques (image non utilisée)
    Aucun paramètre à utiliser, les collisions sont normalement au pixel près (donc faire attention aux coins des rectangles)

Pour les ennemis :
    Utiliser le layer d'objet "entitees", utiliser de préférence des tiles pour un meilleur visuel mais l'image utilisée n'est pas importante
    Les seuls paramètres utilisés par le jeu sont la position x et y de l'objet placé cependant il faut spécifier quelques propriétés:
        -damages -> (int) dégats infligés à chaque coup au joueur (en hp donc coeur/2)
        -health -> (int) vie de l'ennemi, aussi en hp
        -movement -> (str) type de mouvement de l'ennemi (voir docstrings de enemy.py pour + d'infos)
        -speed -> (int) vitesse de déplacement (pour référence, celle par défaut du joueur est de 5)
        -enemy_name -> (str) nom et type de l'ennemi, utilisé pour le référencement des textures (voir structure de fichiers du dossier enemies, son nom correspond au nom du dossier)

Pour les switches :
    Utiliser un layer d'objet "switches", contenant les tiles des switches
    Nom des objets important, indique la catégorie de switch (ex : floor_level, manivelle, pressure_plate, ...)
    Propriétés :
        -function_to_call -> (string) fonction à appeler lorque le switch est utilisé
        -args -> (string) arguments de la fonction (à définir)
        -id -> (string) id du switch, utile pour le référencement et les checks
        -type -> (string) type de switch dans la catégorie (utile pour les textures)

        PROPRIETES PARTICULIERES:
        wall_level :
            -height -> (int) même cas que la hauteur hx des ground props
        manivelle :
            -has_manivelle -> (bool) définit si la manivelle dispose de sa poignée au spawn (possibilité de la rajouter dans le cas contraire)
 