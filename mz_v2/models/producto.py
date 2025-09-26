import reflex as rx
from sqlmodel import Field, Relationship
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class Categoria(rx.Model, table = True):
    #Categorias de productos
    id: Optional[int] = Field(primary_key=True)
    nombre: str = Field(unique=True)
    descripcion: Optional[str] = None
    activa: bool = Field(default=True)

    #Relacion: Una categoria puede tener muchos productos
    productos: List["Producto"] = Relationship(back_populates="categoria")


class Producto(rx.Model, table = True):
    #Modelo para los productos
    id: Optional[int] = Field(primary_key= True)
    nombre: str
    descripcion: Optional[str] = None
    precio: Decimal = Field(decimal_places=2) #Precio con 2 decimales
    stock: int = Field(default=0) 
    categoria_id: Optional[int] = Field(foreign_key="categoria.id")
    imagen_principal: Optional[str] = None #URL de la imagen principal
    imagenes_adicionales: Optional[str] = None #URLS separadas por comas
    activo: bool = Field(default=True)
    destacado: bool = Field(default=False) #Para productos en oferta
    fecha_creacion: datetime = Field(default=datetime.now)

    #Relacion: cada producto pertenece a una categoria
    categoria: Optional[Categoria] = Relationship(back_populates="productos")