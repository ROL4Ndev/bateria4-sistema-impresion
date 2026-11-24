"""Sistema Simple de Impresión · Rolando Sanchez y Christian Roque."""


# INICIO DEL BLOQUE PARA LA ENTREGA
class Nodo:
    """Nodo simple. Cada lista utiliza sus propios nodos."""

    def __init__(self, trabajo, siguiente=None):
        # Dos nodos distintos pueden referirse al mismo objeto Trabajo.
        self.trabajo = trabajo
        self.siguiente = siguiente


