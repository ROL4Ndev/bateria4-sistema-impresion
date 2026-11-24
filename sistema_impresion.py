"""Batería 4, ejercicio 1: Sistema Simple de Impresión.

Integrantes: Rolando Sanchez y Christian Roque.
Python 3.10 o superior. Sin dependencias externas.
Uso: python sistema_impresion.py [--pruebas | --demo]
"""

import sys


class Trabajo:
    """Conserva los datos y el estado de un único trabajo."""

    def __init__(self, identificador, archivo, usuario, paginas, prioridad, impresora):
        # El sistema valida estos datos antes de construir el objeto.
        self.id = identificador
        self.archivo = archivo
        self.usuario = usuario
        self.paginas = paginas
        self.prioridad = prioridad
        self.impresora = impresora
        self.estado = "Pendiente"

    @property
    def segundos(self):
        """Cada página requiere los cinco segundos indicados en el enunciado."""
        return self.paginas * 5

    def __str__(self):
        # Una fila legible permite mostrar el mismo trabajo en varias consultas.
        prioridad = "Alta" if self.prioridad == 1 else "Normal"
        return (f"{self.id:<8} {self.archivo:<22} {self.usuario:<19} "
                f"{self.paginas:>4}  {prioridad:<6} {self.impresora:^3} {self.estado}")


class Nodo:
    """Nodo simple. Cada lista utiliza sus propios nodos."""

    def __init__(self, trabajo, siguiente=None):
        # Dos nodos distintos pueden referirse al mismo objeto Trabajo.
        self.trabajo = trabajo
        self.siguiente = siguiente


class ListaTrabajos:
    """Registro enlazado que conserva incluso trabajos cancelados y completados."""

    def __init__(self):
        # El puntero final permite agregar al historial en tiempo constante.
        self.primero = None
        self.ultimo = None
        self.cantidad = 0

    def agregar(self, trabajo):
        """Agrega una referencia al final, sin copiar ni cambiar el trabajo."""
        nuevo = Nodo(trabajo)
        if self.ultimo is None:
            self.primero = nuevo
        else:
            self.ultimo.siguiente = nuevo
        self.ultimo = nuevo
        self.cantidad += 1

    def buscar(self, identificador):
        """Recorre el historial para encontrar el ID, o devuelve None."""
        for trabajo in self:
            if trabajo.id == identificador:
                return trabajo
        return None

    def __iter__(self):
        """Entrega cada trabajo sin construir una lista auxiliar."""
        actual = self.primero
        while actual is not None:
            yield actual.trabajo
            actual = actual.siguiente


class ColaPrioridad:
    """Cola enlazada ordenada: 1 antes que 2 y FIFO dentro de cada prioridad."""

    def __init__(self):
        # Solo almacena trabajos pendientes de una impresora.
        self.primero = None
        self.cantidad = 0
        self.segundos_pendientes = 0

    def insertar(self, trabajo):
        """Inserta después de TODOS los de igual prioridad para respetar FIFO."""
        nuevo = Nodo(trabajo)
        if self.primero is None or trabajo.prioridad < self.primero.trabajo.prioridad:
            nuevo.siguiente = self.primero
            self.primero = nuevo
        else:
            actual = self.primero
            # El <= es esencial: no adelantamos trabajos de la misma prioridad.
            while (actual.siguiente is not None and
                   actual.siguiente.trabajo.prioridad <= trabajo.prioridad):
                actual = actual.siguiente
            nuevo.siguiente = actual.siguiente
            actual.siguiente = nuevo
        self.cantidad += 1
        self.segundos_pendientes += trabajo.segundos

    def extraer(self):
        """Retira la cabeza, que ya contiene el siguiente trabajo prioritario."""
        if self.primero is None:
            return None
        trabajo = self.primero.trabajo
        self.primero = self.primero.siguiente
        self.cantidad -= 1
        self.segundos_pendientes -= trabajo.segundos
        return trabajo

    def cancelar(self, identificador):
        """Desenlaza el nodo buscado y ajusta el tiempo acumulado de la cola."""
        anterior = None
        actual = self.primero
        while actual is not None:
            if actual.trabajo.id == identificador:
                if anterior is None:
                    self.primero = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                self.cantidad -= 1
                self.segundos_pendientes -= actual.trabajo.segundos
                return actual.trabajo
            anterior = actual
            actual = actual.siguiente
        return None

    def __iter__(self):
        """Permite consultar la cola en el orden en que se imprimirá."""
        actual = self.primero
        while actual is not None:
            yield actual.trabajo
            actual = actual.siguiente


