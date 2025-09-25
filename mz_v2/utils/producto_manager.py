import reflex as rx
from models.producto import Producto, Categoria
from typing import List, Optional
from sqlmodel import select
from decimal import Decimal

#FUnciones para manejar productos
class ProductoManager:

    @staticmethod
    def crear_producto(nombre:str,
                       descripcion:str,
                       precio:Decimal,
                       stock:int,
                       categoria_id:int,
                       imagen_principal:Optional[str] = None) -> Producto:
        #Creamos un nuevo producto
        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            categoria_id=categoria_id,
            imagen_principal=imagen_principal
        )

        #Aqui se guardaria en la base de datos(mas adelante lo vemos)
        return producto
    
    @staticmethod
    def obtener_productos_por_categoria(categoria_id:int) -> List[Producto]:
        #Obtiene todos los productos de una categoria

        #consulta a la base de datos
        with rx.session() as session:
            statement = select(Producto).where(
                Producto.categoria_id == categoria_id,
                Producto.activo == True
            )
            productos = list(session.exec(statement))
            return productos
        
