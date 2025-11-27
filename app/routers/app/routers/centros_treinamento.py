from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app import models, schemas

router = APIRouter(prefix="/centros-treinamento", tags=["Centros de Treinamento"])


@router.post("/", response_model=schemas.CentroTreinoOut, status_code=status.HTTP_201_CREATED)
async def criar_ct(centro: schemas.CentroTreinoCreate, db: AsyncSession = Depends(get_session)):
    novo = models.CentroTreinamento(**centro.dict())
    db.add(novo)
    await db.commit()
    await db.refresh(novo)
    return novo


@router.get("/", response_model=list[schemas.CentroTreinoOut])
async def listar_cts(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(models.CentroTreinamento))
    return result.scalars().all()
