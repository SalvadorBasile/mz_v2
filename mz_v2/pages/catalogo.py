import reflex as rx
from models.producto import Producto, Categoria
from typing import List
from utils.categoria_manager import CategoriaManager
from utils.producto_manager import ProductoManager 

class EstadoCatalogo(rx.State):
    """Estado para manejar el catálogo de productos"""
    productos: List[Producto] = []
    categorias: List[Categoria] = []
    categoria_seleccionada: int = 0
    termino_busqueda: str = ""
    cargando: bool = False
    
    def cargar_productos(self):
        """Carga los productos desde la base de datos"""
        self.cargando = True
        # Simular carga (en la implementación real sería desde la DB)
        self.productos = ProductoManager.obtener_productos_activos()
        self.cargando = False
    
    def filtrar_por_categoria(self, nombre_categoria: str = "Todas las categorias"):
        """Filtra productos por categoría, convirtiendo el nombre a ID"""
        #1.Manejar el caso especial "Todas las categorias"
        if nombre_categoria == "Todas las categorias":
            self.categoria_seleccionada = 0 # 0 para indicar "todos"
            self.cargar_productos()
            return
        
        #2.Obtener el ID 
        categoria_id = CategoriaManager.obtener_id_por_nombre(nombre_categoria)

        #3.Almacenar y filtrar
        if categoria_id is not None:
            self.categoria_seleccionada = categoria_id
            self.productos = ProductoManager.obtener_productos_por_categoria(categoria_id)
    
    def buscar_productos(self, termino: str):
        """Busca productos por término"""
        self.termino_busqueda = termino
        if termino:
            self.productos = ProductoManager.buscar_producto(termino)
            
        else:
            self.cargar_productos()

def tarjeta_producto(producto: Producto) -> rx.Component:
    """Componente para mostrar un producto individual"""
    return rx.card(
        rx.vstack(
            # Imagen del producto
            rx.image(
                src=producto.imagen_principal or "/placeholder-product.jpg",
                alt=producto.nombre,
                width="100%",
                height="200px",
                object_fit="cover",
            ),
            # Información del producto
            rx.vstack(
                rx.heading(producto.nombre, size="2"),
                rx.text(
                    producto.descripcion[:100] + "..." if (producto.descripcion is not None) and (len(producto.descripcion) > 100) else (producto.descripcion or ""),
                    color="gray.600",
                    font_size="sm",
                ),
                rx.hstack(
                    rx.text(f"${producto.precio:,.2f}", font_weight="bold", color="green.600"),
                    rx.spacer(),
                    rx.badge(
                        f"Stock: {producto.stock}",
                        color_scheme="blue" if producto.stock > 0 else "red"
                    ),
                ),
                rx.button(
                    "Ver Detalles",
                    width="100%",
                    on_click=lambda: rx.redirect(f"/producto/{producto.id}"),
                ),
                spacing="2",
                align="stretch",
            ),
            spacing="3",
        ),
        width="300px",
        height="400px",
    )

def barra_filtros() -> rx.Component:
    """Barra de filtros y búsqueda"""
    return rx.hstack(
        # Selector de categorías
        rx.select(
            ["Todas las categorías", "Placas de Video", "Procesadores", "Memorias RAM"],
            placeholder="Seleccionar categoría",
            on_change=lambda value: EstadoCatalogo.filtrar_por_categoria(value), #type: ignore
        ),
        # Barra de búsqueda
        rx.input(
            placeholder="Buscar productos...",
            on_blur=lambda value: EstadoCatalogo.buscar_productos(value), #type: ignore
        ),
        rx.button("Buscar"),
        spacing="3",
        width="100%",
    )

def catalogo_page() -> rx.Component:
    """Página principal del catálogo"""
    return rx.container(
        rx.vstack(
            # Título de la página
            rx.heading("Catálogo de Productos", size="5"),
            
            # Filtros y búsqueda
            barra_filtros(),
            
            # Grid de productos
            rx.cond(
                EstadoCatalogo.cargando,
                rx.spinner(size="3"),  # Mostrar spinner mientras carga
                rx.grid(
                    rx.foreach(
                        EstadoCatalogo.productos,
                        tarjeta_producto,
                    ),
                    columns=["1", "2", "3", "4"],#type: ignore  # Responsive: 1 col en móvil, 4 en desktop
                    spacing="4",
                ),
            ),
            
            spacing="6",
        ),
        max_width="1200px",
        padding="4",
    )