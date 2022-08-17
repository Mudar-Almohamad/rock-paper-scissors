from fastapi import Depends, WebSocket, Query

from api.HTTP.Controllers.Websocket.SocketManager import SocketManager


class NewSocketRequest:
    def __init__(
            self,
            websocket: WebSocket,
            token: str = Depends(SocketManager.can_make_connection),
            mode: str = Query(default="single"),
            rounds: int = Query(default=1)
    ):
        self.websocket = websocket
        self.token = token,
        self.mode = mode
        self.rounds = rounds
