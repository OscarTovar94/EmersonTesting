import pyvisa

NOMBRE_MODELO = "ES-05585-1 640160"
NUMERO_PARTE = "640160"
RECURSO_VISA = "ASRL10::INSTR"

PRUEBAS = [
    {
        "numero": 1,
        "nombre": "Test_1",
        "descripcion": "Continuity J7-1 to J9-6",
        "canal": 101,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 2,
        "nombre": "Test_2",
        "descripcion": "Continuity J7-2 to J9-5",
        "canal": 102,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 3,
        "nombre": "Test_3",
        "descripcion": "Continuity J7-3 to J9-4",
        "canal": 103,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 4,
        "nombre": "Test_4",
        "descripcion": "Continuity J7-4 to J9-3",
        "canal": 104,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 5,
        "nombre": "Test_5",
        "descripcion": "Continuity J7-5 to J9-2",
        "canal": 105,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 6,
        "nombre": "Test_6",
        "descripcion": "Continuity J7-6 to J9-1",
        "canal": 106,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 7,
        "nombre": "Test_7",
        "descripcion": "Continuity J8-1 to J10-6",
        "canal": 107,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 8,
        "nombre": "Test_8",
        "descripcion": "Continuity J8-2 to J10-5",
        "canal": 108,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 9,
        "nombre": "Test_9",
        "descripcion": "Continuity J8-3 to J10-4",
        "canal": 109,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 10,
        "nombre": "Test_10",
        "descripcion": "Continuity J8-4 to J10-3",
        "canal": 110,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 11,
        "nombre": "Test_11",
        "descripcion": "Continuity J8-5 to J10-2",
        "canal": 111,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    },
    {
        "numero": 12,
        "nombre": "Test_12",
        "descripcion": "Continuity J8-6 to J10-1",
        "canal": 112,
        "minimo": 0.0,
        "maximo": 2.0,
        "unidad": "Ω"
    }
]


class PruebaModelo1:
    """Ejecuta las pruebas eléctricas del PCBA Modelo 1."""

    def __init__(self, recurso_visa=RECURSO_VISA):
        self.recurso_visa = recurso_visa

        self.rm = None
        self.daq = None

        self.resultados = []

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

            return True

        except Exception:
            self.cerrar()
            raise

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

    @staticmethod
    def evaluar_resultado(valor, minimo, maximo):
        """Compara una medición contra sus límites."""

        if minimo <= valor <= maximo:
            return "PASS"

        return "FAIL"

    def ejecutar_prueba_individual(self, prueba):
        """Ejecuta y evalúa una prueba individual."""

        numero = prueba["numero"]
        nombre = prueba["nombre"]
        descripcion = prueba["descripcion"]
        canal = prueba["canal"]
        minimo = prueba["minimo"]
        maximo = prueba["maximo"]
        unidad = prueba["unidad"]

        valor = self.medir_resistencia(canal)

        estado = self.evaluar_resultado(
            valor=valor,
            minimo=minimo,
            maximo=maximo
        )

        resultado = {
            "numero": numero,
            "nombre": nombre,
            "descripcion": descripcion,
            "canal": canal,
            "valor": valor,
            "minimo": minimo,
            "maximo": maximo,
            "unidad": unidad,
            "estado": estado,
            "error": ""
        }

        return resultado

    def ejecutar_pruebas(self):
        """
        Ejecuta las 16 pruebas.

        Regresa un diccionario que puede ser utilizado por main.py.
        """

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
                    resultado = self.ejecutar_prueba_individual(
                        prueba
                    )

                except Exception as error_prueba:
                    resultado = {
                        "numero": prueba["numero"],
                        "nombre": prueba["nombre"],
                        "descripcion": prueba["descripcion"],
                        "canal": prueba["canal"],
                        "valor": None,
                        "minimo": prueba["minimo"],
                        "maximo": prueba["maximo"],
                        "unidad": prueba["unidad"],
                        "estado": "ERROR",
                        "error": str(error_prueba)
                    }

                self.resultados.append(resultado)

                self.imprimir_resultado(resultado)

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
                if resultado["estado"] in ("FAIL", "ERROR")
            )

            if cantidad_fail == 0:
                resultado_final = "PASS"
            else:
                resultado_final = "FAIL"

            resultado_general.update({
                "estado": "OK",
                "mensaje": "Secuencia de pruebas terminada.",
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
            resultado_general["mensaje"] = str(error)

        except Exception as error:
            resultado_general["mensaje"] = (
                f"Error al ejecutar las pruebas: {error}"
            )

            resultado_general["mediciones"] = (
                self.resultados.copy()
            )

        finally:
            self.cerrar()

        return resultado_general

    @staticmethod
    def imprimir_resultado(resultado):
        """Muestra el resultado de una prueba en la consola."""

        valor = resultado["valor"]

        if valor is None:
            texto_valor = "Sin lectura"
        else:
            texto_valor = (
                f"{valor:.6f} {resultado['unidad']}"
            )

        print(
            f"{resultado['numero']:02d} | "
            f"{resultado['nombre']} | "
            f"Canal {resultado['canal']} | "
            f"{texto_valor} | "
            f"Límites: {resultado['minimo']} - "
            f"{resultado['maximo']} "
            f"{resultado['unidad']} | "
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
                    f"Error al cerrar ResourceManager: {error}"
                )
            finally:
                self.rm = None


if __name__ == "__main__":
    secuencia = PruebaModelo1()

    resultado = secuencia.ejecutar_pruebas()

    print("\n" + "=" * 70)
    print(f"Modelo: {resultado['modelo']}")
    print(f"Estado de ejecución: {resultado['estado']}")
    print(f"Mensaje: {resultado['mensaje']}")
    print(f"Error del equipo: {resultado['error_equipo']}")
    print(f"Pruebas PASS: {resultado['pruebas_pass']}")
    print(f"Pruebas FAIL: {resultado['pruebas_fail']}")
    print(f"Resultado final: {resultado['resultado_final']}")
    print("=" * 70)
