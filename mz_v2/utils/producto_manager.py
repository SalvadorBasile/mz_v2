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
        
    @staticmethod
    def obtener_productos_activos():
        #Obtiene todos los productos de la bd
        with rx.session() as session:
            statement = select(Producto).where(
                Producto.activo == True
            )
            productos = list(session.exec(statement))
            return productos
        
    @staticmethod
    def buscar_producto(termino:str) -> List[Producto]:
        #Buscar productos por nombre o descripcion
        new_termino = termino.strip()
        if new_termino != "":
            with rx.session() as session:
                statement = select(Producto).where(
                    Producto.nombre.ilike(f"%{new_termino}") | Producto.descripcion.ilike(f"%{new_termino}"),# type: ignore
                    Producto.activo == True
                )
                productos = list(session.exec(statement))
                return productos
        else:
            return []
        

    @staticmethod
    def verificar_stock(producto_id:int, cantidad: int) -> bool:
        #Verificar si hay suficiente stock
        with rx.session() as session:
            producto = session.get(Producto, producto_id)
            if producto and producto.stock >= cantidad:
                return True
            return False
        
    @staticmethod
    def reducir_stock(producto_id: int, cantidad: int) -> bool:
        #Reduce stock despues de una venta
        with rx.session() as session:
            producto = session.get(Producto, producto_id)
            if producto and producto.stock >= cantidad:
                producto.stock -= cantidad
                session.add(producto)
                session.commit()
                return True
            return False