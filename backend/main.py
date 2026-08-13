from fastapi import FastAPI

from routers.auth import router as auth_router
from routers.prestazioni import router as prestazioni_router
from routers.sedi import router as sedi_router
from routers.specialita import router as specialita_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(specialita_router)
app.include_router(prestazioni_router)
app.include_router(sedi_router)


@app.get("/", tags=["root"], summary="Messaggio di benvenuto")
async def root():
    return {"message": "Hello World"}


@app.get("/health", tags=["root"], summary="Stato di salute del servizio")
async def health():
    return {"status": "ok"}