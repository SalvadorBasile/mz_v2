import reflex as rx
from utils.carrito_state import EstadoCarrito
from models.carrito import ItemCarrito

def item_carrito_component(item: ItemCarrito) -> rx.Component:
    """COmponente para mostrar items del carrito"""
    return rx.card(
        rx.hstack(
            #IMagen del producto
            rx.image(
                src=f"/productos/{item.producto_id}.jpg", #Placeholder
                alt="Producto",
                width="80px",
                height="80px",
                object_fit="cover",
            ),

            #Informacion del producto
            rx.vstack(
                rx.heading(f"Producto #{item.producto_id}", size="1"), #EN real seria item.producto.nombre
                rx.text(f"${item.precio_unitario:,.2f} c/u", color="gray/600"),
                spacing="1",
                align="start",
                flex="1",
            ),

            #Control de cantidad
            rx.hstack(
                rx.button(
                    "-",
                    size="1",
                    on_click=lambda: EstadoCarrito.cambiar_cantidad(item.producto_id, item.cantidad -1),#type: ignore
                ),

                rx.text(str(item.cantidad), width="30px", text_align="center"),
                rx.button(
                    "+",
                    size="1",
                    on_click=lambda: EstadoCarrito.cambiar_cantidad(item.producto_id, item.cantidad +1),#type: ignore
                ),
                spacing="1",
            ),

            #Subtotal del item
            rx.text(f"{item.cantidad * item.precio_unitario:,.2f}", font_weight="bold", color="green.600"),

            #Boton eliminar
            rx.button(
                "🗑️",
                size="1",
                variant="ghost",
                color_scheme="red",
                on_click=lambda: EstadoCarrito.remover_producto(item.producto_id),#type: ignore
            ),
            align="center",
            spacing="4",
        ),
        padding="4",
    )


def resumen_carrito() -> rx.Component:
    """REsumen con totales del carrito"""
    return rx.card(
        rx.vstack(
            rx.heading("Resumen  del pedido", size="3"),
            rx.hstack(
                rx.text("Subtotal: "),
                rx.spacer(),
                rx.text(f"${EstadoCarrito.subtotal:,.2f}"),
                width="100%",
            ),

            rx.hstack(
                rx.text("Envio: "),
                rx.spacer(),
                rx.text("A calcular"),
                width="100%",
            ),

            rx.divider(),

            rx.hstack(
                rx.heading("Total: ", size="1"),
                rx.spacer(),
                rx.heading(f"${EstadoCarrito.subtotal:,.2f}", size="1", color="freen.600"),
                width="100%"
            ),
            spacing="3",
        ),
        padding="4",
    )

def carrito_dropdown() -> rx.Component:
    """Dropdown del carrito que aparece en el header"""
    return rx.popover.root(
        rx.popover.trigger(
            rx.button(
                rx.hstack(
                    rx.icon("shopping-cart"),
                    rx.badge(
                        EstadoCarrito.total_items,
                        color_scheme="red",
                        variant="solid",
                    ),
                    spacing="1",
                ),
                variant="ghost",
            ),
        ),

        rx.popover.content(
            rx.vstack(
                rx.heading("Tu Carrito", size="1"),

                rx.cond(
                    EstadoCarrito.total_items > 0,
                    rx.vstack(
                        #LIsta de items (maximo 3 en el dropdown)
                        rx.foreach(
                            EstadoCarrito.items[:3], #Solo mostrar los primeros 3
                            lambda item: rx.hstack(
                                rx.text(f"Producto #{item.producto_id}"),
                                rx.spacer(),
                                rx.text(f"{item.cantidad}x"),
                                rx.text(f"${item.precio_unitario * item.cantidad:,.2f}"),
                                spacing="2",
                            ),
                        ),

                        rx.cond(
                            EstadoCarrito.total_items > 3,
                            rx.text(f"... y {EstadoCarrito.total_items - 3} productos mas"),
                        ),

                        rx.divider(),

                        rx.hstack(
                            rx.text("Total:"),
                            rx.spacer(),
                            rx.text(f"${EstadoCarrito.subtotal:,.2f}", font_weight="bold"),
                        ),

                        rx.button(
                            "Ver Carrito Completo",
                            width="100%",
                            on_click=lambda: rx.redirect("/carrito"),
                        ),
                        spacing="2",
                    ),
                    rx.text("Tu carrito esta vacio", color="gray.500"),
                ),
                spacing="3",
                width="300px",
            ),
            side="bottom",
        ),
    )

def carrito_page() -> rx.Component:
    """PAgina completa del carrito"""
    return rx.container(
        rx.vstack(
            rx.heading("Tu Carrito de Compras", size="4"),

            rx.cond(
                EstadoCarrito.total_items > 0,
                rx.hstack(
                    #Columna izquierda: Item del carrito
                    rx.vstack(
                        rx.foreach(EstadoCarrito.items, item_carrito_component),
                        spacing="3",
                        flex="2",
                        ),
                    rx.vstack(
                        resumen_carrito(),
                        rx.button(
                            "Proceder el Pago",
                            size="3",
                            width="100%",
                            on_click=lambda: rx.redirect("/checkout"),
                        ),
                        rx.button(
                            "Seguir Comprando",
                            size="3",
                            widht="100%",
                            variant="outline",
                            on_click=lambda: rx.redirect("/catalogo"),
                        ),
                        spacing="3",
                        flex="1",
                    ),

                    spacing="8",
                    aling="start",
                    width="100%",
                ),
                #Carrito vacio
                rx.center(
                    rx.vstack(
                        rx.icon("shopping_cart", size=48, color="gray.400"),
                        rx.heading("Tu carrito esta vacio", size="2", color="gray.500"),
                        rx.text("Agrega algunos productos para comenzar"),
                        rx.button(
                            "Explorar Productos",
                            on_click=lambda: rx.redirect("/catalogo"),
                        ),
                        spacing="4",
                    ),
                    heigth="400px",
                ),
            ),
            spacing="6"
        ),
        max_width="1200px",
        padding="4",
    )