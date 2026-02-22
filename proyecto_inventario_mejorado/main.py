import sys
from servicios.inventario import Inventario 
from modelo.producto import Producto

def mostrar_menu(): #Muestra el menú principal del sistema.
    print("\n" + "="*50)
    print("SISTEMA DE GESTIÓN DE INVENTARIOS")
    print("="*50)
    print("1. Añadir producto")
    print("2. Eliminar producto")
    print("3. Actualizar producto")
    print("4. Buscar producto por nombre")
    print("5. Listar todos los productos")
    print("6. Ver valor total del inventario")
    print("7. Exportar reporte")
    print("8. Salir")
    print("="*50)
def obtener_entero(mensaje: str) -> int: # Solicita y valida la entrada de un número entero
    while True:
        try:
            valor = int(input(mensaje))
            return valor
        except ValueError:
            print("Error: Por favor ingrese un número entero válido.")
        except KeyboardInterrupt:
            print("\nOperación cancelada.")
            return None
def obtener_float(mensaje: str) -> float: #Solicita y valida la entrada de un número decimal.
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("Error: El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("Error: Por favor ingrese un número decimal válido.")
        except KeyboardInterrupt:
            print("\nOperación cancelada.")
            return None
def añadir_producto_interactivo(inventario: Inventario): # Interfaz interactiva para añadir un nuevo producto.
    print("\n--- AÑADIR NUEVO PRODUCTO ---")
    try:
        id_producto = obtener_entero("Ingrese el ID del producto: ")
        if id_producto is None:
            return
        
        # Verificar si el ID ya existe
        if inventario.obtener_producto_por_id(id_producto) is not None:
            print(f"Error: Ya existe un producto con ID {id_producto}")
            return
        
        nombre = input("Ingrese el nombre del producto: ").strip()
        if not nombre:
            print("Error: El nombre no puede estar vacío.")
            return
        cantidad = obtener_entero("Ingrese la cantidad: ")
        if cantidad is None:
            return
        
        precio = obtener_float("Ingrese el precio unitario: ")
        if precio is None:
            return
        # Crear y añadir el producto
        nuevo_producto = Producto(id_producto, nombre, cantidad, precio)
        inventario.añadir_producto(nuevo_producto)
        
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")
def eliminar_producto_interactivo(inventario: Inventario): #Elimina un producto.
    print("\n--- ELIMINAR PRODUCTO ---")
    try:
        if not inventario.productos:
            print("El inventario está vacío. No hay productos para eliminar.")
            return
        id_producto = obtener_entero("Ingrese el ID del producto a eliminar: ")
        if id_producto is None:
            return
        
        # Mostrar información del producto antes de eliminar
        producto = inventario.obtener_producto_por_id(id_producto)
        if producto:
            print(f"Producto encontrado: {producto}")
            confirmacion = input("¿Está seguro de que desea eliminar este producto? (s/n): ").lower()
            if confirmacion == 's':
                inventario.eliminar_producto(id_producto)
            else:
                print("Operación cancelada.")
        else:
            print(f"No se encontró un producto con ID {id_producto}")
            
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")

def actualizar_producto_interactivo(inventario: Inventario): #Actualiza un producto.
    print("\n--- ACTUALIZAR PRODUCTO ---")
    try:
        if not inventario.productos:
            print("El inventario está vacío. No hay productos para actualizar.")
            return
        id_producto = obtener_entero("Ingrese el ID del producto a actualizar: ")
        if id_producto is None:
            return
        # Verificar si el producto existe
        producto = inventario.obtener_producto_por_id(id_producto)
        if producto is None:
            print(f"No se encontró un producto con ID {id_producto}")
            return
        print(f"\nProducto actual: {producto}")
        print("\n¿Qué desea actualizar?")
        print("1. Cantidad")
        print("2. Precio")
        print("3. Ambos")
        print("4. Cancelar")
        
        opcion = obtener_entero("Seleccione una opción (1-4): ")
        if opcion is None:
            return
        cantidad = None
        precio = None
        
        if opcion == 1 or opcion == 3:
            cantidad = obtener_entero("Ingrese la nueva cantidad: ")
            if cantidad is None:
                return
        if opcion == 2 or opcion == 3:
            precio = obtener_float("Ingrese el nuevo precio: ")
            if precio is None:
                return
        if opcion == 4:
            print("Operación cancelada.")
            return
        
        if opcion in [1, 2, 3]:
            inventario.actualizar_producto(id_producto, cantidad, precio)
        else:
            print("Opción no válida.")
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")
def buscar_producto_interactivo(inventario: Inventario):  # Busca productos por nombre.
    print("\n--- BUSCAR PRODUCTO POR NOMBRE ---")
    try:
        if not inventario.productos:
            print("El inventario está vacío. No hay productos para buscar.")
            return
        nombre_busqueda = input("Ingrese el nombre o parte del nombre a buscar: ").strip()
        if not nombre_busqueda:
            print("Error: Debe ingresar un término de búsqueda.")
            return
        resultados = inventario.buscar_por_nombre(nombre_busqueda)
        if resultados:
            print(f"\nSe encontraron {len(resultados)} producto(s):")
            print("-" * 50)
            for producto in resultados:
                print(f"- {producto}")
            print("-" * 50)
        else:
            print(f"No se encontraron productos con el nombre '{nombre_busqueda}'")
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")

def main(): #Función principal del programa. Controla el flujo del menú y las operaciones del sistema.
    print("="*60)
    print("BIENVENIDO AL SISTEMA DE GESTIÓN DE INVENTARIOS")
    print("="*60)
    print("\nInicializando sistema...")
    
    inventario = Inventario()  # Se carga el inventario desde el archivo JSON al crear la instancia
    print("\nSistema inicializado correctamente.")
    while True:
        try:
            mostrar_menu()
            opcion = obtener_entero("\nSeleccione una opción (1-8): ")
            if opcion is None:
                continue
            if opcion == 1:
                añadir_producto_interactivo(inventario)
            elif opcion == 2:
                eliminar_producto_interactivo(inventario)
            elif opcion == 3:
                actualizar_producto_interactivo(inventario)
            elif opcion == 4:
                buscar_producto_interactivo(inventario)
            elif opcion == 5:
                inventario.mostrar_todos()
            elif opcion == 6:
                valor_total = inventario.calcular_valor_total_inventario()
                print(f"\nValor total del inventario: ${valor_total:.2f}")
            elif opcion == 7:
                inventario.exportar_reporte()
            elif opcion == 8:
                print("\n" + "="*60)
                print("¡Gracias por usar el Sistema de Gestión de Inventarios!")
                print("Cerrando programa...")
                print("="*60)
                break
            else:
                print("Error: Opción no válida. Por favor seleccione una opción entre 1 y 8.")
        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido por el usuario.")
            respuesta = input("¿Desea salir del programa? (s/n): ").lower()
            if respuesta == 's':
                print("¡Hasta luego!")
                break
        except Exception as e:
            print(f"\nError inesperado en el programa: {e}")
            print("El programa continuará...")
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error fatal: {e}")
        sys.exit(1)