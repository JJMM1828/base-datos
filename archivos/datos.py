"""
Aplicación de Gestión de Inventario en 3 Capas
  - Capa de Acceso a Datos: Conexión y ejecución de consultas en MySQL.
  - Capa de Lógica de Negocio: Lógica de negocio y llamadas a procedimientos almacenados.
  - Capa de Presentación: Interfaz gráfica en Tkinter.

Esta versión se adapta al nuevo modelo en el que:
 - El precio se almacena únicamente en la tabla "productos".
 - En la tabla "detalle_venta" se elimina la columna "precio_unitario"; el subtotal se calcula automáticamente.
 - Se utilizan triggers para validar el stock y calcular el subtotal.
 - La ventana Reportes muestra el gráfico de barras horizontal en la ventana clásica de matplotlib.
 - La ventana Producto Más Vendido muestra, según el mes y año seleccionado, tanto el producto con mayor cantidad vendida como el que generó mayores ingresos.
"""

##############################
# CAPA 1: ACCESO A DATOS (BaseDatos)
##############################
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox


class BaseDatos:
    def __init__(self, host="localhost", usuario="tu_usuario", contrasena="tu_contraseña", base="gestion_inventario"):
        self.host = host
        self.usuario = usuario
        self.contrasena = contrasena
        self.base = base
        self.conexion = None

    def conectar(self):
        """Establece la conexión a la base de datos."""
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.contrasena,
                database=self.base
            )
            self.conexion.autocommit = True
        except Error as e:
            messagebox.showerror("Error de Base de Datos", f"Error conectando a la base de datos:\n{e}")

    def desconectar(self):
        """Cierra la conexión a la base de datos."""
        if self.conexion:
            self.conexion.close()

    def obtener_conexion(self):
        """Devuelve una conexión activa, conectándose si es necesario."""
        if not self.conexion or not self.conexion.is_connected():
            self.conectar()
        return self.conexion

    def ejecutar_consulta(self, consulta, parametros=None):
        """Ejecuta una consulta SQL (INSERT, UPDATE o DELETE) y retorna el cursor."""
        try:
            con = self.obtener_conexion()
            cursor = con.cursor()
            cursor.execute(consulta, parametros)
            con.commit()
            return cursor
        except Error as e:
            messagebox.showerror("Error de Base de Datos", f"Error ejecutando la consulta:\n{e}")
            return None

    def obtener_todos(self, consulta, parametros=None):
        """Ejecuta una consulta SELECT y retorna todos los registros en formato de diccionario."""
        try:
            con = self.obtener_conexion()
            cursor = con.cursor(dictionary=True)
            cursor.execute(consulta, parametros)
            resultado = cursor.fetchall()
            return resultado
        except Error as e:
            messagebox.showerror("Error de Base de Datos", f"Error obteniendo datos:\n{e}")
            return []

