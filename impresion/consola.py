"""Sistema Simple de Impresión · Rolando Sanchez y Christian Roque."""

from .sistema import SistemaImpresion

# INICIO DEL BLOQUE PARA LA ENTREGA
def duracion(segundos):
    """Convierte segundos en minutos y segundos sin perder la unidad original."""
    minutos, resto = divmod(segundos, 60)
    return f"{segundos} s ({minutos} min {resto:02} s)"


def mostrar_trabajos(trabajos):
    """Imprime un iterable de trabajos y avisa cuando no contiene resultados."""
    print(f"{'ID':<8} {'ARCHIVO':<22} {'USUARIO':<19} {'PAGS':>4}  {'PRIOR.':<6} IMP ESTADO")
    cantidad = 0
    for trabajo in trabajos:
        print(trabajo)
        cantidad += 1
    if cantidad == 0:
        print("Sin trabajos para mostrar.")


def mostrar_tiempos(sistema):
    """Distingue suma de carga y tiempo paralelo para vaciar todas las impresoras."""
    total = 0
    maximo = 0
    for impresora in sistema.impresoras:
        segundos = impresora.tiempo_estimado()
        print(f"Impresora {impresora.numero}: {duracion(segundos)}")
        total += segundos
        maximo = max(maximo, segundos)
    print(f"Carga acumulada de las tres: {duracion(total)}")
    print(f"Tiempo para vaciar todas en paralelo: {duracion(maximo)}")
    print("Estimación sin nuevas llegadas. El trabajo activo reserva su duración completa.")


def mostrar_estadisticas(sistema):
    """Muestra métricas de completados y conserva todos los empates."""
    trabajos, paginas = sistema.totales()
    print(f"Trabajos completados: {trabajos}")
    print(f"Páginas totales impresas: {paginas}")
    lideres, maximo = sistema.lideres_usuarios()
    if maximo == 0:
        print("Usuario con más impresiones: sin trabajos completados.")
        print("Impresora con más completados: sin trabajos completados.")
        return
    print(f"Usuario(s) con más impresiones ({maximo} trabajo(s) completado(s)):")
    for trabajo in lideres:
        print(f"  {trabajo.usuario}")
    maximo_impresora = max(imp.completados for imp in sistema.impresoras)
    print(f"Impresora(s) con más completados ({maximo_impresora}):")
    for impresora in sistema.impresoras:
        if impresora.completados == maximo_impresora:
            print(f"  Impresora {impresora.numero}")


