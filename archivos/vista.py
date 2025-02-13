##############################
# CAPA 3: PRESENTACIÓN (Interfaz Gráfica con Tkinter)
##############################
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import matplotlib

from archivos.datos import BaseDatos
from archivos.negocio import LogicaNegocio

matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Ventana Principal
class VentanaPrincipal(tk.Tk):
    def __init__(self, logica: LogicaNegocio):
        super().__init__()
        self.title("Gestión de Inventario")
        self.geometry("600x500")
        self.logica = logica

        # Reescalado
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        marco_principal = ttk.Frame(self, padding=20)
        marco_principal.grid(row=0, column=0, sticky="NSEW")
        marco_principal.columnconfigure(0, weight=1)
        marco_principal.rowconfigure(1, weight=1)

        etiqueta_bienvenida = ttk.Label(marco_principal, text="BIENVENIDO", font=("Helvetica", 24, "bold"))
        etiqueta_bienvenida.grid(row=0, column=0, pady=10, sticky="EW")

        # Botones en 2 filas x 2 columnas
        marco_botones = ttk.Frame(marco_principal)
        marco_botones.grid(row=1, column=0, sticky="NSEW", pady=20)
        marco_botones.columnconfigure(0, weight=1)
        marco_botones.columnconfigure(1, weight=1)
        marco_botones.rowconfigure(0, weight=1)
        marco_botones.rowconfigure(1, weight=1)

        btn_productos = ttk.Button(marco_botones, text="Productos", command=self.abrir_ventana_productos)
        btn_productos.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")

        btn_ventas = ttk.Button(marco_botones, text="Ventas", command=self.abrir_ventana_ventas)
        btn_ventas.grid(row=0, column=1, padx=10, pady=10, sticky="NSEW")

        btn_reportes = ttk.Button(marco_botones, text="Reportes", command=self.abrir_ventana_reportes)
        btn_reportes.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")

        btn_ventana4 = ttk.Button(marco_botones, text="Ventana 4", command=self.abrir_ventana_blanca)
        btn_ventana4.grid(row=1, column=1, padx=10, pady=10, sticky="NSEW")

    def abrir_ventana_productos(self):
        VentanaProductos(self, self.logica)

    def abrir_ventana_ventas(self):
        VentanaVentas(self, self.logica)

    def abrir_ventana_reportes(self):
        VentanaReportes(self, self.logica)

    def abrir_ventana_blanca(self):
        VentanaBlanca(self)

