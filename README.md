# Rock Paper Scissors

## Getting started

Rock Paper Scissors game.

# How to use

## if you want to change APP_KEY (recommended)
### first: you need openssl.
 - if you have git on your machine you can go to `C:\Program Files\Git\usr\bin` and open `openssl.exe` and run `rand -hex 32`, copy string and paste in `.env` file in this project
 - else install openssl and run on cmd `openssl rand -hex 32`, copy string and paste in `.env` file in this project
## if you don't want to change APP_KEY, just skip previous operation.
- Then follow these steps:
1. install python `3.9.0` version
2. open project in Pycharm IDE then open terminal (make sure terminal is cmd not powershell) and follow these steps
    ```
    - pip install virtualenv
    - virtualenv venv
    - cd venv && cd Scripts
    - activate
    ```
3. then in terminal enter: `pip install -r requirements.txt`
4. finally run this command: `uvicorn api.FastAPI.FastAPI:app --reload`
5. Done


