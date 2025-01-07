from app import db

class Game(db.Model):
    __tablename__ = 'games'
    
    id = db.Column(db.String, primary_key=True, unique=True)
    gamemode = db.Column(db.String, nullable=False, default='FFA')
    player_num = db.Column(db.Integer, nullable=False, default=1)
    question_num = db.Column(db.Integer, nullable=False, default=1)
    question_timer = db.Column(db.Integer, nullable=False, default=5)
    category = db.Column(db.String, nullable=False, default='General Knowledge')
    difficulty = db.Column(db.String, nullable=False, default='Easy')
    questions = db.Column(db.String, nullable=False)
    answers = db.Column(db.String, nullable=False)
    correct_answers = db.Column(db.String, nullable=False)

    def config_dict(self):
        return {
            'game_id': self.id,
            'gamemode': self.gamemode,
            'player_num': self.player_num,
            'question_num': self.question_num,
            'question_timer': self.question_timer,
            'category': self.category,
            'difficulty': self.difficulty,
        }
    
    def data_dict(self):
        return {
            'questions': self.questions,
            'answers': self.answers,
            'correct_answers': self.correct_answers,
        }

class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False)
    current_question = db.Column(db.Integer, nullable=True, default=0)
    score = db.Column(db.Integer, default=0)
    correct = db.Column(db.Integer, default=0)
    game_id = db.Column(db.String, db.ForeignKey('games.id'), nullable=False)

    def to_dict(self):
        return {
            'username': self.username,
            'current_question': self.current_question,
            'score': self.score,
            'correct': self.correct,
        }
    