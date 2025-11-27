from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, paginate

from app.database import get_session
from app import models, schemas

router = APIRouter(prefix="/atletas", tags=["Atletas"])


@router.post("/", response_model=schemas.AtletaOut)
async def criar_atleta(atleta: schemas.AtletaCreate, db: AsyncSession = Depends(get_session)):
    novo = models.Atleta(**atleta.dict())

    try:
        db.add(novo)
        await db.commit()
        await db.refresh(novo)
        return novo

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=303,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}"
        )


@router.get("/", response_model=Page[schemas.AtletaListResponse])
async def listar_atletas(
    nome: str | None = None,
    cpf: str | None = None,
    db: AsyncSession = Depends(get_session)
):
    query = (
        select(models.Atleta)
        .options(
            selectinload(models.Atleta.categoria),
            selectinload(models.Atleta.centro_treinamento)
        )
    )

    if nome:
        query = query.where(models.Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.where(models.Atleta.cpf == cpf)

    result = await db.execute(query)
    atletas = result.scalars().all()

    resposta = [
        schemas.AtletaListResponse(
            nome=a.nome,
            categoria=a.categoria.nome,
            centro_treinamento=a.centro_treinamento.nome,
        )
        for a in atletas
    ]

    return paginate(resposta)
