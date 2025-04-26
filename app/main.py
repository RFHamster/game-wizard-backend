from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import agents, chat

app = FastAPI(
    title='Game Wizard',
    description='API minimalista, rápida e escalável para manipulação de oraculos de board game',
    version='1.0.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(agents.router)
app.include_router(chat.router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
