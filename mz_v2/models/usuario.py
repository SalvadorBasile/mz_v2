import reflex as rx
from sqlmodel import Field
from typing import Optional
from datetime import datetime


class Usuario(rx.Model, table = True):
    #Modelo para usuarios/clientes
    id: Optional[int] = Field(primary_key = True)
    email: str = Field(unique=True) #No puede haber emails repetidos
    password_hash: str #Password hasheada o encriptada
    nombre: str
    apellido: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    es_admin: bool = Field(default = False) #False == cliente, True == admin
    fecha_registro: datetime = Field(default = datetime.now)
    