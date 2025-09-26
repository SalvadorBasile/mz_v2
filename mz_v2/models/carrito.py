import reflex as rx
from sqlmodel import Field, Relationship
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from models.producto import Producto
from models.usuario import Usuario

class ItemCarrito(rx.Model, table=True):
    #Cada producto agregado al carrito
    id: Optional[int] = Field(primary_key=True)
    usuario_id: Optional[int] = Field(foreign_key="usuario.id")
    producto_id: int = Field(foreign_key="producto.id")
    cantidad: int = Field(default=1)
    precio_unitario: Decimal = Field(decimal_places=2)
    fecha_agregado: datetime = Field(default_factory=datetime.now)

    #Relaciones
    producto: "Producto" = Relationship()
    usuario: Optional["Usuario"] = Relationship()