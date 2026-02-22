# 10_semana-10_Mejora-de-proyecto
# Sistema de Gestión de Inventarios con Archivos

Un sistema simple de gestión de inventarios que guarda los datos en un archivo de texto.

## Características

- **Persistencia en archivo**: Los productos se guardan automáticamente en `inventario.txt`
- **Carga automática**: Al iniciar, carga los productos guardados
- **Manejo de excepciones**: Control de errores de archivo (no encontrado, permisos, etc.)
- **Operaciones CRUD**: Añadir, eliminar, actualizar y buscar productos
- **Interfaz amigable**: Menú interactivo con validaciones

## Estructura de Archivos
El sistema guarda los productos en `inventario.txt` con el formato: