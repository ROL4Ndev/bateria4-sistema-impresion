"""Sistema Simple de Impresión · Rolando Sanchez y Christian Roque."""

import sys

from impresion.consola import menu, demostracion
from impresion.pruebas_funcionales import ejecutar_pruebas

# INICIO DEL BLOQUE PARA LA ENTREGA
if __name__ == "__main__":
    if len(sys.argv) == 1:
        menu()
    elif sys.argv[1:] == ["--pruebas"]:
        ejecutar_pruebas()
    elif sys.argv[1:] == ["--demo"]:
        demostracion()
    else:
        print("Uso: python sistema_impresion.py [--pruebas | --demo]")
        sys.exit(2)
