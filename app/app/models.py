import uuid
from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import Base


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
    __table_args__ = (
        UniqueConstraint("cpf", name="uq_atleta_cpf"),
    )

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
