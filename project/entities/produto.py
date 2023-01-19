from sqlalchemy import Column, String , Float
from sqlalchemy.sql.functions import percentile_cont
from sqlalchemy.sql.sqltypes import Integer
from marshmallow import Schema, fields

from .entity import Entity, Base


class Produto(Entity, Base):
    __tablename__ = 'produto'

    nome = Column(String)
    description = Column(String)
    editora = Column(String)
    preco = Column(Float)
    faixa_etaria = Column(Integer)
    numero_de_jogadores = Column(String)
    



    def __init__(self, nome, description,editora,preco,faixa_etaria,numero_de_jogadores):
        Entity.__init__(self)
        self.nome = nome
        self.description = description
        self.editora = editora
        self.preco = preco
        self.faixa_etaria = faixa_etaria
        self.numero_de_jogadores = numero_de_jogadores
        

class ProdutoSchema(Schema):
    id = fields.Number()
    nome = fields.Str()
    description = fields.Str()
    editora = fields.Str()
    preco = fields.Float()
    faixa_etaria = fields.Number()
    numero_de_jogadores = fields.Str()