class Impresora:
    """Mantiene una cola independiente y como máximo un trabajo activo."""

    def __init__(self, numero):
        # Los contadores cambian solamente al completar un trabajo.
        self.numero = numero
        self.cola = ColaPrioridad()
        self.actual = None
        self.completados = 0
        self.paginas_impresas = 0

    def iniciar(self):
        """Selecciona el siguiente sin interrumpir una impresión ya iniciada."""
        if self.actual is not None:
            raise ValueError("Esta impresora ya tiene un trabajo en impresión.")
        trabajo = self.cola.extraer()
        if trabajo is None:
            raise ValueError("La impresora no tiene trabajos pendientes.")
        self.actual = trabajo
        trabajo.estado = "En impresión"
        return trabajo

    def completar(self):
        """Confirma manualmente la finalización y contabiliza las páginas una vez."""
        if self.actual is None:
            raise ValueError("La impresora no tiene un trabajo en impresión.")
        trabajo = self.actual
        trabajo.estado = "Completado"
        self.completados += 1
        self.paginas_impresas += trabajo.paginas
        self.actual = None
        return trabajo

    def tiempo_estimado(self):
        """Carga total: cola pendiente más duración íntegra del trabajo activo."""
        activo = 0 if self.actual is None else self.actual.segundos
        return self.cola.segundos_pendientes + activo


class SistemaImpresion:
    """Coordina las tres impresoras, el historial y las reglas de validación."""

    def __init__(self):
        # La tupla fija solo agrupa tres objetos. Las colas e historial son propios.
        self.impresoras = (Impresora(1), Impresora(2), Impresora(3))
        self.historial = ListaTrabajos()

    @staticmethod
    def texto(valor, campo):
        """Rechaza campos vacíos y evita espacios accidentales en los extremos."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{campo} no puede estar vacío.")
        return valor.strip()

    def obtener_impresora(self, numero):
        """Valida el rango antes de acceder a la tupla fija."""
        if type(numero) is not int or numero < 1 or numero > 3:
            raise ValueError("La impresora debe ser 1, 2 o 3.")
        return self.impresoras[numero - 1]

    def enviar(self, identificador, archivo, usuario, paginas, prioridad, numero):
        """Valida primero y luego registra y encola el trabajo en la impresora elegida."""
        impresora = self.obtener_impresora(numero)
        identificador = self.texto(identificador, "El ID")
        archivo = self.texto(archivo, "El archivo")
        usuario = self.texto(usuario, "El usuario")
        if type(paginas) is not int or paginas <= 0:
            raise ValueError("Las páginas deben ser un entero mayor que cero.")
        if type(prioridad) is not int or prioridad not in (1, 2):
            raise ValueError("La prioridad debe ser 1 (Alta) o 2 (Normal).")
        if self.historial.buscar(identificador) is not None:
            raise ValueError("El ID ya existe, incluso si fue cancelado o completado.")
        trabajo = Trabajo(identificador, archivo, usuario, paginas, prioridad, numero)
        impresora.cola.insertar(trabajo)
        self.historial.agregar(trabajo)
        return trabajo

    def iniciar(self, numero):
        """Delega la selección en la impresora solicitada."""
        return self.obtener_impresora(numero).iniciar()

    def completar(self, numero):
        """Delega la confirmación en la impresora solicitada."""
        return self.obtener_impresora(numero).completar()

    def cancelar(self, identificador):
        """Solo permite cancelar trabajos que todavía permanecen pendientes."""
        identificador = self.texto(identificador, "El ID")
        trabajo = self.historial.buscar(identificador)
        if trabajo is None:
            raise ValueError("No existe un trabajo con ese ID.")
        if trabajo.estado != "Pendiente":
            raise ValueError("Solo se pueden cancelar trabajos pendientes.")
        impresora = self.obtener_impresora(trabajo.impresora)
        retirado = impresora.cola.cancelar(identificador)
        if retirado is None:
            raise RuntimeError("Inconsistencia: el trabajo pendiente no está en su cola.")
        trabajo.estado = "Cancelado"
        return trabajo

    def trabajos_usuario(self, usuario):
        """Filtra el historial sin distinguir mayúsculas en el nombre del usuario."""
        clave = self.texto(usuario, "El usuario").casefold()
        for trabajo in self.historial:
            if trabajo.usuario.casefold() == clave:
                yield trabajo

    def contar_usuario(self, usuario):
        """Cuenta todos los enviados, incluidos pendientes y cancelados."""
        cantidad = 0
        for _ in self.trabajos_usuario(usuario):
            cantidad += 1
        return cantidad

    def totales(self):
        """Suma contadores de las tres impresoras: solo impresión completada."""
        trabajos = 0
        paginas = 0
        for impresora in self.impresoras:
            trabajos += impresora.completados
            paginas += impresora.paginas_impresas
        return trabajos, paginas

    def lideres_usuarios(self):
        """Devuelve empates por trabajos completados, sin diccionarios auxiliares.

        Por claridad académica se recorre el historial por cada usuario candidato.
        Se evalúa cada usuario solo en su primera aparición completada: O(N²).
        """
        lideres = ListaTrabajos()
        maximo = 0
        for candidato in self.historial:
            if candidato.estado != "Completado":
                continue
            repetido = False
            for anterior in self.historial:
                if anterior is candidato:
                    break
                if (anterior.estado == "Completado" and
                        anterior.usuario.casefold() == candidato.usuario.casefold()):
                    repetido = True
                    break
            if repetido:
                continue
            cantidad = 0
            for trabajo in self.trabajos_usuario(candidato.usuario):
                if trabajo.estado == "Completado":
                    cantidad += 1
            if cantidad > maximo:
                lideres = ListaTrabajos()
                maximo = cantidad
            if cantidad == maximo:
                lideres.agregar(candidato)
        return lideres, maximo


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
