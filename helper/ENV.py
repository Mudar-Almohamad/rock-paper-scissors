

import os
from dotenv import load_dotenv

load_dotenv()

APP_KEY = os.getenv('APP_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
