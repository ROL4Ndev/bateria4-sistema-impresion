"""Sistema Simple de Impresión · Rolando Sanchez y Christian Roque."""

from .sistema import SistemaImpresion
from .consola import cargar_demo

# INICIO DEL BLOQUE PARA LA ENTREGA

# BLOQUE DE PRUEBAS: se ejecuta con python sistema_impresion.py --pruebas
def ejecutar_pruebas():
    """Verifica comportamiento observable, errores y consistencia de los tiempos."""
    casos = 0

    def verificar(condicion, mensaje):
        # No usa assert para que Python -O no suprima las verificaciones.
        nonlocal casos
        if not condicion:
            raise AssertionError(mensaje)
        casos += 1
        print(f"OK {casos:02}: {mensaje}")

    def rechaza(operacion, mensaje):
        # Comprueba que una operación inválida no se acepta silenciosamente.
        try:
            operacion()
        except ValueError:
            verificar(True, mensaje)
        else:
            raise AssertionError(mensaje)

    sistema = SistemaImpresion()
    verificar(sistema.totales() == (0, 0), "Sistema vacío: cero trabajos y páginas")
    verificar(sistema.lideres_usuarios()[1] == 0, "Sistema vacío: sin usuario líder")
    rechaza(lambda: sistema.iniciar(1), "No iniciar una cola vacía")
    rechaza(lambda: sistema.completar(1), "No completar sin trabajo activo")
    cargar_demo(sistema)
    cola = sistema.obtener_impresora(1).cola
    verificar(tuple(t.id for t in cola) == ("T02", "T03", "T01"), "Prioridad Alta y FIFO entre altas")
    verificar(tuple(i.tiempo_estimado() for i in sistema.impresoras) == (60, 15, 25), "Tres colas independientes y 5 s por página")
    rechaza(lambda: sistema.enviar("T01", "x", "A", 1, 1, 1), "Rechazar ID duplicado")
    for paginas in (0, -1, 1.5, True):
        rechaza(lambda p=paginas: sistema.enviar("X", "x", "A", p, 1, 1), f"Rechazar páginas inválidas: {paginas}")
    for prioridad in (0, 3, True):
        rechaza(lambda p=prioridad: sistema.enviar("X", "x", "A", 1, p, 1), f"Rechazar prioridad inválida: {prioridad}")
    for numero in (0, 4, True):
        rechaza(lambda n=numero: sistema.obtener_impresora(n), f"Rechazar impresora inválida: {numero}")
    rechaza(lambda: sistema.enviar(" ", "x", "A", 1, 1, 1), "Rechazar ID vacío")
    rechaza(lambda: sistema.enviar("X", " ", "A", 1, 1, 1), "Rechazar archivo vacío")
    rechaza(lambda: sistema.enviar("X", "x", " ", 1, 1, 1), "Rechazar usuario vacío")
    verificar(sistema.historial.cantidad == 5, "Errores de entrada no registran trabajos")
    verificar(sistema.iniciar(1).id == "T02", "Extraer el siguiente trabajo prioritario")
    verificar(sistema.obtener_impresora(1).tiempo_estimado() == 60, "Activo mantiene su duración reservada")
    rechaza(lambda: sistema.iniciar(1), "No iniciar otro trabajo en una impresora ocupada")
    rechaza(lambda: sistema.cancelar("T02"), "No cancelar el trabajo activo")
    verificar(sistema.completar(1).estado == "Completado", "Cambio a estado Completado")
    verificar(sistema.totales() == (1, 2), "Contar solo trabajos y páginas completados")
    rechaza(lambda: sistema.completar(1), "Impedir doble contabilización al completar")
    rechaza(lambda: sistema.cancelar("T02"), "No cancelar un completado")
    verificar(sistema.cancelar("T01").estado == "Cancelado", "Cancelar pendiente al final")
    verificar(cola.segundos_pendientes == 20 and cola.cantidad == 1, "Cancelar actualiza tiempo y tamaño")
    rechaza(lambda: sistema.cancelar("NO_EXISTE"), "Rechazar ID inexistente")
    rechaza(lambda: sistema.cancelar("T01"), "No cancelar dos veces")
    rechaza(lambda: sistema.enviar("T01", "x", "A", 1, 1, 1), "No reutilizar ID cancelado")
    verificar(sistema.contar_usuario(" ROLANDO SANCHEZ ") == 3, "Consultar y contar por usuario normalizado")
    verificar(sistema.contar_usuario("Nadie") == 0, "Usuario inexistente: cero trabajos")
    sistema.iniciar(1)
    sistema.completar(1)
    lideres, cantidad = sistema.lideres_usuarios()
    verificar(cantidad == 1 and tuple(t.usuario for t in lideres) == ("Christian Roque", "Rolando Sanchez"), "Conservar empates entre usuarios")
    sistema.iniciar(2)
    sistema.completar(2)
    lideres, cantidad = sistema.lideres_usuarios()
    verificar(cantidad == 2 and tuple(t.usuario for t in lideres) == ("Christian Roque",), "Líder por trabajos completados")
    verificar(sistema.totales() == (3, 9), "Páginas impresas excluyen pendientes y cancelados")
    verificar(tuple(i.tiempo_estimado() for i in sistema.impresoras) == (0, 0, 25), "Colas vaciadas: tiempo cero")
    # Cabeza, medio y último nodo: comprueba el reenlace en todas las posiciones.
    otro = SistemaImpresion()
    for identificador in ("A", "B", "C", "D"):
        otro.enviar(identificador, "x.pdf", "Usuario", 1, 2, 3)
    verificar(tuple(t.id for t in otro.impresoras[2].cola) == ("A", "B", "C", "D"), "FIFO entre trabajos normales")
    otro.cancelar("B")
    otro.cancelar("A")
    otro.cancelar("D")
    verificar(tuple(t.id for t in otro.impresoras[2].cola) == ("C",), "Cancelar nodo medio, cabeza y último")
    otro.cancelar("C")
    verificar(otro.impresoras[2].cola.primero is None and otro.impresoras[2].tiempo_estimado() == 0, "Cancelar único nodo deja cola vacía")
    # Dos impresoras pueden tener trabajos activos al mismo tiempo.
    otro.enviar("E", "e.pdf", "Usuario", 2, 2, 1)
    otro.enviar("F", "f.pdf", "Usuario", 3, 1, 2)
    otro.iniciar(1)
    otro.iniciar(2)
    otro.enviar("G", "g.pdf", "Usuario", 1, 1, 1)
    verificar(otro.impresoras[0].actual.id == "E", "Alta nueva no interrumpe un trabajo activo")
    verificar(otro.impresoras[1].actual.id == "F", "Actividad simultánea en impresoras distintas")
    verificar(otro.impresoras[0].tiempo_estimado() == 15, "Tiempo incluye activo más nuevas llegadas")
    otro.completar(1)
    otro.completar(2)
    verificar(tuple(i.numero for i in otro.impresoras if i.completados == 1) == (1, 2), "Conservar empate entre impresoras")
    verificar(sistema.historial.buscar("T01").estado == "Cancelado", "Historial conserva el estado cancelado")
    print(f"\nRESULTADO: {casos} verificaciones correctas.")