def leer_entero(mensaje, minimo, maximo=None):
    """Repite la lectura si la entrada no es un entero dentro del rango."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < minimo or (maximo is not None and valor > maximo):
                raise ValueError
            return valor
        except ValueError:
            limite = f" a {maximo}" if maximo is not None else " o mayor"
            print(f"Ingrese un entero de {minimo}{limite}.")


def cargar_demo(sistema):
    """Carga datos reproducibles usando las mismas validaciones del menú."""
    if sistema.historial.cantidad:
        raise ValueError("La demostración requiere un sistema vacío. Reinicie para cargarla.")
    sistema.enviar("T01", "informe.pdf", "Rolando Sanchez", 6, 2, 1)
    sistema.enviar("T02", "urgente.pdf", "Christian Roque", 2, 1, 1)
    sistema.enviar("T03", "planos.pdf", "Rolando Sanchez", 4, 1, 1)
    sistema.enviar("T04", "ficha.pdf", "Christian Roque", 3, 2, 2)
    sistema.enviar("T05", "resumen.pdf", "Rolando Sanchez", 5, 2, 3)


def demostracion():
    """Ejecuta un caso determinista útil para la exposición y las capturas."""
    sistema = SistemaImpresion()
    cargar_demo(sistema)
    print("SISTEMA SIMPLE DE IMPRESIÓN - DEMOSTRACIÓN")
    print("Rolando Sanchez y Christian Roque\n")
    print("1. COLA DE LA IMPRESORA 1: prioridad y FIFO")
    mostrar_trabajos(sistema.obtener_impresora(1).cola)
    print("\n2. TIEMPOS INICIALES")
    mostrar_tiempos(sistema)
    print("\n3. PROCESAMIENTO")
    print(f"Iniciado: {sistema.iniciar(1).id}")
    print(f"Completado: {sistema.completar(1).id}")
    print(f"Cancelado: {sistema.cancelar('T01').id}")
    print(f"Iniciado: {sistema.iniciar(1).id}")
    print(f"Completado: {sistema.completar(1).id}")
    print("\n4. HISTORIAL DE ROLANDO")
    mostrar_trabajos(sistema.trabajos_usuario("rolando sanchez"))
    print(f"Trabajos enviados por Rolando: {sistema.contar_usuario('Rolando Sanchez')}")
    print("\n5. ESTADÍSTICAS FINALES")
    mostrar_estadisticas(sistema)
    print("\n6. TIEMPOS FINALES")
    mostrar_tiempos(sistema)


def menu():
    """Mantiene el sistema en memoria hasta que el usuario decide salir."""
    sistema = SistemaImpresion()
    while True:
        print("\nSISTEMA SIMPLE DE IMPRESIÓN")
        print("1. Enviar trabajo")
        print("2. Iniciar siguiente trabajo")
        print("3. Marcar trabajo activo como completado")
        print("4. Cancelar trabajo pendiente")
        print("5. Ver pendientes y trabajo activo de una impresora")
        print("6. Ver trabajos de un usuario")
        print("7. Ver tiempos de las tres impresoras")
        print("8. Ver tiempo de una impresora")
        print("9. Contar trabajos de un usuario")
        print("10. Ver estadísticas y páginas impresas")
        print("11. Ver historial completo")
        print("12. Cargar datos de demostración (sistema vacío)")
        print("0. Salir")
        try:
            opcion = leer_entero("Opción: ", 0, 12)
            if opcion == 0:
                print("Programa finalizado. Los datos de esta sesión no se guardan.")
                return
            if opcion == 1:
                identificador = input("ID único: ")
                archivo = input("Nombre del archivo: ")
                usuario = input("Usuario: ")
                paginas = leer_entero("Número de páginas: ", 1)
                prioridad = leer_entero("Prioridad (1 Alta, 2 Normal): ", 1, 2)
                numero = leer_entero("Impresora (1-3): ", 1, 3)
                trabajo = sistema.enviar(identificador, archivo, usuario, paginas, prioridad, numero)
                print(f"Trabajo {trabajo.id} registrado en impresora {numero}.")
            elif opcion == 2:
                numero = leer_entero("Impresora (1-3): ", 1, 3)
                print(f"En impresión: {sistema.iniciar(numero).id}")
            elif opcion == 3:
                numero = leer_entero("Impresora (1-3): ", 1, 3)
                print(f"Completado: {sistema.completar(numero).id}")
            elif opcion == 4:
                print(f"Cancelado: {sistema.cancelar(input('ID pendiente: ')).id}")
            elif opcion == 5:
                impresora = sistema.obtener_impresora(leer_entero("Impresora (1-3): ", 1, 3))
                print("Activo:", impresora.actual if impresora.actual else "Ninguno")
                print("Pendientes en orden de atención:")
                mostrar_trabajos(impresora.cola)
            elif opcion == 6:
                mostrar_trabajos(sistema.trabajos_usuario(input("Usuario: ")))
            elif opcion == 7:
                mostrar_tiempos(sistema)
            elif opcion == 8:
                impresora = sistema.obtener_impresora(leer_entero("Impresora (1-3): ", 1, 3))
                print(f"Tiempo estimado: {duracion(impresora.tiempo_estimado())}")
                print("Incluye la duración completa del activo y todos los pendientes.")
            elif opcion == 9:
                print(f"Trabajos enviados: {sistema.contar_usuario(input('Usuario: '))}")
            elif opcion == 10:
                mostrar_estadisticas(sistema)
            elif opcion == 11:
                mostrar_trabajos(sistema.historial)
            elif opcion == 12:
                cargar_demo(sistema)
                print("Cinco trabajos cargados. Consulte las colas y los tiempos.")
        except ValueError as error:
            print(f"No se pudo realizar la operación: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma finalizado.")
            return

