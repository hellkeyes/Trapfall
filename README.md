# TRAPFALL

TRAPFALL is a real-time two-player strategy game where two players move across a 10 × 10 board, place hidden traps, and try to reach the opponent's side without losing all their lives.


### About

The game has two players who join the same room. Before the game starts, both players place traps on the board and get a short period to memorize the board.

Once movement begins, players take turns moving one tile at a time. When a player steps on a trap, they lose a life and are moved two steps backwards based on the path they previously took. The trap is then removed, so it can only be triggered once.

A player can win by reaching the opponent's side of the board. A player is also eliminated when they lose all three lives.

The backend manages the actual game state and sends changes to both players through WebSockets. This means the client does not decide whether a move is valid or whether someone has won. The server handles those decisions and broadcasts the result.

### Features

- User authentication using JWT
- Two-player rooms
- Player assignment
- Real-time communication using WebSockets
- Server-side movement and turn validation
- 10 × 10 game board
- Trap placement phase
- Hidden traps during the movement phase
- Three lives per player
- Trap knockback based on movement history
- One-time trap activation
- Player elimination
- Win condition based on reaching the opponent's side
- Player reconnection handling
- Room termination when a disconnected player does not reconnect
- Real-time synchronization of player positions, turns, lives, traps, and game phases
- In-game notifications

### Game Rules

- Board: 10 × 10
- Players: 2
- Lives: 3 per player
- Traps: 8 per player
- Trap placement: 60 seconds
- Memorization: 15 seconds
- Players move one tile per turn
- Triggering a trap removes 1 life
- Triggering a trap moves the player two steps backwards
- A triggered trap is removed
- Reaching the opponent's side wins the game
- Losing all three lives eliminates the player

### Project Status

**V1**

The core game and real-time two-player functionality are complete.

I plan to improve the project further with responsive/mobile controls and additional visual polish, but those improvements are not required for the current version.

### What I Learned

I built TRAPFALL mainly as a way to learn full-stack development through something I actually wanted to make.

While building it, I worked with React state, FastAPI routes, PostgreSQL, JWT authentication, WebSocket connections, room management, real-time state synchronization, server-side validation, and handling disconnects and reconnects.

A lot of the project was also about figuring out what happens when things go wrong, such as invalid moves, disconnected players, players reconnecting again in the game, missing rooms, players trying to start a game too early, and players reaching a game-ending condition.

The code and design are not perfect. There maybe a bug that I didn't find. The goal of the project was to build something of my own and learn by actually building and debugging it.
