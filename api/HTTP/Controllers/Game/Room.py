import random
import string

from fastapi import WebSocket, status

from api.Models.Token import TokenData
from gamelogic.Game import Game


class Room:

    def __init__(
            self,
            mode: str,
            rounds: int,
            waited_mode=True
    ):
        self.players = []
        self.mode = mode
        self.rounds = rounds
        self.game = None
        self.waited_mode = waited_mode
        self.id = self.generate_unique_id()

    def insert_player(self, player: (WebSocket, TokenData, str, int)):
        self.players.append(player)
        if len(self.players) == 2:
            self.waited_mode = False

    @staticmethod
    async def send_personal_message(websocket: WebSocket, message: str):
        await websocket.send_text(message)

    async def join_room(self, player: (WebSocket, TokenData, str, int)):
        if self.mode == "single":
            self.game = Game(self.rounds, player[1].username)
            await self.single_player(player)
        elif self.mode == "multi":
            if len(self.players) == 2:
                self.game = Game(self.rounds, self.players[0][1].username, self.players[1][1].username)
            await self.multi_player(player)

    async def single_player(self, player: (WebSocket, TokenData, str, int)):
        player_socket, user, mode, rounds = player
        await self.send_personal_message(player_socket, "Player %s enter the game" % user.username)
        await self.send_personal_message(player_socket, "How to play: r for Rock,"
                                                 "\n p for Paper and"
                                                 "\n s for Scissors")
        while True:
            await self.send_personal_message(player_socket, "round %d" % self.game.current_round)
            await self.send_personal_message(player_socket, "it's %s turn." % self.game.current_player)
            move = await self.get_user_entry(player_socket, user)
            self.game.insert_move(user.username, move)
            computer_move = Room.get_computer_move()
            self.game.insert_move(self.game.player2_name, computer_move)
            await self.send_personal_message(player_socket, "player %s move: %s, computer move: %s" % (
                user.username, move, computer_move))
            result = self.game.play()
            await self.send_personal_message(player_socket, result)
            finished = self.game.is_finished_game()
            if finished:
                game_result = self.game.get_game_status()
                await self.send_personal_message(player_socket, game_result)
                await self.send_personal_message(player_socket, "Game End.")
                break
        await self.disconnect()

    async def multi_player(self, player: (WebSocket, TokenData, str, int)):
        player, user, mode, rounds = player
        await self.broadcast("Player %s enter the game" % user.username)
        await self.send_personal_message(player, "How to play: r for Rock,"
                                                 "\n p for Paper and"
                                                 "\n s for Scissors")
        if self.waited_mode:
            await self.send_personal_message(player, "Please Wait another player Ms. %s" % user.username)
        if len(self.players) == 2:
            await self.broadcast("round %d" % self.game.current_round)
            await self.broadcast("it's %s turn." % self.game.current_player)
        while True:
            move = await self.get_user_entry(player, user)
            self.game.insert_move(user.username, move)
            if self.game.has_moves_complete():
                await self.broadcast(
                    "player %s move: %s, player %s move: %s" % (
                        self.game.player1_name, self.game.moves[self.game.player1_name], self.game.player2_name,
                        self.game.moves[self.game.player2_name]))
                result = self.game.play()
                await self.broadcast(result)
                finished = self.game.is_finished_game()
                if finished:
                    game_result = self.game.get_game_status()
                    await self.broadcast(game_result)
                    await self.broadcast("Game End.")
                    break
                await self.broadcast("round %d" % self.game.current_round)
            else:
                await self.broadcast("it's %s turn." % self.game.current_player)

        await self.disconnect()

    async def get_user_entry(self, player: WebSocket, user: TokenData):
        while True:
            move = await player.receive_text()
            if await self.check_player_move(player, user, move):
                return move

    async def check_player_move(self, player: WebSocket, user: TokenData, move):
        if self.game:
            if not self.game.check_user(user.username):
                await self.send_personal_message(player, "it's not your turn")
                return False
            elif self.game.check_move(move):
                return True
            else:
                await self.send_personal_message(player, "Wrong entry")
                return False
        else:
            await self.send_personal_message(player, "Please Wait another player Ms. %s" % user.username)
            return False

    async def broadcast(self, message: str):
        for connection in self.players:
            if connection:
                await self.send_personal_message(connection[0], message)

    async def disconnect(self, code=status.WS_1000_NORMAL_CLOSURE, reason="Game End"):
        for connection in self.players:
            if connection:
                await connection[0].close(code=code, reason=reason)

    @staticmethod
    def get_computer_move():
        moves = ("r", "p", "s")
        return moves[int(len(moves) * random.random())]

    def get_game(self) -> dict:
        data = dict()
        data['id'] = self.id
        data['players'] = [self.game.player1_name, self.game.player2_name]
        data['mode'] = self.mode
        data['rounds'] = self.rounds
        data['moves'] = self.game.all_moves
        data['player1_points'] = self.game.player1_points
        data['player2_points'] = self.game.player2_points
        data['result'] = self.game.result

        return data

    @staticmethod
    def generate_unique_id():
        unique_id = ''.join([random.choice(string.ascii_letters
                                           + string.digits) for n in range(32)])
        return unique_id
