from fastapi import Query


class GetHighestScoreRequest:
    def __init__(
            self,
            max_scores: int = Query(default=1),
    ):
        self.max_scores = max_scores
