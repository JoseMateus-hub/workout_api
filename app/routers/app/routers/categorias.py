from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app import models, schemas

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.post("/", response_model=schemas.CategoriaOut, status_code=status.HTTP_201_CREATED)
async def criar_categoria(categoria: schemas.CategoriaCreate, db: AsyncSession = Depends(get_session)):
    nova = models.Categoria(**categoria.dict())
    db.add(nova)
    await db.commit()
    await db.refresh(nova)
    return nova


@router.get("/", response_model=list[schemas.CategoriaOut])
async def listar_categorias(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(models.Categoria))
    return result.scalars().all()
