from uuid import UUID
from pydantic import BaseModel


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


# customização GET ALL
class AtletaListResponse(BaseModel):
    nome: str
    categoria: str
    centro_treinamento: str