# Ventana para el CRUD de Productos
class VentanaProductos(tk.Toplevel):
    def __init__(self, maestro, logica: LogicaNegocio):
        super().__init__(maestro)
        self.title("Gestión de Productos")
        self.geometry("800x600")
        self.logica = logica

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        marco = ttk.Frame(self, padding=20)
        marco.grid(row=0, column=0, sticky="NSEW")
        marco.columnconfigure(1, weight=1)
        marco.rowconfigure(6, weight=1)

        # Formulario de Producto
        ttk.Label(marco, text="ID:").grid(row=0, column=0, sticky="W")
        self.entry_id = ttk.Entry(marco)
        self.entry_id.grid(row=0, column=1, sticky="EW", padx=5, pady=5)
        self.entry_id.config(state="readonly")

        ttk.Label(marco, text="Nombre:").grid(row=1, column=0, sticky="W")
        self.entry_nombre = ttk.Entry(marco)
        self.entry_nombre.grid(row=1, column=1, sticky="EW", padx=5, pady=5)

        ttk.Label(marco, text="Marca:").grid(row=2, column=0, sticky="W")
        self.entry_marca = ttk.Entry(marco)
        self.entry_marca.grid(row=2, column=1, sticky="EW", padx=5, pady=5)

        ttk.Label(marco, text="Stock:").grid(row=3, column=0, sticky="W")
        self.entry_stock = ttk.Entry(marco)
        self.entry_stock.grid(row=3, column=1, sticky="EW", padx=5, pady=5)

        ttk.Label(marco, text="Precio:").grid(row=4, column=0, sticky="W")
        self.entry_precio = ttk.Entry(marco)
        self.entry_precio.grid(row=4, column=1, sticky="EW", padx=5, pady=5)

        marco_botones = ttk.Frame(marco)
        marco_botones.grid(row=5, column=0, columnspan=2, pady=10)
        btn_insertar = ttk.Button(marco_botones, text="Insertar", command=self.insertar_producto)
        btn_insertar.grid(row=0, column=0, padx=5)
        btn_actualizar = ttk.Button(marco_botones, text="Modificar", command=self.actualizar_producto)
        btn_actualizar.grid(row=0, column=1, padx=5)
        btn_eliminar = ttk.Button(marco_botones, text="Eliminar", command=self.eliminar_producto)
        btn_eliminar.grid(row=0, column=2, padx=5)

        # Treeview para mostrar productos
        self.tree = ttk.Treeview(marco, columns=("ID", "Nombre", "Marca", "Stock", "Precio"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Marca", text="Marca")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Precio", text="Precio")
        self.tree.column("ID", width=50)
        self.tree.column("Nombre", width=150)
        self.tree.column("Marca", width=100)
        self.tree.column("Stock", width=80, anchor="center")
        self.tree.column("Precio", width=80, anchor="center")
        self.tree.grid(row=6, column=0, columnspan=2, sticky="NSEW", pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_producto)
        self.cargar_productos()

    def cargar_productos(self):
        """Carga los productos desde la base de datos y actualiza el Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        productos = self.logica.obtener_productos()
        for prod in productos:
            self.tree.insert("", tk.END, values=(prod["id_producto"], prod["nombre"], prod["marca"], prod["stock"], prod["precio"]))

    def seleccionar_producto(self, evento):
        """Carga los datos del producto seleccionado en el formulario."""
        item_sel = self.tree.focus()
        if item_sel:
            valores = self.tree.item(item_sel, "values")
            self.entry_id.config(state="normal")
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, valores[0])
            self.entry_id.config(state="readonly")
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, valores[1])
            self.entry_marca.delete(0, tk.END)
            self.entry_marca.insert(0, valores[2])
            self.entry_stock.delete(0, tk.END)
            self.entry_stock.insert(0, valores[3])
            self.entry_precio.delete(0, tk.END)
            self.entry_precio.insert(0, valores[4])

    def insertar_producto(self):
        nombre = self.entry_nombre.get()
        marca = self.entry_marca.get() if self.entry_marca.get() else "No informado"
        try:
            stock = int(self.entry_stock.get())
            precio = float(self.entry_precio.get())
            self.logica.sp_insertar_producto(nombre, marca, stock, precio)
            messagebox.showinfo("Éxito", "Producto insertado exitosamente.", parent=self)
            self.cargar_productos()
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def actualizar_producto(self):
        id_prod = self.entry_id.get()
        nombre = self.entry_nombre.get()
        marca = self.entry_marca.get() if self.entry_marca.get() else "No informado"
        try:
            stock = int(self.entry_stock.get())
            precio = float(self.entry_precio.get())
            self.logica.sp_actualizar_producto(int(id_prod), nombre, marca, stock, precio)
            messagebox.showinfo("Éxito", "Producto modificado exitosamente.", parent=self)
            self.cargar_productos()
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def eliminar_producto(self):
        id_prod = self.entry_id.get()
        if not id_prod:
            messagebox.showerror("Error", "Seleccione un producto para eliminar.", parent=self)
            return
        try:
            self.logica.sp_eliminar_producto(int(id_prod))
            messagebox.showinfo("Éxito", "Producto eliminado exitosamente.", parent=self)
            self.cargar_productos()
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def limpiar_formulario(self):
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        self.entry_id.config(state="readonly")
        self.entry_nombre.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)

# Ventana para Gestión de Ventas
class VentanaVentas(tk.Toplevel):
    def __init__(self, maestro, logica: LogicaNegocio):
        super().__init__(maestro)
        self.title("Gestión de Ventas")
        self.geometry("800x600")
        self.logica = logica

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        marco = ttk.Frame(self, padding=20)
        marco.grid(row=0, column=0, sticky="NSEW")
        marco.columnconfigure(0, weight=1)
        marco.rowconfigure(3, weight=1)

        # Cabecera: Fecha de la venta
        marco_cabecera = ttk.Frame(marco)
        marco_cabecera.grid(row=0, column=0, sticky="EW", pady=10)
        ttk.Label(marco_cabecera, text="Fecha:").pack(side="left")
        self.entry_fecha = ttk.Entry(marco_cabecera, width=15)
        self.entry_fecha.pack(side="left", padx=5)
        self.entry_fecha.insert(0, date.today().strftime("%Y-%m-%d"))
        self.entry_fecha.config(state="readonly")

        # Sección para agregar productos a la venta
        self.lista_productos = self.logica.obtener_productos()
        self.dic_productos = {str(prod["id_producto"]): prod for prod in self.lista_productos}
        valores_prod = [f'{prod["id_producto"]} - {prod["nombre"]}' for prod in self.lista_productos]

        marco_detalle = ttk.Frame(marco)
        marco_detalle.grid(row=1, column=0, sticky="EW", pady=10)
        ttk.Label(marco_detalle, text="Producto:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_productos = ttk.Combobox(marco_detalle, state="readonly", width=30)
        self.combo_productos.grid(row=0, column=1, padx=5, pady=5)
        self.combo_productos['values'] = valores_prod
        self.combo_productos.bind("<<ComboboxSelected>>", self.seleccionar_producto)
        if valores_prod:
            self.combo_productos.current(0)
        self.etiqueta_stock = ttk.Label(marco_detalle, text="Stock: N/A")
        self.etiqueta_stock.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(marco_detalle, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_cantidad = ttk.Entry(marco_detalle, width=10)
        self.entry_cantidad.grid(row=1, column=1, padx=5, pady=5, sticky="W")
        ttk.Label(marco_detalle, text="Precio Unitario:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_precio = ttk.Entry(marco_detalle, width=10)
        self.entry_precio.grid(row=1, column=3, padx=5, pady=5)
        self.entry_precio.insert(0, "0.00")
        self.entry_precio.config(state="readonly")
        btn_agregar = ttk.Button(marco_detalle, text="Agregar", command=self.agregar_producto)
        btn_agregar.grid(row=1, column=4, padx=5, pady=5)

        # Treeview para detalles de la venta
        self.tree_detalle = ttk.Treeview(marco, columns=("Producto", "Cantidad", "Precio Unitario", "Subtotal"), show="headings")
        self.tree_detalle.heading("Producto", text="Producto")
        self.tree_detalle.heading("Cantidad", text="Cantidad")
        self.tree_detalle.heading("Precio Unitario", text="Precio Unitario")
        self.tree_detalle.heading("Subtotal", text="Subtotal")
        self.tree_detalle.column("Producto", width=200)
        self.tree_detalle.column("Cantidad", width=70, anchor="center")
        self.tree_detalle.column("Precio Unitario", width=100, anchor="center")
        self.tree_detalle.column("Subtotal", width=100, anchor="center")
        self.tree_detalle.grid(row=2, column=0, sticky="NSEW", pady=10)

        # Resumen y acciones
        marco_pie = ttk.Frame(marco)
        marco_pie.grid(row=3, column=0, sticky="EW", pady=10)
        ttk.Label(marco_pie, text="Total:").pack(side="left")
        self.etiqueta_total = ttk.Label(marco_pie, text="0.00", font=("Helvetica", 12, "bold"))
        self.etiqueta_total.pack(side="left", padx=5)
        btn_finalizar = ttk.Button(marco_pie, text="Finalizar Venta", command=self.finalizar_venta)
        btn_finalizar.pack(side="right", padx=5)
        btn_cancelar = ttk.Button(marco_pie, text="Cancelar", command=self.destroy)
        btn_cancelar.pack(side="right", padx=5)

        self.lista_detalles = []
        self.seleccionar_producto()

    def seleccionar_producto(self, evento=None):
        seleccionado = self.combo_productos.get()
        if not seleccionado:
            return
        id_prod = seleccionado.split(" - ")[0]
        producto = self.dic_productos.get(id_prod)
        if producto:
            self.entry_precio.config(state="normal")
            self.entry_precio.delete(0, tk.END)
            self.entry_precio.insert(0, f'{producto["precio"]:.2f}')
            self.entry_precio.config(state="readonly")
            self.etiqueta_stock.config(text=f"Stock: {producto['stock']}")

    def agregar_producto(self):
        seleccionado = self.combo_productos.get()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un producto.", parent=self)
            return
        id_prod = seleccionado.split(" - ")[0]
        producto = self.dic_productos.get(id_prod)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado.", parent=self)
            return
        try:
            cantidad = int(self.entry_cantidad.get())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un entero positivo.", parent=self)
            return
        if cantidad > producto["stock"]:
            messagebox.showerror("Error", f"Stock insuficiente. Disponible: {producto['stock']}", parent=self)
            return
        try:
            precio = float(self.entry_precio.get())
        except ValueError:
            messagebox.showerror("Error", "Precio unitario inválido.", parent=self)
            return
        subtotal = cantidad * precio
        detalle = (producto["id_producto"], seleccionado, cantidad, precio, subtotal)
        self.lista_detalles.append(detalle)
        self.tree_detalle.insert("", tk.END, values=(seleccionado, cantidad, f"{precio:.2f}", f"{subtotal:.2f}"))
        total_actual = sum(item[4] for item in self.lista_detalles)
        self.etiqueta_total.config(text=f"{total_actual:.2f}")
        self.entry_cantidad.delete(0, tk.END)

    def finalizar_venta(self):
        if not self.lista_detalles:
            messagebox.showerror("Error", "No se han agregado productos a la venta.", parent=self)
            return
        fecha_venta = date.today().strftime("%Y-%m-%d")
        try:
            id_venta = self.logica.sp_insertar_venta(fecha_venta)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la venta:\n{e}", parent=self)
            return
        for detalle in self.lista_detalles:
            id_prod, prod_formateado, cantidad, precio, subtotal = detalle
            try:
                self.logica.sp_insertar_detalle_venta(id_venta, id_prod, cantidad, precio)
            except Exception as e:
                messagebox.showerror("Error", f"Error al insertar el detalle de la venta:\n{e}", parent=self)
                return
        messagebox.showinfo("Venta", "Venta registrada exitosamente.", parent=self)
        self.destroy()

# Ventana para Reportes de Ventas
class VentanaReportes(tk.Toplevel):
    def __init__(self, maestro, logica: LogicaNegocio):
        super().__init__(maestro)
        self.title("Reportes de Ventas")
        self.geometry("800x600")
        self.logica = logica

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        marco = ttk.Frame(self, padding=20)
        marco.grid(row=0, column=0, sticky="NSEW")
        marco.columnconfigure(0, weight=1)
        marco.rowconfigure(3, weight=1)

        # Selección de mes y año
        marco_seleccion = ttk.Frame(marco)
        marco_seleccion.grid(row=0, column=0, sticky="EW", pady=10)
        datos_meses = self.logica.obtener_meses_ventas()
        meses = [str(item["mes"]) for item in datos_meses] if datos_meses else [str(date.today().month)]
        ttk.Label(marco_seleccion, text="Mes:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_mes = ttk.Combobox(marco_seleccion, values=meses, state="readonly", width=10)
        self.combo_mes.grid(row=0, column=1, padx=5, pady=5)
        self.combo_mes.current(0)
        datos_anios = self.logica.obtener_anios_ventas()
        anios = [str(item["anio"]) for item in datos_anios] if datos_anios else [str(date.today().year)]
        ttk.Label(marco_seleccion, text="Año:").grid(row=0, column=2, padx=5, pady=5)
        self.combo_anio = ttk.Combobox(marco_seleccion, values=anios, state="readonly", width=10)
        self.combo_anio.grid(row=0, column=3, padx=5, pady=5)
        self.combo_anio.current(0)
        btn_generar = ttk.Button(marco_seleccion, text="Generar Reporte", command=self.generar_reporte)
        btn_generar.grid(row=0, column=4, padx=10, pady=5)

        # Área para el gráfico
        self.marco_grafico = ttk.Frame(marco)
        self.marco_grafico.grid(row=1, column=0, sticky="NSEW", pady=10)
        self.marco_grafico.columnconfigure(0, weight=1)
        self.marco_grafico.rowconfigure(0, weight=1)
        self.canvas = None

        # Información adicional (producto más vendido)
        self.etiqueta_info = ttk.Label(marco, text="", font=("Helvetica", 12))
        self.etiqueta_info.grid(row=2, column=0, pady=10, sticky="W")

    def generar_reporte(self):
        mes = self.combo_mes.get()
        anio = self.combo_anio.get()
        if not mes or not anio:
            messagebox.showerror("Error", "Seleccione mes y año.", parent=self)
            return
        datos_reporte = self.logica.obtener_reporte_ventas_mes_anio(mes, anio)
        if not datos_reporte:
            messagebox.showinfo("Reporte", "No hay datos de ventas para el mes y año seleccionados.", parent=self)
            return

        productos = [item["nombre"] for item in datos_reporte]
        cantidades = [item["total_vendido"] for item in datos_reporte]

        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(productos, cantidades, color="skyblue")
        ax.set_xlabel("Producto")
        ax.set_ylabel("Cantidad Vendida")
        ax.set_title(f"Ventas en {mes}/{anio}")
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(fig, master=self.marco_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="NSEW")

        prod_mas_vendido = datos_reporte[0]["nombre"]
        cantidad_max = datos_reporte[0]["total_vendido"]
        texto_info = f"Producto más vendido: {prod_mas_vendido} (Cantidad: {cantidad_max})"
        self.etiqueta_info.config(text=texto_info)

# Ventana en Blanco para Futura Implementación
class VentanaBlanca(tk.Toplevel):
    def __init__(self, maestro):
        super().__init__(maestro)
        self.title("Ventana en Construcción")
        self.geometry("400x300")
        ttk.Label(self, text="Esta ventana se implementará posteriormente.", font=("Helvetica", 16)).pack(expand=True)

##############################
# EJECUCIÓN PRINCIPAL
##############################
if __name__ == "__main__":
    # Inicializar la base de datos
    bd = BaseDatos(host="127.0.0.1", usuario="root", contrasena="root", base="gestion_inventario")
    # Inicializar la lógica de negocio
    logica = LogicaNegocio(bd)
    # Crear y ejecutar la aplicación principal
    app = VentanaPrincipal(logica)
    app.mainloop()
