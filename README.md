- [Guide d’utilisation :](#guide-dutilisation-)
    - [Prérequis d’installation :](#prérequis-dinstallation-)
    - [Guide d’exécution :](#guide-dexécution-)
    - [Remarques particulières :](#remarques-particulières-)
    - [Aide pour les touches :](#aide-pour-les-touches-)
- [Documentation :](#documentation-)
- [Ressources et liens :](#ressources-et-liens-)
  - [Ressources en ligne d'asset et textures :](#ressources-en-ligne-dasset-et-textures-)
  - [MUSIQUE :](#musique-)
    - [EFFET AUDIO:](#effet-audio)


# Guide d’utilisation : 
### Prérequis d’installation :
*	Python 3.8 ou plus récent
*	Windows 10/11
*	Dossier sources 
*	Modules python :
    *	pygame (2.3.0 ou +) installée depuis la version site python.org, car nous avons eu des problèmes avec la version Microsoft Store
    *	pywebview (4.0.2 ou +) qui a elle-même des prérequis :
        *	.NET Framework (4.6.2 ou +)
        *	Edge Runtime  (https://developer.microsoft.com/en-us/microsoft-edge/webview2/)
        *	wheel library for python
    *	pygame_menu (4.4.0 ou +)
    *	pytmx (3.31 ou +)
    *	Les modules built-in de python : datetime, os, sys, csv, json, random
*	Vérifier le niveau de mise à l’échelle de Windows (voir remarques particulières).

### Guide d’exécution :
Après avoir vérifié que vous remplissez les prérequis d’installation, lancez le fichier main.py avec un interpréteur python. Une fenêtre pygame doit s’ouvrir et un menu apparaître. Lors d’une première exécution, cliquez simplement sur « Nouvelle partie ». Vous voilà maintenant en jeu. Les touches de déplacement par défaut sont les touches Z,Q,S,D du clavier AZERY. Vous trouverez les autres touches dans les paramètres du jeu, toutes sont modifiables.

### Remarques particulières :
Il se peut que l’affichage pygame ne soit pas en plein écran et soit trop petit ou trop grand par rapport à votre écran. Il se peut également qu’à la fermeture d’un terminal la fenêtre change de dimension, devenant la plupart du temps plus petite qu’à l’origine. Dans ce cas, modifiez la mise à l’échelle Windows et paramétrez sa valeur à 100%, cela devrait régler le problème. Enfin, nous avons constaté un bug au niveau de la dernière porte verrouillée du labo, si malgré que le bon code soit rentré avec les leviers la porte refuse de s'ouvrir, veuillez faire une sauvegarde et recharger le jeu.

### Aide pour les touches :
Les touches par défaut de notre jeu sont :
* **Z** - Se déplacer vers le haut
* **S** - Se déplacer vers le bas
* **Q** - Se déplacer à gauche
* **D** - Se déplacer à droite
* **E** - Interagir
* **SPACE/ESPACE** - Attaquer
* **TAB** - Ouvrir l'inventaire
* **ECHAP/ESCAPE** - Sortir, menu de pause
* Dans l'inventaire, les touches de déplacement servent à sélectionner les objets, E à les utiliser et SPACE à les lacher au sol.

# Documentation : 

***Voir la documentation dédiée dans le [répertoire doc](doc)***

# Ressources et liens :
## Ressources en ligne d'asset et textures :
- [itch.io](https://itch.io/c/133871/tiled-resources) 
- [opengameart](https://opengameart.org/)
- [hamsterrpublic tilemaps](https://rpg.hamsterrepublic.com/ohrrpgce/Free_Tilemaps)
## MUSIQUE :
- [Dystopian pack by Tim Beek](https://timbeek.itch.io/dystopian)
### EFFET AUDIO:
- [freesound.org](freesound.org)
