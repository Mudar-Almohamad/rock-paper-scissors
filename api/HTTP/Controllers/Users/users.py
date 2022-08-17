

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from helper.DB import check_user_exist, create_new_user
from api.HTTP.Controllers.Auth.oauth2 import Oauth2



class Users:
    @staticmethod
    def sign_up(username: str, password: str):
        if check_user_exist(username):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is exist")
        else:
            result = create_new_user(username, Oauth2.pwd_context.hash(password))
            if result:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "message": f"Done! User {username} has been created. you can now login into your account"
                    }
                )
            else:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"message": "Internal server error"}
                )
