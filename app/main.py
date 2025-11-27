from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.routers import atletas, categorias, centros_treinamento

app = FastAPI(
    title="Workout API",
    version="1.0.0",
    description="API assíncrona para competição de CrossFit."
)

app.include_router(categorias.router)
app.include_router(centros_treinamento.router)
app.include_router(atletas.router)

add_pagination(app)
