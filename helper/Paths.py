import os
from urllib.parse import urljoin
from pathlib import Path

def _check_if_root_dir(path):
    acc = 0
    container = ['api', 'db', 'gamelogic', 'logger', 'helper',
                 'venv', '.gitignore', 'requirements.txt', 'Procfile',
                 'Procfile.windows', 'README.md', 'runtime.txt', '.env'
                 ]
    for file in os.listdir(path):
        if file in container:
            acc += 1
    if acc > int(len(container) * 50 / 100):
        return True
    return False


def root_dir():
    absolutepath = os.path.abspath('')
    while not _check_if_root_dir(absolutepath):
        absolutepath = os.path.dirname(absolutepath)
    return absolutepath


def logger_dir():
    return os.path.join(root_dir(), 'logger')


def db_dir():
    return os.path.join(root_dir(), 'db')


def enums_dir():
    return os.path.join(root_dir(), 'enums')


def api_dir():
    return os.path.join(root_dir(), 'api')


def path_from_root(relative_path):
    return os.path.join(root_dir(), relative_path)


def make_dirs(*paths):
    try:
        for path in paths:
            os.makedirs(os.path.normpath(path))
    except OSError:
        pass


def delete_dir(absolute):
    try:
        os.rmdir(absolute)
    except OSError:
        pass


def join_urls(base_url, path):
    result = urljoin(base_url, path)
    return result

def create_file_not_exist(path):
    fle = Path(path)
    fle.touch(exist_ok=True)
