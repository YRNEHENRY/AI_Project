# Territory : artificial intelligence creation's

## What is Territory ?
Territory is a high school project aiming at running an AI trained with Q-function on a game running online with Flask.

## Installations
To keep this project running, you will need 2 elements : SQLite and the `requirements.txt`.

### SQLite
The project is running with a database. So, first of all, you will download SQLite at this link : https://www.sqlite.org/index.html

### Requirements.txt
By running our file, the required extensions will install themselves.

If the requirements file does not work, follow these steps to install them manually...

### Requirements.txt doesn't work
#### Python
The projet is running with python. So, you will need to download it at this link : https://www.python.org/downloads/
<br>Now that python is ready, we will need one last element for our future installations: `pip install`.
<br>Open you're terminal and write this line :

    python get-pip.py    
This command will allow us to install the pip command. This command is used to install, from the console, various python frameworks.

#### Flask
The first framework we will use is Flask. Flask is an open-source framework in web and python. This one will allow us to run a web server using python.
<br>To install Flask, you will, always in the terminal, launch this pip command line:

    pip install Flask
#### SqlAlchemy
Then, to run our database, we will need SQLAlchemy. As before you will just need to use this command:

    pip install -U Flask-SQLAlchemy
#### The github repository
Finally, all you need to do is clone or download our project and running our `run.py` file !


    https://github.com/YRNEHENRY/AI_Project.git

## The code

### How to run the project
To run our program you just have to launch the `run.py` file in the root folder.

### How is the code split?
In the `game_app` folder, We have 3 possibilities :
- The 1st one is the `static` folder which will contain our js and css files and our pictures
- The 2nd is the `template` folder which will contain each of our different views of the site
- The 3rd and last one is the different python files in the folder. Each corresponding to a part of the code.

### The AI
Our AI works with the qfunction. Our two AIs will train against each other to fill their Qtable.
<br>As the number of games increases, the epsilon greedy will decrease as well as our learning rate.

## Rules of the game
The goal of the game is to get as many squares as possible.
<br>For that each one will play one after the other.

Be careful, you can't move on a square belonging to your opponent.

If you manage to form a block completely surrounded by your squares. This will create an "enclosure" and take all the squares in the enclosure.

## Teacher's comments
### Review 10/10/22 : Squelette :
- [x] Manque d'une page d'accueille (avec un bouton pour aller vers le jeu)
- [x] le reste semble OK ;)

### Review 30/10/22 : Jeu de base :
- [x] complétez le reedme
- [x] constructeur de Board à discuter
- [x] le mouvement de l'IA est à gérer différemment (directement dans le serveur : quand on recoit un mouvement de joueur, on l'exécute et si le second joueur est une IA, on le fait aussi avant de renvoyer le nouvel état au client)
- [ ] à quoi ressemble le move recu par le serveur ? le serveur doit recevoir le mouvement (pas la nouvelle position) et calculer la nouvelle position en fonction => à mettre dans un fichier business à part idéalement
- [x] get_possible_move devrait être lié à une partie et pas à un joueur (ici : l'IA) + /!\ harcodage de la taille du board
- [x] éviter de print dans le code du serveur... 
- [x] 4x fetch à chaque tour de jeu ? Le JS ne doit en principe faire qu'un seul appel serveur par "tour" et ne contient aucune logique...

### Review 13/11/22 : Enclos :
- Ca marche :)
- on discute de la gestion du mouvement demain.


### Review IA: 12/12/22
 - Ok en gros 
 - En attendant le résultat d'execution pour voir si la q-table est bien complétée et que vous aurez un équilibre entre exploration/ exploitation
