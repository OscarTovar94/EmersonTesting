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


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


ARCHIVOS_MODELOS = {
    "PCBA Modelo 1": "TestPCB1.py",
    "PCBA Modelo 2": "TestPCB2.py",
    "PCBA Modelo 3": "TestPCB3.py"
}

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
            f"Empleado: {self.datos_login['empleado']}    |    "
            f"Orden: {self.datos_login['orden']}    |    "
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
            text=f"Configuración cargada: {self.datos_login['modelo']}",
            font=("Arial", 24, "bold")
        )
        self.label_modelo.pack(
            pady=(60, 15)
        )

        self.label_mensaje = ctk.CTkLabel(
            self.frame_contenido,
            text=(
                "En esta sección se cargará la secuencia de pruebas "
                "correspondiente al modelo seleccionado."
            ),
            font=("Arial", 17),
            text_color="#AEB4C8"
        )
        self.label_mensaje.pack(
            pady=10
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
            pady=40
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
            pady=30
        )

    def cerrar_sesion(self):
        """Cierra la ventana principal y regresa al Login."""

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
        """Ejecuta la secuencia del modelo seleccionado."""

        modelo_seleccionado = self.datos_login["modelo"]

        configuracion = CONFIGURACION_MODELOS.get(
            modelo_seleccionado
        )

        if configuracion is None:
            messagebox.showerror(
                "Modelo no configurado",
                f"No existe una configuración para:\n"
                f"{modelo_seleccionado}"
            )
            return

        nombre_archivo = configuracion["archivo"]
        nombre_clase = configuracion["clase"]

        try:
            self.boton_iniciar.configure(
                state="disabled",
                text="Ejecutando pruebas..."
            )

            self.ventana.update_idletasks()

            modulo_modelo = cargar_modulo_modelo(
                nombre_archivo
            )

            clase_prueba = getattr(
                modulo_modelo,
                nombre_clase
            )

            secuencia = clase_prueba()

            resultado = secuencia.ejecutar_pruebas()

            self.procesar_resultados(resultado)

        except FileNotFoundError as error:
            messagebox.showerror(
                "Archivo no encontrado",
                str(error)
            )

        except AttributeError:
            messagebox.showerror(
                "Clase no encontrada",
                f"El archivo {nombre_archivo} no contiene "
                f"la clase {nombre_clase}."
            )

        except Exception as error:
            messagebox.showerror(
                "Error de prueba",
                f"Ocurrió un error durante la prueba:\n{error}"
            )

        finally:
            self.boton_iniciar.configure(
                state="normal",
                text="Iniciar prueba"
            )

    def procesar_resultados(self, resultado):
        """Recibe los resultados enviados por modelo_1.py."""

        estado_ejecucion = resultado["estado"]
        resultado_final = resultado["resultado_final"]
        mensaje = resultado["mensaje"]
        mediciones = resultado["mediciones"]

        print("\nResultado recibido en main.py")
        print(f"Estado: {estado_ejecucion}")
        print(f"Resultado final: {resultado_final}")
        print(f"Mensaje: {mensaje}")

        for medicion in mediciones:
            print(
                f"{medicion['nombre']} | "
                f"Canal: {medicion['canal']} | "
                f"Valor: {medicion['valor']} | "
                f"Estado: {medicion['estado']}"
            )

        if estado_ejecucion == "ERROR":
            messagebox.showerror(
                "Error de ejecución",
                mensaje
            )
            return

        if resultado_final == "PASS":
            messagebox.showinfo(
                "Resultado",
                "La unidad terminó todas las pruebas correctamente.\n\n"
                "Resultado final: PASS"
            )

        else:
            messagebox.showwarning(
                "Resultado",
                "Una o más pruebas están fuera de límite.\n\n"
                "Resultado final: FAIL"
            )

def cargar_modulo_modelo(nombre_archivo):
    """
    Carga dinámicamente un archivo Python ubicado
    en la carpeta modelos.
    """

    ruta_base = obtener_ruta_base()

    ruta_modelo = os.path.join(
        ruta_base,
        "models",
        nombre_archivo
    )

    if not os.path.exists(ruta_modelo):
        raise FileNotFoundError(
            f"No se encontró el archivo del modelo:\n{ruta_modelo}"
        )

    nombre_modulo = os.path.splitext(nombre_archivo)[0]

    spec = importlib.util.spec_from_file_location(
        nombre_modulo,
        ruta_modelo
    )

    if spec is None or spec.loader is None:
        raise ImportError(
            f"No fue posible cargar el módulo {nombre_archivo}."
        )

    modulo = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(modulo)

    return modulo

if __name__ == "__main__":
    root = ctk.CTk()

    app = VentanaLogin(root)

    root.mainloop()