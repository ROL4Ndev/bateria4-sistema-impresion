"""Sistema Simple de Impresión · Rolando Sanchez y Christian Roque."""

from .nodo import Nodo

# INICIO DEL BLOQUE PARA LA ENTREGA
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


