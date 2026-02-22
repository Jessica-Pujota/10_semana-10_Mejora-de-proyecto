class Producto:
    """
    Clase que representa un producto en el inventario.
    Esta clase encapsula los atributos y comportamientos básicos de un producto.
    """
    
    def __init__(self, id_producto: int, nombre: str, cantidad: int, precio: float):
        """Constructor de la clase Producto."""
        self._id = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio
    
    # Getters y Setters para cada atributo
    @property
    def id(self) -> int:   #Obtiene el ID del producto
        return self._id
    
    @id.setter
    def id(self, nuevo_id: int): #Establece un nuevo ID para el producto
        self._id = nuevo_id
    
    @property
    def nombre(self) -> str: #Obtiene el nombre del producto
        return self._nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre: str): #Establece un nuevo nombre para el producto
        self._nombre = nuevo_nombre
    
    @property
    def cantidad(self) -> int: #Obtiene la cantidad disponible del producto
        return self._cantidad
    @cantidad.setter
    def cantidad(self, nueva_cantidad: int): #Establece una nueva cantidad para el producto
        if nueva_cantidad >= 0:
            self._cantidad = nueva_cantidad
        else:
            raise ValueError("La cantidad no puede ser negativa")
    @property
    def precio(self) -> float: #Obtiene el precio del producto
        return self._precio
    
    @precio.setter
    def precio(self, nuevo_precio: float): #Establece un nuevo precio para el producto
        if nuevo_precio >= 0:
            self._precio = nuevo_precio
        else:
            raise ValueError("El precio no puede ser negativo")
    
    def __str__(self) -> str: #Representación en string del producto.
        return f"ID: {self._id}, Nombre: {self._nombre}, Cantidad: {self._cantidad}, Precio: ${self._precio:.2f}"
    
    def to_dict(self) -> dict: #Convierte el producto a un diccionario.Útil para serialización.
        return {
            'id': self._id,
            'nombre': self._nombre,
            'cantidad': self._cantidad,
            'precio': self._precio
        }
    
    def to_linea_archivo(self) -> str: #Convierte el producto a formato de línea para archivo.
        # Formato: id|nombre|cantidad|precio
        # Returns:str: Línea formateada para guardar en archivo
        return f"{self._id}|{self._nombre}|{self._cantidad}|{self._precio:.2f}\n"
    
    @staticmethod
    def from_linea_archivo(linea: str): #Crea un producto a partir de una línea del archivo.
        #Args: inea (str): Línea del archivo en formato id|nombre|cantidad|precio
                #Returns: 
                # Producto: Nuevo producto creado desde la línea del archivo  
        try:
            partes = linea.strip().split('|')
            if len(partes) != 4:
                raise ValueError(f"Formato incorrecto: {linea}")
            
            id_producto = int(partes[0])
            nombre = partes[1]
            cantidad = int(partes[2])
            precio = float(partes[3])
            
            return Producto(id_producto, nombre, cantidad, precio)
        except (ValueError, IndexError) as e:
            raise ValueError(f"Error al procesar línea del archivo: {e}")