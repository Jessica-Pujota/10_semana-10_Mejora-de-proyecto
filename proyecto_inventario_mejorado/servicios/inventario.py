from typing import List, Optional
from modelo.producto import Producto
from servicios.gestor_archivos import GestorArchivos

class Inventario: #Clase que gestiona el inventario de productos con persistencia en archivo.    
    def __init__(self, gestor_archivos: GestorArchivos = None): #Constructor de la clase Inventario.
        self._productos = []  # Lista privada para almacenar productos en memoria
        self.gestor_archivos = gestor_archivos or GestorArchivos()
        self._cargar_desde_archivo()
    
    def _cargar_desde_archivo(self): #Carga los productos desde el archivo al iniciar el programa. 
        #Maneja excepciones durante la carga.
        try:
            productos_cargados = self.gestor_archivos.cargar_productos()
            self._productos = productos_cargados
        except Exception as e:
            print(f"Error al cargar inventario desde archivo: {e}")
            self._productos = []
    def _guardar_en_archivo(self) -> bool: #Guarda el estado actual del inventario en el archivo.
        try:
            return self.gestor_archivos.guardar_productos(self._productos)
        except Exception as e:
            print(f"Error al guardar inventario en archivo: {e}")
            return False
    @property
    def productos(self) -> List[Producto]: #Obtiene la lista de productos (solo lectura)
        return self._productos.copy()
    
    def añadir_producto(self, producto: Producto) -> bool: #Añade un nuevo producto al inventario y guarda en archivo.
        # Validar que el ID no esté repetido
        if self._buscar_por_id(producto.id) is not None:
            print(f"Error: Ya existe un producto con ID {producto.id}")
            return False
        
        # Añadir a la lista en memoria
        self._productos.append(producto)
        
        # Guardar en archivo
        if self._guardar_en_archivo():
            print(f"Producto '{producto.nombre}' añadido correctamente.")
            return True
        else:
            # Si falla el guardado, revertir el cambio en memoria
            self._productos.remove(producto)
            print("Error: No se pudo guardar el producto en el archivo.")
            return False
    
    def eliminar_producto(self, id_producto: int) -> bool: #Elimina un producto del inventario por su ID.
        producto = self._buscar_por_id(id_producto)
        if producto is None:
            print(f"Error: No se encontró un producto con ID {id_producto}")
            return False

        self.gestor_archivos.backup_archivo()    #Crear backup antes de modificar el archivo
        self._productos.remove(producto)   # Elimina de la lista en memoria
        if self._guardar_en_archivo():  # Guarda en archivo
            print(f"Producto con ID {id_producto} eliminado correctamente.")
            return True
        else: #Si falla el guardado, restaurar el producto
            self._productos.append(producto)
            print("Error: No se pudo actualizar el archivo. Operación cancelada.")
            return False
    
    def actualizar_producto(self, id_producto: int, cantidad: int = None, precio: float = None) -> bool:
        """
        Actualiza la cantidad o precio de un producto.
        """
        producto = self._buscar_por_id(id_producto)
        if producto is None:
            print(f"Error: No se encontró un producto con ID {id_producto}")
            return False
        cantidad_original = producto.cantidad    #Guardar cantidad original para restaurar en caso de error
        precio_original = producto.precio
        
        try:
            # Actualizar solo los campos proporcionados
            if cantidad is not None:
                producto.cantidad = cantidad
            if precio is not None:
                producto.precio = precio
            
            # Guardar en archivo
            if self._guardar_en_archivo():
                print(f"Producto con ID {id_producto} actualizado correctamente.")
                return True
            else:
                # Restaurar valores originales
                producto.cantidad = cantidad_original
                producto.precio = precio_original
                print("Error: No se pudo guardar la actualización en el archivo.")
                return False
                
        except ValueError as e:
            print(f"Error en la validación de datos: {e}")
            return False
    
    def buscar_por_nombre(self, nombre_busqueda: str) -> List[Producto]: #Busca productos por nombre, permitiendo coincidencias parciales.
        if not nombre_busqueda:
            return []
        nombre_busqueda = nombre_busqueda.lower()
        resultados = []
        for producto in self._productos:
            if nombre_busqueda in producto.nombre.lower():
                resultados.append(producto)
        return resultados
    
    def mostrar_todos(self) -> None: # Muestra todos los productos registrados en el inventario.
        if not self._productos:
            print("El inventario está vacío.")
            return
        print("\n" + "="*60)
        print("INVENTARIO COMPLETO")
        print("="*60)
        for producto in self._productos:
            print(f"- {producto}")
        print("="*60)
        print(f"Total de productos: {len(self._productos)}")
        
        # Mostrar ubicación del archivo
        print(f"Archivo de datos: {self.gestor_archivos.nombre_archivo}")
        print("="*60)
    
    def _buscar_por_id(self, id_producto: int) -> Optional[Producto]: # Método privado para buscar un producto por su ID.
        for producto in self._productos:
            if producto.id == id_producto:
                return producto
        return None
    
    def obtener_producto_por_id(self, id_producto: int) -> Optional[Producto]: # Método público para obtener un producto por su ID.
        return self._buscar_por_id(id_producto)
    def calcular_valor_total_inventario(self) -> float: #Calcula el valor total del inventario.
        total = sum(producto.cantidad * producto.precio for producto in self._productos)
        return total
    def exportar_reporte(self, nombre_archivo: str = "reporte_inventario.txt") -> bool: #Exporta un reporte legible del inventario a un archivo.
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write("="*60 + "\n")
                archivo.write("REPORTE DE INVENTARIO\n")
                archivo.write(f"Fecha: {__import__('datetime').datetime.now()}\n")
                archivo.write("="*60 + "\n\n")
                for producto in self._productos:
                    archivo.write(f"{producto}\n")
                archivo.write("\n" + "="*60 + "\n")
                archivo.write(f"Total de productos: {len(self._productos)}\n")
                archivo.write(f"Valor total: ${self.calcular_valor_total_inventario():.2f}\n")
                archivo.write("="*60 + "\n")
            print(f"Reporte exportado a '{nombre_archivo}'")
            return True
        except Exception as e:
            print(f"Error al exportar reporte: {e}")
            return False