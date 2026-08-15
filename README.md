# TrapFall

TrapFall is a two-player browser-based strategy game built with React and FastAPI. Players create or join a room, place hidden traps, and then take turns moving across a 10×10 board while trying to reach the opponent's side.

The project was built to learn how a real-time multiplayer application works, including authentication, APIs, WebSockets, game state, PostgreSQL, migrations, and deployment.

### Tech Stack

React, JavaScript, Vite, Python, FastAPI, WebSockets, SQLAlchemy, PostgreSQL, Alembic, JWT, and Argon2.

The frontend is deployed on Vercel and the backend/database are deployed on Railway.

### Current Features

Users can register and log in, create rooms, join rooms using a room code, play against another player, and reconnect to an existing room/game session.

The backend manages the game state while WebSockets are used for real-time lobby and game updates.

The database stores user information and Alembic is used for migrations.

### Limitations

This is an MVP and is not production-ready.

There is currently no email ownership verification, password reset, proper server-side logout/token invalidation, matchmaking, rate limiting, or serious anti-cheat system.

Active rooms and games are currently stored in backend memory, so the application is not designed for multiple backend instances.

Reconnect handling is implemented, but disconnect and reconnect edge cases are still basic.

There may also be bugs that I have not discovered yet. Some edge cases, especially around WebSockets, reconnects, simultaneous actions, and deployment/network conditions, have not been fully tested.

### Project Status

TrapFall is deployed and playable, but it is still an ongoing project. The goal is to continue improving the architecture, reliability, game logic, and overall user experience as I find problems and learn from them.
