import sqlite3

database = 'database.db'

# clears game table in database
def clear_game_table():
    try:
        db = sqlite3.connect(database)
        cursor = db.cursor()
        cursor.execute('DROP TABLE IF EXISTS games;')
        cursor.execute('DROP TABLE IF EXISTS players;')
        db.commit()
        db.close()
    except:
        print('error occurred clearing game table')

def get_all_games():
    try:
        db = sqlite3.connect(database)
        cursor = db.cursor()
        cursor.execute('SELECT * FROM games')
        games = cursor.fetchall()
        db.close()
        for game in games:
            print(game[0])
    except:
        print('error occurred getting all games')

def get_all_players():
    try:
        db = sqlite3.connect(database)
        cursor = db.cursor()
        cursor.execute('SELECT * FROM players')
        players = cursor.fetchall()
        db.close()
        for player in players:
            print(player[3])
    except:
        print('error occurred getting all players')

get_all_players()
# get_all_games()
# clear_game_table()