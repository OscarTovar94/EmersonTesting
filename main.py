"""
------------------------------------------------------------
Proyecto : EmersonTest
Autor    : Oscar Tovar
Versión  : 1.0
------------------------------------------------------------

Historial de Revisiones

Rev 1.0 - 22/07/2026
- Creación inicial de la aplicación.
- Utilización de DAQ KEYSIGHT 34970A
- MODULOS DAQ KEYSIGHT 34970A:
    - 34902A: 16 Channel Multiplexer
    - 34907: Multi function Switch/Control Module

------------------------------------------------------------
"""
import tkinter as tk
import customtkinter as ctk
import os
import sys
import importlib.util
from tkinter import messagebox
import win32event
import win32api
import winerror


# ---- Control de instancia única ----
MUTEX_NAME = "main"

mutex = win32event.CreateMutex(
    None,
    False,
    MUTEX_NAME
)

if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    sys.exit(0)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


MODELOS_PCBA = [
    "PCBA Modelo 1",
    "PCBA Modelo 2",
    "PCBA Modelo 3"
]

CONFIGURACION_MODELOS = {
    "PCBA Modelo 1": {
        "archivo": "TestPCB1.py",
        "clase": "PruebaModelo1"
    },
    "PCBA Modelo 2": {
        "archivo": "TestPCB2.py",
        "clase": "PruebaModelo2"
    },
    "PCBA Modelo 3": {
        "archivo": "TestPCB3.py",
        "clase": "PruebaModelo3"
    }
}


def obtener_ruta_base():
    """
    Obtiene la carpeta donde se encuentra el ejecutable
    o el archivo main.py.
    """

    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)

    return os.path.dirname(os.path.abspath(__file__))


class VentanaLogin:
    """Ventana de inicio de sesión de la aplicación Emerson."""

    def __init__(self, root):
        self.root = root

        self.root.title("Emerson - Login")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        # Variables de la interfaz
        self.numero_empleado = tk.StringVar()
        self.orden_trabajo = tk.StringVar()
        self.modelo_seleccionado = tk.StringVar(value="Seleccione un modelo")

        self.configurar_ventana()
        self.crear_interfaz()

        # Permite presionar Enter para ingresar
        self.root.bind("<Return>", self.entrar)

        # Coloca el cursor en el primer campo
        self.entry_empleado.focus_set()

    def configurar_ventana(self):
        """Centra la ventana en la pantalla."""

        self.root.update_idletasks()

        ancho_ventana = 600
        alto_ventana = 600

        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        posicion_x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
        posicion_y = int((alto_pantalla / 3) - (alto_ventana / 2))

        self.root.geometry(
            f"{ancho_ventana}x{alto_ventana}"
            f"+{posicion_x}+{posicion_y}"
        )

    def crear_interfaz(self):
        """Crea los elementos visuales de la ventana."""

        # Contenedor principal
        self.frame_principal = ctk.CTkFrame(
            self.root,
            corner_radius=18,
            border_width=1,
            border_color="#3A3D52"
        )
        self.frame_principal.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=35
        )

        # Título
        self.label_titulo = ctk.CTkLabel(
            self.frame_principal,
            text="EMERSON",
            font=("Arial", 34, "bold"),
            text_color="#FFFFFF"
        )
        self.label_titulo.pack(
            pady=(35, 5)
        )

        self.label_subtitulo = ctk.CTkLabel(
            self.frame_principal,
            text="Sistema de pruebas funcionales y eléctricas",
            font=("Arial", 15),
            text_color="#AEB4C8"
        )
        self.label_subtitulo.pack(
            pady=(0, 30)
        )

        # Número de empleado
        self.label_empleado = ctk.CTkLabel(
            self.frame_principal,
            text="Número de empleado",
            font=("Arial", 14, "bold"),
            anchor="w"
        )
        self.label_empleado.pack(
            fill="x",
            padx=55,
            pady=(0, 5)
        )

        self.entry_empleado = ctk.CTkEntry(
            self.frame_principal,
            textvariable=self.numero_empleado,
            placeholder_text="Ingrese el número de empleado",
            height=42,
            font=("Arial", 14)
        )
        self.entry_empleado.pack(
            fill="x",
            padx=55,
            pady=(0, 18)
        )

        # Número de orden
        self.label_orden = ctk.CTkLabel(
            self.frame_principal,
            text="Orden de trabajo",
            font=("Arial", 14, "bold"),
            anchor="w"
        )
        self.label_orden.pack(
            fill="x",
            padx=55,
            pady=(0, 5)
        )

        self.entry_orden = ctk.CTkEntry(
            self.frame_principal,
            textvariable=self.orden_trabajo,
            placeholder_text="Ingrese la orden de trabajo",
            height=42,
            font=("Arial", 14)
        )
        self.entry_orden.pack(
            fill="x",
            padx=55,
            pady=(0, 18)
        )

        # Modelo
        self.label_modelo = ctk.CTkLabel(
            self.frame_principal,
            text="Modelo de PCBA",
            font=("Arial", 14, "bold"),
            anchor="w"
        )
        self.label_modelo.pack(
            fill="x",
            padx=55,
            pady=(0, 5)
        )

        self.combo_modelo = ctk.CTkComboBox(
            self.frame_principal,
            variable=self.modelo_seleccionado,
            values=MODELOS_PCBA,
            state="readonly",
            height=42,
            font=("Arial", 14),
            dropdown_font=("Arial", 14)
        )
        self.combo_modelo.pack(
            fill="x",
            padx=55,
            pady=(0, 30)
        )

        # Botón Entrar
        self.boton_entrar = ctk.CTkButton(
            self.frame_principal,
            text="Entrar",
            command=self.entrar,
            height=45,
            corner_radius=8,
            font=("Arial", 16, "bold")
        )
        self.boton_entrar.pack(
            fill="x",
            padx=55,
            pady=(0, 25)
        )

    def validar_datos(self):
        """Valida los datos capturados por el operador."""

        empleado = self.numero_empleado.get().strip()
        orden = self.orden_trabajo.get().strip()
        modelo = self.modelo_seleccionado.get().strip()

        if not empleado:
            messagebox.showwarning(
                "Datos incompletos",
                "Ingrese el número de empleado."
            )
            self.entry_empleado.focus_set()
            return False

        if not empleado.isdigit():
            messagebox.showwarning(
                "Número de empleado inválido",
                "El número de empleado debe contener solamente números."
            )
            self.entry_empleado.focus_set()
            self.entry_empleado.select_range(0, "end")
            return False

        if not orden:
            messagebox.showwarning(
                "Datos incompletos",
                "Ingrese el número de orden de trabajo."
            )
            self.entry_orden.focus_set()
            return False

        if modelo not in MODELOS_PCBA:
            messagebox.showwarning(
                "Datos incompletos",
                "Seleccione un modelo de PCBA."
            )
            self.combo_modelo.focus_set()
            return False

        return True

    def entrar(self, event=None):
        """Valida los datos y abre la ventana principal."""

        if not self.validar_datos():
            return

        datos_login = {
            "empleado": self.numero_empleado.get().strip(),
            "orden": self.orden_trabajo.get().strip(),
            "modelo": self.modelo_seleccionado.get().strip()
        }

        # Oculta la ventana de Login
        self.root.withdraw()

        # Abre la ventana principal
        VentanaPrincipal(
            root_login=self.root,
            datos_login=datos_login
        )


