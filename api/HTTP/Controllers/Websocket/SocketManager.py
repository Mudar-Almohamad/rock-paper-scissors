from typing import List, Union

from fastapi import Query, WebSocket, status

from api.HTTP.Controllers.Game.Room import Room
from api.Models.Token import TokenData
from helper.DB import create_new_game


class SocketManager(object):
    def __init__(self):
        self.online_rooms: List[Room] = []

    async def link_connection(self, websocket: WebSocket, user: TokenData, mode: str, rounds: int):
        room = self.get_available_room(mode, rounds)
        room.insert_player((websocket, user, mode, rounds))
        if room not in self.online_rooms:
            self.online_rooms.append(room)
        await room.join_room((websocket, user, mode, rounds))
        if room in self.online_rooms:
            create_new_game(room.get_game())
            self.online_rooms.remove(room)

    def get_available_room(self, mode: str, rounds: int) -> Room:
        if mode == "single":
            return Room(mode, rounds, waited_mode=False)
        else:
            for room in self.online_rooms:
                if room.waited_mode:
                    if room.rounds == rounds:
                        room.waited_mode = False
                        return room
        return Room(mode, rounds)

    @staticmethod
    async def can_make_connection(
            websocket: WebSocket,
            token: Union[str, None] = Query(default=None),
            mode: str = Query(default="single"),
            rounds: int = Query(default=1)
    ):
        await websocket.accept()
        if not token:
            await websocket.send_text("you must log in to play")
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        if mode != "single" and mode != "multi":
            await websocket.send_text("mode must be `single` of `multi`")
            await websocket.close(code=status.WS_1003_UNSUPPORTED_DATA)
        if rounds <= 0:
            await websocket.send_text("rounds mustn't be less than zero")
            await websocket.close(code=status.WS_1003_UNSUPPORTED_DATA)
        return token
