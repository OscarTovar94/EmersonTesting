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

import pyvisa


LIMITE_CONTINUIDAD = 2.0  # ohms


def medir_continuidad(
    instrumento,
    canal,
    limite=LIMITE_CONTINUIDAD
):
    """Medir la continuidad de un canal específico y comparar con el límite."""
    resultado = None

    comando = f"MEAS:RES? AUTO,(@{canal})"

    try:
        resistencia = float(instrumento.query(comando))
    except (ValueError, pyvisa.errors.VisaIOError) as error:
        return {
            "canal": canal,
            "resistencia": None,
            "resultado": "ERROR",
            "detalle": str(error),
        }

    resultado = "PASS" if resistencia <= limite else "FAIL"

    return {
        "canal": canal,
        "resistencia": resistencia,
        "resultado": resultado,
    }


rm = pyvisa.ResourceManager()

# Modifica la dirección según tu configuración GPIB.
daq = rm.open_resource("GPIB0::9::INSTR")

daq.timeout = 5000
daq.write("*RST")
daq.write("*CLS")

pruebas = [
    {"canal": 101, "desde": "TP1", "hasta": "TP15", "limite": 2.0},
    {"canal": 102, "desde": "J1-1", "hasta": "R23-1", "limite": 1.5},
    {"canal": 103, "desde": "J1-2", "hasta": "U4-7", "limite": 2.0},
]

for prueba in pruebas:
    resultado = medir_continuidad(
        daq,
        prueba["canal"],
        prueba["limite"],
    )

    print(
        prueba["desde"],
        "→",
        prueba["hasta"],
        resultado,
    )

daq.close()
rm.close()
