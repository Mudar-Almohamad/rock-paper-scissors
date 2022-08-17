from fastapi import FastAPI, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.websockets import WebSocketState

from api.HTTP.Controllers.Auth.oauth2 import Oauth2
from api.HTTP.Controllers.Game.Games import Games
from api.HTTP.Controllers.Users.users import Users
from api.HTTP.Controllers.Websocket.SocketManager import SocketManager
from api.HTTP.Requests.User.GetCurrentUserRequest import GetCurrentUserRequest
from api.HTTP.Requests.Games.GetHighestScoreRequest import GetHighestScoreRequest
from api.HTTP.Requests.Websocket.NewSocketRequest import NewSocketRequest
from api.Models.Token import Token, TokenData

app = FastAPI()

sockets = SocketManager()


@app.post("/signup")
async def sign_up(form_data: OAuth2PasswordRequestForm = Depends()):
    return Users.sign_up(form_data.username, form_data.password)


@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return Oauth2.login(form_data.username, form_data.password)


@app.websocket("/websocket")
async def new_socket(request: NewSocketRequest = Depends()):
    if request.websocket.application_state != WebSocketState.DISCONNECTED:
        try:
            user = await Oauth2.get_current_user(request.token[0])
            await sockets.link_connection(
                request.websocket,
                user,
                request.mode,
                request.rounds
            )
        except Exception as err:
            await request.websocket.send_text("This token has expired")
            await request.websocket.close(code=status.WS_1006_ABNORMAL_CLOSURE)


@app.get("/users/me/", response_model=TokenData)
async def who_am_i(request: GetCurrentUserRequest = Depends()):
    return request.current_user


@app.get("/games")
def get_all_games():
    return Games.get_all()


@app.get("/get-highest-score")
def get_highest_score_list(request: GetHighestScoreRequest = Depends()):
    return Games.get_highest_score_list(request)