class VentanaPrincipal:
    """Ventana principal de la aplicación Emerson."""

    def __init__(self, root_login, datos_login):
        self.root_login = root_login
        self.datos_login = datos_login
        # Datos recibidos desde el login
        self.modelo = datos_login["modelo"]
        self.empleado = datos_login["empleado"]
        self.orden = datos_login["orden"]

        self.ventana = ctk.CTkToplevel(self.root_login)

        self.ventana.title("Emerson - Sistema de Pruebas")
        self.ventana.geometry("1100x700")
        self.ventana.minsize(900, 600)

        # Evita que la ventana quede detrás del Login
        self.ventana.lift()
        self.ventana.focus_force()

        # Controla el cierre de la aplicación
        self.ventana.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar_aplicacion
        )

        self.crear_interfaz()
        self.cargar_pruebas_modelo()

        # Maximiza la ventana después de abrirla
        self.ventana.after(
            100,
            lambda: self.ventana.state("zoomed")
        )

    def crear_interfaz(self):
        """Crea temporalmente la interfaz principal."""

        # Encabezado
        self.frame_encabezado = ctk.CTkFrame(
            self.ventana,
            height=90,
            corner_radius=0
        )
        self.frame_encabezado.pack(
            fill="x"
        )
        self.frame_encabezado.pack_propagate(False)

        self.label_titulo = ctk.CTkLabel(
            self.frame_encabezado,
            text="Emerson Testing",
            font=("Arial", 28, "bold")
        )
        self.label_titulo.pack(
            side="left",
            padx=30,
            pady=20
        )

        texto_informacion = (
            f"#Empleado: {self.datos_login['empleado']}    |    "
            f"#Orden: {self.datos_login['orden']}    |    "
            f"Modelo: {self.datos_login['modelo']}"
        )

        self.label_informacion = ctk.CTkLabel(
            self.frame_encabezado,
            text=texto_informacion,
            font=("Arial", 15)
        )
        self.label_informacion.pack(
            side="right",
            padx=30,
            pady=20
        )

        # Contenido principal
        self.frame_contenido = ctk.CTkFrame(
            self.ventana,
            corner_radius=12
        )
        self.frame_contenido.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        self.label_modelo = ctk.CTkLabel(
            self.frame_contenido,
            text=f"{self.datos_login['modelo']}",
            font=("Arial", 24, "bold")
        )
        self.label_modelo.pack(
            pady=(10, 15)
        )

        self.frame_tabla = ctk.CTkScrollableFrame(
            self.frame_contenido,
            label_text="Resultados de pruebas"
        )

        self.frame_tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.label_status = ctk.CTkLabel(
            self.frame_contenido,
            text=(
                "En Espera"
            ),
            font=("Arial",50, "bold"),
            text_color="#002060",
            bg_color="#A6C9EC",
        )
        self.label_status.pack(
            pady=10
        )

        self.boton_iniciar = ctk.CTkButton(
            self.frame_contenido,
            text="Iniciar prueba",
            command=self.iniciar_pruebas,
            width=240,
            height=50,
            font=("Arial", 17, "bold")
        )

        self.boton_iniciar.pack(
            pady=20
        )

        self.boton_cerrar_sesion = ctk.CTkButton(
            self.frame_contenido,
            text="Cerrar sesión",
            command=self.cerrar_sesion,
            width=180,
            height=42,
            font=("Arial", 15, "bold"),
            fg_color="#A33A3A",
            hover_color="#7F2D2D"
        )
        self.boton_cerrar_sesion.pack(
            pady=20
        )

    def cerrar_sesion(self):
        """Cierra la ventana principal y regresa al Login."""

        self.label_status.configure(
            text="En Espera",
            text_color="#002060",
            bg_color="#A6C9EC"
        )

        respuesta = messagebox.askyesno(
            "Cerrar sesión",
            "¿Desea regresar a la ventana de Login?"
        )

        if not respuesta:
            return

        self.ventana.destroy()

        # Limpia algunos datos del Login
        self.root_login.deiconify()
        self.root_login.lift()
        self.root_login.focus_force()

    def cerrar_aplicacion(self):
        """Cierra completamente la aplicación."""

        respuesta = messagebox.askyesno(
            "Salir",
            "¿Desea cerrar la aplicación Emerson?"
        )

        if respuesta:
            self.root_login.destroy()

    def iniciar_pruebas(self):
        """Ejecuta la secuencia de pruebas del modelo seleccionado."""

        try:
            configuracion = CONFIGURACION_MODELOS.get(
                self.modelo
            )

            if configuracion is None:
                messagebox.showerror(
                    "Error",
                    f"No existe configuración para el modelo: {self.modelo}"
                )
                return

            nombre_clase = configuracion["clase"]

            # Reinicia visualmente las filas
            for fila in self.filas_pruebas:
                fila["valor"].configure(
                    text="---"
                )

                fila["estado"].configure(
                    text="PENDIENTE",
                    text_color="#9C5700"
                )

            self.label_status.configure(
                text="En Proceso",
                text_color="#9C5700",
                bg_color="#FFEB9C"
            )

            self.boton_iniciar.configure(
                state="disabled"
            )

            # Fuerza a Tkinter a dibujar los cambios antes de medir
            self.ventana.update_idletasks()

            clase_prueba = getattr(
                self.modulo_modelo,
                nombre_clase
            )

            secuencia = clase_prueba()

            resultado = secuencia.ejecutar_pruebas()

            self.procesar_resultados(
                resultado
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible ejecutar las pruebas:\n\n{error}"
            )

        finally:
            self.boton_iniciar.configure(
                state="normal"
            )

    def procesar_resultados(self, resultado):
        """Muestra los resultados en la tabla dinámica."""

        estado_ejecucion = resultado["estado"]
        resultado_final = resultado["resultado_final"]
        mensaje = resultado["mensaje"]
        mediciones = resultado["mediciones"]

        for indice, medicion in enumerate(mediciones):

            if indice >= len(self.filas_pruebas):
                break

            label_valor = self.filas_pruebas[indice]["valor"]
            label_estado = self.filas_pruebas[indice]["estado"]

            valor = medicion["valor"]
            unidad = medicion["unidad"]
            estado = medicion["estado"]

            if valor is None:
                texto_valor = "Sin lectura"
            else:
                texto_valor = f"{valor:.4f} {unidad}"

            label_valor.configure(
                text=texto_valor
            )

            if estado == "PASS":
                color_estado = "#41C76F"

            elif estado == "FAIL":
                color_estado = "#FF5C5C"

            else:
                color_estado = "#F2A541"

            label_estado.configure(
                text=estado,
                text_color=color_estado
            )

        if estado_ejecucion == "ERROR":
            messagebox.showerror(
                "Error de ejecución",
                mensaje
            )
            return

        if resultado_final == "PASS":
            self.label_status.configure(
                text="PASS",
                text_color="#006100",
                bg_color="#C6EFCE"
                )
        else:
            self.label_status.configure(
                text="FAIL",
                text_color="#9C0006",
                bg_color="#FFC7CE"
                )

    def crear_tabla_pruebas(self, pruebas):
        """Crea una fila por cada prueba del modelo cargado."""

        # Elimina filas anteriores
        for widget in self.frame_tabla.winfo_children():
            widget.destroy()

        self.filas_pruebas = []

        # Encabezados
        encabezados = [
            "Prueba",
            "Descripción",
            "Canal",
            "Límites",
            "Valor",
            "Estado"
        ]

        for columna, texto in enumerate(encabezados):
            label = ctk.CTkLabel(
                self.frame_tabla,
                text=texto,
                font=("Arial", 14, "bold")
            )
            label.grid(
                row=0,
                column=columna,
                padx=10,
                pady=8,
                sticky="ew"
            )

        # Crear una fila por cada prueba
        for indice, prueba in enumerate(pruebas, start=1):

            label_nombre = ctk.CTkLabel(
                self.frame_tabla,
                text=prueba["nombre"],
                font=("Arial", 13)
            )
            label_nombre.grid(
                row=indice,
                column=0,
                padx=10,
                pady=5,
                sticky="w"
            )

            label_descripcion = ctk.CTkLabel(
                self.frame_tabla,
                text=prueba["descripcion"],
                font=("Arial", 13)
            )
            label_descripcion.grid(
                row=indice,
                column=1,
                padx=10,
                pady=5,
                sticky="w"
            )

            label_canal = ctk.CTkLabel(
                self.frame_tabla,
                text=str(prueba["canal"]),
                font=("Arial", 13)
            )
            label_canal.grid(
                row=indice,
                column=2,
                padx=10,
                pady=5
            )

            texto_limites = (
                f"{prueba['minimo']} - "
                f"{prueba['maximo']} "
                f"{prueba['unidad']}"
            )

            label_limites = ctk.CTkLabel(
                self.frame_tabla,
                text=texto_limites,
                font=("Arial", 13)
            )
            label_limites.grid(
                row=indice,
                column=3,
                padx=10,
                pady=5
            )

            label_valor = ctk.CTkLabel(
                self.frame_tabla,
                text="---",
                font=("Arial", 13)
            )
            label_valor.grid(
                row=indice,
                column=4,
                padx=10,
                pady=5
            )

            label_estado = ctk.CTkLabel(
                self.frame_tabla,
                text="PENDIENTE",
                font=("Arial", 13, "bold"),
                text_color="#D9A441"
            )
            label_estado.grid(
                row=indice,
                column=5,
                padx=10,
                pady=5
            )

            self.filas_pruebas.append({
                "valor": label_valor,
                "estado": label_estado
            })

    def cargar_pruebas_modelo(self):
        """Carga las pruebas del modelo y las muestra sin ejecutarlas."""

        try:
            configuracion = CONFIGURACION_MODELOS.get(self.modelo)

            if configuracion is None:
                messagebox.showerror(
                    "Error",
                    f"No existe configuración para el modelo: {self.modelo}"
                )
                return

            nombre_archivo = configuracion["archivo"]

            self.modulo_modelo = cargar_modulo_modelo(
                nombre_archivo
            )

            self.crear_tabla_pruebas(
                self.modulo_modelo.PRUEBAS
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible cargar las pruebas:\n\n{error}"
            )


def cargar_modulo_modelo(nombre_archivo):
    """Carga dinámicamente un archivo Python de la carpeta modelos."""

    ruta_base = os.path.dirname(
        os.path.abspath(__file__)
    )

    ruta_archivo = os.path.join(
        ruta_base,
        "models",
        nombre_archivo
    )

    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(
            f"No se encontró el archivo:\n{ruta_archivo}"
        )

    nombre_modulo = os.path.splitext(
        nombre_archivo
    )[0]

    especificacion = importlib.util.spec_from_file_location(
        nombre_modulo,
        ruta_archivo
    )

    modulo = importlib.util.module_from_spec(
        especificacion
    )

    especificacion.loader.exec_module(
        modulo
    )

    return modulo


if __name__ == "__main__":
    root = ctk.CTk()

    app = VentanaLogin(root)

    root.mainloop()
