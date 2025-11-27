from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi_pagination import add_pagination, Page, paginate
from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint, select
from sqlalchemy.orm import declarative_base, relationship, selectinload
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from uuid import UUID
import uuid

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/workout"

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

class Categoria(Base):
    __tablename__ = "categorias"

    pk_id = Column(Integer, primary_key=True)
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    nome = Column(String(40), nullable=False, unique=True)

    atletas = relationship("Atleta", back_populates="categoria")

class CentroTreinamento(Base):
    __tablename__ = "centros_treinamento"

    pk_id = Column(Integer, primary_key=True)
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    nome = Column(String(20), nullable=False, unique=True)
    endereco = Column(String(60), nullable=False)
    proprietario = Column(String(30), nullable=False)

    atletas = relationship("Atleta", back_populates="centro_treinamento")

class Atleta(Base):
    __tablename__ = "atletas"
    __table_args__ = (UniqueConstraint("cpf", name="uq_atleta_cpf"),)

    pk_id = Column(Integer, primary_key=True)
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    nome = Column(String(50), nullable=False)
    cpf = Column(String(11), nullable=False)
    idade = Column(Integer, nullable=False)
    peso = Column(Float, nullable=False)
    altura = Column(Float, nullable=False)
    sexo = Column(String(1), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.pk_id"), nullable=False)
    centro_treinamento_id = Column(Integer, ForeignKey("centros_treinamento.pk_id"), nullable=False)

    categoria = relationship("Categoria", back_populates="atletas")
    centro_treinamento = relationship("CentroTreinamento", back_populates="atletas")

class CategoriaBase(BaseModel):
    nome: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaOut(CategoriaBase):
    id: UUID
    class Config:
        from_attributes = True

class CentroTreinoBase(BaseModel):
    nome: str
    endereco: str
    proprietario: str

class CentroTreinoCreate(CentroTreinoBase):
    pass

class CentroTreinoOut(CentroTreinoBase):
    id: UUID
    class Config:
        from_attributes = True

class AtletaBase(BaseModel):
    nome: str
    cpf: str
    idade: int
    peso: float
    altura: float
    sexo: str
    categoria_id: int
    centro_treinamento_id: int

class AtletaCreate(AtletaBase):
    pass

class AtletaOut(AtletaBase):
    id: UUID
    class Config:
        from_attributes = True

class AtletaListResponse(BaseModel):
    nome: str
    categoria: str
    centro_treinamento: str

app = FastAPI(title="Workout API", version="1.0.0")

router_categorias = APIRouter(prefix="/categorias", tags=["Categorias"])

@router_categorias.post("/", response_model=CategoriaOut, status_code=status.HTTP_201_CREATED)
async def criar_categoria(categoria: CategoriaCreate, db: AsyncSession = Depends(get_session)):
    nova = Categoria(**categoria.dict())
    db.add(nova)
    await db.commit()
    await db.refresh(nova)
    return nova

@router_categorias.get("/", response_model=list[CategoriaOut])
async def listar_categorias(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Categoria))
    return result.scalars().all()

app.include_router(router_categorias)

router_ct = APIRouter(prefix="/centros-treinamento", tags=["Centros de Treinamento"])

@router_ct.post("/", response_model=CentroTreinoOut, status_code=status.HTTP_201_CREATED)
async def criar_ct(centro: CentroTreinoCreate, db: AsyncSession = Depends(get_session)):
    novo = CentroTreinamento(**centro.dict())
    db.add(novo)
    await db.commit()
    await db.refresh(novo)
    return novo

@router_ct.get("/", response_model=list[CentroTreinoOut])
async def listar_ct(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CentroTreinamento))
    return result.scalars().all()

app.include_router(router_ct)

router_atletas = APIRouter(prefix="/atletas", tags=["Atletas"])

@router_atletas.post("/", response_model=AtletaOut)
async def criar_atleta(atleta: AtletaCreate, db: AsyncSession = Depends(get_session)):
    novo = Atleta(**atleta.dict())
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

@router_atletas.get("/", response_model=Page[AtletaListResponse])
async def listar_atletas(
    nome: str | None = None,
    cpf: str | None = None,
    db: AsyncSession = Depends(get_session)
):
    query = (
        select(Atleta)
        .options(
            selectinload(Atleta.categoria),
            selectinload(Atleta.centro_treinamento)
        )
    )

    if nome:
        query = query.where(Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.where(Atleta.cpf == cpf)

    result = await db.execute(query)
    atletas = result.scalars().all()

    resposta = [
        AtletaListResponse(
            nome=a.nome,
            categoria=a.categoria.nome,
            centro_treinamento=a.centro_treinamento.nome
        )
        for a in atletas
    ]

    return paginate(resposta)

app.include_router(router_atletas)

add_pagination(app)
