from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Game(BaseModel):
    item_id: int
    name: str
    price: float
    release: date


db_games = [
    Game(item_id=1, name="Magic to Master", price=49.99, release=date(2023, 1, 8)),
    Game(item_id=2, name="Golden Axe Warrior", price=59.99, release=date(1991, 6, 1)),
]


@app.get("/db_games", response_model=list[Game])
async def read_games():
    return db_games


@app.get("/db_games/{item_id}", response_model=Game)
async def read_game(item_id: int):
    game = next((game for game in db_games if game.item_id == item_id), None)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


# Создание нового пользователя
@app.post("/db_games/", response_model=Game)
async def create_user(game: Game):
    db_games.append(game)
    return game


# Обновление данных пользователя


@app.put("/db_games/{item_id}", response_model=Game)
async def update_user(item_id: int, game: Game):
    for db_game in db_games:
        if db_game.item_id == item_id:
            db_game.name = game.name
            db_game.price = game.price
            db_game.release = game.release
            return db_game
    raise HTTPException(status_code=404, detail="Game not found")


# Удаление пользователя по его ID
@app.delete("/db_games/{item_id}", response_model=Game)
async def delete_user(item_id: int):
    db_game_index = next((i for i, u in enumerate(db_games) if u.item_id == item_id), None)
    if db_game_index is None:
        raise HTTPException(status_code=404, detail="Game not found")
    deleted_user = db_games.pop(db_game_index)
    return deleted_user
