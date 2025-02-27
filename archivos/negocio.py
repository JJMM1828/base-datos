##############################
# CAPA 2: LÓGICA DE NEGOCIO (LogicaNegocio)
##############################
from archivos.datos import BaseDatos
from mysql.connector import Error


class LogicaNegocio:
    def __init__(self, bd: BaseDatos):
        self.bd = bd

    # OPERACIONES SOBRE PRODUCTOS (procedimientos almacenados)
    def sp_insertar_producto(self, nombre, marca, stock, precio):
        """Inserta un producto llamando al procedimiento almacenado sp_insertar_producto."""
        con = self.bd.obtener_conexion()
        cursor = con.cursor()
        try:
            cursor.callproc('sp_insertar_producto', [nombre, marca, stock, precio])
            con.commit()
        except Error as e:
            raise e

    def sp_actualizar_producto(self, id_producto, nombre, marca, stock, precio):
        """Actualiza un producto llamando al procedimiento almacenado sp_actualizar_producto."""
        con = self.bd.obtener_conexion()
        cursor = con.cursor()
        try:
            cursor.callproc('sp_actualizar_producto', [id_producto, nombre, marca, stock, precio])
            con.commit()
        except Error as e:
            raise e

    def sp_eliminar_producto(self, id_producto):
        """Elimina un producto llamando al procedimiento almacenado sp_eliminar_producto."""
        con = self.bd.obtener_conexion()
        cursor = con.cursor()
        try:
            cursor.callproc('sp_eliminar_producto', [id_producto])
            con.commit()
        except Error as e:
            raise e

    def obtener_productos(self):
        """Retorna todos los productos (consulta directa)."""
        consulta = "SELECT * FROM productos"
        return self.bd.obtener_todos(consulta)

    # OPERACIONES SOBRE VENTAS (procedimientos almacenados)
    def sp_insertar_venta(self, fecha):
        """
        Inserta una venta (cabecera) llamando al procedimiento sp_insertar_venta y retorna el ID de la venta.
        Se inserta con total = 0 (los triggers actualizarán el total).
        """
        con = self.bd.obtener_conexion()
        cursor = con.cursor()
        try:
            parametros = [fecha, 0]  # El segundo parámetro es de salida
            resultado = cursor.callproc('sp_insertar_venta', parametros)
            con.commit()
            id_venta = resultado[1]
            return id_venta
        except Error as e:
            raise e

    def sp_insertar_detalle_venta(self, id_venta, id_producto, cantidad):
        """
        Inserta un detalle de venta llamando al procedimiento sp_insertar_detalle_venta.
        NOTA: No se envía el precio unitario, ya que se obtiene de la tabla productos.
        """
        con = self.bd.obtener_conexion()
        cursor = con.cursor()
        try:
            cursor.callproc('sp_insertar_detalle_venta', [id_venta, id_producto, cantidad])
            con.commit()
        except Error as e:
            raise e

    # MÉTODOS PARA REPORTES (consulta directa)
    def obtener_meses_ventas(self):
        """Retorna los meses (numéricos) en los que existen registros en ventas."""
        consulta = "SELECT DISTINCT MONTH(fecha) as mes FROM ventas ORDER BY mes"
        return self.bd.obtener_todos(consulta)

    def obtener_anios_ventas(self):
        """Retorna los años en los que existen registros en ventas."""
        consulta = "SELECT DISTINCT YEAR(fecha) as anio FROM ventas ORDER BY anio"
        return self.bd.obtener_todos(consulta)

    def obtener_reporte_ventas_mes_anio(self, mes, anio):
        """
        Retorna el reporte de ventas agrupado por producto para el mes y año dados.
        Devuelve el nombre del producto, la suma de las cantidades vendidas y el total de ingresos.
        """
        consulta = """
        SELECT p.nombre, SUM(dv.cantidad) as total_vendido, SUM(dv.subtotal) as total_ingresos
        FROM ventas v
        JOIN detalle_venta dv ON v.id_venta = dv.id_venta
        JOIN productos p ON dv.id_producto = p.id_producto
        WHERE MONTH(v.fecha) = %s AND YEAR(v.fecha) = %s
        GROUP BY p.id_producto
        """
        parametros = (mes, anio)
        return self.bd.obtener_todos(consulta, parametros)

