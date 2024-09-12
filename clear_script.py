import sqlite3

database = 'database.db'

# clears game table in database
def clear_game_table():
    try:
        db = sqlite3.connect(database)
        cursor = db.cursor()
        cursor.execute('DROP TABLE IF EXISTS games')
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
            print(game[3])
    except:
        print('error occurred getting all games')

get_all_games()