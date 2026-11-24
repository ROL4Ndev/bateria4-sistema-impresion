"""Reúne los módulos en el único archivo Python solicitado por la guía.

Uso desde la raíz: python herramientas/generar_entrega.py
Solo necesita la biblioteca estándar de Python.
"""
from pathlib import Path
import ast

RAIZ = Path(__file__).resolve().parents[1]
MARCADOR = "# INICIO DEL BLOQUE PARA LA ENTREGA\n"
MODULOS = ['impresion/trabajo.py', 'impresion/nodo.py', 'impresion/lista_trabajos.py', 'impresion/cola_prioridad.py', 'impresion/impresora.py', 'impresion/sistema.py', 'impresion/consola.py', 'impresion/pruebas_funcionales.py', 'main.py']
CABECERA = '"""Batería 4, ejercicio 1: Sistema Simple de Impresión.\n\nIntegrantes: Rolando Sanchez y Christian Roque.\nPython 3.10 o superior. Sin dependencias externas.\nUso: python sistema_impresion.py [--pruebas | --demo]\n"""\n\nimport sys\n\n\n'


def generar():
    """Conserva el orden de las clases y deja las pruebas al final."""
    bloques = []
    for nombre in MODULOS:
        texto = (RAIZ / nombre).read_text(encoding="utf-8")
        if texto.count(MARCADOR) != 1:
            raise ValueError(f"Marcador ausente o repetido en {nombre}")
        bloques.append(texto.split(MARCADOR, 1)[1])
    resultado = CABECERA + "".join(bloques)
    arbol = ast.parse(resultado)
    clases = [n.name for n in arbol.body if isinstance(n, ast.ClassDef)]
    if clases != ["Trabajo", "Nodo", "ListaTrabajos", "ColaPrioridad", "Impresora", "SistemaImpresion"]:
        raise ValueError("La entrega debe contener las seis clases en orden.")
    destino = RAIZ / "sistema_impresion.py"
    destino.write_text(resultado, encoding="utf-8", newline="\n")
    print(f"Generado: {destino.name} (6 clases, menú y pruebas integrados).")


if __name__ == "__main__":
    generar()
