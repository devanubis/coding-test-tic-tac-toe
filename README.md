# Introduction
This is a Tic-Tac-Toe REST API which runs as a Django app.

# Install and setup
Start by creating a python virtual environment, from the project directory (same as this README.md)
```
python -m venv ./venv
source ./venv/bin/activate
```
Next install the requirements
```
pip install -r requirements.txt
```
And then initialise the Django database with:
```
python tic_tac_toe/manage.py migrate
```
To start the Django server:
```
python tic_tac_toe/manage.py runserver
```
From there, you can access the API end points at:
```
localhost:8000
```
There is a web browser UI at API end points for convenience,
but the API can also be accessed through `curl` etc.

# API
## Start a new game
To start a new game of tic-tac-toe, make a POST request to:
```
/game/new
```

The response will be a JSON object, with a key (UUID) for the game.
You will need this key to access the game state and make moves. 

Optionally your POST request may include a JSON object with the following
values:
```
player:
    To choose yor player marker.
    This can be either:
        X (default)
        O (letter not number)
    The character must be uppercase.

opponent_level:
    To choose the opponent's playing strategy. This can be either:
        B (defaut, opponent will make the "best" move, see the  tictactoe-py library)
        R (opponent will make random moves)
```
e.g.
```
{
  "player": "O",
  "opponent_level": "R"
}
```

## Accessing the game

Once you have a game key, you can access the game with a GET request to:
```
/game/{key}
```

This will return a JSON object with the game's current state e.g.
```
{
    "key": "66e94f01-3618-466b-84ed-9dcde432f0b3",
    "player": "X",
    "opponent_level": "B",
    "board": [
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null
    ]
}
```

The board is a simple JSON array, with 9 positions.
The positions are ordered top to bottom, left to right e.g.:
1|4|7
2|5|8
3|6|9

The columns and rows are each indexed from 1 to 3 e.g. 
* position 5 is column 2 row 2
* position 1 is column 1 row 1
position 6 is column 2 row 3

## Making a move

You as the human player will always get the first move in a game. 

To make a move pick the column and row to place a marker in,

e.g. to play in the center position:
```
{
  "col": 2,
  "row": 2
}
```

Each time you POST a move, the opponent will then play its own move,
and the API response will contain the state of the game board after
both moves have been made.

## End game

If a move results in the game being won, then the JSON response will
include a "winner" key, with the winning player's mark.

Once a game has been won, it will no loner accept new moves. Subsequent GET
requests to view the game's state will also include the "winner" key.

### Ties
In the case of a tie or stalemate, the "winner" key will be set to "T".
The same end-game conditions apply, no further moves may be made.

## Request responses

### Successful requests
Successful GET or POST requests will receive an apropriate HTTP response code,
along with their JSON response body. 

e.g.
* Creating a new game receives a 201 response
* GETing a game state receives a 200 response
* Playing a legal move receives a 200 response

### Failed requests

#### Unknown game
If the game key is not found in the database, a 404 response will be returned. 

#### Invalid inputs
If invalid values are given for any of the JSON POST data for creating a new
game or playing a move then a 400 response will be returned, along with a JSON
object explaining the validation issue.

#### Illegal moves
Requests for illegal moves (i.e. playing to an already occupied position) will 
receive an HTTP 400 response.

Similarly, for games which have completed, subsequent requests to play
additional moves will also receive a 400 response.

#### Internal error states
It should not be possible to submit a move which puts the player board into an
illegal state. However, should a game enter an illegal state through other
means, then GET or POST requests for that game will return a 500 response.

# Improvements for future
## Two-player
There's currently only a single player mode, but it would be fairly easy to add
a two-player mode by keeping track of the last player to play a turn, and 
allowing the move POST requests to accept a player marker.

It would be best to use sessions to keep lock the players once they've made
their first moves.

## House-keeping
It would probably be worth recording the date-time of the last move in a game,
to make it easier to house-keep old compelted/abandoned games. But since this
is just a toy app it's not worth having a script to do that and it's easier to
just drop and rebuild the database.
