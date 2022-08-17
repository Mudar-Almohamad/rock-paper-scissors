from fastapi import status, HTTPException
from fastapi.responses import JSONResponse

from api.HTTP.Requests.Games.GetHighestScoreRequest import GetHighestScoreRequest
from api.Models.Token import TokenData
from helper.DB import get_all_games, get_highest_score


class Games:
    def __init__(self):
        pass

    @staticmethod
    def get_all():
        return JSONResponse(content=get_all_games(), status_code=status.HTTP_200_OK)

    @staticmethod
    def get_highest_score_list(request: GetHighestScoreRequest):
        if request.max_scores <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="max_scores must be higher than 1"
            )
        high_game = get_highest_score(request.max_scores)
        if high_game:
            return JSONResponse(content=high_game, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "message": "No Games Found"
                }
            )
