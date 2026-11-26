# Diccionario de datos
| Campo | Significado |
|---|---|
| fecha | Fecha de servicio |
| linea | Línea de transporte |
| hora_num | Hora inicial de franja, 4–23 |
| demanda_original | Afluencia original, puede ser nula |
| demanda | Afluencia consolidada |
| demanda_predicha | Estimación horaria |
| es_festivo | Indicador de festivo colombiano |
| dia_semana_num | Domingo=1 a sábado=7 |
| tipo_dia | Clasificación de día |
| en_horario_operacion | Indicador de franja operativa |
| operacion_parcial | Indicador de franja parcialmente operativa |
| origen_demanda | Observado, imputado, cero estructural u observado fuera de horario |
| metodo_imputacion | Método aplicado a faltantes |
| corte_imputacion | Límite temporal de datos usados |
| archivo_fuente / fila_excel_origen | Trazabilidad de origen |
| run_id_modelo | Ejecución MLflow asociada |

Clave horaria: fecha, linea, hora_num. Las tablas de medianas tienen niveles de agrupación decrecientes (línea, hora, día, festivo; línea, hora, día; línea, hora; línea).
