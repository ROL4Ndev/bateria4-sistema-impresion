"""Sistema Simple de Impresión · Rolando Sanchez y Christian Roque."""

from .nodo import Nodo

# INICIO DEL BLOQUE PARA LA ENTREGA
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


