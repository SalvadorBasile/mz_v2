import reflex as rx
from models.producto import Producto
from utils.producto_manager import ProductoManager
from typing import Optional

class EstadoProductoDetalle(rx.State):
    #Estado para la pagina de detalle de producto
    producto: Optional[Producto] = None
    cantidad_seleccionada: int = 1
    imagen_seleccionada: int = 1 #Indice de la imagen q se esta mostrando
    cargando: bool = False

    def cargar_producto(self, producto_id: int):
        #Cargar un producto especifico por su ID
        self.cargando = True
        #En la implementacion real:
        self.producto = ProductoManager.obtener_producto_por_id(producto_id)
        self.cargando = False


    def cambiar_cantidad(self, nueva_cantidad: int):
        #Cambia la cantidad a agregar en el carrito
        if self.producto and nueva_cantidad >= 1 and nueva_cantidad <= self.producto.stock:
            self.cantidad_seleccionada = nueva_cantidad

    
    def agregar_al_carrito(self):
        #Agregar el producto al carrito
        if self.producto and self.cantidad_seleccionada <= self.producto.stock:
            #Aqui se integraria con el sistema de carrito
            print(f"Agregando {self.cantidad_seleccionada} x {self.producto.nombre}")
            return rx.toast.success(f"Producto agregado al carrito")
        else:
            return rx.toast.error("No hay suficiente stock")
        
def galeria_imagenes(producto: Producto) -> rx.Component:
        #Galeria de imagenes del producto
        return rx.vstack(
            #Imagen principal
            rx.image(
                src=producto.imagen_principal or "/placeholder-product.jpg",
                alt=producto.nombre,
                width="100%",
                max_width="500px",
                height="400px",
                object_fit="cover",
                border_radius="md",
            ),
            #MIniaturas (si hay imagenes adicionales)
            rx.hstack(
                rx.image(
                    src=producto.imagen_principal or "/placeholder-product.jpg",
                    widht="80px",
                    height="80px",
                    object_fit="cover",
                    border_radius="md",
                    cursor="pointer",
                    border="2px solid blue" if EstadoProductoDetalle.imagen_seleccionada == 0 else "2px solid transparent",
                ),
                #Aqui agregariamos mas miniaturas si el producto tiene mas imagenes
                spacing="2"
            ),
            spacing="4",
            align="center",
        )
    
def info_producto(producto: Producto) -> rx.Component:
        #Info detallada del producto
        return rx.vstack(
            #NOmbre del producto
            rx.heading(producto.nombre, size="6"),
            #Precio
            rx.heading(f"{producto.precio:,.2f}", size="4", color="green.600"),
            #DEscripcion
            rx.text(producto.descripcion, color="gray.700", font_size="md"),
            #EStado del stock
            rx.hstack(
                rx.text("Disponibilidad: ", font_weight="bold"),
                rx.badge(
                    f"{producto.stock} en stock" if producto.stock > 0 else "Sin stock",
                    color_scheme="green" if producto.stock > 0 else "red",
                ),
            ),

            #Selector de cantidad
            rx.cond(
                producto.stock > 0,
                rx.hstack(
                    rx.text("Cantidad: ", font_weight="bold"),
                    rx.numeric_input( #type: ignore
                        value=EstadoProductoDetalle.cantidad_seleccionada,
                        min=1,
                        max=producto.stock,
                        on_change=EstadoProductoDetalle.cambiar_cantidad,
                    ),
                    rx.text(f"(maximo {producto.stock})"),
                ),
            ),

            #Botones de accion
            rx.cond(
                producto.stock > 0,
                rx.vstack(
                    rx.button(
                        "Agregar al carrito",
                        size="3",
                        width="100%",
                        on_click=lambda: EstadoProductoDetalle.agregar_al_carrito,
                    ),
                    rx.button(
                        "Comprar Ahora",
                        size="3",
                        width="100%",
                        variant="outline",
                    ),
                ),
                rx.button(
                    "Producto Agotado",
                    size="3",
                    width="100%",
                    disabled=True,
                ),
            ),
            spacing="4",
            aling="start",
            width="100%",
        )
    

def producto_detalle_page() -> rx.Component:
        #Pagina de detalle del producto
        return rx.container(
            rx.cond(
                EstadoProductoDetalle.cargando,
                rx.center(rx.spinner(size="3")),
                rx.cond(
                    EstadoProductoDetalle.producto,
                    rx.vstack(
                        #Breadcrumb
                        rx.hstack(
                            rx.link("Inicio", href="/"),
                            rx.text(" > "),
                            rx.link("Catalogo", href="/catalogo"),
                            rx.text(" > "),
                            rx.text(EstadoProductoDetalle.producto.nombre if EstadoProductoDetalle.producto else "", font_size="bold"),
                            spacing="1",
                            color="gray.600",
                        ),

                        #Contenido principal del producto
                        rx.grid(
                            #COlumna izquierda: Galeria de imagenes
                            galeria_imagenes(EstadoProductoDetalle.producto),#type: ignore
                            #COlumna derecha: Info del producto
                            info_producto(EstadoProductoDetalle.producto), #type: ignore

                            columns="2",
                            spacing="8",
                            width="100%",
                        ),
                        #Productos relacionados
                        rx.vstack(
                            rx.heading("Productos Relacionados", size="6"),
                            rx.text("Aqui mostramos productos de la misma categoria"),
                            spacing="4",
                            width="100%",
                            margin_top="8",
                        ),
                        spacing="6",
                        widht="100%",
                    ),

                    #Si no se encuentra producto
                    rx.center(
                        rx.vstack(
                            rx.heading("Producto no encontrado!", size="7"),
                            rx.text("El producto que buscas no existe o no esta disponible."),
                            rx.link("Volver al catalogo", href="/catalogo"),
                            spacing="4",
                        )
                    ),
                ),
            ),
            max_widht="1200px",
            padding="4",
        )