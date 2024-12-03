class Player:
    def __init__(self, game_id:str, username:str, score:int, db_connection) -> None:
        self.game_id = game_id
        self.username = username
        self.score = score
        self.db_connection = db_connection
        self.db_cursor = self.db_connection.cursor()
        self.init_player_table()
        
    def init_player_table(self) -> None:
        try:
            self.db_connection.execute("PRAGMA foreign_keys = ON;")
            self.db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    username TEXT PRIMARY KEY,
                    score INTEGER DEFAULT 0,
                    game_id TEXT NOT NULL,
                    FOREIGN KEY (game_id) REFERENCES games(game_id)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE
                );
            """)
        except Exception as e:
            print(e)
            raise Exception("Error initializing player table")
    
    def create_player(self) -> None:
        try:
            self.db_cursor.execute("""
                INSERT INTO players (username, score, game_id)
                VALUES (?, ?, ?)
            """, (self.username, self.score, self.game_id))
            self.db_connection.commit()
        except Exception as e:
            print(e)
            raise Exception("Error creating player")
    
    def get_player(self, username, game_id):
        try:
            self.db_cursor.execute("""
                SELECT * FROM players WHERE username = ? AND game_id = ?
            """, (username, game_id))
            player = self.db_cursor.fetchone()
            if player:
                self.username = player[0]
                self.score = player[1]
                self.game_id = player[2]
                return self
            else:
                raise Exception("Player not found")
        except Exception as e:
            print(e)
            raise Exception("Error getting player")
    
    def update_score(self, max_time:int, curr_time:int, correct:bool) -> None:
        try:
            self.score = self.calc_weight_score(max_time, curr_time, correct)
            self.db_cursor.execute("""
                UPDATE players SET score = ? WHERE username =
                    (SELECT username FROM players WHERE game_id = ? LIMIT 1)
            """, (self.score, self.game_id))
            self.db_connection.commit()
        except Exception as e:
            print(e)
            raise Exception("Error updating score")
    
    def calc_weight_score(self, max_time:int, curr_time:int, correct:bool) -> int:
        """
        helper function to calculate the weighted score for the user
        """
        if (correct):
            return self.score + (1000)
        else:
            return self.score - (1000)