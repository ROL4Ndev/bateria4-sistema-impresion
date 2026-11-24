# Guion de exposición de ocho minutos

**Rolando Sanchez y Christian Roque**  
**Batería 4, ejercicio 1 · Sistema Simple de Impresión**

| Diapositiva | Responsable | Tiempo | Punto principal |
| --- | --- | --- | --- |
| 1 Sistema Simple de Impresión | Christian | 15 s | Integrantes y ejercicio. |
| 2 Problema | Christian | 25 s | Los urgentes adelantan a pendientes normales. |
| 3 Alcance y reglas | Christian | 30 s | Tres impresoras, cinco segundos y prioridad. |
| 4 Diseño de clases | Rolando | 35 s | Relaciones e historial compartido. |
| 5 Cola enlazada | Rolando | 35 s | Cabeza, Nodo y siguiente. |
| 6 Flujo de inserción | Rolando | 35 s | Decisiones y recorrido para insertar. |
| 7 Inserción y FIFO | Rolando | 45 s | Explicar <= y los dos enlaces. |
| 8 Extracción | Rolando | 25 s | Mover la cabeza y restar tiempo. |
| 9 Finalización | Rolando | 20 s | Contar una vez y liberar actual. |
| 10 Cancelación | Rolando | 35 s | Validar Pendiente y retirar el nodo. |
| 11 Estimación de tiempos | Rolando | 40 s | Carga acumulada y máximo en paralelo. |
| 12 Demostración | Christian | 55 s | Ejecutar --demo y explicar los resultados. |
| 13 Pruebas | Christian | 35 s | Ejecutar --pruebas y mostrar 48 correctas. |
| 14 Complejidad | Rolando | 25 s | Diferenciar n y N e identificar O(N²). |
| 15 Conclusiones | Christian | 25 s | Prioridad, historial y conteos. |
| **Total** | **Rolando 4 min 55 s / Christian 3 min 05 s** | **480 s** | **8 minutos** |

## Ubicación de los fragmentos de código

| Diapositiva | Clase y método | Líneas del archivo entregado |
| --- | --- | --- |
| 5 | Nodo.__init__ | 39 a 42 |
| 7 | ColaPrioridad.insertar | 96 a 101 |
| 8 | ColaPrioridad.extraer | 107 a 113 |
| 9 | Impresora.completar | 166 a 171 |
| 10 | ColaPrioridad.cancelar | 120 a 129 |

## Rolando: puntos que debes dominar

### Cola y nodos

“Nuestra cola usa una lista simplemente enlazada. Cada nodo contiene un trabajo y un enlace al siguiente. La cabeza siempre representa el próximo trabajo pendiente. Hay una cola independiente por impresora.”

### Inserción y FIFO

“La prioridad Alta vale 1 y la Normal vale 2. Como 1 es menor, queda antes. Si el trabajo llega con la misma prioridad, seguimos avanzando mientras la prioridad siguiente sea menor o igual. Ese igual hace que el nuevo quede después de los que llegaron antes y conserva FIFO.”

Ejemplo: llega T01 Normal, luego T02 Alta y después T03 Alta. El resultado es T02, T03, T01. Si se usara `<` en el recorrido en lugar de `<=`, una nueva Alta podría adelantar a otra Alta.

### Historial y estados

“El historial tiene sus propios nodos, pero apunta a los mismos objetos Trabajo. Cuando cambiamos un estado, la consulta del historial muestra el cambio. Cancelar elimina el nodo de la cola, pero mantiene el trabajo registrado.”

“Iniciar no significa completar. Primero el trabajo pasa a En impresión. Solo cuando confirmamos Completado sumamos sus páginas. Esto impide contar un cancelado o sumar dos veces la misma impresión.”

### Tiempos

“Multiplicamos las páginas por cinco. Al insertar sumamos ese tiempo al acumulado de la cola y al extraer o cancelar lo restamos. El tiempo del trabajo activo se suma por separado. Con cargas de 60, 15 y 25 segundos, hay 100 segundos de trabajo total y se termina en 60 si las tres operan en paralelo.”

“Es una simulación manual. No hay cuenta regresiva. El activo reserva su duración completa hasta que confirmamos que terminó.”

### Complejidad y pregunta difícil

“Insertar en la cola cuesta O(n), porque podemos recorrerla completa. Extraer cuesta O(1), porque retiramos la cabeza. Enviar desde el sistema cuesta O(N), porque antes revisamos el historial para que el ID sea único.”

“El reporte de usuario con más impresiones cuesta O(N²), porque compara usuarios recorriendo el historial. Es una limitación de esta implementación simple. Para mayor volumen, añadiríamos un índice propio por usuario.”

## Christian: demostración

Ejecutar en una terminal abierta en la carpeta del proyecto:

```bash
python sistema_impresion.py --demo
python sistema_impresion.py --pruebas
```

Explicar estos resultados, sin leer toda la salida:

- Cola 1: T02, T03, T01. Alta primero y FIFO entre las dos altas.
- Al completar T02, cancelar T01 y completar T03, el total es 2 trabajos y 6 páginas.
- Rolando tiene 3 trabajos enviados, pero solo uno de ellos se completó en la demostración.
- Ambos usuarios empatan con una impresión completada. La impresora 1 tiene dos.
- Quedan 15 segundos en impresora 2 y 25 en impresora 3. Se terminaría todo en 25 segundos en paralelo.
- El bloque de pruebas termina con 48 verificaciones correctas.

Si el docente pide usar el menú, seguir los pasos del apartado 8 del README. Practicar esa secuencia antes de exponer para no consumir los 8 minutos buscando opciones.

## Organización del código si el docente pregunta

“Las clases están separadas en módulos para desarrollar y revisar el proyecto. La guía solicita un único archivo Python para Canvas; por eso tenemos un generador que reúne esas mismas clases, el menú y las pruebas en `sistema_impresion.py`. Las dos versiones ejecutan la misma lógica. Para la exposición usamos el archivo oficial, que coincide con las capturas y los números de línea de las diapositivas.”

Comandos de desarrollo: `python main.py --demo` y `python main.py --pruebas`.
Comando para preparar la entrega: `python herramientas/generar_entrega.py`.
