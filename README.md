# Territory : artificial intelligence creation's

DE BUCK Henry 👨🏼‍💻 & SOMME Aurélien 👨🏻‍💻

Review 10/10/22 : Squelette :
-----------------------------
- Manque d'une page d'accueille (avec un bouton pour aller vers le jeu)
- le reste semble OK ;)

Review 30/10/22 : Jeu de base :
----------------------------
- complétez le reedme
- constructeur de Board à discuter
- le mouvement de l'IA est à gérer différemment (directement dans le serveur : quand on recoit un mouvement de joueur, on l'exécute et si le second joueur est une IA, on le fait aussi avant de renvoyer le nouvel état au client)
- à quoi ressemble le move recu par le serveur ? le serveur doit recevoir le mouvement (pas la nouvelle position) et calculer la nouvelle position en fonction => à mettre dans un fichier business à part idéalement
- get_possible_move devrait être lié à une partie et pas à un joueur (ici : l'IA) + /!\ harcodage de la taille du board
- éviter de print dans le code du serveur... 
- 4x fetch à chaque tour de jeu ? Le JS ne doit en principe faire qu'un seul appel serveur par "tour" et ne contient aucune logique...
