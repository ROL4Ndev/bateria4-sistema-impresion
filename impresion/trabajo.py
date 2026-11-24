"""Sistema Simple de Impresión · Rolando Sanchez y Christian Roque."""


# INICIO DEL BLOQUE PARA LA ENTREGA
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


