from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, insert
import csv
import time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)

def init_db():
    db.drop_all()
    db.create_all()

def insert(object):
    db.session.add(object)
    db.session.commit()

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.VARCHAR(25), nullable = False, unique = True)
    nb_wins = db.Column(db.Integer, nullable = False)
    nb_defeats = db.Column(db.Integer, nullable = False)
    nb_draws = db.Column(db.Integer, nullable = False)

class Humans (db.Model):
    __tablename__ = "humans"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    password = db.Column(db.VARCHAR(50), nullable = False)
    email = db.Column(db.VARCHAR(50), nullable = False, unique = True)
    name = db.Column(db.VARCHAR(25), nullable = False)
    first_name = db.Column(db.VARCHAR(25), nullable = False)

    fk_user = db.Column(db.Integer,db.ForeignKey('users.id')) # foreign key to user

class AIs (db.Model):
    __tablename__ = "ais"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    fk_user = db.Column(db.Integer,db.ForeignKey('users.id')) # foreign key to user

class Boards(db.Model):
    __tablename__ = "boards"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    size = db.Column(db.Integer, nullable = False)
    state_board = db.Column(db.VARCHAR(36), nullable = False)
    turn = db.Column(db.Integer, nullable = False)
    position_p1 = db.Column(db.String(2), nullable = False)
    position_p2 = db.Column(db.String(2), nullable = False)

    fk_player_1 = db.Column(Integer, ForeignKey("users.id")) # foreign key to user 1
    fk_player_2 = db.Column(Integer, ForeignKey("users.id")) # foreign key to user 2

class historys(db.Model):
    __tablename__ = "historys"

    id = db.Column(db.Integer, primary_key = True)
    nb_turn = db.Column(db.Integer, nullable = False, primary_key = True)
    action = db.Column(db.String(2), nullable = False)
    state = db.Column(db.String(50), nullable = False)
    position_1 = db.Column(db.String(4), nullable = False)
    position_2 = db.Column(db.String(4), nullable = False)

class QTableState4(db.Model):
    # 16 chiffres pour board (4x4) + 4 chiffres pour pos joueurs + 1 chiffre (1 ou 2) pour turn
    state = db.Column(db.String(21), primary_key=True)
    left_score = db.Column(db.Integer, default=0)
    right_score = db.Column(db.Integer, default=0)
    up_score = db.Column(db.Integer, default=0)
    down_score = db.Column(db.Integer, default=0)

    @staticmethod
    def export_to_csv(file_path : str):
        # Retrieve all instances of QTableState4 from the database
        instances = QTableState4.query.all()
        fieldnames = ['state', 'left_score', 'right_score', 'up_score', 'down_score']

        # Check if there are instances to export
        if not instances:
            print("ERROR : no instances to export.")
            return

        # Open CSV file in write mode
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames) # Write the first line with the variable names

            # Write the values of each instance in a line of the CSV file
            for instance in instances:
                row = [
                    instance.state,
                    instance.left_score,
                    instance.right_score,
                    instance.up_score,
                    instance.down_score
                ]
                writer.writerow(row)
        
        print(f"Export complete.")


    @staticmethod
    def import_from_csv(file_path : str):
        # Empty the existing table to avoid duplicates
        QTableState4.delete_all()
        start = time.time()

        # Open CSV file in read mode
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)

            # Ignore the first line containing variable names
            next(reader)

            # Insert each row as a new instance in the database
            for row in reader:
                instance = QTableState4(state=row[0], left_score=row[1], right_score=row[2],
                                       up_score=row[3], down_score=row[4])
                db.session.add(instance)

        db.session.commit()
        end = time.time()
        print(f"Import complete.")
        print(f"Time elapsed : {end - start} seconds.")
    
    @staticmethod
    def delete_all():
        QTableState4.query.delete()
        db.session.commit()

class QTableState5(db.Model):
    #16 chiffres pour board (5x5) + 4 chiffres pour pos joueurs + 1 chiffres (1 ou 2) pour turn
	state = db.Column(db.String(30), primary_key = True)
	left_score = db.Column(db.Integer, default=0)
	right_score = db.Column(db.Integer, default=0)
	up_score = db.Column(db.Integer, default=0)
	down_score = db.Column(db.Integer, default=0)
        

@staticmethod
def export5x5(path : str):
# Retrieve all instances of QTableState4 from the database
        instances = QTableState5.query.all()
        fieldnames = ['state', 'left_score', 'right_score', 'up_score', 'down_score']

        # Check if there are instances to export
        if not instances:
            print("ERROR : no instances to export.")
            return

        # Open CSV file in write mode
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames) # Write the first line with the variable names

            # Write the values of each instance in a line of the CSV file
            for instance in instances:
                row = [
                    instance.state,
                    instance.left_score,
                    instance.right_score,
                    instance.up_score,
                    instance.down_score
                ]
                writer.writerow(row)
        
        print(f"Export complete.")


class QTableState6(db.Model):
    #16 chiffres pour board (6x6) + 4 chiffres pour pos joueurs + 1 chiffres (1 ou 2) pour turn
	state = db.Column(db.String(41), primary_key = True)
	left_score = db.Column(db.Integer, default=0)
	right_score = db.Column(db.Integer, default=0)
	up_score = db.Column(db.Integer, default=0)
	down_score = db.Column(db.Integer, default=0)