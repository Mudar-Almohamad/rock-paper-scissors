from fastapi import Depends

from api.HTTP.Controllers.Auth.oauth2 import Oauth2
from api.Models.Token import TokenData


class GetCurrentUserRequest:
    def __init__(
            self,
            current_user: TokenData = Depends(Oauth2.get_current_user)
    ):
        self.current_user = current_user
