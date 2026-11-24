# Archivos para la entrega

**Rolando Sanchez y Christian Roque**  
Batería 4, ejercicio 1: Sistema Simple de Impresión.

| Destino | Archivos |
| --- | --- |
| Canvas, semana 15 | `sistema_impresion.py`, `README.md` y el enlace del repositorio. La guía exige el código en un único archivo ejecutable. |
| GitHub | Subir el contenido de esta carpeta a la raíz del repositorio: código oficial, módulos, `main.py`, generador, README y las carpetas de imágenes y diagramas. Incluir también los documentos y la presentación si se desea conservar todo el trabajo en el mismo repositorio. |
| Exposición, semana 16 | `Diapositivas_Sistema_Impresion.pptx` o su PDF. La presentación tiene 15 diapositivas para ocho minutos. |
| Preparación de la exposición | `GUION_EXPOSICION.md`, con el reparto de tiempos y las explicaciones. |
| Informe | `Informe_Sistema_Impresion_Sanchez_Roque.docx` y su PDF, disponibles como documentación complementaria. |

La guía también indica compartir el repositorio con **lmelendez-tecsup**. La fecha exacta y cualquier instrucción adicional se consultan en Canvas.

## Presentación

El rediseño está guardado en [Canva](https://www.canva.com/d/5f1H1_tQs_jI-Rh). El PowerPoint y el PDF incluidos son copias del diseño aprobado. El archivo `Presentacion_Canva.url` abre el diseño editable.

## Antes de subir el código

```bash
python herramientas/generar_entrega.py
python sistema_impresion.py --pruebas
python main.py --pruebas
```

Subir los archivos extraídos a GitHub para que se puedan consultar el código y el README directamente. Los recursos deben mantener sus rutas relativas para que las imágenes del README se visualicen.
