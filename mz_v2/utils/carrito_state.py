import reflex as rx
from models.carrito import ItemCarrito
from models.producto import Producto
from typing import List, Dict, Optional
from decimal import Decimal

class EstadoCarrito(rx.State):
    """Estado global del carrito de compras"""
    items: List[ItemCarrito] = []
    total_items:int = 0
    subtotal: Decimal = Decimal('0.00')

    def agregar_producto(self, producto_id: int, cantidad: int = 1):
        """Agregar un producto al carrito"""
        #Buscar si el producto ya esta en el carrito
        item_existente = None
        for item in self.items:
            if item.producto_id == producto_id:
                item_existente = item
                break
        
        if item_existente:
            #SI ya existe, aumentar la cantidad
            item_existente.cantidad += cantidad
        else:
            #Si no existe, crear un nuevo item
            #EN la implementcion real obtendriamos el producto de la DB
            producto = self.obtener_producto(producto_id)
            if producto and producto.stock >= cantidad:
                nuevo_item = ItemCarrito(
                    producto_id=producto_id,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )

                self.items.append(nuevo_item)
        
        self.actualizar_totales()

    def remover_producto(self, producto_id: int):
        """Remueve un producto completamente del carrito"""
        self.items = [item for item in self.items if item.producto_id != producto_id]
        self.actualizar_totales()

    def cambiar_cantidad(self, producto_id: int, nueva_cantidad: int):
        """Cambia la cantidad de un producto en el carrito"""
        if nueva_cantidad <= 0:
            self.remover_producto(producto_id)
            return
        
        for item in self.items:
            if item.producto_id == producto_id:
                #Verificar stock disponible
                producto = self.obtener_producto(producto_id)
                if producto and nueva_cantidad <= producto.stock:
                    item.cantidad = nueva_cantidad
                    break
        
        self.actualizar_totales()

    
    def actualizar_totales(self):
        """Recalcula los totales del carrito"""
        self.total_items = sum(item.cantidad for item in self.items)
        # CORRECCIÓN CLAVE: Inicializamos la suma con Decimal(0) para mantener el tipo
        self.subtotal = sum(
            (item.cantidad * item.precio_unitario
            for item in self.items),start=Decimal(0)
        )

    def vaciar_carrito(self):
        """Vaciar completamente el carrito"""
        self.items = []
        self.total_items = 0
        self.subtotal = Decimal('0.00')

    def obtener_producto(self, producto_id: int) -> Optional[Producto]:
        """Obtiene un producto por ID (placeholder)"""
        #EN la implementacion real seria una consulta a la DB
        return None
    
    def guardar_carrito_usuario(self, usuario_id: int):
        """Guardar el carrito en la base de datos para usuarios registrados"""
        #Implementar guardado en la DB
        pass

    def cargar_carrito_usuario(self, usuario_id: int):
        """CArga el carrito desde la base de datos"""
        #Implementar carga desde DB
        pass



