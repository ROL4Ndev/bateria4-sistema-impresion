"""Sistema Simple de Impresión · Rolando Sanchez y Christian Roque."""

from .cola_prioridad import ColaPrioridad

# INICIO DEL BLOQUE PARA LA ENTREGA
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


