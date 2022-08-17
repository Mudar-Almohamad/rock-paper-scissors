

class Game:
    win_logic = {
        'rp': '01',
        'rs': '10',
        'pr': '10',
        'ps': '01',
        'sr': '01',
        'sp': '10',
    }

    def __init__(self, max_rounds, player1_name, player2_name="Computer"):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.current_round = 1
        self.current_player = self.player1_name
        self.max_rounds = max_rounds
        self.player1_points = 0
        self.player2_points = 0
        self.moves = {
            self.player1_name: "",
            self.player2_name: ""
        }
        self.all_moves = {}
        self.result = ""

    def play(self):
        self.all_moves['round' + str(self.current_round)] = self.moves.copy()
        player1_move, player2_move = self.moves[self.player1_name], self.moves[self.player2_name]
        self.current_round += 1
        if player1_move == player2_move:
            return "Draw"

        result = Game.win_logic[player1_move + player2_move]
        if result == '01':
            self.player2_points += 1
            result_inform = "Point for %s" % self.player2_name
        else:
            self.player1_points += 1
            result_inform = "Point for %s" % self.player1_name

        self.reset_moves()
        return result_inform

    def insert_move(self, username, move):
        self.moves[username] = move
        self.swap_players()

    def has_moves_complete(self):
        return len(self.moves[self.player1_name]) and len(self.moves[self.player2_name])

    def reset_moves(self):
        self.moves[self.player1_name] = ""
        self.moves[self.player2_name] = ""

    def swap_players(self):
        if self.current_player == self.player1_name:
            self.current_player = self.player2_name
        else:
            self.current_player = self.player1_name

    @staticmethod
    def check_move(move: str):
        move = move.lower()
        return move in {"r", "p", "s"}

    def check_user(self, username: str):
        return self.current_player == username

    def is_finished_game(self):
        return self.current_round > self.max_rounds

    def get_game_status(self):
        if self.player1_points == self.player2_points:
            self.result = "Draw"
            return "It's draw"
        elif self.player1_points > self.player2_points:
            self.result = "%s wins" % self.player1_name
            return self.result
        elif self.player1_points < self.player2_points:
            self.result = "%s wins" % self.player2_name
            return self.result