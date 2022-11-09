# Territory : artificial intelligence creation's

## Installations
To keep this project running, you will need 3 elements : python, flask and sqlalchemy.

### Python
The projet is running with python. So first of all, you will need to download it at this link : https://www.python.org/downloads/
<br>Now that python is ready, we will need one last element for our future installations: `pip install`.
<br>Open you're terminal and write this line :

    python get-pip.py    
This command will allow us to install the pip command. This command is used to install, from the console, various python frameworks.

### Flask
The first framework we will use is Flask. Flask is an open-source framework in web and python. This one will allow us to run a web server using python.
<br>To install Flask, you will, always in the terminal, launch this pip command line:

    pip install Flask
### SqlAlchemy
Then, to run our database, we will need SQLAlchemy. As before you will just need to use this command:

    pip install -U Flask-SQLAlchemy
### The github repository
Finally, all you need to do is clone or download our project and running our `run.py` file !


    https://github.com/YRNEHENRY/AI_Project.git


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
