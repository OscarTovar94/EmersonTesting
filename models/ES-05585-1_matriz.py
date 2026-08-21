import pyvisa
import time
from itertools import combinations

# ============================================================
# CONFIGURACIÓN GENERAL DEL MODELO
# ============================================================

NOMBRE_MODELO = "ES-05585-1 640160"
NUMERO_PARTE = "640160"
RECURSO_VISA = "ASRL10::INSTR"

# ------------------------------------------------------------
# DISTRIBUCIÓN DE MÓDULOS EN EL 34970A
#
# SLOT 1 -> 34902A  (continuidades + canal de matriz)
# SLOT 2 -> 34907A  (selección HI)
# SLOT 3 -> 34907A  (selección LO)
#
# En un 34907A:
#   s01 = puerto digital 1
#   s02 = puerto digital 2
#
# Ejemplo:
#   slot 2, puerto 1 -> canal 201
#   slot 2, puerto 2 -> canal 202
#   slot 3, puerto 1 -> canal 301
#   slot 3, puerto 2 -> canal 302
# ------------------------------------------------------------

PUERTO_HI_1 = 201
PUERTO_HI_2 = 202

PUERTO_LO_1 = 301
PUERTO_LO_2 = 302

# Canal del 34902A reservado para medir la matriz de cortos.
CANAL_MATRIZ = 104

# Tiempo para permitir que los relevadores se estabilicen.
TIEMPO_RELE = 0.500

# IMPORTANTE:
# Este ejemplo asume que escribir un bit = 1 activa el relé
# correspondiente y 0 lo desactiva.
#
# Si tu interfaz 34907A -> ULN2803A queda invertida eléctricamente,
# cambia esta constante a False y valida primero con UN SOLO relé.
SALIDA_ACTIVA_EN_1 = False


# ============================================================
# MAPEO DE LAS 12 REDES
# ============================================================
#
# Cada pareja representa la continuidad que sí debe existir.
#
# NET1  = J7-1 / J9-6
# NET2  = J7-2 / J9-5
# ...
#
# NET1 a NET8  -> puerto 1, bits 0 a 7
# NET9 a NET12 -> puerto 2, bits 0 a 3
# ============================================================

"""
C=n(n-1)/2
"""

REDES = {
    1:  {"nombre": "NET1",  "puntos": "J7-1 / J9-6",  "puerto": 1, "bit": 0},
    2:  {"nombre": "NET2",  "puntos": "J7-2 / J9-5",  "puerto": 1, "bit": 1},
    3:  {"nombre": "NET3",  "puntos": "J7-3 / J9-4",  "puerto": 1, "bit": 2},
    4:  {"nombre": "NET4",  "puntos": "J7-4 / J9-3",  "puerto": 1, "bit": 3},
    5:  {"nombre": "NET5",  "puntos": "J7-5 / J9-2",  "puerto": 1, "bit": 4},
    6:  {"nombre": "NET6",  "puntos": "J7-6 / J9-1",  "puerto": 1, "bit": 5},
    7:  {"nombre": "NET7",  "puntos": "J8-1 / J10-6", "puerto": 1, "bit": 6},
    8:  {"nombre": "NET8",  "puntos": "J8-2 / J10-5", "puerto": 1, "bit": 7},
    9:  {"nombre": "NET9",  "puntos": "J8-3 / J10-4", "puerto": 2, "bit": 0},
    10: {"nombre": "NET10", "puntos": "J8-4 / J10-3", "puerto": 2, "bit": 1},
    11: {"nombre": "NET11", "puntos": "J8-5 / J10-2", "puerto": 2, "bit": 2},
    12: {"nombre": "NET12", "puntos": "J8-6 / J10-1", "puerto": 2, "bit": 3},
}


# ============================================================
# PRUEBAS DE CONTINUIDAD
# ============================================================

