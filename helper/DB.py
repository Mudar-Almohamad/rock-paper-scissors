import json
import os
from json import JSONDecodeError

from helper.Paths import db_dir, create_file_not_exist


def get_file_name(file: str):
    files = {
        'games': 'games.json',
        'users': 'users.json'
    }
    return files[file]


def get_all_users() -> dict:
    path = os.path.join(db_dir(), get_file_name('users'))
    create_file_not_exist(path)
    with open(path, 'r') as f:
        users = json.loads(f.read())
        return users


def check_user_exist(username: str, get_user_if_exist=False) -> bool or dict:
    try:
        user = get_all_users().get(username)
        if user:
            return user if get_user_if_exist else True
        else:
            return None if get_user_if_exist else False
    except JSONDecodeError:
        return False


def create_new_user(username: str, password: str) -> bool:
    file_path = os.path.join(db_dir(), get_file_name('users'))
    with open(file_path, 'r') as f:
        try:
            users = json.loads(f.read())
        except JSONDecodeError:
            users = dict()
    users[username] = {
        'username': username,
        'password': password
    }
    users = json.dumps(users)
    with open(file_path, 'w') as f:
        f.write(users)
        return True


def get_all_games() -> dict:
    path = os.path.join(db_dir(), get_file_name('games'))
    create_file_not_exist(path)
    with open(path, 'r') as f:
        games = json.loads(f.read())
        return games


def create_new_game(game: dict):
    file_path = os.path.join(db_dir(), get_file_name('games'))
    create_file_not_exist(file_path)
    with open(file_path, 'r') as f:
        try:
            games = json.loads(f.read())
            if 'games' not in games:
                games['games'] = []
            else:
                for prev_game in games['games']:
                    if prev_game['id'] == game['id']:
                        return False
        except JSONDecodeError:
            games = {
                'games': []
            }

    games['games'].append(game)

    games = json.dumps(games)
    with open(file_path, 'w') as f:
        f.write(games)
        return True


def get_highest_score(max_scores_count: int):
    path = os.path.join(db_dir(), get_file_name('games'))
    create_file_not_exist(path)
    with open(path, 'r') as f:
        games = json.loads(f.read())
    players = set()
    for game in games['games']:
        players.add(game['players'][0])
        players.add(game['players'][1])

    try:
        players.remove('Computer')
    except KeyError:
        pass
    scores = []
    for player in players:
        wins = 0
        for game in games['games']:
            if player in game['result']:
                wins += 1
        if wins > 0:
            scores.append({
                'player': player,
                'wins': wins
            })

    if not scores:
        return scores
    new_scores = []
    for _ in range(max_scores_count):
        if scores:
            max_score = scores[0]
            for score in scores[1:]:
                if max_score['wins'] < score['wins']:
                    max_score = score
            if max_score:
                new_scores.append(max_score)
                scores.remove(max_score)
    return new_scores
