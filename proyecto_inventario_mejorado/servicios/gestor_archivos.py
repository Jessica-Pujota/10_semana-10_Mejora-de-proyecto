import os
from typing import List, Optional
from modelo.producto import Producto
class GestorArchivos: #Clase responsable de todas las operaciones de lectura/escritura de archivos.
    # Implementa manejo de excepciones para todas las operaciones de archivo.
    
    def __init__(self, nombre_archivo: str = "datos/inventario.txt"): #Constructor del gestor de archivos.
        #Args: nombre_archivo (str): Ruta del archivo de inventario
        self.nombre_archivo = nombre_archivo
        self._asegurar_directorio()
    def _asegurar_directorio(self): #Método privado para asegurar que el directorio del archivo exista.
        try:
            directorio = os.path.dirname(self.nombre_archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)
                print(f"Directorio '{directorio}' creado exitosamente.")
        except PermissionError:
            print(f"Error: No hay permisos para crear el directorio '{directorio}'")
        except Exception as e:
            print(f"Error inesperado al crear directorio: {e}")
    
    def guardar_productos(self, productos: List[Producto]) -> bool: #Guarda la lista de productos en el archivo.
        #Args:
        # productos (List[Producto]): Lista de productos a guardar
        # Returns: bool: True si se guardó correctamente, False en caso de error  
        try:
            with open(self.nombre_archivo, 'w', encoding='utf-8') as archivo:
                for producto in productos:
                    archivo.write(producto.to_linea_archivo())
            return True
        except PermissionError:
            print(f"Error: No hay permisos de escritura en '{self.nombre_archivo}'")
            return False
        except IOError as e:
            print(f"Error de E/S al guardar el archivo: {e}")
            return False
        except Exception as e:
            print(f"Error inesperado al guardar productos: {e}")
            return False
    def cargar_productos(self) -> List[Producto]: # Carga los productos desde el archivo.
        """
        Returns: List[Producto]: Lista de productos cargados 
        Maneja los siguientes errores:
            - FileNotFoundError: El archivo no existe (retorna lista vacía)
            - PermissionError: No hay permisos de lectura
            - ValueError: Error en el formato de los datos """
        productos = []
        # Verificar si el archivo existe
        if not os.path.exists(self.nombre_archivo):
            print(f"Archivo '{self.nombre_archivo}' no encontrado. Se creará uno nuevo al guardar.")
            return productos
        try:
            with open(self.nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()
                for num_linea, linea in enumerate(lineas, 1):
                    linea = linea.strip()
                    if not linea:  # Saltar líneas vacías
                        continue
                    try:
                        producto = Producto.from_linea_archivo(linea)
                        productos.append(producto)
                    except ValueError as e:
                        print(f"Advertencia: Línea {num_linea} ignorada - {e}")
                        continue
            print(f"Se cargaron {len(productos)} productos desde '{self.nombre_archivo}'")
            return productos
            
        except PermissionError:
            print(f"Error: No hay permisos de lectura en '{self.nombre_archivo}'")
            return productos
        except IOError as e:
            print(f"Error de E/S al leer el archivo: {e}")
            return productos
        except Exception as e:
            print(f"Error inesperado al cargar productos: {e}")
            return productos
    
    def backup_archivo(self) -> bool: #Crea una copia de seguridad del archivo actual.
        if not os.path.exists(self.nombre_archivo):
            return False
        try:
            # Crear nombre de backup con timestamp
            import time
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            nombre_backup = f"{self.nombre_archivo}.{timestamp}.bak"
            # Copiar archivo
            with open(self.nombre_archivo, 'r', encoding='utf-8') as origen:
                with open(nombre_backup, 'w', encoding='utf-8') as destino:
                    destino.write(origen.read())
            print(f"Backup creado: {nombre_backup}")
            return True
        except Exception as e:
            print(f"Error al crear backup: {e}")
            return False