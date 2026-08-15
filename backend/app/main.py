from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.auth.routes import router as auth_router
from backend.app.routes.room import router as room_router
from backend.app.websocket.routes import router as websocket_router

app = FastAPI(title='Trap Game')


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://trapfall.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(room_router)
app.include_router(websocket_router)

@app.get('/')
def root():
    return 'hello'
    

