"""Sistema Simple de Impresión · Rolando Sanchez y Christian Roque."""

from .trabajo import Trabajo
from .impresora import Impresora
from .lista_trabajos import ListaTrabajos

# INICIO DEL BLOQUE PARA LA ENTREGA
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


