from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import date, datetime
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, ForeignKey,
    Numeric, Boolean, Enum, Text,DECIMAL,Double
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
Base = declarative_base()

class Reserva(Base):
    __tablename__ = "reserva"
    id_reserva = Column(Integer,primary_key=True,autoincrement=True)
    id_hospede_principal = Column(Integer,ForeignKey("hospede.id_hospede"),nullable=False)
    numero_quarto = Column(Integer,ForeignKey("quarto.numero_quarto"),nullable=False)
    data_checkin = Column(Date,nullable=False)
    data_checkout = Column(Date,nullable=False)
    status_reserva = Column(String(30),nullable=False)
    valor_total = Column(DECIMAL(10,2),nullable=False)
class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer,primary_key=True,autoincrement=True)
    nome_completo = Column(String(1000),nullable=False)
    email = Column(String(500),nullable=False)
    senha_hash = Column(String(2000),nullable=False)
    perfil_id = Column(Integer,ForeignKey("perfil.id"))

class Hospede(Base):
    __tablename__ = "hospede"
    id_hospede = Column(Integer,primary_key=True,autoincrement=True)
    nome_completo = Column(String(150),nullable=False)
    documento = Column(String(50),unique=True,nullable=False)
    telefone = Column(String(20))
    email = Column(String(100),unique=True)
    id_usuario_sistema = Column(Integer,ForeignKey("usuario.id"))

class Tipo_de_quarto(Base):
     __tablename__ = 'tipo_de_quarto'
     id_tipo = Column(Integer,primary_key=True,autoincrement=True)
     nome_tipo = Column(String(50),nullable=False,unique=True)
     capacidade_maxima = Column(Integer,nullable=False)
     preco_diaria_base = Column(DECIMAL(precision=10,scale=2),nullable=False)
     descricao = Column(Text)

     quartos = relationship("Quarto",back_populates="tipo_de_quarto")

class Quarto(Base):
    __tablename__ = 'quarto'
    numero_quarto = Column(Integer,primary_key=True,unique=True)
    id_tipo = Column(Integer,ForeignKey("tipo_de_quarto.id_tipo"))
    status_limpeza = Column(String(20),default='sujo',nullable=False)
    localizacao = Column(String(50))

    tipo_de_quarto = relationship("Tipo_de_quarto", back_populates="quartos")

class Perfil(Base):
    __tablename__ = 'perfil'
    id = Column(Integer,primary_key=True,autoincrement=True)
    nome_perfil = Column(String(200),unique=True,nullable=False)