PRUEBAS_CONTINUIDAD = [
    {
        "numero": 1,
        "nombre": "Test_1",
        "tipo": "CONTINUITY",
        "descripcion": "Continuity J7-1 to J9-6",
        "canal": 101,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 2,
        "nombre": "Test_2",
        "tipo": "CONTINUITY",
        "descripcion": "Continuity J7-2 to J9-5",
        "canal": 102,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 3,
        "nombre": "Test_3",
        "tipo": "CONTINUITY",
        "descripcion": "Continuity J7-3 to J9-4",
        "canal": 103,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 4,
        "nombre": "Test_4",
        "tipo": "CONTINUITY",
        "descripcion": "Continuity J7-4 to J9-3",
        "canal": 104,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 5,
        "nombre": "Test_5",
        "tipo": "CONTINUITY",
        "descripcion": "Continuity J7-5 to J9-2",
        "canal": 105,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 6,
        "nombre": "Test_6",
        "tipo": "CONTINUITY",
        "descripcion": "Continuity J7-6 to J9-1",
        "canal": 106,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 7,
        "nombre": "Test_7",
        "tipo": "CONTINUITY",
        "descripcion": "Continuity J8-1 to J10-6",
        "canal": 107,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 8,
        "nombre": "Test_8",
        "tipo": "CONTINUITY",
        "descripcion": "Continuity J8-2 to J10-5",
        "canal": 108,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 9,
        "nombre": "Test_9",
        "tipo": "CONTINUITY",
        "descripcion": "Continuity J8-3 to J10-4",
        "canal": 109,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 10,
        "nombre": "Test_10",
        "tipo": "CONTINUITY",
        "descripcion": "Continuity J8-4 to J10-3",
        "canal": 110,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 11,
        "nombre": "Test_11",
        "tipo": "CONTINUITY",
        "descripcion": "Continuity J8-5 to J10-2",
        "canal": 111,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 12,
        "nombre": "Test_12",
        "tipo": "CONTINUITY",
        "descripcion": "Continuity J8-6 to J10-1",
        "canal": 112,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
]

# ============================================================
# GENERAR LAS 66 PRUEBAS DE CORTO
# ============================================================
#
# OJO:
# LIMITE_SHORT_MINIMO es solamente un valor de ejemplo.
# Debe definirse después de caracterizar eléctricamente la PCB.
# Si las redes tienen componentes entre ellas, 100 kΩ puede no
# ser el criterio correcto.
# ============================================================

LIMITE_SHORT_MINIMO = 100_000.0

PRUEBAS_SHORT = []

numero_prueba = len(PRUEBAS_CONTINUIDAD) + 1

for net_hi, net_lo in combinations(REDES.keys(), 2):
    PRUEBAS_SHORT.append(
        {
            "numero": numero_prueba,
            "nombre": f"Test_{numero_prueba}",
            "tipo": "SHORT",
            "descripcion": (
                f"Short {REDES[net_hi]['nombre']} to "
                f"{REDES[net_lo]['nombre']} | "
                f"{REDES[net_hi]['puntos']} <-> "
                f"{REDES[net_lo]['puntos']}"
            ),
            "hi": net_hi,
            "lo": net_lo,
            "canal": CANAL_MATRIZ,
            "minimo": LIMITE_SHORT_MINIMO,
            "maximo": None,
            "unidad": "Ω"
        }
    )

    numero_prueba += 1


# Lista completa que usa main.py
PRUEBAS = PRUEBAS_CONTINUIDAD + PRUEBAS_SHORT


class PruebaModelo1:
    """Ejecuta las pruebas eléctricas del PCBA ES-05585-1."""

    def __init__(self, recurso_visa=RECURSO_VISA):
        self.recurso_visa = recurso_visa
        self.rm = None
        self.daq = None
        self.resultados = []

    # ========================================================
    # CONEXIÓN
    # ========================================================

    def conectar(self):
        """Establece comunicación con el Keysight 34970A."""

        try:
            self.rm = pyvisa.ResourceManager()

            recursos = self.rm.list_resources()

            print("Recursos VISA encontrados:")
            print(recursos)

            if self.recurso_visa not in recursos:
                raise ConnectionError(
                    f"El recurso {self.recurso_visa} no fue encontrado."
                )

            self.daq = self.rm.open_resource(
                self.recurso_visa
            )

            self.daq.timeout = 15000
            self.daq.write_termination = "\n"
            self.daq.read_termination = "\n"

            self.daq.write("*CLS")
            self.daq.write("*RST")

            # Esperar a que el 34970A termine el reset
            time.sleep(2.0)

            # Inicializar matriz
            self.apagar_matriz()

            # Dejar estabilizar relevadores / puertos
            time.sleep(0.25)

            error = self.daq.query(
                "SYST:ERR?"
            ).strip()

            print(
                "Estado DAQ después de inicialización:",
                error
            )

            # Seguridad: al iniciar, intentar dejar toda la matriz apagada.
            self.apagar_matriz()

            return True

        except Exception:
            self.cerrar()
            raise

    # ========================================================
    # CONTROL DIGITAL 34907A
    # ========================================================

    def escribir_puerto_digital(self, canal_puerto, valor):
        """
        Escribe un byte decimal (0...255) a un puerto del 34907A.

        Ejemplos SCPI:
            SOUR:DIG:DATA:BYTE 1,(@201)
            SOUR:DIG:DATA:BYTE 128,(@201)
            SOUR:DIG:DATA:BYTE 0,(@202)
        """

        if self.daq is None:
            raise RuntimeError(
                "No existe una conexión activa con el DAQ."
            )

        if not 0 <= valor <= 255:
            raise ValueError(
                "El valor digital debe estar entre 0 y 255."
            )

        comando = (
            f"SOUR:DIG:DATA:BYTE {valor},"
            f"(@{canal_puerto})"
        )

        print(f"[DIO] {comando}")
        self.daq.write(comando)

    def valor_activo(self, bit):
        """
        Retorna el valor decimal que corresponde a un bit.

        bit 0 -> 1
        bit 1 -> 2
        bit 2 -> 4
        bit 3 -> 8
        ...
        bit 7 -> 128
        """

        mascara = 1 << bit

        if SALIDA_ACTIVA_EN_1:
            return mascara

        # Si la interfaz física es activa en 0, todos los demás
        # bits quedan en 1 y solamente el bit seleccionado queda en 0.
        return 255 ^ mascara

    def valor_apagado(self):
        """
        Retorna el byte que deja todas las salidas inactivas,
        según la polaridad configurada.
        """

        if SALIDA_ACTIVA_EN_1:
            return 0

        return 255

    def apagar_hi(self):
        """Desactiva todos los relevadores del banco HI."""

        valor = self.valor_apagado()

        self.escribir_puerto_digital(
            PUERTO_HI_1,
            valor
        )

        self.escribir_puerto_digital(
            PUERTO_HI_2,
            valor
        )

    def apagar_lo(self):
        """Desactiva todos los relevadores del banco LO."""

        valor = self.valor_apagado()

        self.escribir_puerto_digital(
            PUERTO_LO_1,
            valor
        )

        self.escribir_puerto_digital(
            PUERTO_LO_2,
            valor
        )

    def apagar_matriz(self):
        """Desactiva todos los relevadores HI y LO."""

        self.apagar_hi()
        self.apagar_lo()

    def activar_net_hi(self, numero_net):
        """
        Activa una sola NET en el banco HI.

        NET1..NET8  -> puerto 201
        NET9..NET12 -> puerto 202
        """

        if numero_net not in REDES:
            raise ValueError(
                f"NET HI no válida: {numero_net}"
            )

        datos = REDES[numero_net]

        # Break-before-make.
        self.apagar_hi()
        time.sleep(0.010)

        if datos["puerto"] == 1:
            canal_puerto = PUERTO_HI_1
        else:
            canal_puerto = PUERTO_HI_2

        valor = self.valor_activo(
            datos["bit"]
        )

        self.escribir_puerto_digital(
            canal_puerto,
            valor
        )

        print(
            f"[HI] {datos['nombre']} activada -> "
            f"{datos['puntos']} | "
            f"Puerto {canal_puerto} | "
            f"Bit {datos['bit']} | Valor {valor}"
        )

    def activar_net_lo(self, numero_net):
        """
        Activa una sola NET en el banco LO.

        NET1..NET8  -> puerto 301
        NET9..NET12 -> puerto 302
        """

        if numero_net not in REDES:
            raise ValueError(
                f"NET LO no válida: {numero_net}"
            )

        datos = REDES[numero_net]

        # Break-before-make.
        self.apagar_lo()
        time.sleep(0.010)

        if datos["puerto"] == 1:
            canal_puerto = PUERTO_LO_1
        else:
            canal_puerto = PUERTO_LO_2

        valor = self.valor_activo(
            datos["bit"]
        )

        self.escribir_puerto_digital(
            canal_puerto,
            valor
        )

        print(
            f"[LO] {datos['nombre']} activada -> "
            f"{datos['puntos']} | "
            f"Puerto {canal_puerto} | "
            f"Bit {datos['bit']} | Valor {valor}"
        )

    def seleccionar_matriz(self, net_hi, net_lo):
        """
        Selecciona las dos redes que serán medidas por el DMM.
        """

        if net_hi == net_lo:
            raise ValueError(
                "HI y LO no pueden conectarse a la misma NET."
            )

        # Primero todo OFF.
        self.apagar_matriz()
        time.sleep(0.010)

        # Después seleccionar un solo HI y un solo LO.
        self.activar_net_hi(net_hi)
        self.activar_net_lo(net_lo)

        # Tiempo de estabilización del relevador.
        time.sleep(TIEMPO_RELE)

    # ========================================================
    # MEDICIÓN DE RESISTENCIA
    # ========================================================

    def medir_resistencia(self, canal):
        """Realiza una medición de resistencia en un canal."""

        if self.daq is None:
            raise RuntimeError(
                "No existe una conexión activa con el DAQ."
            )

        respuesta = self.daq.query(
            f"MEAS:RES? (@{canal})"
        )

        respuesta = respuesta.strip()

        return float(respuesta)

    # ========================================================
    # EVALUACIÓN
    # ========================================================

    @staticmethod
    def evaluar_resultado(
        valor,
        minimo,
        maximo
    ):
        """
        Evalúa la medición.

        CONTINUIDAD:
            minimo <= valor <= maximo

        SHORT:
            minimo <= valor
            porque maximo es None.
        """

        if maximo is None:
            return (
                "PASS"
                if valor >= minimo
                else "FAIL"
            )

        return (
            "PASS"
            if minimo <= valor <= maximo
            else "FAIL"
        )

    # ========================================================
    # EJECUCIÓN DE UNA PRUEBA
    # ========================================================

    def ejecutar_prueba_individual(self, prueba):
        """Ejecuta continuidad o prueba de corto."""

        numero = prueba["numero"]
        nombre = prueba["nombre"]
        tipo = prueba.get(
            "tipo",
            "CONTINUITY"
        )
        descripcion = prueba["descripcion"]
        canal = prueba["canal"]
        minimo = prueba["minimo"]
        maximo = prueba["maximo"]
        unidad = prueba["unidad"]

        try:
            if tipo == "CONTINUITY":

                valor = self.medir_resistencia(
                    canal
                )

            elif tipo == "SHORT":

                net_hi = prueba["hi"]
                net_lo = prueba["lo"]

                self.seleccionar_matriz(
                    net_hi,
                    net_lo
                )

                valor = self.medir_resistencia(
                    canal
                )

            else:
                raise ValueError(
                    f"Tipo de prueba desconocido: {tipo}"
                )

            estado = self.evaluar_resultado(
                valor=valor,
                minimo=minimo,
                maximo=maximo
            )

            return {
                "numero": numero,
                "nombre": nombre,
                "tipo": tipo,
                "descripcion": descripcion,
                "canal": canal,
                "valor": valor,
                "minimo": minimo,
                "maximo": maximo,
                "unidad": unidad,
                "estado": estado,
                "error": ""
            }

        finally:
            # Después de cada SHORT se apagan los relevadores.
            if tipo == "SHORT":
                try:
                    self.apagar_matriz()
                except Exception:
                    pass

    # ========================================================
    # SECUENCIA COMPLETA
    # ========================================================

    def ejecutar_pruebas(self, callback_resultado=None):
        """Ejecuta continuidades y cortos."""

        self.resultados.clear()

        resultado_general = {
            "modelo": NOMBRE_MODELO,
            "estado": "ERROR",
            "mensaje": "",
            "error_equipo": "",
            "total_pruebas": len(PRUEBAS),
            "pruebas_pass": 0,
            "pruebas_fail": 0,
            "resultado_final": "FAIL",
            "mediciones": []
        }

        try:
            self.conectar()

            for prueba in PRUEBAS:

                try:
                    resultado = (
                        self.ejecutar_prueba_individual(
                            prueba
                        )
                    )

                except Exception as error_prueba:
                    resultado = {
                        "numero": prueba["numero"],
                        "nombre": prueba["nombre"],
                        "tipo": prueba.get(
                            "tipo",
                            ""
                        ),
                        "descripcion": prueba["descripcion"],
                        "canal": prueba["canal"],
                        "valor": None,
                        "minimo": prueba["minimo"],
                        "maximo": prueba["maximo"],
                        "unidad": prueba["unidad"],
                        "estado": "ERROR",
                        "error": str(error_prueba)
                    }

                self.resultados.append(
                    resultado
                )

                self.imprimir_resultado(
                    resultado
                )

                if callback_resultado is not None:
                    callback_resultado(
                        resultado
                    )

            error_equipo = self.daq.query(
                "SYST:ERR?"
            ).strip()

            cantidad_pass = sum(
                1
                for resultado in self.resultados
                if resultado["estado"] == "PASS"
            )

            cantidad_fail = sum(
                1
                for resultado in self.resultados
                if resultado["estado"] in (
                    "FAIL",
                    "ERROR"
                )
            )

            resultado_final = (
                "PASS"
                if cantidad_fail == 0
                else "FAIL"
            )

            resultado_general.update({
                "estado": "OK",
                "mensaje": (
                    "Secuencia de pruebas terminada."
                ),
                "error_equipo": error_equipo,
                "pruebas_pass": cantidad_pass,
                "pruebas_fail": cantidad_fail,
                "resultado_final": resultado_final,
                "mediciones": self.resultados.copy()
            })

        except pyvisa.errors.VisaIOError as error:

            resultado_general["mensaje"] = (
                f"Error de comunicación VISA: {error}"
            )

            resultado_general["mediciones"] = (
                self.resultados.copy()
            )

        except ConnectionError as error:
            resultado_general["mensaje"] = str(
                error
            )

        except Exception as error:
            resultado_general["mensaje"] = (
                f"Error al ejecutar las pruebas: {error}"
            )

            resultado_general["mediciones"] = (
                self.resultados.copy()
            )

        finally:
            try:
                self.apagar_matriz()
            except Exception:
                pass

            self.cerrar()

        return resultado_general

    @staticmethod
    def imprimir_resultado(resultado):
        """Muestra el resultado de una prueba."""

        valor = resultado["valor"]

        if valor is None:
            texto_valor = "Sin lectura"
        else:
            texto_valor = (
                f"{valor:.6f} "
                f"{resultado['unidad']}"
            )

        print(
            f"{resultado['numero']:02d} | "
            f"{resultado.get('tipo', '')} | "
            f"{resultado['nombre']} | "
            f"Canal {resultado['canal']} | "
            f"{texto_valor} | "
            f"{resultado['estado']}"
        )

    def cerrar(self):
        """Cierra la conexión VISA."""

        if self.daq is not None:
            try:
                self.daq.close()
            except Exception as error:
                print(
                    f"Error al cerrar el DAQ: {error}"
                )
            finally:
                self.daq = None

        if self.rm is not None:
            try:
                self.rm.close()
            except Exception as error:
                print(
                    "Error al cerrar "
                    f"ResourceManager: {error}"
                )
            finally:
                self.rm = None


if __name__ == "__main__":
    secuencia = PruebaModelo1()

    resultado = secuencia.ejecutar_pruebas()

    print("\n" + "=" * 70)
    print(
        f"Modelo: {resultado['modelo']}"
    )
    print(
        "Estado de ejecución: "
        f"{resultado['estado']}"
    )
    print(
        f"Mensaje: {resultado['mensaje']}"
    )
    print(
        "Error del equipo: "
        f"{resultado['error_equipo']}"
    )
    print(
        "Pruebas PASS: "
        f"{resultado['pruebas_pass']}"
    )
    print(
        "Pruebas FAIL: "
        f"{resultado['pruebas_fail']}"
    )
    print(
        "Resultado final: "
        f"{resultado['resultado_final']}"
    )
    print("=" * 70)
