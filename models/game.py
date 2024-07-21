class Game:
    def __init__(self, room_id):
        self.room_id = room_id
        self.state = "waiting"
        self.questions = [
            {"question": "which of the following animals is a mammal?", "answers": ["dog", "cat", "fish", "bird"], "correct": "dog"},
            {"question": "which of the following animals is a reptile?", "answers": ["dog", "cat", "fish", "bird"], "correct": "fish"},
            ]
        self.current_question = 1
        self.players = []
        self.timer = 30
        self.active_connections = 0
        
    def update_active_connections(self, connections):
        """
        returns tuple of (connections, error)
        """
        if (connections < 0 or connections > 2):
            return (self.active_connections, "room is full")
        
        self.active_connections = connections
        return (self.active_connections, None)
    
    def update_game_state(self, state):
        self.state = state
        return (self.state, False)
    
    def add_player(self, username):
        self.players.append(username)