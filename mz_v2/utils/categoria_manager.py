import reflex as rx
from sqlmodel import Session, select
from typing import Optional
from models.producto import Categoria

class CategoriaManager:
    @staticmethod
    def obtener_id_por_nombre(nombre_categoria: str) -> Optional[int]:
        #Busca el id de una categoria dado su nombre
        with rx.session() as session:
            statement = select(Categoria.id).where(Categoria.nombre == nombre_categoria)
            resultado = session.exec(statement).first()
            return resultado
