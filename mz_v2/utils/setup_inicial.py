import reflex as rx
from models.producto import Categoria
from sqlmodel import select

def crear_categorias_iniciales():
    #Crea las categorias basicas para una tienda de hardware
    categorias = [
        {"nombre": "Placas de Video", "descripcion": "Tarjetas graficas para gaming y trabajo"},
        {"nombre": "Procesadores", "descripcion": "CPUs Intel y AMD"},
        {"nombre": "Memorias RAM", "descripcion": "Memoria del sistema"},
        {"nombre": "Almacenamiento", "descripcion": "Discos duros, SSD, NVMe"},
        {"nombre": "Placas Madre", "descripcion": "Motherboards para diferentes sockets"},
        {"nombre": "Fuentes de poder", "descripcion": "PSU Certificadas"},
        {"nombre": "Gabinete", "descripcion": "Cases y torres para PC"},
        {"nombre": "Refrigeracion", "descripcion": "Coolers y sistemas de enfriamiento"},
        {"nombre": "Perifericos", "descripcion": "Teclados, mouse, monitores"},
    ]

    with rx.session() as session:
        for cat_data in categorias:
            #Verificar si la categoria ya existe
            categoria_existente = session.exec(select(Categoria).where(Categoria.nombre == cat_data["nombre"])).first()

            if not categoria_existente:
                nueva_categoria = Categoria(**cat_data) # type: ignore
                session.add(nueva_categoria)
        
        session.commit()

    print("Categorias iniciales creadas exitosamente")