# from sqlalchemy import Column, Integer, String, Boolean
# from sqlalchemy.sql import exists

# from meta import engine, session
# from meta import Base
from elixir import *

metadata.bind = "sqlite:///teste.sqlite"
metadata.bind.echo = False

class Rom(Entity):
    using_options(tablename='roms')

    id = Field(Integer, primary_key=True)
    aparelho = Field(Unicode(30), required=True)
    versao_miui = Field(Unicode(30), required=True)
    versao_android = Field(Unicode(30), required=True)
    link = Field(Unicode(100), required=True)
    arquivo = Field(Unicode(30), required=True)
    baixada = Field(Boolean, default=False)

    @classmethod
    def cria(cls, nome_aparelho, versao_miui, versao_android, link, nome_arquivo):
        return cls(aparelho=nome_aparelho, versao_miui=versao_miui, versao_android=versao_android, link=link, arquivo=nome_arquivo)

    @classmethod
    def existe(cls, nome_aparelho):
        return len(cls.query.filter_by(aparelho=nome_aparelho).all()) != 0
