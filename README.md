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
